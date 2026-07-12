// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VLeafEval.h for the primary calling header

#include "VLeafEval__pch.h"
#include "VLeafEval___024root.h"

void VLeafEval___024root___ico_sequent__TOP__0(VLeafEval___024root* vlSelf);

void VLeafEval___024root___eval_ico(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___eval_ico\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VicoTriggered.word(0U))) {
        VLeafEval___024root___ico_sequent__TOP__0(vlSelf);
    }
}

VL_INLINE_OPT void VLeafEval___024root___ico_sequent__TOP__0(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___ico_sequent__TOP__0\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.LeafEval__DOT__sl_wa = ((IData)(vlSelfRef.LeafEval__DOT__sl_cpw)
                                       ? (((IData)(vlSelfRef.a_sl) 
                                           << 7U) | (IData)(vlSelfRef.LeafEval__DOT__cpw_p))
                                       : (((IData)(vlSelfRef.wslot) 
                                           << 7U) | (IData)(vlSelfRef.waddr)));
}

void VLeafEval___024root___eval_triggers__ico(VLeafEval___024root* vlSelf);

bool VLeafEval___024root___eval_phase__ico(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___eval_phase__ico\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VicoExecute;
    // Body
    VLeafEval___024root___eval_triggers__ico(vlSelf);
    __VicoExecute = vlSelfRef.__VicoTriggered.any();
    if (__VicoExecute) {
        VLeafEval___024root___eval_ico(vlSelf);
    }
    return (__VicoExecute);
}

void VLeafEval___024root___eval_act(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___eval_act\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

void VLeafEval___024root___nba_sequent__TOP__0(VLeafEval___024root* vlSelf);

void VLeafEval___024root___eval_nba(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___eval_nba\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VLeafEval___024root___nba_sequent__TOP__0(vlSelf);
    }
}

VL_INLINE_OPT void VLeafEval___024root___nba_sequent__TOP__0(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___nba_sequent__TOP__0\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    SData/*8:0*/ __Vfunc_LeafEval__DOT__sq__1__Vfuncout;
    __Vfunc_LeafEval__DOT__sq__1__Vfuncout = 0;
    CData/*4:0*/ __Vfunc_LeafEval__DOT__sq__1__n;
    __Vfunc_LeafEval__DOT__sq__1__n = 0;
    SData/*8:0*/ __Vfunc_LeafEval__DOT__sq__2__Vfuncout;
    __Vfunc_LeafEval__DOT__sq__2__Vfuncout = 0;
    CData/*4:0*/ __Vfunc_LeafEval__DOT__sq__2__n;
    __Vfunc_LeafEval__DOT__sq__2__n = 0;
    SData/*8:0*/ __Vfunc_LeafEval__DOT__sq__3__Vfuncout;
    __Vfunc_LeafEval__DOT__sq__3__Vfuncout = 0;
    CData/*4:0*/ __Vfunc_LeafEval__DOT__sq__3__n;
    __Vfunc_LeafEval__DOT__sq__3__n = 0;
    CData/*4:0*/ __Vdly__LeafEval__DOT__st;
    __Vdly__LeafEval__DOT__st = 0;
    CData/*4:0*/ __Vdly__LeafEval__DOT__maxh;
    __Vdly__LeafEval__DOT__maxh = 0;
    CData/*7:0*/ __Vdly__LeafEval__DOT__holes;
    __Vdly__LeafEval__DOT__holes = 0;
    CData/*7:0*/ __Vdly__LeafEval__DOT__toprisk;
    __Vdly__LeafEval__DOT__toprisk = 0;
    CData/*7:0*/ __Vdly__LeafEval__DOT__spawn;
    __Vdly__LeafEval__DOT__spawn = 0;
    CData/*7:0*/ __Vdly__LeafEval__DOT__setup;
    __Vdly__LeafEval__DOT__setup = 0;
    SData/*10:0*/ __Vdly__LeafEval__DOT__pollution;
    __Vdly__LeafEval__DOT__pollution = 0;
    SData/*9:0*/ __Vdly__LeafEval__DOT__buried;
    __Vdly__LeafEval__DOT__buried = 0;
    SData/*15:0*/ __Vdly__LeafEval__DOT__rdy_ext;
    __Vdly__LeafEval__DOT__rdy_ext = 0;
    SData/*15:0*/ __Vdly__LeafEval__DOT__vrdy;
    __Vdly__LeafEval__DOT__vrdy = 0;
    CData/*0:0*/ __Vdly__LeafEval__DOT__anyvir;
    __Vdly__LeafEval__DOT__anyvir = 0;
    CData/*3:0*/ __Vdly__LeafEval__DOT__wc;
    __Vdly__LeafEval__DOT__wc = 0;
    CData/*3:0*/ __Vdly__LeafEval__DOT__wr_;
    __Vdly__LeafEval__DOT__wr_ = 0;
    CData/*0:0*/ __Vdly__LeafEval__DOT__seen;
    __Vdly__LeafEval__DOT__seen = 0;
    CData/*4:0*/ __Vdly__LeafEval__DOT__fillcnt;
    __Vdly__LeafEval__DOT__fillcnt = 0;
    CData/*3:0*/ __Vdly__LeafEval__DOT__cmd_l;
    __Vdly__LeafEval__DOT__cmd_l = 0;
    CData/*0:0*/ __Vdly__LeafEval__DOT__node_leaf;
    __Vdly__LeafEval__DOT__node_leaf = 0;
    CData/*5:0*/ __Vdly__rv_cells;
    __Vdly__rv_cells = 0;
    CData/*3:0*/ __Vdly__rv_vir;
    __Vdly__rv_vir = 0;
    VlWide<4>/*127:0*/ __Vdly__LeafEval__DOT__markb;
    VL_ZERO_W(128, __Vdly__LeafEval__DOT__markb);
    CData/*0:0*/ __Vdly__LeafEval__DOT__anyclear;
    __Vdly__LeafEval__DOT__anyclear = 0;
    CData/*4:0*/ __Vdly__LeafEval__DOT__fwp;
    __Vdly__LeafEval__DOT__fwp = 0;
    CData/*6:0*/ __Vdly__LeafEval__DOT__fwp2;
    __Vdly__LeafEval__DOT__fwp2 = 0;
    CData/*6:0*/ __Vdly__LeafEval__DOT__cpw_p;
    __Vdly__LeafEval__DOT__cpw_p = 0;
    SData/*8:0*/ __Vdly__LeafEval__DOT__sr_addr;
    __Vdly__LeafEval__DOT__sr_addr = 0;
    CData/*4:0*/ __Vdly__LeafEval__DOT__fo1;
    __Vdly__LeafEval__DOT__fo1 = 0;
    CData/*6:0*/ __Vdly__LeafEval__DOT__off_b;
    __Vdly__LeafEval__DOT__off_b = 0;
    CData/*6:0*/ __Vdly__LeafEval__DOT__off_a;
    __Vdly__LeafEval__DOT__off_a = 0;
    CData/*1:0*/ __Vdly__LeafEval__DOT__li;
    __Vdly__LeafEval__DOT__li = 0;
    CData/*3:0*/ __Vdly__LeafEval__DOT__sstep;
    __Vdly__LeafEval__DOT__sstep = 0;
    CData/*4:0*/ __Vdly__LeafEval__DOT__scnt;
    __Vdly__LeafEval__DOT__scnt = 0;
    CData/*4:0*/ __Vdly__LeafEval__DOT__srun;
    __Vdly__LeafEval__DOT__srun = 0;
    CData/*1:0*/ __Vdly__LeafEval__DOT__smcol;
    __Vdly__LeafEval__DOT__smcol = 0;
    CData/*7:0*/ __Vdly__LeafEval__DOT__soff;
    __Vdly__LeafEval__DOT__soff = 0;
    CData/*7:0*/ __Vdly__LeafEval__DOT__srstart;
    __Vdly__LeafEval__DOT__srstart = 0;
    CData/*4:0*/ __Vdly__LeafEval__DOT__gdest;
    __Vdly__LeafEval__DOT__gdest = 0;
    CData/*6:0*/ __Vdly__LeafEval__DOT__vo;
    __Vdly__LeafEval__DOT__vo = 0;
    CData/*4:0*/ __Vdly__LeafEval__DOT__run_h;
    __Vdly__LeafEval__DOT__run_h = 0;
    CData/*4:0*/ __Vdly__LeafEval__DOT__run_v;
    __Vdly__LeafEval__DOT__run_v = 0;
    CData/*4:0*/ __Vdly__LeafEval__DOT__p;
    __Vdly__LeafEval__DOT__p = 0;
    CData/*4:0*/ __Vdly__LeafEval__DOT__span_lo;
    __Vdly__LeafEval__DOT__span_lo = 0;
    CData/*4:0*/ __Vdly__LeafEval__DOT__span_hi;
    __Vdly__LeafEval__DOT__span_hi = 0;
    CData/*4:0*/ __Vdly__LeafEval__DOT__vspan_lo;
    __Vdly__LeafEval__DOT__vspan_lo = 0;
    CData/*4:0*/ __Vdly__LeafEval__DOT__vspan_hi;
    __Vdly__LeafEval__DOT__vspan_hi = 0;
    CData/*2:0*/ __VdlyVal__LeafEval__DOT__bcell__v0;
    __VdlyVal__LeafEval__DOT__bcell__v0 = 0;
    CData/*6:0*/ __VdlyDim0__LeafEval__DOT__bcell__v0;
    __VdlyDim0__LeafEval__DOT__bcell__v0 = 0;
    CData/*0:0*/ __VdlySet__LeafEval__DOT__bcell__v0;
    __VdlySet__LeafEval__DOT__bcell__v0 = 0;
    CData/*2:0*/ __VdlyVal__LeafEval__DOT__bcell__v1;
    __VdlyVal__LeafEval__DOT__bcell__v1 = 0;
    CData/*6:0*/ __VdlyDim0__LeafEval__DOT__bcell__v1;
    __VdlyDim0__LeafEval__DOT__bcell__v1 = 0;
    CData/*0:0*/ __VdlySet__LeafEval__DOT__bcell__v1;
    __VdlySet__LeafEval__DOT__bcell__v1 = 0;
    CData/*2:0*/ __VdlyVal__LeafEval__DOT__bcell__v2;
    __VdlyVal__LeafEval__DOT__bcell__v2 = 0;
    CData/*6:0*/ __VdlyDim0__LeafEval__DOT__bcell__v2;
    __VdlyDim0__LeafEval__DOT__bcell__v2 = 0;
    CData/*0:0*/ __VdlySet__LeafEval__DOT__bcell__v2;
    __VdlySet__LeafEval__DOT__bcell__v2 = 0;
    CData/*2:0*/ __VdlyVal__LeafEval__DOT__bcell__v3;
    __VdlyVal__LeafEval__DOT__bcell__v3 = 0;
    CData/*6:0*/ __VdlyDim0__LeafEval__DOT__bcell__v3;
    __VdlyDim0__LeafEval__DOT__bcell__v3 = 0;
    CData/*0:0*/ __VdlySet__LeafEval__DOT__bcell__v3;
    __VdlySet__LeafEval__DOT__bcell__v3 = 0;
    CData/*6:0*/ __VdlyDim0__LeafEval__DOT__bcell__v4;
    __VdlyDim0__LeafEval__DOT__bcell__v4 = 0;
    CData/*0:0*/ __VdlySet__LeafEval__DOT__bcell__v4;
    __VdlySet__LeafEval__DOT__bcell__v4 = 0;
    CData/*2:0*/ __VdlyVal__LeafEval__DOT__bcell__v5;
    __VdlyVal__LeafEval__DOT__bcell__v5 = 0;
    CData/*6:0*/ __VdlyDim0__LeafEval__DOT__bcell__v5;
    __VdlyDim0__LeafEval__DOT__bcell__v5 = 0;
    CData/*0:0*/ __VdlySet__LeafEval__DOT__bcell__v5;
    __VdlySet__LeafEval__DOT__bcell__v5 = 0;
    CData/*6:0*/ __VdlyDim0__LeafEval__DOT__bcell__v6;
    __VdlyDim0__LeafEval__DOT__bcell__v6 = 0;
    CData/*7:0*/ __VdlyVal__LeafEval__DOT__slotram__DOT__mem__v0;
    __VdlyVal__LeafEval__DOT__slotram__DOT__mem__v0 = 0;
    SData/*8:0*/ __VdlyDim0__LeafEval__DOT__slotram__DOT__mem__v0;
    __VdlyDim0__LeafEval__DOT__slotram__DOT__mem__v0 = 0;
    CData/*0:0*/ __VdlySet__LeafEval__DOT__slotram__DOT__mem__v0;
    __VdlySet__LeafEval__DOT__slotram__DOT__mem__v0 = 0;
    // Body
    __Vdly__LeafEval__DOT__st = vlSelfRef.LeafEval__DOT__st;
    __Vdly__LeafEval__DOT__maxh = vlSelfRef.LeafEval__DOT__maxh;
    __Vdly__LeafEval__DOT__holes = vlSelfRef.LeafEval__DOT__holes;
    __Vdly__LeafEval__DOT__toprisk = vlSelfRef.LeafEval__DOT__toprisk;
    __Vdly__LeafEval__DOT__spawn = vlSelfRef.LeafEval__DOT__spawn;
    __Vdly__LeafEval__DOT__setup = vlSelfRef.LeafEval__DOT__setup;
    __Vdly__LeafEval__DOT__pollution = vlSelfRef.LeafEval__DOT__pollution;
    __Vdly__LeafEval__DOT__buried = vlSelfRef.LeafEval__DOT__buried;
    __Vdly__LeafEval__DOT__rdy_ext = vlSelfRef.LeafEval__DOT__rdy_ext;
    __Vdly__LeafEval__DOT__vrdy = vlSelfRef.LeafEval__DOT__vrdy;
    __Vdly__LeafEval__DOT__anyvir = vlSelfRef.LeafEval__DOT__anyvir;
    __Vdly__LeafEval__DOT__wc = vlSelfRef.LeafEval__DOT__wc;
    __Vdly__LeafEval__DOT__wr_ = vlSelfRef.LeafEval__DOT__wr_;
    __Vdly__LeafEval__DOT__seen = vlSelfRef.LeafEval__DOT__seen;
    __Vdly__LeafEval__DOT__fillcnt = vlSelfRef.LeafEval__DOT__fillcnt;
    __Vdly__LeafEval__DOT__cmd_l = vlSelfRef.LeafEval__DOT__cmd_l;
    __Vdly__LeafEval__DOT__node_leaf = vlSelfRef.LeafEval__DOT__node_leaf;
    __Vdly__rv_cells = vlSelfRef.rv_cells;
    __Vdly__rv_vir = vlSelfRef.rv_vir;
    __Vdly__LeafEval__DOT__markb[0U] = vlSelfRef.LeafEval__DOT__markb[0U];
    __Vdly__LeafEval__DOT__markb[1U] = vlSelfRef.LeafEval__DOT__markb[1U];
    __Vdly__LeafEval__DOT__markb[2U] = vlSelfRef.LeafEval__DOT__markb[2U];
    __Vdly__LeafEval__DOT__markb[3U] = vlSelfRef.LeafEval__DOT__markb[3U];
    __Vdly__LeafEval__DOT__anyclear = vlSelfRef.LeafEval__DOT__anyclear;
    __Vdly__LeafEval__DOT__fwp = vlSelfRef.LeafEval__DOT__fwp;
    __Vdly__LeafEval__DOT__fwp2 = vlSelfRef.LeafEval__DOT__fwp2;
    __Vdly__LeafEval__DOT__sr_addr = vlSelfRef.LeafEval__DOT__sr_addr;
    __Vdly__LeafEval__DOT__fo1 = vlSelfRef.LeafEval__DOT__fo1;
    __Vdly__LeafEval__DOT__off_b = vlSelfRef.LeafEval__DOT__off_b;
    __Vdly__LeafEval__DOT__off_a = vlSelfRef.LeafEval__DOT__off_a;
    __Vdly__LeafEval__DOT__li = vlSelfRef.LeafEval__DOT__li;
    __Vdly__LeafEval__DOT__sstep = vlSelfRef.LeafEval__DOT__sstep;
    __Vdly__LeafEval__DOT__scnt = vlSelfRef.LeafEval__DOT__scnt;
    __Vdly__LeafEval__DOT__srun = vlSelfRef.LeafEval__DOT__srun;
    __Vdly__LeafEval__DOT__smcol = vlSelfRef.LeafEval__DOT__smcol;
    __Vdly__LeafEval__DOT__soff = vlSelfRef.LeafEval__DOT__soff;
    __Vdly__LeafEval__DOT__srstart = vlSelfRef.LeafEval__DOT__srstart;
    __Vdly__LeafEval__DOT__gdest = vlSelfRef.LeafEval__DOT__gdest;
    __Vdly__LeafEval__DOT__run_h = vlSelfRef.LeafEval__DOT__run_h;
    __Vdly__LeafEval__DOT__run_v = vlSelfRef.LeafEval__DOT__run_v;
    __Vdly__LeafEval__DOT__p = vlSelfRef.LeafEval__DOT__p;
    __Vdly__LeafEval__DOT__span_lo = vlSelfRef.LeafEval__DOT__span_lo;
    __Vdly__LeafEval__DOT__span_hi = vlSelfRef.LeafEval__DOT__span_hi;
    __Vdly__LeafEval__DOT__vspan_lo = vlSelfRef.LeafEval__DOT__vspan_lo;
    __Vdly__LeafEval__DOT__vspan_hi = vlSelfRef.LeafEval__DOT__vspan_hi;
    __Vdly__LeafEval__DOT__cpw_p = vlSelfRef.LeafEval__DOT__cpw_p;
    __Vdly__LeafEval__DOT__vo = vlSelfRef.LeafEval__DOT__vo;
    __VdlySet__LeafEval__DOT__bcell__v0 = 0U;
    __VdlySet__LeafEval__DOT__bcell__v1 = 0U;
    __VdlySet__LeafEval__DOT__bcell__v2 = 0U;
    __VdlySet__LeafEval__DOT__bcell__v3 = 0U;
    __VdlySet__LeafEval__DOT__bcell__v4 = 0U;
    __VdlySet__LeafEval__DOT__bcell__v5 = 0U;
    __VdlySet__LeafEval__DOT__slotram__DOT__mem__v0 = 0U;
    if ((((IData)(vlSelfRef.wr) & (0U != (IData)(vlSelfRef.wslot))) 
         | (IData)(vlSelfRef.LeafEval__DOT__sl_cpw))) {
        __VdlyVal__LeafEval__DOT__slotram__DOT__mem__v0 
            = ((IData)(vlSelfRef.LeafEval__DOT__sl_cpw)
                ? vlSelfRef.LeafEval__DOT__bcell[vlSelfRef.LeafEval__DOT__cpw_p]
                : (IData)(vlSelfRef.wdata));
        __VdlyDim0__LeafEval__DOT__slotram__DOT__mem__v0 
            = vlSelfRef.LeafEval__DOT__sl_wa;
        __VdlySet__LeafEval__DOT__slotram__DOT__mem__v0 = 1U;
    }
    if (vlSelfRef.rst) {
        __Vdly__LeafEval__DOT__st = 0U;
        vlSelfRef.done = 0U;
        vlSelfRef.LeafEval__DOT__sl_cpw = 0U;
    } else {
        if (((IData)(vlSelfRef.wr) & (0U == (IData)(vlSelfRef.wslot)))) {
            __VdlyVal__LeafEval__DOT__bcell__v0 = vlSelfRef.wdata;
            __VdlyDim0__LeafEval__DOT__bcell__v0 = vlSelfRef.waddr;
            __VdlySet__LeafEval__DOT__bcell__v0 = 1U;
        }
        if (((((((((0U == (IData)(vlSelfRef.LeafEval__DOT__st)) 
                   | (0x11U == (IData)(vlSelfRef.LeafEval__DOT__st))) 
                  | (0x1cU == (IData)(vlSelfRef.LeafEval__DOT__st))) 
                 | (0x1aU == (IData)(vlSelfRef.LeafEval__DOT__st))) 
                | (0x1bU == (IData)(vlSelfRef.LeafEval__DOT__st))) 
               | (0x12U == (IData)(vlSelfRef.LeafEval__DOT__st))) 
              | (0x13U == (IData)(vlSelfRef.LeafEval__DOT__st))) 
             | (0x14U == (IData)(vlSelfRef.LeafEval__DOT__st)))) {
            if ((0U == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                if (((IData)(vlSelfRef.start) | (IData)(vlSelfRef.cmd_go))) {
                    vlSelfRef.done = 0U;
                    if (((IData)(vlSelfRef.start) | 
                         (1U == (IData)(vlSelfRef.cmd)))) {
                        __Vdly__LeafEval__DOT__maxh = 0U;
                        __Vdly__LeafEval__DOT__holes = 0U;
                        __Vdly__LeafEval__DOT__toprisk = 0U;
                        __Vdly__LeafEval__DOT__spawn = 0U;
                        __Vdly__LeafEval__DOT__setup = 0U;
                        __Vdly__LeafEval__DOT__pollution = 0U;
                        __Vdly__LeafEval__DOT__buried = 0U;
                        __Vdly__LeafEval__DOT__rdy_ext = 0U;
                        __Vdly__LeafEval__DOT__vrdy = 0U;
                        __Vdly__LeafEval__DOT__anyvir = 0U;
                        __Vdly__LeafEval__DOT__wc = 0U;
                        __Vdly__LeafEval__DOT__wr_ = 0U;
                        __Vdly__LeafEval__DOT__seen = 0U;
                        __Vdly__LeafEval__DOT__fillcnt = 0U;
                        __Vdly__LeafEval__DOT__st = 1U;
                    } else if (((2U == (IData)(vlSelfRef.cmd)) 
                                | (3U == (IData)(vlSelfRef.cmd)))) {
                        __Vdly__LeafEval__DOT__cmd_l 
                            = vlSelfRef.cmd;
                        __Vdly__LeafEval__DOT__st = 0x11U;
                    } else if ((4U == (IData)(vlSelfRef.cmd))) {
                        __Vdly__LeafEval__DOT__node_leaf = 1U;
                        vlSelfRef.legal = 0U;
                        __Vdly__rv_cells = 0U;
                        __Vdly__rv_vir = 0U;
                        vlSelfRef.imm = 0U;
                        __Vdly__LeafEval__DOT__markb[0U] = 0U;
                        __Vdly__LeafEval__DOT__markb[1U] = 0U;
                        __Vdly__LeafEval__DOT__markb[2U] = 0U;
                        __Vdly__LeafEval__DOT__markb[3U] = 0U;
                        __Vdly__LeafEval__DOT__anyclear = 0U;
                        __Vdly__LeafEval__DOT__fwp = 0U;
                        __Vdly__LeafEval__DOT__st = 0x12U;
                    }
                }
            } else if ((0x11U == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                __Vdly__LeafEval__DOT__fwp2 = 0U;
                __Vdly__LeafEval__DOT__cpw_p = 0U;
                __Vdly__LeafEval__DOT__sr_addr = ((IData)(vlSelfRef.a_sl) 
                                                  << 7U);
                if ((2U == (IData)(vlSelfRef.LeafEval__DOT__cmd_l))) {
                    __Vdly__LeafEval__DOT__st = 0x1cU;
                } else {
                    vlSelfRef.LeafEval__DOT__sl_cpw = 1U;
                    __Vdly__LeafEval__DOT__st = 0x1bU;
                }
            } else if ((0x1cU == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                __Vdly__LeafEval__DOT__sr_addr = (0x1ffU 
                                                  & ((IData)(1U) 
                                                     + (IData)(vlSelfRef.LeafEval__DOT__sr_addr)));
                __Vdly__LeafEval__DOT__st = 0x1aU;
            } else if ((0x1aU == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                __Vdly__LeafEval__DOT__sr_addr = (0x1ffU 
                                                  & ((IData)(1U) 
                                                     + (IData)(vlSelfRef.LeafEval__DOT__sr_addr)));
                __VdlyVal__LeafEval__DOT__bcell__v1 
                    = (7U & (IData)(vlSelfRef.LeafEval__DOT__sl_qb));
                __VdlyDim0__LeafEval__DOT__bcell__v1 
                    = vlSelfRef.LeafEval__DOT__fwp2;
                __VdlySet__LeafEval__DOT__bcell__v1 = 1U;
                if ((0x7fU == (IData)(vlSelfRef.LeafEval__DOT__fwp2))) {
                    vlSelfRef.done = 1U;
                    __Vdly__LeafEval__DOT__st = 0U;
                } else {
                    __Vdly__LeafEval__DOT__fwp2 = (0x7fU 
                                                   & ((IData)(1U) 
                                                      + (IData)(vlSelfRef.LeafEval__DOT__fwp2)));
                }
            } else if ((0x1bU == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                if ((0x7fU == (IData)(vlSelfRef.LeafEval__DOT__cpw_p))) {
                    vlSelfRef.LeafEval__DOT__sl_cpw = 0U;
                    vlSelfRef.done = 1U;
                    __Vdly__LeafEval__DOT__st = 0U;
                } else {
                    __Vdly__LeafEval__DOT__cpw_p = 
                        (0x7fU & ((IData)(1U) + (IData)(vlSelfRef.LeafEval__DOT__cpw_p)));
                }
            } else if ((0x12U == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                if (((0x10U == (IData)(vlSelfRef.LeafEval__DOT__fwp)) 
                     | vlSelfRef.LeafEval__DOT__occ_of
                     [((0x78U & ((IData)(vlSelfRef.LeafEval__DOT__fwp) 
                                 << 3U)) | (IData)(vlSelfRef.a_col))])) {
                    __Vdly__LeafEval__DOT__fo1 = vlSelfRef.LeafEval__DOT__fwp;
                    if ((2U & (IData)(vlSelfRef.a_o4))) {
                        if ((7U == (IData)(vlSelfRef.a_col))) {
                            vlSelfRef.done = 1U;
                            __Vdly__LeafEval__DOT__st = 0U;
                        } else {
                            __Vdly__LeafEval__DOT__st = 0x13U;
                        }
                    } else if ((2U <= (IData)(vlSelfRef.LeafEval__DOT__fwp))) {
                        __Vdly__LeafEval__DOT__off_b 
                            = ((0x78U & (((IData)(vlSelfRef.LeafEval__DOT__fwp) 
                                          - (IData)(1U)) 
                                         << 3U)) | (IData)(vlSelfRef.a_col));
                        vlSelfRef.legal = 1U;
                        __Vdly__LeafEval__DOT__st = 0x14U;
                        __Vdly__LeafEval__DOT__off_a 
                            = ((0x78U & (((IData)(vlSelfRef.LeafEval__DOT__fwp) 
                                          - (IData)(2U)) 
                                         << 3U)) | (IData)(vlSelfRef.a_col));
                    } else {
                        vlSelfRef.done = 1U;
                        __Vdly__LeafEval__DOT__st = 0U;
                    }
                    __Vdly__LeafEval__DOT__fwp = 0U;
                } else {
                    __Vdly__LeafEval__DOT__fwp = (0x1fU 
                                                  & ((IData)(1U) 
                                                     + (IData)(vlSelfRef.LeafEval__DOT__fwp)));
                }
            } else if ((0x13U == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                if (((0x10U == (IData)(vlSelfRef.LeafEval__DOT__fwp)) 
                     | vlSelfRef.LeafEval__DOT__occ_of
                     [((0x78U & ((IData)(vlSelfRef.LeafEval__DOT__fwp) 
                                 << 3U)) | (7U & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.a_col))))])) {
                    vlSelfRef.LeafEval__DOT__fo2b__DOT__fom 
                        = (((IData)(vlSelfRef.LeafEval__DOT__fo1) 
                            < (IData)(vlSelfRef.LeafEval__DOT__fwp))
                            ? (IData)(vlSelfRef.LeafEval__DOT__fo1)
                            : (IData)(vlSelfRef.LeafEval__DOT__fwp));
                    if ((1U <= (IData)(vlSelfRef.LeafEval__DOT__fo2b__DOT__fom))) {
                        __Vdly__LeafEval__DOT__off_a 
                            = ((0x78U & (((IData)(vlSelfRef.LeafEval__DOT__fo2b__DOT__fom) 
                                          - (IData)(1U)) 
                                         << 3U)) | (IData)(vlSelfRef.a_col));
                        vlSelfRef.legal = 1U;
                        __Vdly__LeafEval__DOT__st = 0x14U;
                        __Vdly__LeafEval__DOT__off_b 
                            = ((0x78U & (((IData)(vlSelfRef.LeafEval__DOT__fo2b__DOT__fom) 
                                          - (IData)(1U)) 
                                         << 3U)) | 
                               (7U & ((IData)(1U) + (IData)(vlSelfRef.a_col))));
                    } else {
                        vlSelfRef.done = 1U;
                        __Vdly__LeafEval__DOT__st = 0U;
                    }
                } else {
                    __Vdly__LeafEval__DOT__fwp = (0x1fU 
                                                  & ((IData)(1U) 
                                                     + (IData)(vlSelfRef.LeafEval__DOT__fwp)));
                }
            } else {
                if ((1U & (IData)(vlSelfRef.a_o4))) {
                    __VdlyVal__LeafEval__DOT__bcell__v2 
                        = vlSelfRef.a_cb;
                    __VdlyVal__LeafEval__DOT__bcell__v3 
                        = vlSelfRef.a_ca;
                } else {
                    __VdlyVal__LeafEval__DOT__bcell__v2 
                        = vlSelfRef.a_ca;
                    __VdlyVal__LeafEval__DOT__bcell__v3 
                        = vlSelfRef.a_cb;
                }
                __VdlyDim0__LeafEval__DOT__bcell__v2 
                    = vlSelfRef.LeafEval__DOT__off_a;
                __VdlySet__LeafEval__DOT__bcell__v2 = 1U;
                __Vdly__LeafEval__DOT__li = 0U;
                __Vdly__LeafEval__DOT__st = 0x15U;
                __Vdly__LeafEval__DOT__sstep = 1U;
                __Vdly__LeafEval__DOT__scnt = 8U;
                __Vdly__LeafEval__DOT__srun = 0U;
                __Vdly__LeafEval__DOT__smcol = 0U;
                __VdlyDim0__LeafEval__DOT__bcell__v3 
                    = vlSelfRef.LeafEval__DOT__off_b;
                __VdlySet__LeafEval__DOT__bcell__v3 = 1U;
                __Vdly__LeafEval__DOT__soff = (0x78U 
                                               & (IData)(vlSelfRef.LeafEval__DOT__off_a));
            }
        } else if (((((((((0x15U == (IData)(vlSelfRef.LeafEval__DOT__st)) 
                          | (0x16U == (IData)(vlSelfRef.LeafEval__DOT__st))) 
                         | (0x17U == (IData)(vlSelfRef.LeafEval__DOT__st))) 
                        | (0x18U == (IData)(vlSelfRef.LeafEval__DOT__st))) 
                       | (0x19U == (IData)(vlSelfRef.LeafEval__DOT__st))) 
                      | (1U == (IData)(vlSelfRef.LeafEval__DOT__st))) 
                     | (2U == (IData)(vlSelfRef.LeafEval__DOT__st))) 
                    | (3U == (IData)(vlSelfRef.LeafEval__DOT__st)))) {
            if ((0x15U == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                vlSelfRef.LeafEval__DOT__scan__DOT__c_ 
                    = vlSelfRef.LeafEval__DOT__col_of
                    [(0x7fU & (IData)(vlSelfRef.LeafEval__DOT__soff))];
                vlSelfRef.LeafEval__DOT__scan__DOT__brk 
                    = ((0U == (IData)(vlSelfRef.LeafEval__DOT__scan__DOT__c_)) 
                       | ((IData)(vlSelfRef.LeafEval__DOT__scan__DOT__c_) 
                          != (IData)(vlSelfRef.LeafEval__DOT__smcol)));
                if (((IData)(vlSelfRef.LeafEval__DOT__scan__DOT__brk) 
                     & (4U <= (IData)(vlSelfRef.LeafEval__DOT__srun)))) {
                    if ((0U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & (IData)(vlSelfRef.LeafEval__DOT__srstart))));
                    }
                    if ((1U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + (IData)(vlSelfRef.LeafEval__DOT__sstep)) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + (IData)(vlSelfRef.LeafEval__DOT__sstep)) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + (IData)(vlSelfRef.LeafEval__DOT__sstep)))));
                    }
                    if ((2U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.LeafEval__DOT__sstep), 1U)) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.LeafEval__DOT__sstep), 1U)) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.LeafEval__DOT__sstep), 1U)))));
                    }
                    if ((3U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(3U) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(3U) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(3U) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((4U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.LeafEval__DOT__sstep), 2U)) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.LeafEval__DOT__sstep), 2U)) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.LeafEval__DOT__sstep), 2U)))));
                    }
                    if ((5U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(5U) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(5U) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(5U) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((6U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(6U) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(6U) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(6U) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((7U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(7U) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(7U) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(7U) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((8U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.LeafEval__DOT__sstep), 3U)) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.LeafEval__DOT__sstep), 3U)) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.LeafEval__DOT__sstep), 3U)))));
                    }
                    if ((9U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(9U) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(9U) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(9U) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((0xaU < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(0xaU) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(0xaU) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xaU) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((0xbU < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(0xbU) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(0xbU) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xbU) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((0xcU < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(0xcU) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(0xcU) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xcU) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((0xdU < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(0xdU) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(0xdU) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xdU) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((0xeU < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(0xeU) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(0xeU) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xeU) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((0xfU < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(0xfU) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(0xfU) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xfU) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                }
                if ((0U == (IData)(vlSelfRef.LeafEval__DOT__scan__DOT__c_))) {
                    __Vdly__LeafEval__DOT__srun = 0U;
                    __Vdly__LeafEval__DOT__smcol = 0U;
                } else if (((IData)(vlSelfRef.LeafEval__DOT__scan__DOT__c_) 
                            != (IData)(vlSelfRef.LeafEval__DOT__smcol))) {
                    __Vdly__LeafEval__DOT__smcol = vlSelfRef.LeafEval__DOT__scan__DOT__c_;
                    __Vdly__LeafEval__DOT__srstart 
                        = vlSelfRef.LeafEval__DOT__soff;
                    __Vdly__LeafEval__DOT__srun = 1U;
                } else {
                    __Vdly__LeafEval__DOT__srun = (0x1fU 
                                                   & ((IData)(1U) 
                                                      + (IData)(vlSelfRef.LeafEval__DOT__srun)));
                }
                if ((1U == (IData)(vlSelfRef.LeafEval__DOT__scnt))) {
                    __Vdly__LeafEval__DOT__st = 0x16U;
                } else {
                    __Vdly__LeafEval__DOT__soff = (0xffU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__soff) 
                                                      + (IData)(vlSelfRef.LeafEval__DOT__sstep)));
                    __Vdly__LeafEval__DOT__scnt = (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__scnt) 
                                                      - (IData)(1U)));
                }
            } else if ((0x16U == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                if ((4U <= (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                    if ((0U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & (IData)(vlSelfRef.LeafEval__DOT__srstart))));
                    }
                    if ((1U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + (IData)(vlSelfRef.LeafEval__DOT__sstep)) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + (IData)(vlSelfRef.LeafEval__DOT__sstep)) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + (IData)(vlSelfRef.LeafEval__DOT__sstep)))));
                    }
                    if ((2U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.LeafEval__DOT__sstep), 1U)) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.LeafEval__DOT__sstep), 1U)) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.LeafEval__DOT__sstep), 1U)))));
                    }
                    if ((3U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(3U) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(3U) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(3U) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((4U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.LeafEval__DOT__sstep), 2U)) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.LeafEval__DOT__sstep), 2U)) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.LeafEval__DOT__sstep), 2U)))));
                    }
                    if ((5U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(5U) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(5U) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(5U) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((6U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(6U) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(6U) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(6U) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((7U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(7U) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(7U) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(7U) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((8U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.LeafEval__DOT__sstep), 3U)) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.LeafEval__DOT__sstep), 3U)) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.LeafEval__DOT__sstep), 3U)))));
                    }
                    if ((9U < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(9U) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(9U) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(9U) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((0xaU < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(0xaU) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(0xaU) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xaU) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((0xbU < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(0xbU) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(0xbU) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xbU) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((0xcU < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(0xcU) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(0xcU) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xcU) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((0xdU < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(0xdU) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(0xdU) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xdU) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((0xeU < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(0xeU) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(0xeU) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xeU) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                    if ((0xfU < (IData)(vlSelfRef.LeafEval__DOT__srun))) {
                        __Vdly__LeafEval__DOT__markb[(3U 
                                                      & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                          + 
                                                          ((IData)(0xfU) 
                                                           * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                                         >> 5U))] 
                            = (__Vdly__LeafEval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                       + ((IData)(0xfU) 
                                          * (IData)(vlSelfRef.LeafEval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.LeafEval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xfU) 
                                                       * (IData)(vlSelfRef.LeafEval__DOT__sstep))))));
                    }
                }
                __Vdly__LeafEval__DOT__smcol = 0U;
                __Vdly__LeafEval__DOT__srun = 0U;
                if ((0U == (IData)(vlSelfRef.LeafEval__DOT__li))) {
                    __Vdly__LeafEval__DOT__soff = (7U 
                                                   & (IData)(vlSelfRef.LeafEval__DOT__off_a));
                    __Vdly__LeafEval__DOT__sstep = 8U;
                    __Vdly__LeafEval__DOT__scnt = 0x10U;
                    __Vdly__LeafEval__DOT__li = 1U;
                    __Vdly__LeafEval__DOT__st = 0x15U;
                } else if ((1U == (IData)(vlSelfRef.LeafEval__DOT__li))) {
                    __Vdly__LeafEval__DOT__soff = (0x78U 
                                                   & (IData)(vlSelfRef.LeafEval__DOT__off_b));
                    __Vdly__LeafEval__DOT__sstep = 1U;
                    __Vdly__LeafEval__DOT__scnt = 8U;
                    __Vdly__LeafEval__DOT__li = 2U;
                    __Vdly__LeafEval__DOT__st = 0x15U;
                } else if ((2U == (IData)(vlSelfRef.LeafEval__DOT__li))) {
                    __Vdly__LeafEval__DOT__soff = (7U 
                                                   & (IData)(vlSelfRef.LeafEval__DOT__off_b));
                    __Vdly__LeafEval__DOT__sstep = 8U;
                    __Vdly__LeafEval__DOT__scnt = 0x10U;
                    __Vdly__LeafEval__DOT__li = 3U;
                    __Vdly__LeafEval__DOT__st = 0x15U;
                } else {
                    __Vdly__LeafEval__DOT__fwp2 = 0U;
                    __Vdly__LeafEval__DOT__st = 0x17U;
                }
            } else if ((0x17U == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                if ((1U & (vlSelfRef.LeafEval__DOT__markb[
                           ((IData)(vlSelfRef.LeafEval__DOT__fwp2) 
                            >> 5U)] >> (0x1fU & (IData)(vlSelfRef.LeafEval__DOT__fwp2))))) {
                    __Vdly__rv_cells = (0x3fU & ((IData)(1U) 
                                                 + (IData)(vlSelfRef.rv_cells)));
                    if (vlSelfRef.LeafEval__DOT__vir_of
                        [vlSelfRef.LeafEval__DOT__fwp2]) {
                        __Vdly__rv_vir = (0xfU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.rv_vir)));
                    }
                    __VdlyDim0__LeafEval__DOT__bcell__v4 
                        = vlSelfRef.LeafEval__DOT__fwp2;
                    __VdlySet__LeafEval__DOT__bcell__v4 = 1U;
                    __Vdly__LeafEval__DOT__anyclear = 1U;
                }
                if ((0x7fU == (IData)(vlSelfRef.LeafEval__DOT__fwp2))) {
                    __Vdly__LeafEval__DOT__wc = 0U;
                    __Vdly__LeafEval__DOT__gdest = 0xfU;
                    __Vdly__LeafEval__DOT__fwp = 0xfU;
                    __Vdly__LeafEval__DOT__st = (((IData)(vlSelfRef.LeafEval__DOT__anyclear) 
                                                  | (vlSelfRef.LeafEval__DOT__markb[3U] 
                                                     >> 0x1fU))
                                                  ? 0x18U
                                                  : 0x19U);
                } else {
                    __Vdly__LeafEval__DOT__fwp2 = (0x7fU 
                                                   & ((IData)(1U) 
                                                      + (IData)(vlSelfRef.LeafEval__DOT__fwp2)));
                }
            } else if ((0x18U == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                vlSelfRef.LeafEval__DOT__grv__DOT__t 
                    = vlSelfRef.LeafEval__DOT__bcell
                    [((0x78U & ((IData)(vlSelfRef.LeafEval__DOT__fwp) 
                                << 3U)) | (7U & (IData)(vlSelfRef.LeafEval__DOT__wc)))];
                if ((0U != (IData)(vlSelfRef.LeafEval__DOT__grv__DOT__t))) {
                    if ((4U & (IData)(vlSelfRef.LeafEval__DOT__grv__DOT__t))) {
                        __Vdly__LeafEval__DOT__gdest 
                            = (0x1fU & ((IData)(vlSelfRef.LeafEval__DOT__fwp) 
                                        - (IData)(1U)));
                    } else {
                        if (((IData)(vlSelfRef.LeafEval__DOT__gdest) 
                             != (IData)(vlSelfRef.LeafEval__DOT__fwp))) {
                            __VdlyVal__LeafEval__DOT__bcell__v5 
                                = vlSelfRef.LeafEval__DOT__grv__DOT__t;
                            __VdlyDim0__LeafEval__DOT__bcell__v5 
                                = ((0x78U & ((IData)(vlSelfRef.LeafEval__DOT__gdest) 
                                             << 3U)) 
                                   | (7U & (IData)(vlSelfRef.LeafEval__DOT__wc)));
                            __VdlySet__LeafEval__DOT__bcell__v5 = 1U;
                            __VdlyDim0__LeafEval__DOT__bcell__v6 
                                = ((0x78U & ((IData)(vlSelfRef.LeafEval__DOT__fwp) 
                                             << 3U)) 
                                   | (7U & (IData)(vlSelfRef.LeafEval__DOT__wc)));
                        }
                        __Vdly__LeafEval__DOT__gdest 
                            = (0x1fU & ((IData)(vlSelfRef.LeafEval__DOT__gdest) 
                                        - (IData)(1U)));
                    }
                }
                if ((0U == (IData)(vlSelfRef.LeafEval__DOT__fwp))) {
                    if ((7U == (IData)(vlSelfRef.LeafEval__DOT__wc))) {
                        __Vdly__LeafEval__DOT__st = 0x19U;
                    } else {
                        __Vdly__LeafEval__DOT__wc = 
                            (0xfU & ((IData)(1U) + (IData)(vlSelfRef.LeafEval__DOT__wc)));
                        __Vdly__LeafEval__DOT__gdest = 0xfU;
                        __Vdly__LeafEval__DOT__fwp = 0xfU;
                    }
                } else {
                    __Vdly__LeafEval__DOT__fwp = (0x1fU 
                                                  & ((IData)(vlSelfRef.LeafEval__DOT__fwp) 
                                                     - (IData)(1U)));
                }
            } else if ((0x19U == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                vlSelfRef.imm = (0xffffU & (((IData)(0xb4U) 
                                             * (IData)(vlSelfRef.rv_vir)) 
                                            + ((IData)(0xaU) 
                                               * (IData)(vlSelfRef.rv_cells))));
                if (vlSelfRef.LeafEval__DOT__node_leaf) {
                    __Vdly__LeafEval__DOT__maxh = 0U;
                    __Vdly__LeafEval__DOT__holes = 0U;
                    __Vdly__LeafEval__DOT__toprisk = 0U;
                    __Vdly__LeafEval__DOT__spawn = 0U;
                    __Vdly__LeafEval__DOT__setup = 0U;
                    __Vdly__LeafEval__DOT__pollution = 0U;
                    __Vdly__LeafEval__DOT__buried = 0U;
                    __Vdly__LeafEval__DOT__rdy_ext = 0U;
                    __Vdly__LeafEval__DOT__vrdy = 0U;
                    __Vdly__LeafEval__DOT__anyvir = 0U;
                    __Vdly__LeafEval__DOT__wc = 0U;
                    __Vdly__LeafEval__DOT__wr_ = 0U;
                    __Vdly__LeafEval__DOT__seen = 0U;
                    __Vdly__LeafEval__DOT__fillcnt = 0U;
                    __Vdly__LeafEval__DOT__st = 1U;
                } else {
                    vlSelfRef.done = 1U;
                    __Vdly__LeafEval__DOT__st = 0U;
                }
            } else if ((1U == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                if (vlSelfRef.LeafEval__DOT__occ_of
                    [(((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                       << 3U) | (7U & (IData)(vlSelfRef.LeafEval__DOT__wc)))]) {
                    if ((1U & (~ (IData)(vlSelfRef.LeafEval__DOT__seen)))) {
                        if (((0x1fU & ((IData)(0x10U) 
                                       - (IData)(vlSelfRef.LeafEval__DOT__wr_))) 
                             > (IData)(vlSelfRef.LeafEval__DOT__maxh))) {
                            __Vdly__LeafEval__DOT__maxh 
                                = (0x1fU & ((IData)(0x10U) 
                                            - (IData)(vlSelfRef.LeafEval__DOT__wr_)));
                        }
                        __Vdly__LeafEval__DOT__seen = 1U;
                    }
                    if (vlSelfRef.LeafEval__DOT__vir_of
                        [(((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                           << 3U) | (7U & (IData)(vlSelfRef.LeafEval__DOT__wc)))]) {
                        __Vdly__LeafEval__DOT__buried 
                            = (0x3ffU & ((IData)(vlSelfRef.LeafEval__DOT__buried) 
                                         + (IData)(vlSelfRef.LeafEval__DOT__fillcnt)));
                        __Vdly__LeafEval__DOT__anyvir = 1U;
                    }
                    __Vdly__LeafEval__DOT__fillcnt 
                        = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.LeafEval__DOT__fillcnt)));
                    if ((3U > (IData)(vlSelfRef.LeafEval__DOT__wr_))) {
                        __Vdly__LeafEval__DOT__toprisk 
                            = (0xffU & ((IData)(1U) 
                                        + (IData)(vlSelfRef.LeafEval__DOT__toprisk)));
                    }
                    if (((4U > (IData)(vlSelfRef.LeafEval__DOT__wr_)) 
                         & ((3U == (IData)(vlSelfRef.LeafEval__DOT__wc)) 
                            | (4U == (IData)(vlSelfRef.LeafEval__DOT__wc))))) {
                        __Vdly__LeafEval__DOT__spawn 
                            = (0xffU & ((IData)(1U) 
                                        + (IData)(vlSelfRef.LeafEval__DOT__spawn)));
                    }
                } else if (vlSelfRef.LeafEval__DOT__seen) {
                    __Vdly__LeafEval__DOT__holes = 
                        (0xffU & ((IData)(1U) + (IData)(vlSelfRef.LeafEval__DOT__holes)));
                }
                if ((0xfU == (IData)(vlSelfRef.LeafEval__DOT__wr_))) {
                    __Vdly__LeafEval__DOT__wr_ = 0U;
                    __Vdly__LeafEval__DOT__seen = 0U;
                    __Vdly__LeafEval__DOT__fillcnt = 0U;
                    if ((7U == (IData)(vlSelfRef.LeafEval__DOT__wc))) {
                        __Vdly__LeafEval__DOT__vo = 0U;
                        __Vdly__LeafEval__DOT__st = 2U;
                    } else {
                        __Vdly__LeafEval__DOT__wc = 
                            (0xfU & ((IData)(1U) + (IData)(vlSelfRef.LeafEval__DOT__wc)));
                    }
                } else {
                    __Vdly__LeafEval__DOT__wr_ = (0xfU 
                                                  & ((IData)(1U) 
                                                     + (IData)(vlSelfRef.LeafEval__DOT__wr_)));
                }
            } else if ((2U == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                if (vlSelfRef.LeafEval__DOT__vir_of
                    [vlSelfRef.LeafEval__DOT__vo]) {
                    __Vdly__LeafEval__DOT__run_h = 1U;
                    __Vdly__LeafEval__DOT__run_v = 1U;
                    __Vdly__LeafEval__DOT__p = vlSelfRef.LeafEval__DOT__v_c;
                    __Vdly__LeafEval__DOT__st = 3U;
                } else if ((0x7fU == (IData)(vlSelfRef.LeafEval__DOT__vo))) {
                    __Vdly__LeafEval__DOT__wc = 0U;
                    __Vdly__LeafEval__DOT__wr_ = 0U;
                    __Vdly__LeafEval__DOT__st = 0xeU;
                } else {
                    __Vdly__LeafEval__DOT__vo = (0x7fU 
                                                 & ((IData)(1U) 
                                                    + (IData)(vlSelfRef.LeafEval__DOT__vo)));
                }
            } else if ((((0U != (IData)(vlSelfRef.LeafEval__DOT__p)) 
                         & (vlSelfRef.LeafEval__DOT__col_of
                            [(((IData)(vlSelfRef.LeafEval__DOT__v_r) 
                               << 3U) | (7U & ((IData)(vlSelfRef.LeafEval__DOT__p) 
                                               - (IData)(1U))))] 
                            == (IData)(vlSelfRef.LeafEval__DOT__v_col))) 
                        & vlSelfRef.LeafEval__DOT__occ_of
                        [(((IData)(vlSelfRef.LeafEval__DOT__v_r) 
                           << 3U) | (7U & ((IData)(vlSelfRef.LeafEval__DOT__p) 
                                           - (IData)(1U))))])) {
                __Vdly__LeafEval__DOT__run_h = (0x1fU 
                                                & ((IData)(1U) 
                                                   + (IData)(vlSelfRef.LeafEval__DOT__run_h)));
                __Vdly__LeafEval__DOT__p = (0x1fU & 
                                            ((IData)(vlSelfRef.LeafEval__DOT__p) 
                                             - (IData)(1U)));
            } else {
                __Vdly__LeafEval__DOT__span_lo = vlSelfRef.LeafEval__DOT__p;
                __Vdly__LeafEval__DOT__st = 4U;
            }
        } else if (((((((((4U == (IData)(vlSelfRef.LeafEval__DOT__st)) 
                          | (5U == (IData)(vlSelfRef.LeafEval__DOT__st))) 
                         | (6U == (IData)(vlSelfRef.LeafEval__DOT__st))) 
                        | (7U == (IData)(vlSelfRef.LeafEval__DOT__st))) 
                       | (8U == (IData)(vlSelfRef.LeafEval__DOT__st))) 
                      | (9U == (IData)(vlSelfRef.LeafEval__DOT__st))) 
                     | (0xaU == (IData)(vlSelfRef.LeafEval__DOT__st))) 
                    | (0xbU == (IData)(vlSelfRef.LeafEval__DOT__st)))) {
            if ((4U == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                if (((0U != (IData)(vlSelfRef.LeafEval__DOT__span_lo)) 
                     & ((~ vlSelfRef.LeafEval__DOT__occ_of
                         [(((IData)(vlSelfRef.LeafEval__DOT__v_r) 
                            << 3U) | (7U & ((IData)(vlSelfRef.LeafEval__DOT__span_lo) 
                                            - (IData)(1U))))]) 
                        | (vlSelfRef.LeafEval__DOT__col_of
                           [(((IData)(vlSelfRef.LeafEval__DOT__v_r) 
                              << 3U) | (7U & ((IData)(vlSelfRef.LeafEval__DOT__span_lo) 
                                              - (IData)(1U))))] 
                           == (IData)(vlSelfRef.LeafEval__DOT__v_col))))) {
                    __Vdly__LeafEval__DOT__span_lo 
                        = (0x1fU & ((IData)(vlSelfRef.LeafEval__DOT__span_lo) 
                                    - (IData)(1U)));
                } else {
                    __Vdly__LeafEval__DOT__p = vlSelfRef.LeafEval__DOT__v_c;
                    __Vdly__LeafEval__DOT__st = 5U;
                }
            } else if ((5U == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                if ((((7U != (IData)(vlSelfRef.LeafEval__DOT__p)) 
                      & vlSelfRef.LeafEval__DOT__occ_of
                      [(((IData)(vlSelfRef.LeafEval__DOT__v_r) 
                         << 3U) | (7U & ((IData)(1U) 
                                         + (IData)(vlSelfRef.LeafEval__DOT__p))))]) 
                     & (vlSelfRef.LeafEval__DOT__col_of
                        [(((IData)(vlSelfRef.LeafEval__DOT__v_r) 
                           << 3U) | (7U & ((IData)(1U) 
                                           + (IData)(vlSelfRef.LeafEval__DOT__p))))] 
                        == (IData)(vlSelfRef.LeafEval__DOT__v_col)))) {
                    __Vdly__LeafEval__DOT__run_h = 
                        (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.LeafEval__DOT__run_h)));
                    __Vdly__LeafEval__DOT__p = (0x1fU 
                                                & ((IData)(1U) 
                                                   + (IData)(vlSelfRef.LeafEval__DOT__p)));
                } else {
                    __Vdly__LeafEval__DOT__span_hi 
                        = vlSelfRef.LeafEval__DOT__p;
                    __Vdly__LeafEval__DOT__st = 6U;
                }
            } else if ((6U == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                if (((7U != (IData)(vlSelfRef.LeafEval__DOT__span_hi)) 
                     & ((~ vlSelfRef.LeafEval__DOT__occ_of
                         [(((IData)(vlSelfRef.LeafEval__DOT__v_r) 
                            << 3U) | (7U & ((IData)(1U) 
                                            + (IData)(vlSelfRef.LeafEval__DOT__span_hi))))]) 
                        | (vlSelfRef.LeafEval__DOT__col_of
                           [(((IData)(vlSelfRef.LeafEval__DOT__v_r) 
                              << 3U) | (7U & ((IData)(1U) 
                                              + (IData)(vlSelfRef.LeafEval__DOT__span_hi))))] 
                           == (IData)(vlSelfRef.LeafEval__DOT__v_col))))) {
                    __Vdly__LeafEval__DOT__span_hi 
                        = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.LeafEval__DOT__span_hi)));
                } else {
                    __Vdly__LeafEval__DOT__p = vlSelfRef.LeafEval__DOT__v_r;
                    __Vdly__LeafEval__DOT__st = 7U;
                }
            } else if ((7U == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                if ((((0U != (IData)(vlSelfRef.LeafEval__DOT__p)) 
                      & vlSelfRef.LeafEval__DOT__occ_of
                      [((0x78U & (((IData)(vlSelfRef.LeafEval__DOT__p) 
                                   - (IData)(1U)) << 3U)) 
                        | (IData)(vlSelfRef.LeafEval__DOT__v_c))]) 
                     & (vlSelfRef.LeafEval__DOT__col_of
                        [((0x78U & (((IData)(vlSelfRef.LeafEval__DOT__p) 
                                     - (IData)(1U)) 
                                    << 3U)) | (IData)(vlSelfRef.LeafEval__DOT__v_c))] 
                        == (IData)(vlSelfRef.LeafEval__DOT__v_col)))) {
                    __Vdly__LeafEval__DOT__run_v = 
                        (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.LeafEval__DOT__run_v)));
                    __Vdly__LeafEval__DOT__p = (0x1fU 
                                                & ((IData)(vlSelfRef.LeafEval__DOT__p) 
                                                   - (IData)(1U)));
                } else {
                    __Vdly__LeafEval__DOT__vspan_lo 
                        = vlSelfRef.LeafEval__DOT__p;
                    __Vdly__LeafEval__DOT__st = 8U;
                }
            } else if ((8U == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                if (((0U != (IData)(vlSelfRef.LeafEval__DOT__vspan_lo)) 
                     & ((~ vlSelfRef.LeafEval__DOT__occ_of
                         [((0x78U & (((IData)(vlSelfRef.LeafEval__DOT__vspan_lo) 
                                      - (IData)(1U)) 
                                     << 3U)) | (IData)(vlSelfRef.LeafEval__DOT__v_c))]) 
                        | (vlSelfRef.LeafEval__DOT__col_of
                           [((0x78U & (((IData)(vlSelfRef.LeafEval__DOT__vspan_lo) 
                                        - (IData)(1U)) 
                                       << 3U)) | (IData)(vlSelfRef.LeafEval__DOT__v_c))] 
                           == (IData)(vlSelfRef.LeafEval__DOT__v_col))))) {
                    __Vdly__LeafEval__DOT__vspan_lo 
                        = (0x1fU & ((IData)(vlSelfRef.LeafEval__DOT__vspan_lo) 
                                    - (IData)(1U)));
                } else {
                    __Vdly__LeafEval__DOT__p = vlSelfRef.LeafEval__DOT__v_r;
                    __Vdly__LeafEval__DOT__st = 9U;
                }
            } else if ((9U == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                if ((((0xfU != (IData)(vlSelfRef.LeafEval__DOT__p)) 
                      & vlSelfRef.LeafEval__DOT__occ_of
                      [((0x78U & (((IData)(1U) + (IData)(vlSelfRef.LeafEval__DOT__p)) 
                                  << 3U)) | (IData)(vlSelfRef.LeafEval__DOT__v_c))]) 
                     & (vlSelfRef.LeafEval__DOT__col_of
                        [((0x78U & (((IData)(1U) + (IData)(vlSelfRef.LeafEval__DOT__p)) 
                                    << 3U)) | (IData)(vlSelfRef.LeafEval__DOT__v_c))] 
                        == (IData)(vlSelfRef.LeafEval__DOT__v_col)))) {
                    __Vdly__LeafEval__DOT__run_v = 
                        (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.LeafEval__DOT__run_v)));
                    __Vdly__LeafEval__DOT__p = (0x1fU 
                                                & ((IData)(1U) 
                                                   + (IData)(vlSelfRef.LeafEval__DOT__p)));
                } else {
                    __Vdly__LeafEval__DOT__vspan_hi 
                        = vlSelfRef.LeafEval__DOT__p;
                    __Vdly__LeafEval__DOT__st = 0xaU;
                }
            } else if ((0xaU == (IData)(vlSelfRef.LeafEval__DOT__st))) {
                if (((0xfU != (IData)(vlSelfRef.LeafEval__DOT__vspan_hi)) 
                     & ((~ vlSelfRef.LeafEval__DOT__occ_of
                         [((0x78U & (((IData)(1U) + (IData)(vlSelfRef.LeafEval__DOT__vspan_hi)) 
                                     << 3U)) | (IData)(vlSelfRef.LeafEval__DOT__v_c))]) 
                        | (vlSelfRef.LeafEval__DOT__col_of
                           [((0x78U & (((IData)(1U) 
                                        + (IData)(vlSelfRef.LeafEval__DOT__vspan_hi)) 
                                       << 3U)) | (IData)(vlSelfRef.LeafEval__DOT__v_c))] 
                           == (IData)(vlSelfRef.LeafEval__DOT__v_col))))) {
                    __Vdly__LeafEval__DOT__vspan_hi 
                        = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.LeafEval__DOT__vspan_hi)));
                } else {
                    __Vdly__LeafEval__DOT__p = 0U;
                    __Vdly__LeafEval__DOT__st = 0xbU;
                }
            } else {
                if ((((((7U & (IData)(vlSelfRef.LeafEval__DOT__p)) 
                        != (IData)(vlSelfRef.LeafEval__DOT__v_c)) 
                       & vlSelfRef.LeafEval__DOT__occ_of
                       [(((IData)(vlSelfRef.LeafEval__DOT__v_r) 
                          << 3U) | (7U & (IData)(vlSelfRef.LeafEval__DOT__p)))]) 
                      & (~ vlSelfRef.LeafEval__DOT__vir_of
                         [(((IData)(vlSelfRef.LeafEval__DOT__v_r) 
                            << 3U) | (7U & (IData)(vlSelfRef.LeafEval__DOT__p)))])) 
                     & (vlSelfRef.LeafEval__DOT__col_of
                        [(((IData)(vlSelfRef.LeafEval__DOT__v_r) 
                           << 3U) | (7U & (IData)(vlSelfRef.LeafEval__DOT__p)))] 
                        != (IData)(vlSelfRef.LeafEval__DOT__v_col)))) {
                    __Vdly__LeafEval__DOT__pollution 
                        = (0x7ffU & ((IData)(1U) + (IData)(vlSelfRef.LeafEval__DOT__pollution)));
                }
                if ((7U == (IData)(vlSelfRef.LeafEval__DOT__p))) {
                    __Vdly__LeafEval__DOT__p = 0U;
                    __Vdly__LeafEval__DOT__st = 0xcU;
                } else {
                    __Vdly__LeafEval__DOT__p = (0x1fU 
                                                & ((IData)(1U) 
                                                   + (IData)(vlSelfRef.LeafEval__DOT__p)));
                }
            }
        } else if ((0xcU == (IData)(vlSelfRef.LeafEval__DOT__st))) {
            if ((((((0xfU & (IData)(vlSelfRef.LeafEval__DOT__p)) 
                    != (IData)(vlSelfRef.LeafEval__DOT__v_r)) 
                   & vlSelfRef.LeafEval__DOT__occ_of
                   [((0x78U & ((IData)(vlSelfRef.LeafEval__DOT__p) 
                               << 3U)) | (IData)(vlSelfRef.LeafEval__DOT__v_c))]) 
                  & (~ vlSelfRef.LeafEval__DOT__vir_of
                     [((0x78U & ((IData)(vlSelfRef.LeafEval__DOT__p) 
                                 << 3U)) | (IData)(vlSelfRef.LeafEval__DOT__v_c))])) 
                 & (vlSelfRef.LeafEval__DOT__col_of
                    [((0x78U & ((IData)(vlSelfRef.LeafEval__DOT__p) 
                                << 3U)) | (IData)(vlSelfRef.LeafEval__DOT__v_c))] 
                    != (IData)(vlSelfRef.LeafEval__DOT__v_col)))) {
                __Vdly__LeafEval__DOT__pollution = 
                    (0x7ffU & ((IData)(1U) + (IData)(vlSelfRef.LeafEval__DOT__pollution)));
            }
            if ((0xfU == (IData)(vlSelfRef.LeafEval__DOT__p))) {
                __Vdly__LeafEval__DOT__st = 0xdU;
            } else {
                __Vdly__LeafEval__DOT__p = (0x1fU & 
                                            ((IData)(1U) 
                                             + (IData)(vlSelfRef.LeafEval__DOT__p)));
            }
        } else if ((0xdU == (IData)(vlSelfRef.LeafEval__DOT__st))) {
            vlSelfRef.LeafEval__DOT__fin__DOT__hq = 
                ((4U <= (0x1fU & ((IData)(1U) + ((IData)(vlSelfRef.LeafEval__DOT__span_hi) 
                                                 - (IData)(vlSelfRef.LeafEval__DOT__span_lo)))))
                  ? ([&]() {
                        __Vfunc_LeafEval__DOT__sq__1__n 
                            = vlSelfRef.LeafEval__DOT__run_h;
                        __Vfunc_LeafEval__DOT__sq__1__Vfuncout 
                            = (0x1ffU & ((IData)(__Vfunc_LeafEval__DOT__sq__1__n) 
                                         * (IData)(__Vfunc_LeafEval__DOT__sq__1__n)));
                    }(), (IData)(__Vfunc_LeafEval__DOT__sq__1__Vfuncout))
                  : 0U);
            vlSelfRef.LeafEval__DOT__fin__DOT__vq = 
                ((4U <= (0x1fU & ((IData)(1U) + ((IData)(vlSelfRef.LeafEval__DOT__vspan_hi) 
                                                 - (IData)(vlSelfRef.LeafEval__DOT__vspan_lo)))))
                  ? ([&]() {
                        __Vfunc_LeafEval__DOT__sq__2__n 
                            = vlSelfRef.LeafEval__DOT__run_v;
                        __Vfunc_LeafEval__DOT__sq__2__Vfuncout 
                            = (0x1ffU & ((IData)(__Vfunc_LeafEval__DOT__sq__2__n) 
                                         * (IData)(__Vfunc_LeafEval__DOT__sq__2__n)));
                    }(), (IData)(__Vfunc_LeafEval__DOT__sq__2__Vfuncout))
                  : 0U);
            if ((0x7fU == (IData)(vlSelfRef.LeafEval__DOT__vo))) {
                __Vdly__LeafEval__DOT__wc = 0U;
                __Vdly__LeafEval__DOT__wr_ = 0U;
                __Vdly__LeafEval__DOT__st = 0xeU;
            } else {
                __Vdly__LeafEval__DOT__vo = (0x7fU 
                                             & ((IData)(1U) 
                                                + (IData)(vlSelfRef.LeafEval__DOT__vo)));
                __Vdly__LeafEval__DOT__st = 2U;
            }
            vlSelfRef.LeafEval__DOT__fin__DOT__mx = 
                (((IData)(vlSelfRef.LeafEval__DOT__fin__DOT__hq) 
                  > (IData)(vlSelfRef.LeafEval__DOT__fin__DOT__vq))
                  ? (IData)(vlSelfRef.LeafEval__DOT__fin__DOT__hq)
                  : (IData)(vlSelfRef.LeafEval__DOT__fin__DOT__vq));
            __Vdly__LeafEval__DOT__rdy_ext = (0xffffU 
                                              & ((IData)(vlSelfRef.LeafEval__DOT__rdy_ext) 
                                                 + (IData)(vlSelfRef.LeafEval__DOT__fin__DOT__mx)));
            __Vdly__LeafEval__DOT__vrdy = (0xffffU 
                                           & ((IData)(vlSelfRef.LeafEval__DOT__vrdy) 
                                              + VL_EXTEND_II(16,9, 
                                                             ([&]() {
                                __Vfunc_LeafEval__DOT__sq__3__n 
                                    = vlSelfRef.LeafEval__DOT__run_v;
                                __Vfunc_LeafEval__DOT__sq__3__Vfuncout 
                                    = (0x1ffU & ((IData)(__Vfunc_LeafEval__DOT__sq__3__n) 
                                                 * (IData)(__Vfunc_LeafEval__DOT__sq__3__n)));
                            }(), (IData)(__Vfunc_LeafEval__DOT__sq__3__Vfuncout)))));
        } else if ((0xeU == (IData)(vlSelfRef.LeafEval__DOT__st))) {
            vlSelfRef.LeafEval__DOT__suh__DOT__c0 = 
                vlSelfRef.LeafEval__DOT__col_of[(((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                                                  << 3U) 
                                                 | (7U 
                                                    & (IData)(vlSelfRef.LeafEval__DOT__wc)))];
            if ((((0U != (IData)(vlSelfRef.LeafEval__DOT__suh__DOT__c0)) 
                  & (vlSelfRef.LeafEval__DOT__col_of
                     [(((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                        << 3U) | (7U & ((IData)(1U) 
                                        + (IData)(vlSelfRef.LeafEval__DOT__wc))))] 
                     == (IData)(vlSelfRef.LeafEval__DOT__suh__DOT__c0))) 
                 & (vlSelfRef.LeafEval__DOT__col_of
                    [(((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                       << 3U) | (7U & ((IData)(2U) 
                                       + (IData)(vlSelfRef.LeafEval__DOT__wc))))] 
                    == (IData)(vlSelfRef.LeafEval__DOT__suh__DOT__c0)))) {
                vlSelfRef.LeafEval__DOT__suh__DOT__t 
                    = (((vlSelfRef.LeafEval__DOT__vir_of
                         [(((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                            << 3U) | (7U & (IData)(vlSelfRef.LeafEval__DOT__wc)))] 
                         & (vlSelfRef.LeafEval__DOT__col_of
                            [(((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                               << 3U) | (7U & (IData)(vlSelfRef.LeafEval__DOT__wc)))] 
                            == (IData)(vlSelfRef.LeafEval__DOT__suh__DOT__c0))) 
                        | (vlSelfRef.LeafEval__DOT__vir_of
                           [(((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                              << 3U) | (7U & ((IData)(1U) 
                                              + (IData)(vlSelfRef.LeafEval__DOT__wc))))] 
                           & (vlSelfRef.LeafEval__DOT__col_of
                              [(((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                                 << 3U) | (7U & ((IData)(1U) 
                                                 + (IData)(vlSelfRef.LeafEval__DOT__wc))))] 
                              == (IData)(vlSelfRef.LeafEval__DOT__suh__DOT__c0)))) 
                       | (vlSelfRef.LeafEval__DOT__vir_of
                          [(((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                             << 3U) | (7U & ((IData)(2U) 
                                             + (IData)(vlSelfRef.LeafEval__DOT__wc))))] 
                          & (vlSelfRef.LeafEval__DOT__col_of
                             [(((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                                << 3U) | (7U & ((IData)(2U) 
                                                + (IData)(vlSelfRef.LeafEval__DOT__wc))))] 
                             == (IData)(vlSelfRef.LeafEval__DOT__suh__DOT__c0))));
                if (((~ (IData)(vlSelfRef.LeafEval__DOT__suh__DOT__t)) 
                     & (0U != (IData)(vlSelfRef.LeafEval__DOT__wc)))) {
                    vlSelfRef.LeafEval__DOT__suh__DOT__t 
                        = (vlSelfRef.LeafEval__DOT__vir_of
                           [(((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                              << 3U) | (7U & ((IData)(vlSelfRef.LeafEval__DOT__wc) 
                                              - (IData)(1U))))] 
                           & (vlSelfRef.LeafEval__DOT__col_of
                              [(((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                                 << 3U) | (7U & ((IData)(vlSelfRef.LeafEval__DOT__wc) 
                                                 - (IData)(1U))))] 
                              == (IData)(vlSelfRef.LeafEval__DOT__suh__DOT__c0)));
                }
                if (((~ (IData)(vlSelfRef.LeafEval__DOT__suh__DOT__t)) 
                     & (5U > (IData)(vlSelfRef.LeafEval__DOT__wc)))) {
                    vlSelfRef.LeafEval__DOT__suh__DOT__t 
                        = (vlSelfRef.LeafEval__DOT__vir_of
                           [(((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                              << 3U) | (7U & ((IData)(3U) 
                                              + (IData)(vlSelfRef.LeafEval__DOT__wc))))] 
                           & (vlSelfRef.LeafEval__DOT__col_of
                              [(((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                                 << 3U) | (7U & ((IData)(3U) 
                                                 + (IData)(vlSelfRef.LeafEval__DOT__wc))))] 
                              == (IData)(vlSelfRef.LeafEval__DOT__suh__DOT__c0)));
                }
                if (vlSelfRef.LeafEval__DOT__suh__DOT__t) {
                    __Vdly__LeafEval__DOT__setup = 
                        (0xffU & ((IData)(1U) + (IData)(vlSelfRef.LeafEval__DOT__setup)));
                }
            }
            if ((5U == (IData)(vlSelfRef.LeafEval__DOT__wc))) {
                __Vdly__LeafEval__DOT__wc = 0U;
                if ((0xfU == (IData)(vlSelfRef.LeafEval__DOT__wr_))) {
                    __Vdly__LeafEval__DOT__wr_ = 0U;
                    __Vdly__LeafEval__DOT__st = 0xfU;
                } else {
                    __Vdly__LeafEval__DOT__wr_ = (0xfU 
                                                  & ((IData)(1U) 
                                                     + (IData)(vlSelfRef.LeafEval__DOT__wr_)));
                }
            } else {
                __Vdly__LeafEval__DOT__wc = (0xfU & 
                                             ((IData)(1U) 
                                              + (IData)(vlSelfRef.LeafEval__DOT__wc)));
            }
        } else if ((0xfU == (IData)(vlSelfRef.LeafEval__DOT__st))) {
            vlSelfRef.LeafEval__DOT__suv__DOT__c0 = 
                vlSelfRef.LeafEval__DOT__col_of[(((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                                                  << 3U) 
                                                 | (7U 
                                                    & (IData)(vlSelfRef.LeafEval__DOT__wc)))];
            if ((((0U != (IData)(vlSelfRef.LeafEval__DOT__suv__DOT__c0)) 
                  & (vlSelfRef.LeafEval__DOT__col_of
                     [((0x78U & (((IData)(1U) + (IData)(vlSelfRef.LeafEval__DOT__wr_)) 
                                 << 3U)) | (7U & (IData)(vlSelfRef.LeafEval__DOT__wc)))] 
                     == (IData)(vlSelfRef.LeafEval__DOT__suv__DOT__c0))) 
                 & (vlSelfRef.LeafEval__DOT__col_of
                    [((0x78U & (((IData)(2U) + (IData)(vlSelfRef.LeafEval__DOT__wr_)) 
                                << 3U)) | (7U & (IData)(vlSelfRef.LeafEval__DOT__wc)))] 
                    == (IData)(vlSelfRef.LeafEval__DOT__suv__DOT__c0)))) {
                vlSelfRef.LeafEval__DOT__suv__DOT__t 
                    = (((vlSelfRef.LeafEval__DOT__vir_of
                         [(((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                            << 3U) | (7U & (IData)(vlSelfRef.LeafEval__DOT__wc)))] 
                         & (vlSelfRef.LeafEval__DOT__col_of
                            [(((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                               << 3U) | (7U & (IData)(vlSelfRef.LeafEval__DOT__wc)))] 
                            == (IData)(vlSelfRef.LeafEval__DOT__suv__DOT__c0))) 
                        | (vlSelfRef.LeafEval__DOT__vir_of
                           [((0x78U & (((IData)(1U) 
                                        + (IData)(vlSelfRef.LeafEval__DOT__wr_)) 
                                       << 3U)) | (7U 
                                                  & (IData)(vlSelfRef.LeafEval__DOT__wc)))] 
                           & (vlSelfRef.LeafEval__DOT__col_of
                              [((0x78U & (((IData)(1U) 
                                           + (IData)(vlSelfRef.LeafEval__DOT__wr_)) 
                                          << 3U)) | 
                                (7U & (IData)(vlSelfRef.LeafEval__DOT__wc)))] 
                              == (IData)(vlSelfRef.LeafEval__DOT__suv__DOT__c0)))) 
                       | (vlSelfRef.LeafEval__DOT__vir_of
                          [((0x78U & (((IData)(2U) 
                                       + (IData)(vlSelfRef.LeafEval__DOT__wr_)) 
                                      << 3U)) | (7U 
                                                 & (IData)(vlSelfRef.LeafEval__DOT__wc)))] 
                          & (vlSelfRef.LeafEval__DOT__col_of
                             [((0x78U & (((IData)(2U) 
                                          + (IData)(vlSelfRef.LeafEval__DOT__wr_)) 
                                         << 3U)) | 
                               (7U & (IData)(vlSelfRef.LeafEval__DOT__wc)))] 
                             == (IData)(vlSelfRef.LeafEval__DOT__suv__DOT__c0))));
                if (((~ (IData)(vlSelfRef.LeafEval__DOT__suv__DOT__t)) 
                     & (0U != (IData)(vlSelfRef.LeafEval__DOT__wr_)))) {
                    vlSelfRef.LeafEval__DOT__suv__DOT__t 
                        = (vlSelfRef.LeafEval__DOT__vir_of
                           [((0x78U & (((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                                        - (IData)(1U)) 
                                       << 3U)) | (7U 
                                                  & (IData)(vlSelfRef.LeafEval__DOT__wc)))] 
                           & (vlSelfRef.LeafEval__DOT__col_of
                              [((0x78U & (((IData)(vlSelfRef.LeafEval__DOT__wr_) 
                                           - (IData)(1U)) 
                                          << 3U)) | 
                                (7U & (IData)(vlSelfRef.LeafEval__DOT__wc)))] 
                              == (IData)(vlSelfRef.LeafEval__DOT__suv__DOT__c0)));
                }
                if (((~ (IData)(vlSelfRef.LeafEval__DOT__suv__DOT__t)) 
                     & (0xdU > (IData)(vlSelfRef.LeafEval__DOT__wr_)))) {
                    vlSelfRef.LeafEval__DOT__suv__DOT__t 
                        = (vlSelfRef.LeafEval__DOT__vir_of
                           [((0x78U & (((IData)(3U) 
                                        + (IData)(vlSelfRef.LeafEval__DOT__wr_)) 
                                       << 3U)) | (7U 
                                                  & (IData)(vlSelfRef.LeafEval__DOT__wc)))] 
                           & (vlSelfRef.LeafEval__DOT__col_of
                              [((0x78U & (((IData)(3U) 
                                           + (IData)(vlSelfRef.LeafEval__DOT__wr_)) 
                                          << 3U)) | 
                                (7U & (IData)(vlSelfRef.LeafEval__DOT__wc)))] 
                              == (IData)(vlSelfRef.LeafEval__DOT__suv__DOT__c0)));
                }
                if (vlSelfRef.LeafEval__DOT__suv__DOT__t) {
                    __Vdly__LeafEval__DOT__setup = 
                        (0xffU & ((IData)(1U) + (IData)(vlSelfRef.LeafEval__DOT__setup)));
                }
            }
            if ((0xdU == (IData)(vlSelfRef.LeafEval__DOT__wr_))) {
                __Vdly__LeafEval__DOT__wr_ = 0U;
                if ((7U == (IData)(vlSelfRef.LeafEval__DOT__wc))) {
                    __Vdly__LeafEval__DOT__st = 0x10U;
                } else {
                    __Vdly__LeafEval__DOT__wc = (0xfU 
                                                 & ((IData)(1U) 
                                                    + (IData)(vlSelfRef.LeafEval__DOT__wc)));
                }
            } else {
                __Vdly__LeafEval__DOT__wr_ = (0xfU 
                                              & ((IData)(1U) 
                                                 + (IData)(vlSelfRef.LeafEval__DOT__wr_)));
            }
        } else if ((0x10U == (IData)(vlSelfRef.LeafEval__DOT__st))) {
            vlSelfRef.sco = (0xffffU & ((((((((((IData)(0x1388U) 
                                                - ((IData)(0xcU) 
                                                   * (IData)(vlSelfRef.LeafEval__DOT__maxh))) 
                                               - ((IData)(0x14U) 
                                                  * (IData)(vlSelfRef.LeafEval__DOT__holes))) 
                                              - ((IData)(0x5aU) 
                                                 * (IData)(vlSelfRef.LeafEval__DOT__toprisk))) 
                                             - ((IData)(0x96U) 
                                                * (IData)(vlSelfRef.LeafEval__DOT__spawn))) 
                                            + ((IData)(0x3cU) 
                                               * (IData)(vlSelfRef.LeafEval__DOT__setup))) 
                                           - ((IData)(0x1eU) 
                                              * (IData)(vlSelfRef.LeafEval__DOT__buried))) 
                                          + ((IData)(0xcU) 
                                             * (IData)(vlSelfRef.LeafEval__DOT__rdy_ext))) 
                                         + ((IData)(0xcU) 
                                            * (IData)(vlSelfRef.LeafEval__DOT__vrdy))) 
                                        - ((IData)(6U) 
                                           * (IData)(vlSelfRef.LeafEval__DOT__pollution))));
            vlSelfRef.win = (1U & (~ (IData)(vlSelfRef.LeafEval__DOT__anyvir)));
            vlSelfRef.done = 1U;
            __Vdly__LeafEval__DOT__st = 0U;
        } else {
            __Vdly__LeafEval__DOT__st = 0U;
        }
    }
    vlSelfRef.LeafEval__DOT__st = __Vdly__LeafEval__DOT__st;
    vlSelfRef.LeafEval__DOT__maxh = __Vdly__LeafEval__DOT__maxh;
    vlSelfRef.LeafEval__DOT__holes = __Vdly__LeafEval__DOT__holes;
    vlSelfRef.LeafEval__DOT__toprisk = __Vdly__LeafEval__DOT__toprisk;
    vlSelfRef.LeafEval__DOT__spawn = __Vdly__LeafEval__DOT__spawn;
    vlSelfRef.LeafEval__DOT__setup = __Vdly__LeafEval__DOT__setup;
    vlSelfRef.LeafEval__DOT__pollution = __Vdly__LeafEval__DOT__pollution;
    vlSelfRef.LeafEval__DOT__buried = __Vdly__LeafEval__DOT__buried;
    vlSelfRef.LeafEval__DOT__rdy_ext = __Vdly__LeafEval__DOT__rdy_ext;
    vlSelfRef.LeafEval__DOT__vrdy = __Vdly__LeafEval__DOT__vrdy;
    vlSelfRef.LeafEval__DOT__anyvir = __Vdly__LeafEval__DOT__anyvir;
    vlSelfRef.LeafEval__DOT__wc = __Vdly__LeafEval__DOT__wc;
    vlSelfRef.LeafEval__DOT__wr_ = __Vdly__LeafEval__DOT__wr_;
    vlSelfRef.LeafEval__DOT__seen = __Vdly__LeafEval__DOT__seen;
    vlSelfRef.LeafEval__DOT__fillcnt = __Vdly__LeafEval__DOT__fillcnt;
    vlSelfRef.LeafEval__DOT__cmd_l = __Vdly__LeafEval__DOT__cmd_l;
    vlSelfRef.LeafEval__DOT__node_leaf = __Vdly__LeafEval__DOT__node_leaf;
    vlSelfRef.rv_cells = __Vdly__rv_cells;
    vlSelfRef.rv_vir = __Vdly__rv_vir;
    vlSelfRef.LeafEval__DOT__markb[0U] = __Vdly__LeafEval__DOT__markb[0U];
    vlSelfRef.LeafEval__DOT__markb[1U] = __Vdly__LeafEval__DOT__markb[1U];
    vlSelfRef.LeafEval__DOT__markb[2U] = __Vdly__LeafEval__DOT__markb[2U];
    vlSelfRef.LeafEval__DOT__markb[3U] = __Vdly__LeafEval__DOT__markb[3U];
    vlSelfRef.LeafEval__DOT__anyclear = __Vdly__LeafEval__DOT__anyclear;
    vlSelfRef.LeafEval__DOT__fwp = __Vdly__LeafEval__DOT__fwp;
    vlSelfRef.LeafEval__DOT__fwp2 = __Vdly__LeafEval__DOT__fwp2;
    vlSelfRef.LeafEval__DOT__fo1 = __Vdly__LeafEval__DOT__fo1;
    vlSelfRef.LeafEval__DOT__off_b = __Vdly__LeafEval__DOT__off_b;
    vlSelfRef.LeafEval__DOT__off_a = __Vdly__LeafEval__DOT__off_a;
    vlSelfRef.LeafEval__DOT__li = __Vdly__LeafEval__DOT__li;
    vlSelfRef.LeafEval__DOT__sstep = __Vdly__LeafEval__DOT__sstep;
    vlSelfRef.LeafEval__DOT__scnt = __Vdly__LeafEval__DOT__scnt;
    vlSelfRef.LeafEval__DOT__srun = __Vdly__LeafEval__DOT__srun;
    vlSelfRef.LeafEval__DOT__smcol = __Vdly__LeafEval__DOT__smcol;
    vlSelfRef.LeafEval__DOT__soff = __Vdly__LeafEval__DOT__soff;
    vlSelfRef.LeafEval__DOT__srstart = __Vdly__LeafEval__DOT__srstart;
    vlSelfRef.LeafEval__DOT__gdest = __Vdly__LeafEval__DOT__gdest;
    vlSelfRef.LeafEval__DOT__run_h = __Vdly__LeafEval__DOT__run_h;
    vlSelfRef.LeafEval__DOT__run_v = __Vdly__LeafEval__DOT__run_v;
    vlSelfRef.LeafEval__DOT__p = __Vdly__LeafEval__DOT__p;
    vlSelfRef.LeafEval__DOT__span_lo = __Vdly__LeafEval__DOT__span_lo;
    vlSelfRef.LeafEval__DOT__span_hi = __Vdly__LeafEval__DOT__span_hi;
    vlSelfRef.LeafEval__DOT__vspan_lo = __Vdly__LeafEval__DOT__vspan_lo;
    vlSelfRef.LeafEval__DOT__vspan_hi = __Vdly__LeafEval__DOT__vspan_hi;
    vlSelfRef.LeafEval__DOT__cpw_p = __Vdly__LeafEval__DOT__cpw_p;
    vlSelfRef.LeafEval__DOT__vo = __Vdly__LeafEval__DOT__vo;
    if (__VdlySet__LeafEval__DOT__bcell__v0) {
        vlSelfRef.LeafEval__DOT__bcell[__VdlyDim0__LeafEval__DOT__bcell__v0] 
            = __VdlyVal__LeafEval__DOT__bcell__v0;
    }
    if (__VdlySet__LeafEval__DOT__bcell__v1) {
        vlSelfRef.LeafEval__DOT__bcell[__VdlyDim0__LeafEval__DOT__bcell__v1] 
            = __VdlyVal__LeafEval__DOT__bcell__v1;
    }
    if (__VdlySet__LeafEval__DOT__bcell__v2) {
        vlSelfRef.LeafEval__DOT__bcell[__VdlyDim0__LeafEval__DOT__bcell__v2] 
            = __VdlyVal__LeafEval__DOT__bcell__v2;
    }
    if (__VdlySet__LeafEval__DOT__bcell__v3) {
        vlSelfRef.LeafEval__DOT__bcell[__VdlyDim0__LeafEval__DOT__bcell__v3] 
            = __VdlyVal__LeafEval__DOT__bcell__v3;
    }
    if (__VdlySet__LeafEval__DOT__bcell__v4) {
        vlSelfRef.LeafEval__DOT__bcell[__VdlyDim0__LeafEval__DOT__bcell__v4] = 0U;
    }
    if (__VdlySet__LeafEval__DOT__bcell__v5) {
        vlSelfRef.LeafEval__DOT__bcell[__VdlyDim0__LeafEval__DOT__bcell__v5] 
            = __VdlyVal__LeafEval__DOT__bcell__v5;
        vlSelfRef.LeafEval__DOT__bcell[__VdlyDim0__LeafEval__DOT__bcell__v6] = 0U;
    }
    vlSelfRef.LeafEval__DOT__sl_wa = ((IData)(vlSelfRef.LeafEval__DOT__sl_cpw)
                                       ? (((IData)(vlSelfRef.a_sl) 
                                           << 7U) | (IData)(vlSelfRef.LeafEval__DOT__cpw_p))
                                       : (((IData)(vlSelfRef.wslot) 
                                           << 7U) | (IData)(vlSelfRef.waddr)));
    vlSelfRef.LeafEval__DOT__v_c = (7U & (IData)(vlSelfRef.LeafEval__DOT__vo));
    vlSelfRef.LeafEval__DOT__v_r = (0xfU & ((IData)(vlSelfRef.LeafEval__DOT__vo) 
                                            >> 3U));
    vlSelfRef.LeafEval__DOT__sl_qb = vlSelfRef.LeafEval__DOT__slotram__DOT__mem
        [vlSelfRef.LeafEval__DOT__sr_addr];
    vlSelfRef.LeafEval__DOT__occ_of[0U] = (0U != (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0U]));
    vlSelfRef.LeafEval__DOT__occ_of[1U] = (0U != (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [1U]));
    vlSelfRef.LeafEval__DOT__occ_of[2U] = (0U != (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [2U]));
    vlSelfRef.LeafEval__DOT__occ_of[3U] = (0U != (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [3U]));
    vlSelfRef.LeafEval__DOT__occ_of[4U] = (0U != (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [4U]));
    vlSelfRef.LeafEval__DOT__occ_of[5U] = (0U != (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [5U]));
    vlSelfRef.LeafEval__DOT__occ_of[6U] = (0U != (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [6U]));
    vlSelfRef.LeafEval__DOT__occ_of[7U] = (0U != (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [7U]));
    vlSelfRef.LeafEval__DOT__occ_of[8U] = (0U != (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [8U]));
    vlSelfRef.LeafEval__DOT__occ_of[9U] = (0U != (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [9U]));
    vlSelfRef.LeafEval__DOT__occ_of[0xaU] = (0U != 
                                             (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0xaU]));
    vlSelfRef.LeafEval__DOT__occ_of[0xbU] = (0U != 
                                             (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0xbU]));
    vlSelfRef.LeafEval__DOT__occ_of[0xcU] = (0U != 
                                             (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0xcU]));
    vlSelfRef.LeafEval__DOT__occ_of[0xdU] = (0U != 
                                             (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0xdU]));
    vlSelfRef.LeafEval__DOT__occ_of[0xeU] = (0U != 
                                             (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0xeU]));
    vlSelfRef.LeafEval__DOT__occ_of[0xfU] = (0U != 
                                             (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0xfU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x10U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x10U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x11U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x11U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x12U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x12U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x13U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x13U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x14U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x14U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x15U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x15U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x16U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x16U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x17U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x17U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x18U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x18U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x19U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x19U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x1aU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x1aU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x1bU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x1bU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x1cU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x1cU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x1dU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x1dU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x1eU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x1eU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x1fU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x1fU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x20U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x20U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x21U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x21U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x22U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x22U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x23U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x23U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x24U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x24U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x25U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x25U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x26U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x26U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x27U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x27U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x28U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x28U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x29U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x29U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x2aU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x2aU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x2bU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x2bU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x2cU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x2cU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x2dU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x2dU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x2eU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x2eU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x2fU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x2fU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x30U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x30U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x31U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x31U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x32U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x32U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x33U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x33U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x34U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x34U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x35U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x35U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x36U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x36U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x37U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x37U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x38U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x38U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x39U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x39U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x3aU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x3aU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x3bU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x3bU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x3cU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x3cU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x3dU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x3dU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x3eU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x3eU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x3fU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x3fU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x40U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x40U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x41U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x41U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x42U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x42U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x43U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x43U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x44U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x44U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x45U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x45U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x46U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x46U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x47U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x47U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x48U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x48U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x49U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x49U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x4aU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x4aU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x4bU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x4bU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x4cU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x4cU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x4dU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x4dU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x4eU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x4eU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x4fU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x4fU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x50U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x50U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x51U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x51U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x52U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x52U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x53U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x53U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x54U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x54U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x55U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x55U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x56U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x56U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x57U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x57U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x58U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x58U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x59U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x59U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x5aU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x5aU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x5bU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x5bU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x5cU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x5cU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x5dU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x5dU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x5eU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x5eU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x5fU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x5fU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x60U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x60U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x61U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x61U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x62U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x62U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x63U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x63U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x64U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x64U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x65U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x65U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x66U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x66U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x67U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x67U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x68U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x68U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x69U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x69U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x6aU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x6aU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x6bU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x6bU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x6cU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x6cU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x6dU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x6dU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x6eU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x6eU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x6fU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x6fU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x70U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x70U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x71U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x71U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x72U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x72U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x73U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x73U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x74U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x74U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x75U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x75U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x76U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x76U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x77U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x77U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x78U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x78U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x79U] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x79U]));
    vlSelfRef.LeafEval__DOT__occ_of[0x7aU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x7aU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x7bU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x7bU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x7cU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x7cU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x7dU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x7dU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x7eU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x7eU]));
    vlSelfRef.LeafEval__DOT__occ_of[0x7fU] = (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0x7fU]));
    vlSelfRef.LeafEval__DOT__vir_of[0U] = ((vlSelfRef.LeafEval__DOT__bcell
                                            [0U] >> 2U) 
                                           & (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [0U])));
    vlSelfRef.LeafEval__DOT__vir_of[1U] = ((vlSelfRef.LeafEval__DOT__bcell
                                            [1U] >> 2U) 
                                           & (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [1U])));
    vlSelfRef.LeafEval__DOT__vir_of[2U] = ((vlSelfRef.LeafEval__DOT__bcell
                                            [2U] >> 2U) 
                                           & (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [2U])));
    vlSelfRef.LeafEval__DOT__vir_of[3U] = ((vlSelfRef.LeafEval__DOT__bcell
                                            [3U] >> 2U) 
                                           & (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [3U])));
    vlSelfRef.LeafEval__DOT__vir_of[4U] = ((vlSelfRef.LeafEval__DOT__bcell
                                            [4U] >> 2U) 
                                           & (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [4U])));
    vlSelfRef.LeafEval__DOT__vir_of[5U] = ((vlSelfRef.LeafEval__DOT__bcell
                                            [5U] >> 2U) 
                                           & (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [5U])));
    vlSelfRef.LeafEval__DOT__vir_of[6U] = ((vlSelfRef.LeafEval__DOT__bcell
                                            [6U] >> 2U) 
                                           & (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [6U])));
    vlSelfRef.LeafEval__DOT__vir_of[7U] = ((vlSelfRef.LeafEval__DOT__bcell
                                            [7U] >> 2U) 
                                           & (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [7U])));
    vlSelfRef.LeafEval__DOT__vir_of[8U] = ((vlSelfRef.LeafEval__DOT__bcell
                                            [8U] >> 2U) 
                                           & (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [8U])));
    vlSelfRef.LeafEval__DOT__vir_of[9U] = ((vlSelfRef.LeafEval__DOT__bcell
                                            [9U] >> 2U) 
                                           & (0U != 
                                              (3U & 
                                               vlSelfRef.LeafEval__DOT__bcell
                                               [9U])));
    vlSelfRef.LeafEval__DOT__vir_of[0xaU] = ((vlSelfRef.LeafEval__DOT__bcell
                                              [0xaU] 
                                              >> 2U) 
                                             & (0U 
                                                != 
                                                (3U 
                                                 & vlSelfRef.LeafEval__DOT__bcell
                                                 [0xaU])));
    vlSelfRef.LeafEval__DOT__vir_of[0xbU] = ((vlSelfRef.LeafEval__DOT__bcell
                                              [0xbU] 
                                              >> 2U) 
                                             & (0U 
                                                != 
                                                (3U 
                                                 & vlSelfRef.LeafEval__DOT__bcell
                                                 [0xbU])));
    vlSelfRef.LeafEval__DOT__vir_of[0xcU] = ((vlSelfRef.LeafEval__DOT__bcell
                                              [0xcU] 
                                              >> 2U) 
                                             & (0U 
                                                != 
                                                (3U 
                                                 & vlSelfRef.LeafEval__DOT__bcell
                                                 [0xcU])));
    vlSelfRef.LeafEval__DOT__vir_of[0xdU] = ((vlSelfRef.LeafEval__DOT__bcell
                                              [0xdU] 
                                              >> 2U) 
                                             & (0U 
                                                != 
                                                (3U 
                                                 & vlSelfRef.LeafEval__DOT__bcell
                                                 [0xdU])));
    vlSelfRef.LeafEval__DOT__vir_of[0xeU] = ((vlSelfRef.LeafEval__DOT__bcell
                                              [0xeU] 
                                              >> 2U) 
                                             & (0U 
                                                != 
                                                (3U 
                                                 & vlSelfRef.LeafEval__DOT__bcell
                                                 [0xeU])));
    vlSelfRef.LeafEval__DOT__vir_of[0xfU] = ((vlSelfRef.LeafEval__DOT__bcell
                                              [0xfU] 
                                              >> 2U) 
                                             & (0U 
                                                != 
                                                (3U 
                                                 & vlSelfRef.LeafEval__DOT__bcell
                                                 [0xfU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x10U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x10U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x10U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x11U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x11U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x11U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x12U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x12U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x12U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x13U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x13U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x13U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x14U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x14U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x14U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x15U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x15U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x15U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x16U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x16U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x16U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x17U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x17U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x17U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x18U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x18U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x18U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x19U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x19U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x19U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x1aU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x1aU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x1aU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x1bU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x1bU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x1bU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x1cU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x1cU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x1cU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x1dU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x1dU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x1dU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x1eU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x1eU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x1eU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x1fU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x1fU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x1fU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x20U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x20U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x20U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x21U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x21U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x21U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x22U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x22U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x22U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x23U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x23U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x23U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x24U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x24U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x24U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x25U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x25U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x25U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x26U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x26U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x26U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x27U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x27U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x27U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x28U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x28U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x28U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x29U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x29U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x29U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x2aU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x2aU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x2aU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x2bU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x2bU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x2bU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x2cU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x2cU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x2cU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x2dU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x2dU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x2dU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x2eU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x2eU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x2eU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x2fU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x2fU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x2fU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x30U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x30U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x30U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x31U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x31U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x31U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x32U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x32U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x32U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x33U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x33U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x33U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x34U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x34U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x34U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x35U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x35U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x35U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x36U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x36U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x36U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x37U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x37U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x37U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x38U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x38U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x38U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x39U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x39U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x39U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x3aU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x3aU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x3aU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x3bU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x3bU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x3bU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x3cU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x3cU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x3cU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x3dU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x3dU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x3dU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x3eU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x3eU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x3eU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x3fU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x3fU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x3fU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x40U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x40U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x40U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x41U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x41U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x41U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x42U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x42U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x42U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x43U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x43U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x43U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x44U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x44U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x44U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x45U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x45U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x45U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x46U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x46U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x46U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x47U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x47U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x47U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x48U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x48U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x48U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x49U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x49U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x49U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x4aU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x4aU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x4aU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x4bU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x4bU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x4bU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x4cU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x4cU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x4cU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x4dU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x4dU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x4dU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x4eU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x4eU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x4eU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x4fU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x4fU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x4fU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x50U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x50U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x50U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x51U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x51U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x51U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x52U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x52U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x52U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x53U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x53U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x53U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x54U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x54U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x54U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x55U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x55U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x55U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x56U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x56U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x56U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x57U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x57U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x57U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x58U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x58U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x58U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x59U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x59U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x59U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x5aU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x5aU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x5aU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x5bU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x5bU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x5bU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x5cU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x5cU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x5cU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x5dU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x5dU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x5dU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x5eU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x5eU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x5eU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x5fU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x5fU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x5fU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x60U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x60U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x60U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x61U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x61U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x61U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x62U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x62U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x62U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x63U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x63U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x63U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x64U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x64U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x64U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x65U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x65U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x65U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x66U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x66U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x66U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x67U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x67U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x67U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x68U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x68U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x68U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x69U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x69U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x69U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x6aU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x6aU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x6aU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x6bU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x6bU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x6bU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x6cU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x6cU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x6cU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x6dU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x6dU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x6dU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x6eU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x6eU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x6eU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x6fU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x6fU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x6fU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x70U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x70U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x70U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x71U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x71U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x71U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x72U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x72U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x72U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x73U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x73U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x73U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x74U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x74U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x74U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x75U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x75U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x75U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x76U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x76U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x76U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x77U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x77U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x77U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x78U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x78U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x78U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x79U] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x79U] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x79U])));
    vlSelfRef.LeafEval__DOT__vir_of[0x7aU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x7aU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x7aU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x7bU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x7bU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x7bU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x7cU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x7cU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x7cU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x7dU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x7dU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x7dU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x7eU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x7eU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x7eU])));
    vlSelfRef.LeafEval__DOT__vir_of[0x7fU] = ((vlSelfRef.LeafEval__DOT__bcell
                                               [0x7fU] 
                                               >> 2U) 
                                              & (0U 
                                                 != 
                                                 (3U 
                                                  & vlSelfRef.LeafEval__DOT__bcell
                                                  [0x7fU])));
    vlSelfRef.LeafEval__DOT__col_of[0U] = (3U & vlSelfRef.LeafEval__DOT__bcell
                                           [0U]);
    vlSelfRef.LeafEval__DOT__col_of[1U] = (3U & vlSelfRef.LeafEval__DOT__bcell
                                           [1U]);
    vlSelfRef.LeafEval__DOT__col_of[2U] = (3U & vlSelfRef.LeafEval__DOT__bcell
                                           [2U]);
    vlSelfRef.LeafEval__DOT__col_of[3U] = (3U & vlSelfRef.LeafEval__DOT__bcell
                                           [3U]);
    vlSelfRef.LeafEval__DOT__col_of[4U] = (3U & vlSelfRef.LeafEval__DOT__bcell
                                           [4U]);
    vlSelfRef.LeafEval__DOT__col_of[5U] = (3U & vlSelfRef.LeafEval__DOT__bcell
                                           [5U]);
    vlSelfRef.LeafEval__DOT__col_of[6U] = (3U & vlSelfRef.LeafEval__DOT__bcell
                                           [6U]);
    vlSelfRef.LeafEval__DOT__col_of[7U] = (3U & vlSelfRef.LeafEval__DOT__bcell
                                           [7U]);
    vlSelfRef.LeafEval__DOT__col_of[8U] = (3U & vlSelfRef.LeafEval__DOT__bcell
                                           [8U]);
    vlSelfRef.LeafEval__DOT__col_of[9U] = (3U & vlSelfRef.LeafEval__DOT__bcell
                                           [9U]);
    vlSelfRef.LeafEval__DOT__col_of[0xaU] = (3U & vlSelfRef.LeafEval__DOT__bcell
                                             [0xaU]);
    vlSelfRef.LeafEval__DOT__col_of[0xbU] = (3U & vlSelfRef.LeafEval__DOT__bcell
                                             [0xbU]);
    vlSelfRef.LeafEval__DOT__col_of[0xcU] = (3U & vlSelfRef.LeafEval__DOT__bcell
                                             [0xcU]);
    vlSelfRef.LeafEval__DOT__col_of[0xdU] = (3U & vlSelfRef.LeafEval__DOT__bcell
                                             [0xdU]);
    vlSelfRef.LeafEval__DOT__col_of[0xeU] = (3U & vlSelfRef.LeafEval__DOT__bcell
                                             [0xeU]);
    vlSelfRef.LeafEval__DOT__col_of[0xfU] = (3U & vlSelfRef.LeafEval__DOT__bcell
                                             [0xfU]);
    vlSelfRef.LeafEval__DOT__col_of[0x10U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x10U]);
    vlSelfRef.LeafEval__DOT__col_of[0x11U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x11U]);
    vlSelfRef.LeafEval__DOT__col_of[0x12U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x12U]);
    vlSelfRef.LeafEval__DOT__col_of[0x13U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x13U]);
    vlSelfRef.LeafEval__DOT__col_of[0x14U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x14U]);
    vlSelfRef.LeafEval__DOT__col_of[0x15U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x15U]);
    vlSelfRef.LeafEval__DOT__col_of[0x16U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x16U]);
    vlSelfRef.LeafEval__DOT__col_of[0x17U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x17U]);
    vlSelfRef.LeafEval__DOT__col_of[0x18U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x18U]);
    vlSelfRef.LeafEval__DOT__col_of[0x19U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x19U]);
    vlSelfRef.LeafEval__DOT__col_of[0x1aU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x1aU]);
    vlSelfRef.LeafEval__DOT__col_of[0x1bU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x1bU]);
    vlSelfRef.LeafEval__DOT__col_of[0x1cU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x1cU]);
    vlSelfRef.LeafEval__DOT__col_of[0x1dU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x1dU]);
    vlSelfRef.LeafEval__DOT__col_of[0x1eU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x1eU]);
    vlSelfRef.LeafEval__DOT__col_of[0x1fU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x1fU]);
    vlSelfRef.LeafEval__DOT__col_of[0x20U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x20U]);
    vlSelfRef.LeafEval__DOT__col_of[0x21U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x21U]);
    vlSelfRef.LeafEval__DOT__col_of[0x22U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x22U]);
    vlSelfRef.LeafEval__DOT__col_of[0x23U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x23U]);
    vlSelfRef.LeafEval__DOT__col_of[0x24U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x24U]);
    vlSelfRef.LeafEval__DOT__col_of[0x25U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x25U]);
    vlSelfRef.LeafEval__DOT__col_of[0x26U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x26U]);
    vlSelfRef.LeafEval__DOT__col_of[0x27U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x27U]);
    vlSelfRef.LeafEval__DOT__col_of[0x28U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x28U]);
    vlSelfRef.LeafEval__DOT__col_of[0x29U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x29U]);
    vlSelfRef.LeafEval__DOT__col_of[0x2aU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x2aU]);
    vlSelfRef.LeafEval__DOT__col_of[0x2bU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x2bU]);
    vlSelfRef.LeafEval__DOT__col_of[0x2cU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x2cU]);
    vlSelfRef.LeafEval__DOT__col_of[0x2dU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x2dU]);
    vlSelfRef.LeafEval__DOT__col_of[0x2eU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x2eU]);
    vlSelfRef.LeafEval__DOT__col_of[0x2fU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x2fU]);
    vlSelfRef.LeafEval__DOT__col_of[0x30U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x30U]);
    vlSelfRef.LeafEval__DOT__col_of[0x31U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x31U]);
    vlSelfRef.LeafEval__DOT__col_of[0x32U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x32U]);
    vlSelfRef.LeafEval__DOT__col_of[0x33U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x33U]);
    vlSelfRef.LeafEval__DOT__col_of[0x34U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x34U]);
    vlSelfRef.LeafEval__DOT__col_of[0x35U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x35U]);
    vlSelfRef.LeafEval__DOT__col_of[0x36U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x36U]);
    vlSelfRef.LeafEval__DOT__col_of[0x37U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x37U]);
    vlSelfRef.LeafEval__DOT__col_of[0x38U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x38U]);
    vlSelfRef.LeafEval__DOT__col_of[0x39U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x39U]);
    vlSelfRef.LeafEval__DOT__col_of[0x3aU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x3aU]);
    vlSelfRef.LeafEval__DOT__col_of[0x3bU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x3bU]);
    vlSelfRef.LeafEval__DOT__col_of[0x3cU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x3cU]);
    vlSelfRef.LeafEval__DOT__col_of[0x3dU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x3dU]);
    vlSelfRef.LeafEval__DOT__col_of[0x3eU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x3eU]);
    vlSelfRef.LeafEval__DOT__col_of[0x3fU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x3fU]);
    vlSelfRef.LeafEval__DOT__col_of[0x40U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x40U]);
    vlSelfRef.LeafEval__DOT__col_of[0x41U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x41U]);
    vlSelfRef.LeafEval__DOT__col_of[0x42U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x42U]);
    vlSelfRef.LeafEval__DOT__col_of[0x43U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x43U]);
    vlSelfRef.LeafEval__DOT__col_of[0x44U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x44U]);
    vlSelfRef.LeafEval__DOT__col_of[0x45U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x45U]);
    vlSelfRef.LeafEval__DOT__col_of[0x46U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x46U]);
    vlSelfRef.LeafEval__DOT__col_of[0x47U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x47U]);
    vlSelfRef.LeafEval__DOT__col_of[0x48U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x48U]);
    vlSelfRef.LeafEval__DOT__col_of[0x49U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x49U]);
    vlSelfRef.LeafEval__DOT__col_of[0x4aU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x4aU]);
    vlSelfRef.LeafEval__DOT__col_of[0x4bU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x4bU]);
    vlSelfRef.LeafEval__DOT__col_of[0x4cU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x4cU]);
    vlSelfRef.LeafEval__DOT__col_of[0x4dU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x4dU]);
    vlSelfRef.LeafEval__DOT__col_of[0x4eU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x4eU]);
    vlSelfRef.LeafEval__DOT__col_of[0x4fU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x4fU]);
    vlSelfRef.LeafEval__DOT__col_of[0x50U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x50U]);
    vlSelfRef.LeafEval__DOT__col_of[0x51U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x51U]);
    vlSelfRef.LeafEval__DOT__col_of[0x52U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x52U]);
    vlSelfRef.LeafEval__DOT__col_of[0x53U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x53U]);
    vlSelfRef.LeafEval__DOT__col_of[0x54U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x54U]);
    vlSelfRef.LeafEval__DOT__col_of[0x55U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x55U]);
    vlSelfRef.LeafEval__DOT__col_of[0x56U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x56U]);
    vlSelfRef.LeafEval__DOT__col_of[0x57U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x57U]);
    vlSelfRef.LeafEval__DOT__col_of[0x58U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x58U]);
    vlSelfRef.LeafEval__DOT__col_of[0x59U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x59U]);
    vlSelfRef.LeafEval__DOT__col_of[0x5aU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x5aU]);
    vlSelfRef.LeafEval__DOT__col_of[0x5bU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x5bU]);
    vlSelfRef.LeafEval__DOT__col_of[0x5cU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x5cU]);
    vlSelfRef.LeafEval__DOT__col_of[0x5dU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x5dU]);
    vlSelfRef.LeafEval__DOT__col_of[0x5eU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x5eU]);
    vlSelfRef.LeafEval__DOT__col_of[0x5fU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x5fU]);
    vlSelfRef.LeafEval__DOT__col_of[0x60U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x60U]);
    vlSelfRef.LeafEval__DOT__col_of[0x61U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x61U]);
    vlSelfRef.LeafEval__DOT__col_of[0x62U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x62U]);
    vlSelfRef.LeafEval__DOT__col_of[0x63U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x63U]);
    vlSelfRef.LeafEval__DOT__col_of[0x64U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x64U]);
    vlSelfRef.LeafEval__DOT__col_of[0x65U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x65U]);
    vlSelfRef.LeafEval__DOT__col_of[0x66U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x66U]);
    vlSelfRef.LeafEval__DOT__col_of[0x67U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x67U]);
    vlSelfRef.LeafEval__DOT__col_of[0x68U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x68U]);
    vlSelfRef.LeafEval__DOT__col_of[0x69U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x69U]);
    vlSelfRef.LeafEval__DOT__col_of[0x6aU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x6aU]);
    vlSelfRef.LeafEval__DOT__col_of[0x6bU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x6bU]);
    vlSelfRef.LeafEval__DOT__col_of[0x6cU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x6cU]);
    vlSelfRef.LeafEval__DOT__col_of[0x6dU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x6dU]);
    vlSelfRef.LeafEval__DOT__col_of[0x6eU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x6eU]);
    vlSelfRef.LeafEval__DOT__col_of[0x6fU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x6fU]);
    vlSelfRef.LeafEval__DOT__col_of[0x70U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x70U]);
    vlSelfRef.LeafEval__DOT__col_of[0x71U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x71U]);
    vlSelfRef.LeafEval__DOT__col_of[0x72U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x72U]);
    vlSelfRef.LeafEval__DOT__col_of[0x73U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x73U]);
    vlSelfRef.LeafEval__DOT__col_of[0x74U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x74U]);
    vlSelfRef.LeafEval__DOT__col_of[0x75U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x75U]);
    vlSelfRef.LeafEval__DOT__col_of[0x76U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x76U]);
    vlSelfRef.LeafEval__DOT__col_of[0x77U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x77U]);
    vlSelfRef.LeafEval__DOT__col_of[0x78U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x78U]);
    vlSelfRef.LeafEval__DOT__col_of[0x79U] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x79U]);
    vlSelfRef.LeafEval__DOT__col_of[0x7aU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x7aU]);
    vlSelfRef.LeafEval__DOT__col_of[0x7bU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x7bU]);
    vlSelfRef.LeafEval__DOT__col_of[0x7cU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x7cU]);
    vlSelfRef.LeafEval__DOT__col_of[0x7dU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x7dU]);
    vlSelfRef.LeafEval__DOT__col_of[0x7eU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x7eU]);
    vlSelfRef.LeafEval__DOT__col_of[0x7fU] = (3U & 
                                              vlSelfRef.LeafEval__DOT__bcell
                                              [0x7fU]);
    vlSelfRef.LeafEval__DOT__sr_addr = __Vdly__LeafEval__DOT__sr_addr;
    if (__VdlySet__LeafEval__DOT__slotram__DOT__mem__v0) {
        vlSelfRef.LeafEval__DOT__slotram__DOT__mem[__VdlyDim0__LeafEval__DOT__slotram__DOT__mem__v0] 
            = __VdlyVal__LeafEval__DOT__slotram__DOT__mem__v0;
    }
    vlSelfRef.LeafEval__DOT__v_col = vlSelfRef.LeafEval__DOT__col_of
        [vlSelfRef.LeafEval__DOT__vo];
}

void VLeafEval___024root___eval_triggers__act(VLeafEval___024root* vlSelf);

bool VLeafEval___024root___eval_phase__act(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___eval_phase__act\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    VlTriggerVec<1> __VpreTriggered;
    CData/*0:0*/ __VactExecute;
    // Body
    VLeafEval___024root___eval_triggers__act(vlSelf);
    __VactExecute = vlSelfRef.__VactTriggered.any();
    if (__VactExecute) {
        __VpreTriggered.andNot(vlSelfRef.__VactTriggered, vlSelfRef.__VnbaTriggered);
        vlSelfRef.__VnbaTriggered.thisOr(vlSelfRef.__VactTriggered);
        VLeafEval___024root___eval_act(vlSelf);
    }
    return (__VactExecute);
}

bool VLeafEval___024root___eval_phase__nba(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___eval_phase__nba\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = vlSelfRef.__VnbaTriggered.any();
    if (__VnbaExecute) {
        VLeafEval___024root___eval_nba(vlSelf);
        vlSelfRef.__VnbaTriggered.clear();
    }
    return (__VnbaExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VLeafEval___024root___dump_triggers__ico(VLeafEval___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void VLeafEval___024root___dump_triggers__nba(VLeafEval___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void VLeafEval___024root___dump_triggers__act(VLeafEval___024root* vlSelf);
#endif  // VL_DEBUG

void VLeafEval___024root___eval(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___eval\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    IData/*31:0*/ __VicoIterCount;
    CData/*0:0*/ __VicoContinue;
    IData/*31:0*/ __VnbaIterCount;
    CData/*0:0*/ __VnbaContinue;
    // Body
    __VicoIterCount = 0U;
    vlSelfRef.__VicoFirstIteration = 1U;
    __VicoContinue = 1U;
    while (__VicoContinue) {
        if (VL_UNLIKELY((0x64U < __VicoIterCount))) {
#ifdef VL_DEBUG
            VLeafEval___024root___dump_triggers__ico(vlSelf);
#endif
            VL_FATAL_MT("LeafEval.sv", 14, "", "Input combinational region did not converge.");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        __VicoContinue = 0U;
        if (VLeafEval___024root___eval_phase__ico(vlSelf)) {
            __VicoContinue = 1U;
        }
        vlSelfRef.__VicoFirstIteration = 0U;
    }
    __VnbaIterCount = 0U;
    __VnbaContinue = 1U;
    while (__VnbaContinue) {
        if (VL_UNLIKELY((0x64U < __VnbaIterCount))) {
#ifdef VL_DEBUG
            VLeafEval___024root___dump_triggers__nba(vlSelf);
#endif
            VL_FATAL_MT("LeafEval.sv", 14, "", "NBA region did not converge.");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        __VnbaContinue = 0U;
        vlSelfRef.__VactIterCount = 0U;
        vlSelfRef.__VactContinue = 1U;
        while (vlSelfRef.__VactContinue) {
            if (VL_UNLIKELY((0x64U < vlSelfRef.__VactIterCount))) {
#ifdef VL_DEBUG
                VLeafEval___024root___dump_triggers__act(vlSelf);
#endif
                VL_FATAL_MT("LeafEval.sv", 14, "", "Active region did not converge.");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
            vlSelfRef.__VactContinue = 0U;
            if (VLeafEval___024root___eval_phase__act(vlSelf)) {
                vlSelfRef.__VactContinue = 1U;
            }
        }
        if (VLeafEval___024root___eval_phase__nba(vlSelf)) {
            __VnbaContinue = 1U;
        }
    }
}

#ifdef VL_DEBUG
void VLeafEval___024root___eval_debug_assertions(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___eval_debug_assertions\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY((vlSelfRef.clk & 0xfeU))) {
        Verilated::overWidthError("clk");}
    if (VL_UNLIKELY((vlSelfRef.rst & 0xfeU))) {
        Verilated::overWidthError("rst");}
    if (VL_UNLIKELY((vlSelfRef.wr & 0xfeU))) {
        Verilated::overWidthError("wr");}
    if (VL_UNLIKELY((vlSelfRef.waddr & 0x80U))) {
        Verilated::overWidthError("waddr");}
    if (VL_UNLIKELY((vlSelfRef.wdata & 0xf8U))) {
        Verilated::overWidthError("wdata");}
    if (VL_UNLIKELY((vlSelfRef.wslot & 0xfcU))) {
        Verilated::overWidthError("wslot");}
    if (VL_UNLIKELY((vlSelfRef.start & 0xfeU))) {
        Verilated::overWidthError("start");}
    if (VL_UNLIKELY((vlSelfRef.cmd & 0xf0U))) {
        Verilated::overWidthError("cmd");}
    if (VL_UNLIKELY((vlSelfRef.cmd_go & 0xfeU))) {
        Verilated::overWidthError("cmd_go");}
    if (VL_UNLIKELY((vlSelfRef.a_sl & 0xfcU))) {
        Verilated::overWidthError("a_sl");}
    if (VL_UNLIKELY((vlSelfRef.a_o4 & 0xfcU))) {
        Verilated::overWidthError("a_o4");}
    if (VL_UNLIKELY((vlSelfRef.a_col & 0xf8U))) {
        Verilated::overWidthError("a_col");}
    if (VL_UNLIKELY((vlSelfRef.a_ca & 0xfcU))) {
        Verilated::overWidthError("a_ca");}
    if (VL_UNLIKELY((vlSelfRef.a_cb & 0xfcU))) {
        Verilated::overWidthError("a_cb");}
}
#endif  // VL_DEBUG
