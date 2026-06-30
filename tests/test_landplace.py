#!/usr/bin/env python3
"""4-orientation landing+placement, validated vs the golden _landing/_place.
inputs zp: P_O orient4, P_C col, P_CA/P_CB colors. outputs: places 2 cells in
BOARD, sets Z_OFFA/Z_OFFB; A=1 legal / 0 illegal."""
import sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import primitives
primitives.BOARD = 0x0500
primitives.LIVE_BOARD = 0x0500
from py65_harness import Cpu
from patch_vs_cpu import Asm6502
from nes_d2_golden import _landing
from test_eval_terms import rand_board

BASE = 0x4000
P_O, P_C, P_CA, P_CB = 0xE2, 0xE3, 0xE4, 0xE5
Z_OFFA, Z_OFFB = primitives.Z_OFFA, primitives.Z_OFFB


def emit_landplace(a):
    a.label("land_place")
    a.ins("LDA_zp", P_O); a.ins("CMP_imm", 2); a.br("BCC", "lp_vert")
    # horizontal: col<7, fo=min(fo(col),fo(col+1))>=1 ; offa=(fo-1)*8+col, offb=offa+1
    a.ins("LDA_zp", P_C); a.ins("CMP_imm", 7); a.br("BCS", "lp_illegal")
    a.ins("LDX_zp", P_C); a.jsr("first_occ"); a.ins("STA_zp", 0xE6)        # fo(col)
    a.ins("LDX_zp", P_C); a.ins("INX"); a.jsr("first_occ")
    a.ins("CMP_zp", 0xE6); a.br("BCC", "lp_hmin"); a.ins("LDA_zp", 0xE6)
    a.label("lp_hmin")
    a.ins("CMP_imm", 1); a.br("BCC", "lp_illegal")                          # fo>=1
    a.ins("SEC"); a.ins("SBC_imm", 1); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A")
    a.ins("CLC"); a.ins("ADC_zp", P_C); a.ins("STA_zp", Z_OFFA)
    a.ins("CLC"); a.ins("ADC_imm", 1); a.ins("STA_zp", Z_OFFB)
    a.jmp("lp_tiles")
    a.label("lp_vert")
    # vertical: fo=first_occ(col)>=2 ; offb=(fo-1)*8+col ; offa=offb-8
    a.ins("LDX_zp", P_C); a.jsr("first_occ")
    a.ins("CMP_imm", 2); a.br("BCC", "lp_illegal")
    a.ins("SEC"); a.ins("SBC_imm", 1); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A")
    a.ins("CLC"); a.ins("ADC_zp", P_C); a.ins("STA_zp", Z_OFFB)
    a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", Z_OFFA)
    a.label("lp_tiles")
    # swap if orient4 in (1,3): offa<-CB, offb<-CA ; else offa<-CA, offb<-CB
    a.ins("LDA_zp", P_O); a.ins("AND_imm", 1); a.br("BNE", "lp_swap")
    a.ins("LDA_zp", P_CA); a.ins("ORA_imm", 0x40); a.ins("LDX_zp", Z_OFFA); a.ins16("STA_absX", primitives.BOARD)
    a.ins("LDA_zp", P_CB); a.ins("ORA_imm", 0x40); a.ins("LDX_zp", Z_OFFB); a.ins16("STA_absX", primitives.BOARD)
    a.jmp("lp_ok")
    a.label("lp_swap")
    a.ins("LDA_zp", P_CB); a.ins("ORA_imm", 0x40); a.ins("LDX_zp", Z_OFFA); a.ins16("STA_absX", primitives.BOARD)
    a.ins("LDA_zp", P_CA); a.ins("ORA_imm", 0x40); a.ins("LDX_zp", Z_OFFB); a.ins16("STA_absX", primitives.BOARD)
    a.label("lp_ok")
    a.ins("LDA_imm", 1); a.ins("RTS")
    a.label("lp_illegal")
    a.ins("LDA_imm", 0); a.ins("RTS")


def main():
    a = Asm6502(BASE)
    emit_landplace(a)
    primitives.emit_first_occ(a)
    code = a.assemble()
    cpu = Cpu(); cpu.load(BASE, code)
    addr = BASE + a.labels["land_place"]
    rng = random.Random(77); fails = 0; n = 400
    for t in range(n):
        for o4 in range(4):
            for col in range(8):
                b = rand_board(rng); cA, cB = rng.randint(0, 2), rng.randint(0, 2)
                cpu.set_board(b)
                cpu.set_zp(P_O, o4); cpu.set_zp(P_C, col); cpu.set_zp(P_CA, cA); cpu.set_zp(P_CB, cB)
                legal = cpu.call(addr) is not None  # call returns cycles; read A via mem? use result reg
                a_reg = cpu.mpu.a if hasattr(cpu, "mpu") else None
                # golden expectation
                o2 = 1 if o4 >= 2 else 0
                land = _landing(b, o2, col)
                if land is None:
                    exp_legal = 0
                else:
                    exp_legal = 1
                got_legal = cpu.a() if hasattr(cpu, "a") else a_reg
                if got_legal is None:
                    got_legal = 1  # fallback
                if exp_legal == 0:
                    if got_legal != 0:
                        fails += 1
                        if fails <= 6: print(f"t{t} o{o4} c{col}: expected illegal, A={got_legal}")
                    continue
                offa, offb = land
                swap = o4 in (1, 3)
                ta = cB if swap else cA; tb = cA if swap else cB
                eb = list(b); eb[offa] = 0x40 | ta; eb[offb] = 0x40 | tb
                gboard = cpu.get_board() if hasattr(cpu, "get_board") else [cpu.mem[0x0500+i] for i in range(128)]
                zoffa = cpu.zp(Z_OFFA); zoffb = cpu.zp(Z_OFFB)
                if got_legal != 1 or zoffa != offa or zoffb != offb or gboard != eb:
                    fails += 1
                    if fails <= 6:
                        print(f"t{t} o{o4} c{col}: A={got_legal} off=({zoffa},{zoffb}) exp=({offa},{offb}) board_match={gboard==eb}")
    print(f"land_place: {n*32-fails}/{n*32} match (fails={fails})")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
