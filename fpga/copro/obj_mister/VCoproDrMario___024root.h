// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See VCoproDrMario.h for the primary calling header

#ifndef VERILATED_VCOPRODRMARIO___024ROOT_H_
#define VERILATED_VCOPRODRMARIO___024ROOT_H_  // guard

#include "verilated.h"


class VCoproDrMario__Syms;

class alignas(VL_CACHE_LINE_BYTES) VCoproDrMario___024root final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        VL_IN8(clk,0,0);
        VL_IN8(clk_cpu,0,0);
        CData/*0:0*/ CoproDrMario__DOT__cpu_rst;
        VL_IN8(ce,0,0);
        VL_IN8(enable,0,0);
        VL_IN8(prg_read,0,0);
        VL_IN8(prg_write,0,0);
        VL_IN8(prg_din,7,0);
        VL_OUT8(prg_dout,7,0);
        VL_OUT8(copro_sel,0,0);
        CData/*7:0*/ CoproDrMario__DOT__DO;
        CData/*4:0*/ CoproDrMario__DOT__rst_cnt;
        CData/*0:0*/ CoproDrMario__DOT__parked;
        CData/*0:0*/ CoproDrMario__DOT__rst_m;
        CData/*7:0*/ CoproDrMario__DOT__DI;
        CData/*0:0*/ CoproDrMario__DOT__a_ram;
        CData/*7:0*/ CoproDrMario__DOT__rom_q;
        CData/*7:0*/ CoproDrMario__DOT__ram_a_q;
        CData/*7:0*/ CoproDrMario__DOT__ram_b_q;
        CData/*0:0*/ CoproDrMario__DOT____Vcellinp__wram__wren_a;
        CData/*0:0*/ CoproDrMario__DOT__sel_ram_d;
        CData/*0:0*/ CoproDrMario__DOT__sel_rom_d;
        CData/*0:0*/ CoproDrMario__DOT__sel_vec_d;
        CData/*0:0*/ CoproDrMario__DOT__ab0_d;
        CData/*7:0*/ CoproDrMario__DOT__hb_din;
        CData/*0:0*/ CoproDrMario__DOT__hb_we;
        CData/*7:0*/ CoproDrMario__DOT__cpu6502__DOT__ABL;
        CData/*7:0*/ CoproDrMario__DOT__cpu6502__DOT__ABH;
        CData/*7:0*/ CoproDrMario__DOT__cpu6502__DOT__ADD;
        CData/*7:0*/ CoproDrMario__DOT__cpu6502__DOT__IRHOLD;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__IRHOLD_valid;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__C;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__Z;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__I;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__D;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__V;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__N;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__AN;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__HC;
        CData/*7:0*/ CoproDrMario__DOT__cpu6502__DOT__AI;
        CData/*7:0*/ CoproDrMario__DOT__cpu6502__DOT__IR;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__CO;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__NMI_edge;
        CData/*1:0*/ CoproDrMario__DOT__cpu6502__DOT__regsel;
        CData/*7:0*/ CoproDrMario__DOT__cpu6502__DOT__P;
        CData/*5:0*/ CoproDrMario__DOT__cpu6502__DOT__state;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__PC_inc;
        CData/*1:0*/ CoproDrMario__DOT__cpu6502__DOT__src_reg;
        CData/*1:0*/ CoproDrMario__DOT__cpu6502__DOT__dst_reg;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__index_y;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__load_reg;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__inc;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__write_back;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__load_only;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__store;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__adc_sbc;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__compare;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__shift;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__rotate;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__backwards;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__cond_true;
        CData/*2:0*/ CoproDrMario__DOT__cpu6502__DOT__cond_code;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__shift_right;
        CData/*3:0*/ CoproDrMario__DOT__cpu6502__DOT__op;
    };
    struct {
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__adc_bcd;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__adj_bcd;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__bit_ins;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__plp;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__php;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__clc;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__sec;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__cld;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__sed;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__cli;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__sei;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__clv;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__res;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__write_register;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT____Vcellinp__ALU__BCD;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__AI7;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__BI7;
        CData/*7:0*/ CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_BI;
        CData/*4:0*/ CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_h;
        CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_HC;
        CData/*4:0*/ __Vdly__CoproDrMario__DOT__rst_cnt;
        CData/*5:0*/ __Vdly__CoproDrMario__DOT__cpu6502__DOT__state;
        CData/*7:0*/ __VdlyVal__CoproDrMario__DOT__wram__DOT__mem__v0;
        CData/*0:0*/ __VdlySet__CoproDrMario__DOT__wram__DOT__mem__v0;
        CData/*7:0*/ __VdlyVal__CoproDrMario__DOT__wram__DOT__mem__v1;
        CData/*0:0*/ __VdlySet__CoproDrMario__DOT__wram__DOT__mem__v1;
        CData/*0:0*/ __VstlFirstIteration;
        CData/*0:0*/ __VicoFirstIteration;
        CData/*0:0*/ __Vtrigprevexpr___TOP__clk_cpu__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__clk__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__CoproDrMario__DOT__cpu_rst__0;
        CData/*0:0*/ __VactContinue;
        VL_IN16(prg_ain,15,0);
        SData/*15:0*/ CoproDrMario__DOT__AB;
        SData/*11:0*/ CoproDrMario__DOT__a_addr;
        SData/*11:0*/ CoproDrMario__DOT__hb_addr;
        SData/*15:0*/ CoproDrMario__DOT__cpu6502__DOT__PC;
        SData/*15:0*/ CoproDrMario__DOT__cpu6502__DOT__PC_temp;
        SData/*8:0*/ CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp;
        SData/*11:0*/ __VdlyDim0__CoproDrMario__DOT__wram__DOT__mem__v0;
        SData/*11:0*/ __VdlyDim0__CoproDrMario__DOT__wram__DOT__mem__v1;
        IData/*31:0*/ __VactIterCount;
        VlUnpacked<CData/*7:0*/, 16384> CoproDrMario__DOT__rom;
        VlUnpacked<CData/*7:0*/, 4> CoproDrMario__DOT__cpu6502__DOT__AXYS;
        VlUnpacked<CData/*7:0*/, 4096> CoproDrMario__DOT__wram__DOT__mem;
    };
    VlTriggerVec<1> __VstlTriggered;
    VlTriggerVec<1> __VicoTriggered;
    VlTriggerVec<3> __VactTriggered;
    VlTriggerVec<3> __VnbaTriggered;

    // INTERNAL VARIABLES
    VCoproDrMario__Syms* const vlSymsp;

    // CONSTRUCTORS
    VCoproDrMario___024root(VCoproDrMario__Syms* symsp, const char* v__name);
    ~VCoproDrMario___024root();
    VL_UNCOPYABLE(VCoproDrMario___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
