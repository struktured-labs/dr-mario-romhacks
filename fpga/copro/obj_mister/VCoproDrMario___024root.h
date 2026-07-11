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
        CData/*0:0*/ CoproDrMario__DOT__WE;
        CData/*4:0*/ CoproDrMario__DOT__rst_cnt;
        CData/*0:0*/ CoproDrMario__DOT__parked;
        CData/*0:0*/ CoproDrMario__DOT__rst_m;
        CData/*7:0*/ CoproDrMario__DOT__DI;
        CData/*0:0*/ CoproDrMario__DOT__a_ram;
        CData/*0:0*/ CoproDrMario__DOT__lev_wr_board;
        CData/*0:0*/ CoproDrMario__DOT__lev_start;
        CData/*0:0*/ CoproDrMario__DOT__lev_wr_arg;
        CData/*2:0*/ CoproDrMario__DOT__lev_enc;
        CData/*1:0*/ CoproDrMario__DOT__lev_colenc;
        CData/*1:0*/ CoproDrMario__DOT__lev_wslot;
        CData/*1:0*/ CoproDrMario__DOT__lev_a_o4;
        CData/*1:0*/ CoproDrMario__DOT__lev_a_sl;
        CData/*1:0*/ CoproDrMario__DOT__lev_a_ca;
        CData/*1:0*/ CoproDrMario__DOT__lev_a_cb;
        CData/*2:0*/ CoproDrMario__DOT__lev_a_col;
        CData/*0:0*/ CoproDrMario__DOT__lev_done;
        CData/*0:0*/ CoproDrMario__DOT__lev_win;
        CData/*0:0*/ CoproDrMario__DOT__lev_legal;
        CData/*5:0*/ CoproDrMario__DOT__lev_rvc;
        CData/*3:0*/ CoproDrMario__DOT__lev_rvv;
        CData/*7:0*/ CoproDrMario__DOT__lev_q;
        CData/*7:0*/ CoproDrMario__DOT__rom_q;
        CData/*7:0*/ CoproDrMario__DOT__ram_a_q;
        CData/*7:0*/ CoproDrMario__DOT__ram_b_q;
        CData/*0:0*/ CoproDrMario__DOT__sel_ram_d;
        CData/*0:0*/ CoproDrMario__DOT__sel_rom_d;
        CData/*0:0*/ CoproDrMario__DOT__sel_vec_d;
        CData/*0:0*/ CoproDrMario__DOT__sel_lev_d;
        CData/*0:0*/ CoproDrMario__DOT__ab0_d;
        CData/*7:0*/ CoproDrMario__DOT__hb_din;
        CData/*0:0*/ CoproDrMario__DOT__hb_we;
        CData/*0:0*/ CoproDrMario__DOT____VdfgRegularize_hb6d3a560_2_2;
        CData/*0:0*/ CoproDrMario__DOT____VdfgRegularize_hb6d3a560_2_3;
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
    };
    struct {
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
        CData/*4:0*/ CoproDrMario__DOT__leafeval__DOT__st;
        CData/*0:0*/ CoproDrMario__DOT__leafeval__DOT__node_leaf;
        CData/*4:0*/ CoproDrMario__DOT__leafeval__DOT__fo1;
        CData/*4:0*/ CoproDrMario__DOT__leafeval__DOT__fwp;
        CData/*6:0*/ CoproDrMario__DOT__leafeval__DOT__off_a;
        CData/*6:0*/ CoproDrMario__DOT__leafeval__DOT__off_b;
        CData/*1:0*/ CoproDrMario__DOT__leafeval__DOT__li;
        CData/*7:0*/ CoproDrMario__DOT__leafeval__DOT__soff;
        CData/*3:0*/ CoproDrMario__DOT__leafeval__DOT__sstep;
        CData/*4:0*/ CoproDrMario__DOT__leafeval__DOT__scnt;
        CData/*4:0*/ CoproDrMario__DOT__leafeval__DOT__srun;
        CData/*1:0*/ CoproDrMario__DOT__leafeval__DOT__smcol;
        CData/*7:0*/ CoproDrMario__DOT__leafeval__DOT__srstart;
        CData/*6:0*/ CoproDrMario__DOT__leafeval__DOT__fwp2;
        CData/*4:0*/ CoproDrMario__DOT__leafeval__DOT__gdest;
        CData/*0:0*/ CoproDrMario__DOT__leafeval__DOT__anyclear;
        CData/*3:0*/ CoproDrMario__DOT__leafeval__DOT__wc;
        CData/*3:0*/ CoproDrMario__DOT__leafeval__DOT__wr_;
        CData/*4:0*/ CoproDrMario__DOT__leafeval__DOT__maxh;
        CData/*7:0*/ CoproDrMario__DOT__leafeval__DOT__holes;
        CData/*7:0*/ CoproDrMario__DOT__leafeval__DOT__toprisk;
        CData/*7:0*/ CoproDrMario__DOT__leafeval__DOT__spawn;
        CData/*7:0*/ CoproDrMario__DOT__leafeval__DOT__setup;
        CData/*0:0*/ CoproDrMario__DOT__leafeval__DOT__anyvir;
    };
    struct {
        CData/*0:0*/ CoproDrMario__DOT__leafeval__DOT__seen;
        CData/*4:0*/ CoproDrMario__DOT__leafeval__DOT__fillcnt;
        CData/*6:0*/ CoproDrMario__DOT__leafeval__DOT__vo;
        CData/*3:0*/ CoproDrMario__DOT__leafeval__DOT__v_r;
        CData/*2:0*/ CoproDrMario__DOT__leafeval__DOT__v_c;
        CData/*1:0*/ CoproDrMario__DOT__leafeval__DOT__v_col;
        CData/*4:0*/ CoproDrMario__DOT__leafeval__DOT__run_h;
        CData/*4:0*/ CoproDrMario__DOT__leafeval__DOT__run_v;
        CData/*4:0*/ CoproDrMario__DOT__leafeval__DOT__p;
        CData/*4:0*/ CoproDrMario__DOT__leafeval__DOT__span_lo;
        CData/*4:0*/ CoproDrMario__DOT__leafeval__DOT__span_hi;
        CData/*4:0*/ CoproDrMario__DOT__leafeval__DOT__vspan_lo;
        CData/*4:0*/ CoproDrMario__DOT__leafeval__DOT__vspan_hi;
        CData/*4:0*/ CoproDrMario__DOT__leafeval__DOT__fo2b__DOT__fom;
        CData/*0:0*/ CoproDrMario__DOT__leafeval__DOT__scan__DOT__brk;
        CData/*1:0*/ CoproDrMario__DOT__leafeval__DOT__scan__DOT__c_;
        CData/*2:0*/ CoproDrMario__DOT__leafeval__DOT__grv__DOT__t;
        CData/*1:0*/ CoproDrMario__DOT__leafeval__DOT__suh__DOT__c0;
        CData/*0:0*/ CoproDrMario__DOT__leafeval__DOT__suh__DOT__t;
        CData/*1:0*/ CoproDrMario__DOT__leafeval__DOT__suv__DOT__c0;
        CData/*0:0*/ CoproDrMario__DOT__leafeval__DOT__suv__DOT__t;
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
        SData/*15:0*/ CoproDrMario__DOT__lev_sco;
        SData/*15:0*/ CoproDrMario__DOT__lev_imm;
        SData/*11:0*/ CoproDrMario__DOT__hb_addr;
        SData/*15:0*/ CoproDrMario__DOT__cpu6502__DOT__PC;
        SData/*15:0*/ CoproDrMario__DOT__cpu6502__DOT__PC_temp;
        SData/*8:0*/ CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp;
        SData/*10:0*/ CoproDrMario__DOT__leafeval__DOT__pollution;
        SData/*9:0*/ CoproDrMario__DOT__leafeval__DOT__buried;
        SData/*15:0*/ CoproDrMario__DOT__leafeval__DOT__rdy_ext;
        SData/*15:0*/ CoproDrMario__DOT__leafeval__DOT__vrdy;
        SData/*8:0*/ CoproDrMario__DOT__leafeval__DOT__fin__DOT__hq;
        SData/*8:0*/ CoproDrMario__DOT__leafeval__DOT__fin__DOT__vq;
        SData/*8:0*/ CoproDrMario__DOT__leafeval__DOT__fin__DOT__mx;
        SData/*11:0*/ __VdlyDim0__CoproDrMario__DOT__wram__DOT__mem__v0;
        SData/*11:0*/ __VdlyDim0__CoproDrMario__DOT__wram__DOT__mem__v1;
        VlWide<4>/*127:0*/ CoproDrMario__DOT__leafeval__DOT__markb;
        IData/*31:0*/ CoproDrMario__DOT__leafeval__DOT__i;
        IData/*31:0*/ __VactIterCount;
        VlUnpacked<CData/*7:0*/, 16384> CoproDrMario__DOT__rom;
        VlUnpacked<CData/*7:0*/, 4> CoproDrMario__DOT__cpu6502__DOT__AXYS;
        VlUnpacked<CData/*2:0*/, 128> CoproDrMario__DOT__leafeval__DOT__bcell;
        VlUnpacked<CData/*2:0*/, 128> CoproDrMario__DOT__leafeval__DOT__s_live;
        VlUnpacked<CData/*2:0*/, 128> CoproDrMario__DOT__leafeval__DOT__s_w1;
        VlUnpacked<CData/*2:0*/, 128> CoproDrMario__DOT__leafeval__DOT__s_w2;
        VlUnpacked<CData/*1:0*/, 128> CoproDrMario__DOT__leafeval__DOT__col_of;
        VlUnpacked<CData/*0:0*/, 128> CoproDrMario__DOT__leafeval__DOT__occ_of;
        VlUnpacked<CData/*0:0*/, 128> CoproDrMario__DOT__leafeval__DOT__vir_of;
        VlUnpacked<CData/*7:0*/, 4096> CoproDrMario__DOT__wram__DOT__mem;
    };
    VlNBACommitQueue<VlUnpacked<CData/*2:0*/, 128>, false, CData/*2:0*/, 1> __VdlyCommitQueueCoproDrMario__DOT__leafeval__DOT__bcell;
    VlNBACommitQueue<VlUnpacked<CData/*2:0*/, 128>, false, CData/*2:0*/, 1> __VdlyCommitQueueCoproDrMario__DOT__leafeval__DOT__s_w2;
    VlNBACommitQueue<VlUnpacked<CData/*2:0*/, 128>, false, CData/*2:0*/, 1> __VdlyCommitQueueCoproDrMario__DOT__leafeval__DOT__s_w1;
    VlNBACommitQueue<VlUnpacked<CData/*2:0*/, 128>, false, CData/*2:0*/, 1> __VdlyCommitQueueCoproDrMario__DOT__leafeval__DOT__s_live;
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
