// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See VLeafEval.h for the primary calling header

#ifndef VERILATED_VLEAFEVAL___024ROOT_H_
#define VERILATED_VLEAFEVAL___024ROOT_H_  // guard

#include "verilated.h"


class VLeafEval__Syms;

class alignas(VL_CACHE_LINE_BYTES) VLeafEval___024root final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        VL_IN8(clk,0,0);
        VL_IN8(rst,0,0);
        VL_IN8(wr,0,0);
        VL_IN8(waddr,6,0);
        VL_IN8(wdata,2,0);
        VL_IN8(wslot,1,0);
        VL_IN8(start,0,0);
        VL_IN8(cmd,3,0);
        VL_IN8(cmd_go,0,0);
        VL_IN8(a_sl,1,0);
        VL_IN8(a_o4,1,0);
        VL_IN8(a_col,2,0);
        VL_IN8(a_ca,1,0);
        VL_IN8(a_cb,1,0);
        VL_OUT8(done,0,0);
        VL_OUT8(win,0,0);
        VL_OUT8(legal,0,0);
        VL_OUT8(rv_cells,5,0);
        VL_OUT8(rv_vir,3,0);
        CData/*6:0*/ LeafEval__DOT__cpw_p;
        CData/*0:0*/ LeafEval__DOT__sl_cpw;
        CData/*7:0*/ LeafEval__DOT__sl_qb;
        CData/*3:0*/ LeafEval__DOT__cmd_l;
        CData/*4:0*/ LeafEval__DOT__st;
        CData/*0:0*/ LeafEval__DOT__node_leaf;
        CData/*4:0*/ LeafEval__DOT__fo1;
        CData/*4:0*/ LeafEval__DOT__fwp;
        CData/*6:0*/ LeafEval__DOT__off_a;
        CData/*6:0*/ LeafEval__DOT__off_b;
        CData/*1:0*/ LeafEval__DOT__li;
        CData/*7:0*/ LeafEval__DOT__soff;
        CData/*3:0*/ LeafEval__DOT__sstep;
        CData/*4:0*/ LeafEval__DOT__scnt;
        CData/*4:0*/ LeafEval__DOT__srun;
        CData/*1:0*/ LeafEval__DOT__smcol;
        CData/*7:0*/ LeafEval__DOT__srstart;
        CData/*6:0*/ LeafEval__DOT__fwp2;
        CData/*4:0*/ LeafEval__DOT__gdest;
        CData/*0:0*/ LeafEval__DOT__anyclear;
        CData/*3:0*/ LeafEval__DOT__wc;
        CData/*3:0*/ LeafEval__DOT__wr_;
        CData/*4:0*/ LeafEval__DOT__maxh;
        CData/*7:0*/ LeafEval__DOT__holes;
        CData/*7:0*/ LeafEval__DOT__toprisk;
        CData/*7:0*/ LeafEval__DOT__spawn;
        CData/*7:0*/ LeafEval__DOT__setup;
        CData/*0:0*/ LeafEval__DOT__anyvir;
        CData/*0:0*/ LeafEval__DOT__seen;
        CData/*4:0*/ LeafEval__DOT__fillcnt;
        CData/*6:0*/ LeafEval__DOT__vo;
        CData/*3:0*/ LeafEval__DOT__v_r;
        CData/*2:0*/ LeafEval__DOT__v_c;
        CData/*1:0*/ LeafEval__DOT__v_col;
        CData/*4:0*/ LeafEval__DOT__run_h;
        CData/*4:0*/ LeafEval__DOT__run_v;
        CData/*4:0*/ LeafEval__DOT__p;
        CData/*4:0*/ LeafEval__DOT__span_lo;
        CData/*4:0*/ LeafEval__DOT__span_hi;
        CData/*4:0*/ LeafEval__DOT__vspan_lo;
        CData/*4:0*/ LeafEval__DOT__vspan_hi;
        CData/*4:0*/ LeafEval__DOT__fo2b__DOT__fom;
        CData/*0:0*/ LeafEval__DOT__scan__DOT__brk;
        CData/*1:0*/ LeafEval__DOT__scan__DOT__c_;
        CData/*2:0*/ LeafEval__DOT__grv__DOT__t;
    };
    struct {
        CData/*1:0*/ LeafEval__DOT__suh__DOT__c0;
        CData/*0:0*/ LeafEval__DOT__suh__DOT__t;
        CData/*1:0*/ LeafEval__DOT__suv__DOT__c0;
        CData/*0:0*/ LeafEval__DOT__suv__DOT__t;
        CData/*0:0*/ __VstlFirstIteration;
        CData/*0:0*/ __VicoFirstIteration;
        CData/*0:0*/ __Vtrigprevexpr___TOP__clk__0;
        CData/*0:0*/ __VactContinue;
        VL_OUT16(sco,15,0);
        VL_OUT16(imm,15,0);
        SData/*8:0*/ LeafEval__DOT__sr_addr;
        SData/*8:0*/ LeafEval__DOT__sl_wa;
        SData/*10:0*/ LeafEval__DOT__pollution;
        SData/*9:0*/ LeafEval__DOT__buried;
        SData/*15:0*/ LeafEval__DOT__rdy_ext;
        SData/*15:0*/ LeafEval__DOT__vrdy;
        SData/*8:0*/ LeafEval__DOT__fin__DOT__hq;
        SData/*8:0*/ LeafEval__DOT__fin__DOT__vq;
        SData/*8:0*/ LeafEval__DOT__fin__DOT__mx;
        VlWide<4>/*127:0*/ LeafEval__DOT__markb;
        IData/*31:0*/ __VactIterCount;
        VlUnpacked<CData/*2:0*/, 128> LeafEval__DOT__bcell;
        VlUnpacked<CData/*1:0*/, 128> LeafEval__DOT__col_of;
        VlUnpacked<CData/*0:0*/, 128> LeafEval__DOT__occ_of;
        VlUnpacked<CData/*0:0*/, 128> LeafEval__DOT__vir_of;
        VlUnpacked<CData/*7:0*/, 512> LeafEval__DOT__slotram__DOT__mem;
    };
    VlTriggerVec<1> __VstlTriggered;
    VlTriggerVec<1> __VicoTriggered;
    VlTriggerVec<1> __VactTriggered;
    VlTriggerVec<1> __VnbaTriggered;

    // INTERNAL VARIABLES
    VLeafEval__Syms* const vlSymsp;

    // CONSTRUCTORS
    VLeafEval___024root(VLeafEval__Syms* symsp, const char* v__name);
    ~VLeafEval___024root();
    VL_UNCOPYABLE(VLeafEval___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
