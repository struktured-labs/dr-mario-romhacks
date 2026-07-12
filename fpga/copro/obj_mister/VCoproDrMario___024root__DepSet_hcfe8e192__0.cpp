// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VCoproDrMario.h for the primary calling header

#include "VCoproDrMario__pch.h"
#include "VCoproDrMario___024root.h"

void VCoproDrMario___024root___ico_sequent__TOP__0(VCoproDrMario___024root* vlSelf);

void VCoproDrMario___024root___eval_ico(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___eval_ico\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VicoTriggered.word(0U))) {
        VCoproDrMario___024root___ico_sequent__TOP__0(vlSelf);
    }
}

VL_INLINE_OPT void VCoproDrMario___024root___ico_sequent__TOP__0(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___ico_sequent__TOP__0\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.copro_sel = ((IData)(vlSelfRef.enable) 
                           & (0x5000U == (0xfe00U & (IData)(vlSelfRef.prg_ain))));
}

void VCoproDrMario___024root___eval_triggers__ico(VCoproDrMario___024root* vlSelf);

bool VCoproDrMario___024root___eval_phase__ico(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___eval_phase__ico\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VicoExecute;
    // Body
    VCoproDrMario___024root___eval_triggers__ico(vlSelf);
    __VicoExecute = vlSelfRef.__VicoTriggered.any();
    if (__VicoExecute) {
        VCoproDrMario___024root___eval_ico(vlSelf);
    }
    return (__VicoExecute);
}

void VCoproDrMario___024root___eval_act(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___eval_act\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

void VCoproDrMario___024root___nba_sequent__TOP__0(VCoproDrMario___024root* vlSelf);
void VCoproDrMario___024root___nba_sequent__TOP__1(VCoproDrMario___024root* vlSelf);
void VCoproDrMario___024root___nba_sequent__TOP__2(VCoproDrMario___024root* vlSelf);
void VCoproDrMario___024root___nba_sequent__TOP__3(VCoproDrMario___024root* vlSelf);
void VCoproDrMario___024root___nba_sequent__TOP__4(VCoproDrMario___024root* vlSelf);
void VCoproDrMario___024root___nba_sequent__TOP__5(VCoproDrMario___024root* vlSelf);
void VCoproDrMario___024root___nba_sequent__TOP__6(VCoproDrMario___024root* vlSelf);
void VCoproDrMario___024root___nba_sequent__TOP__7(VCoproDrMario___024root* vlSelf);
void VCoproDrMario___024root___nba_comb__TOP__0(VCoproDrMario___024root* vlSelf);

void VCoproDrMario___024root___eval_nba(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___eval_nba\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((3ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VCoproDrMario___024root___nba_sequent__TOP__0(vlSelf);
    }
    if ((2ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VCoproDrMario___024root___nba_sequent__TOP__1(vlSelf);
    }
    if ((1ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VCoproDrMario___024root___nba_sequent__TOP__2(vlSelf);
    }
    if ((5ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VCoproDrMario___024root___nba_sequent__TOP__3(vlSelf);
    }
    if ((3ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VCoproDrMario___024root___nba_sequent__TOP__4(vlSelf);
    }
    if ((1ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VCoproDrMario___024root___nba_sequent__TOP__5(vlSelf);
    }
    if ((5ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VCoproDrMario___024root___nba_sequent__TOP__6(vlSelf);
    }
    if ((2ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VCoproDrMario___024root___nba_sequent__TOP__7(vlSelf);
    }
    if ((5ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VCoproDrMario___024root___nba_comb__TOP__0(vlSelf);
    }
}

VL_INLINE_OPT void VCoproDrMario___024root___nba_sequent__TOP__0(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___nba_sequent__TOP__0\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VdlySet__CoproDrMario__DOT__wram__DOT__mem__v0 = 0U;
    vlSelfRef.__VdlySet__CoproDrMario__DOT__wram__DOT__mem__v1 = 0U;
}

VL_INLINE_OPT void VCoproDrMario___024root___nba_sequent__TOP__1(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___nba_sequent__TOP__1\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    SData/*11:0*/ __Vfunc_CoproDrMario__DOT__xlate__0__Vfuncout;
    __Vfunc_CoproDrMario__DOT__xlate__0__Vfuncout = 0;
    SData/*8:0*/ __Vfunc_CoproDrMario__DOT__xlate__0__a;
    __Vfunc_CoproDrMario__DOT__xlate__0__a = 0;
    SData/*11:0*/ __Vfunc_CoproDrMario__DOT__xlate__1__Vfuncout;
    __Vfunc_CoproDrMario__DOT__xlate__1__Vfuncout = 0;
    SData/*8:0*/ __Vfunc_CoproDrMario__DOT__xlate__1__a;
    __Vfunc_CoproDrMario__DOT__xlate__1__a = 0;
    // Body
    vlSelfRef.__Vdly__CoproDrMario__DOT__rst_cnt = vlSelfRef.CoproDrMario__DOT__rst_cnt;
    if (vlSelfRef.CoproDrMario__DOT__hb_we) {
        vlSelfRef.__VdlyVal__CoproDrMario__DOT__wram__DOT__mem__v1 
            = vlSelfRef.CoproDrMario__DOT__hb_din;
        vlSelfRef.__VdlyDim0__CoproDrMario__DOT__wram__DOT__mem__v1 
            = vlSelfRef.CoproDrMario__DOT__hb_addr;
        vlSelfRef.__VdlySet__CoproDrMario__DOT__wram__DOT__mem__v1 = 1U;
    }
    vlSelfRef.CoproDrMario__DOT__ram_b_q = vlSelfRef.CoproDrMario__DOT__wram__DOT__mem
        [vlSelfRef.CoproDrMario__DOT__hb_addr];
    vlSelfRef.CoproDrMario__DOT__hb_we = 0U;
    if ((((IData)(vlSelfRef.ce) & (IData)(vlSelfRef.prg_write)) 
         & (IData)(vlSelfRef.copro_sel))) {
        if ((0x84U == (0x1ffU & (IData)(vlSelfRef.prg_ain)))) {
            vlSelfRef.__Vdly__CoproDrMario__DOT__rst_cnt = 0x1fU;
            vlSelfRef.CoproDrMario__DOT__hb_din = 0U;
            vlSelfRef.CoproDrMario__DOT__hb_addr = 0x8ffU;
        } else {
            vlSelfRef.CoproDrMario__DOT__hb_din = vlSelfRef.prg_din;
            __Vfunc_CoproDrMario__DOT__xlate__0__a 
                = (0x1ffU & (IData)(vlSelfRef.prg_ain));
            __Vfunc_CoproDrMario__DOT__xlate__0__Vfuncout 
                = ((IData)((0U == (0x180U & (IData)(__Vfunc_CoproDrMario__DOT__xlate__0__a))))
                    ? (0x500U | (0x7fU & (IData)(__Vfunc_CoproDrMario__DOT__xlate__0__a)))
                    : ((IData)((0x80U == (0x180U & (IData)(__Vfunc_CoproDrMario__DOT__xlate__0__a))))
                        ? ((0x40U & (IData)(__Vfunc_CoproDrMario__DOT__xlate__0__a))
                            ? 0x8feU : ((0x20U & (IData)(__Vfunc_CoproDrMario__DOT__xlate__0__a))
                                         ? 0x8feU : 
                                        ((0x10U & (IData)(__Vfunc_CoproDrMario__DOT__xlate__0__a))
                                          ? 0x8feU : 
                                         ((8U & (IData)(__Vfunc_CoproDrMario__DOT__xlate__0__a))
                                           ? 0x8feU
                                           : ((4U & (IData)(__Vfunc_CoproDrMario__DOT__xlate__0__a))
                                               ? ((2U 
                                                   & (IData)(__Vfunc_CoproDrMario__DOT__xlate__0__a))
                                                   ? 
                                                  ((1U 
                                                    & (IData)(__Vfunc_CoproDrMario__DOT__xlate__0__a))
                                                    ? 0x8feU
                                                    : 0x835U)
                                                   : 
                                                  ((1U 
                                                    & (IData)(__Vfunc_CoproDrMario__DOT__xlate__0__a))
                                                    ? 0x834U
                                                    : 0x8ffU))
                                               : ((2U 
                                                   & (IData)(__Vfunc_CoproDrMario__DOT__xlate__0__a))
                                                   ? 
                                                  ((1U 
                                                    & (IData)(__Vfunc_CoproDrMario__DOT__xlate__0__a))
                                                    ? 0x827U
                                                    : 0x826U)
                                                   : 
                                                  ((1U 
                                                    & (IData)(__Vfunc_CoproDrMario__DOT__xlate__0__a))
                                                    ? 0x825U
                                                    : 0x824U)))))))
                        : 0x8feU));
            vlSelfRef.CoproDrMario__DOT__hb_addr = __Vfunc_CoproDrMario__DOT__xlate__0__Vfuncout;
        }
        vlSelfRef.CoproDrMario__DOT__hb_we = 1U;
    } else {
        if (((0U != (IData)(vlSelfRef.CoproDrMario__DOT__rst_cnt)) 
             & (~ (IData)(vlSelfRef.CoproDrMario__DOT__parked)))) {
            vlSelfRef.__Vdly__CoproDrMario__DOT__rst_cnt 
                = (0x1fU & ((IData)(vlSelfRef.CoproDrMario__DOT__rst_cnt) 
                            - (IData)(1U)));
        }
        __Vfunc_CoproDrMario__DOT__xlate__1__a = (0x1ffU 
                                                  & (IData)(vlSelfRef.prg_ain));
        __Vfunc_CoproDrMario__DOT__xlate__1__Vfuncout 
            = ((IData)((0U == (0x180U & (IData)(__Vfunc_CoproDrMario__DOT__xlate__1__a))))
                ? (0x500U | (0x7fU & (IData)(__Vfunc_CoproDrMario__DOT__xlate__1__a)))
                : ((IData)((0x80U == (0x180U & (IData)(__Vfunc_CoproDrMario__DOT__xlate__1__a))))
                    ? ((0x40U & (IData)(__Vfunc_CoproDrMario__DOT__xlate__1__a))
                        ? 0x8feU : ((0x20U & (IData)(__Vfunc_CoproDrMario__DOT__xlate__1__a))
                                     ? 0x8feU : ((0x10U 
                                                  & (IData)(__Vfunc_CoproDrMario__DOT__xlate__1__a))
                                                  ? 0x8feU
                                                  : 
                                                 ((8U 
                                                   & (IData)(__Vfunc_CoproDrMario__DOT__xlate__1__a))
                                                   ? 0x8feU
                                                   : 
                                                  ((4U 
                                                    & (IData)(__Vfunc_CoproDrMario__DOT__xlate__1__a))
                                                    ? 
                                                   ((2U 
                                                     & (IData)(__Vfunc_CoproDrMario__DOT__xlate__1__a))
                                                     ? 
                                                    ((1U 
                                                      & (IData)(__Vfunc_CoproDrMario__DOT__xlate__1__a))
                                                      ? 0x8feU
                                                      : 0x835U)
                                                     : 
                                                    ((1U 
                                                      & (IData)(__Vfunc_CoproDrMario__DOT__xlate__1__a))
                                                      ? 0x834U
                                                      : 0x8ffU))
                                                    : 
                                                   ((2U 
                                                     & (IData)(__Vfunc_CoproDrMario__DOT__xlate__1__a))
                                                     ? 
                                                    ((1U 
                                                      & (IData)(__Vfunc_CoproDrMario__DOT__xlate__1__a))
                                                      ? 0x827U
                                                      : 0x826U)
                                                     : 
                                                    ((1U 
                                                      & (IData)(__Vfunc_CoproDrMario__DOT__xlate__1__a))
                                                      ? 0x825U
                                                      : 0x824U)))))))
                    : 0x8feU));
        vlSelfRef.CoproDrMario__DOT__hb_addr = __Vfunc_CoproDrMario__DOT__xlate__1__Vfuncout;
    }
    vlSelfRef.prg_dout = vlSelfRef.CoproDrMario__DOT__ram_b_q;
}

extern const VlUnpacked<CData/*0:0*/, 16384> VCoproDrMario__ConstPool__TABLE_h5eb454e9_0;
extern const VlUnpacked<CData/*3:0*/, 16384> VCoproDrMario__ConstPool__TABLE_hc29132ea_0;

VL_INLINE_OPT void VCoproDrMario___024root___nba_sequent__TOP__2(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___nba_sequent__TOP__2\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    SData/*8:0*/ __Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__3__Vfuncout;
    __Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__3__Vfuncout = 0;
    CData/*4:0*/ __Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__3__n;
    __Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__3__n = 0;
    SData/*8:0*/ __Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__4__Vfuncout;
    __Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__4__Vfuncout = 0;
    CData/*4:0*/ __Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__4__n;
    __Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__4__n = 0;
    SData/*8:0*/ __Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__5__Vfuncout;
    __Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__5__Vfuncout = 0;
    CData/*4:0*/ __Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__5__n;
    __Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__5__n = 0;
    SData/*13:0*/ __Vtableidx7;
    __Vtableidx7 = 0;
    CData/*4:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__st;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0;
    CData/*4:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__maxh;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__maxh = 0;
    CData/*7:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__holes;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__holes = 0;
    CData/*7:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__toprisk;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__toprisk = 0;
    CData/*7:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__spawn;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__spawn = 0;
    CData/*7:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__setup;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__setup = 0;
    SData/*10:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__pollution;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__pollution = 0;
    SData/*9:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__buried;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__buried = 0;
    SData/*15:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__rdy_ext;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__rdy_ext = 0;
    SData/*15:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__vrdy;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__vrdy = 0;
    CData/*0:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__anyvir;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__anyvir = 0;
    CData/*3:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__wc;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__wc = 0;
    CData/*3:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__wr_;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__wr_ = 0;
    CData/*0:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__seen;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__seen = 0;
    CData/*4:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__fillcnt;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__fillcnt = 0;
    CData/*3:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__cmd_l;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__cmd_l = 0;
    CData/*0:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__node_leaf;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__node_leaf = 0;
    CData/*5:0*/ __Vdly__CoproDrMario__DOT__lev_rvc;
    __Vdly__CoproDrMario__DOT__lev_rvc = 0;
    CData/*3:0*/ __Vdly__CoproDrMario__DOT__lev_rvv;
    __Vdly__CoproDrMario__DOT__lev_rvv = 0;
    VlWide<4>/*127:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__markb;
    VL_ZERO_W(128, __Vdly__CoproDrMario__DOT__leafeval__DOT__markb);
    CData/*0:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__anyclear;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__anyclear = 0;
    CData/*4:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp = 0;
    CData/*6:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp2;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp2 = 0;
    CData/*6:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__cpw_p;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__cpw_p = 0;
    SData/*8:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__sr_addr;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__sr_addr = 0;
    CData/*4:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__fo1;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__fo1 = 0;
    CData/*6:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__off_b;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__off_b = 0;
    CData/*6:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__off_a;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__off_a = 0;
    CData/*1:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__li;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__li = 0;
    CData/*3:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__sstep;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__sstep = 0;
    CData/*4:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__scnt;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__scnt = 0;
    CData/*4:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__srun;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__srun = 0;
    CData/*1:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__smcol;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__smcol = 0;
    CData/*7:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__soff;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__soff = 0;
    CData/*7:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__srstart;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__srstart = 0;
    CData/*4:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__gdest;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__gdest = 0;
    CData/*6:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__vo;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__vo = 0;
    CData/*4:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__run_h;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__run_h = 0;
    CData/*4:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__run_v;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__run_v = 0;
    CData/*4:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__p;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__p = 0;
    CData/*4:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__span_lo;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__span_lo = 0;
    CData/*4:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__span_hi;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__span_hi = 0;
    CData/*4:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__vspan_lo;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__vspan_lo = 0;
    CData/*4:0*/ __Vdly__CoproDrMario__DOT__leafeval__DOT__vspan_hi;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__vspan_hi = 0;
    CData/*7:0*/ __VdlyVal__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0;
    __VdlyVal__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0 = 0;
    CData/*1:0*/ __VdlyDim0__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0;
    __VdlyDim0__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0 = 0;
    CData/*0:0*/ __VdlySet__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0;
    __VdlySet__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0 = 0;
    CData/*2:0*/ __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v0;
    __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v0 = 0;
    CData/*6:0*/ __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v0;
    __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v0 = 0;
    CData/*0:0*/ __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v0;
    __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v0 = 0;
    CData/*2:0*/ __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v1;
    __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v1 = 0;
    CData/*6:0*/ __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v1;
    __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v1 = 0;
    CData/*0:0*/ __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v1;
    __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v1 = 0;
    CData/*2:0*/ __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v2;
    __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v2 = 0;
    CData/*6:0*/ __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v2;
    __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v2 = 0;
    CData/*0:0*/ __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v2;
    __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v2 = 0;
    CData/*2:0*/ __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v3;
    __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v3 = 0;
    CData/*6:0*/ __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v3;
    __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v3 = 0;
    CData/*0:0*/ __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v3;
    __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v3 = 0;
    CData/*6:0*/ __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v4;
    __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v4 = 0;
    CData/*0:0*/ __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v4;
    __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v4 = 0;
    CData/*2:0*/ __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v5;
    __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v5 = 0;
    CData/*6:0*/ __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v5;
    __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v5 = 0;
    CData/*0:0*/ __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v5;
    __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v5 = 0;
    CData/*6:0*/ __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v6;
    __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v6 = 0;
    CData/*7:0*/ __VdlyVal__CoproDrMario__DOT__leafeval__DOT__slotram__DOT__mem__v0;
    __VdlyVal__CoproDrMario__DOT__leafeval__DOT__slotram__DOT__mem__v0 = 0;
    SData/*8:0*/ __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__slotram__DOT__mem__v0;
    __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__slotram__DOT__mem__v0 = 0;
    CData/*0:0*/ __VdlySet__CoproDrMario__DOT__leafeval__DOT__slotram__DOT__mem__v0;
    __VdlySet__CoproDrMario__DOT__leafeval__DOT__slotram__DOT__mem__v0 = 0;
    // Body
    __VdlySet__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0 = 0U;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__maxh 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__maxh;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__holes 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__holes;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__toprisk 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__toprisk;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__spawn 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__spawn;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__setup 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__setup;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__pollution 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__pollution;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__buried 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__buried;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__rdy_ext 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__rdy_ext;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__vrdy 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vrdy;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__anyvir 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__anyvir;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__wc = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__wr_ = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__seen 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__seen;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__fillcnt 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fillcnt;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__cmd_l 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__cmd_l;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__node_leaf 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__node_leaf;
    __Vdly__CoproDrMario__DOT__lev_rvc = vlSelfRef.CoproDrMario__DOT__lev_rvc;
    __Vdly__CoproDrMario__DOT__lev_rvv = vlSelfRef.CoproDrMario__DOT__lev_rvv;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[0U] 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__markb[0U];
    __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[1U] 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__markb[1U];
    __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[2U] 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__markb[2U];
    __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[3U] 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__markb[3U];
    __Vdly__CoproDrMario__DOT__leafeval__DOT__anyclear 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__anyclear;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp2 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp2;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__sr_addr 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sr_addr;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__fo1 = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fo1;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__off_b 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__off_b;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__off_a 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__off_a;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__li = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__li;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__sstep 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__scnt 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__scnt;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__srun 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__smcol 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__smcol;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__soff 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__soff;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__srstart 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__gdest 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__gdest;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__run_h 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__run_h;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__run_v 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__run_v;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__p = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__span_lo 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__span_lo;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__span_hi 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__span_hi;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__vspan_lo 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vspan_lo;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__vspan_hi 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vspan_hi;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__cpw_p 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__cpw_p;
    __Vdly__CoproDrMario__DOT__leafeval__DOT__vo = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vo;
    __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v0 = 0U;
    __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v1 = 0U;
    __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v2 = 0U;
    __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v3 = 0U;
    __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v4 = 0U;
    __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v5 = 0U;
    __VdlySet__CoproDrMario__DOT__leafeval__DOT__slotram__DOT__mem__v0 = 0U;
    if (((IData)(vlSelfRef.CoproDrMario__DOT____VdfgRegularize_hb6d3a560_2_3) 
         & (IData)(vlSelfRef.CoproDrMario__DOT__a_ram))) {
        vlSelfRef.__VdlyVal__CoproDrMario__DOT__wram__DOT__mem__v0 
            = vlSelfRef.CoproDrMario__DOT__DO;
        vlSelfRef.__VdlyDim0__CoproDrMario__DOT__wram__DOT__mem__v0 
            = vlSelfRef.CoproDrMario__DOT__a_addr;
        vlSelfRef.__VdlySet__CoproDrMario__DOT__wram__DOT__mem__v0 = 1U;
    }
    if (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__NMI_edge) 
         & (0xbU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)))) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__NMI_edge = 0U;
    }
    if (vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__write_register) {
        __VdlyVal__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0 
            = ((0x1aU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                ? (IData)(vlSelfRef.CoproDrMario__DOT__DI)
                : ((0xf0U & ((((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD) 
                               >> 4U) + ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__adj_bcd)
                                          ? ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__adc_bcd)
                                              ? ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__CO)
                                                  ? 6U
                                                  : 0U)
                                              : ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__CO)
                                                  ? 0U
                                                  : 0xaU))
                                          : 0U)) << 4U)) 
                   | (0xfU & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD) 
                              + ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__adj_bcd)
                                  ? ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__adc_bcd)
                                      ? ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__HC)
                                          ? 6U : 0U)
                                      : ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__HC)
                                          ? 0U : 0xaU))
                                  : 0U)))));
        __VdlyDim0__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0 
            = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__regsel;
        __VdlySet__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0 = 1U;
    }
    if ((((IData)(vlSelfRef.CoproDrMario__DOT__lev_wr_board) 
          & (0U != (IData)(vlSelfRef.CoproDrMario__DOT__lev_wslot))) 
         | (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sl_cpw))) {
        __VdlyVal__CoproDrMario__DOT__leafeval__DOT__slotram__DOT__mem__v0 
            = ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sl_cpw)
                ? vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
               [vlSelfRef.CoproDrMario__DOT__leafeval__DOT__cpw_p]
                : (IData)(vlSelfRef.CoproDrMario__DOT__lev_enc));
        __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__slotram__DOT__mem__v0 
            = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sl_wa;
        __VdlySet__CoproDrMario__DOT__leafeval__DOT__slotram__DOT__mem__v0 = 1U;
    }
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__cond_code 
        = (7U & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR) 
                 >> 5U));
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC = 
        (0xffffU & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp) 
                    + (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_inc)));
    vlSelfRef.CoproDrMario__DOT__sel_ram_d = vlSelfRef.CoproDrMario__DOT__a_ram;
    vlSelfRef.CoproDrMario__DOT__ram_a_q = vlSelfRef.CoproDrMario__DOT__wram__DOT__mem
        [vlSelfRef.CoproDrMario__DOT__a_addr];
    vlSelfRef.CoproDrMario__DOT__sel_rom_d = (2U == 
                                              (3U & 
                                               ((IData)(vlSelfRef.CoproDrMario__DOT__AB) 
                                                >> 0xeU)));
    vlSelfRef.CoproDrMario__DOT__sel_vec_d = (0x7ffeU 
                                              == (0x7fffU 
                                                  & ((IData)(vlSelfRef.CoproDrMario__DOT__AB) 
                                                     >> 1U)));
    vlSelfRef.CoproDrMario__DOT__sel_lev_d = (0x70U 
                                              == (0xffU 
                                                  & ((IData)(vlSelfRef.CoproDrMario__DOT__AB) 
                                                     >> 8U)));
    vlSelfRef.CoproDrMario__DOT__ab0_d = (1U & (IData)(vlSelfRef.CoproDrMario__DOT__AB));
    vlSelfRef.CoproDrMario__DOT__rom_q = vlSelfRef.CoproDrMario__DOT__rom
        [(0x3fffU & (IData)(vlSelfRef.CoproDrMario__DOT__AB))];
    if ((((((0x21U != (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)) 
            & (0x22U != (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
           & (0x1eU != (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
          & (0x1fU != (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
         & (0x20U != (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)))) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ABL 
            = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__AB));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ABH 
            = (0xffU & ((IData)(vlSelfRef.CoproDrMario__DOT__AB) 
                        >> 8U));
    }
    __Vtableidx7 = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR) 
                     << 6U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state));
    if (VCoproDrMario__ConstPool__TABLE_h5eb454e9_0
        [__Vtableidx7]) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__op 
            = VCoproDrMario__ConstPool__TABLE_hc29132ea_0
            [__Vtableidx7];
    }
    if ((1U & (~ (IData)(vlSelfRef.CoproDrMario__DOT__cpu_rst)))) {
        if (((0x1eU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)) 
             | (0x21U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)))) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IRHOLD 
                = vlSelfRef.CoproDrMario__DOT__DI;
        }
    }
    if ((0xbU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__I = 1U;
    } else if ((0x27U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__I 
            = (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__DI) 
                     >> 2U));
    } else if ((0x24U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        if (vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__sei) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__I = 1U;
        }
        if (vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__cli) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__I = 0U;
        }
    } else if ((0xcU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        if (vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__plp) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__I 
                = (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD) 
                         >> 2U));
        }
    }
    if ((0x2eU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__Z 
            = (1U & (~ (IData)((0U != (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD)))));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__N 
            = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AN;
    } else if ((0x27U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__Z 
            = (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__DI) 
                     >> 1U));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__N 
            = (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__DI) 
                     >> 7U));
    } else if ((0xcU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        if (vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__plp) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__Z 
                = (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD) 
                         >> 1U));
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__N 
                = (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD) 
                         >> 7U));
        } else {
            if (((((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__load_reg) 
                   & (1U != (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__regsel))) 
                  | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__compare)) 
                 | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__bit_ins))) {
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__Z 
                    = (1U & (~ (IData)((0U != (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD)))));
            }
            if ((((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__load_reg) 
                  & (1U != (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__regsel))) 
                 | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__compare))) {
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__N 
                    = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AN;
            }
        }
    } else if (((0xdU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)) 
                & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__bit_ins))) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__N 
            = (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__DI) 
                     >> 7U));
    }
    if (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__shift) 
         & (0x2eU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)))) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__C 
            = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__CO;
    } else if ((0x27U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__C 
            = (1U & (IData)(vlSelfRef.CoproDrMario__DOT__DI));
    } else if (((~ (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__write_back)) 
                & (0xcU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)))) {
        if ((((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__adc_sbc) 
              | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__shift)) 
             | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__compare))) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__C 
                = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__CO;
        } else if (vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__plp) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__C 
                = (1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD));
        } else {
            if (vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__sec) {
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__C = 1U;
            }
            if (vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__clc) {
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__C = 0U;
            }
        }
    }
    if ((0x27U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__V 
            = (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__DI) 
                     >> 6U));
    } else if ((0xcU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        if (vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__adc_sbc) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__V 
                = ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__AI7) 
                   ^ ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__BI7) 
                      ^ ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AN) 
                         ^ (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__CO))));
        }
        if (vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__clv) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__V = 0U;
        }
        if (vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__plp) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__V 
                = (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD) 
                         >> 6U));
        }
    } else if (((0xdU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)) 
                & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__bit_ins))) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__V 
            = (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__DI) 
                     >> 6U));
    }
    vlSelfRef.CoproDrMario__DOT__lev_q = (0xffU & (
                                                   (8U 
                                                    & (IData)(vlSelfRef.CoproDrMario__DOT__AB))
                                                    ? 
                                                   ((4U 
                                                     & (IData)(vlSelfRef.CoproDrMario__DOT__AB))
                                                     ? 
                                                    ((2U 
                                                      & (IData)(vlSelfRef.CoproDrMario__DOT__AB))
                                                      ? (IData)(vlSelfRef.CoproDrMario__DOT__lev_done)
                                                      : 
                                                     ((1U 
                                                       & (IData)(vlSelfRef.CoproDrMario__DOT__AB))
                                                       ? (IData)(vlSelfRef.CoproDrMario__DOT__lev_done)
                                                       : 
                                                      ((IData)(vlSelfRef.CoproDrMario__DOT__lev_imm) 
                                                       >> 8U)))
                                                     : 
                                                    ((2U 
                                                      & (IData)(vlSelfRef.CoproDrMario__DOT__AB))
                                                      ? 
                                                     ((1U 
                                                       & (IData)(vlSelfRef.CoproDrMario__DOT__AB))
                                                       ? (IData)(vlSelfRef.CoproDrMario__DOT__lev_imm)
                                                       : (IData)(vlSelfRef.CoproDrMario__DOT__lev_rvv))
                                                      : 
                                                     ((1U 
                                                       & (IData)(vlSelfRef.CoproDrMario__DOT__AB))
                                                       ? (IData)(vlSelfRef.CoproDrMario__DOT__lev_rvc)
                                                       : 
                                                      ((0xeU 
                                                        == 
                                                        (0xfU 
                                                         & ((IData)(vlSelfRef.CoproDrMario__DOT__AB) 
                                                            >> 4U)))
                                                        ? (IData)(vlSelfRef.CoproDrMario__DOT__lev_legal)
                                                        : (IData)(vlSelfRef.CoproDrMario__DOT__lev_done)))))
                                                    : 
                                                   ((4U 
                                                     & (IData)(vlSelfRef.CoproDrMario__DOT__AB))
                                                     ? (IData)(vlSelfRef.CoproDrMario__DOT__lev_done)
                                                     : 
                                                    ((2U 
                                                      & (IData)(vlSelfRef.CoproDrMario__DOT__AB))
                                                      ? 
                                                     ((1U 
                                                       & (IData)(vlSelfRef.CoproDrMario__DOT__AB))
                                                       ? (IData)(vlSelfRef.CoproDrMario__DOT__lev_done)
                                                       : (IData)(vlSelfRef.CoproDrMario__DOT__lev_win))
                                                      : 
                                                     ((1U 
                                                       & (IData)(vlSelfRef.CoproDrMario__DOT__AB))
                                                       ? 
                                                      ((IData)(vlSelfRef.CoproDrMario__DOT__lev_sco) 
                                                       >> 8U)
                                                       : (IData)(vlSelfRef.CoproDrMario__DOT__lev_sco))))));
    if (__VdlySet__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AXYS[__VdlyDim0__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0] 
            = __VdlyVal__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0;
    }
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__HC = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_HC;
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__adj_bcd 
        = ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__adc_sbc) 
           & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__D));
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AN = 
        (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp) 
               >> 7U));
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__BI7 
        = (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_BI) 
                 >> 7U));
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__AI7 
        = (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI) 
                 >> 7U));
    if (vlSelfRef.CoproDrMario__DOT__cpu_rst) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IRHOLD_valid = 0U;
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__res = 1U;
    } else {
        if (((0x1eU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)) 
             | (0x21U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)))) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IRHOLD_valid = 1U;
        } else if ((0xcU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IRHOLD_valid = 0U;
        }
        if ((0xcU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__res = 0U;
        }
    }
    if (((0xcU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)) 
         | (8U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)))) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__adc_bcd 
            = ((0x61U == (0xe3U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
               && (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__D));
    }
    if ((0xcU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__php 
            = (8U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__shift_right 
            = (0x42U == (0xc3U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__inc 
            = ((0xe6U == (0xe7U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
               || (0xc8U == (0xdfU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__rotate 
            = ((0x2aU == (0xafU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
               || (0x26U == (0xa7U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__dst_reg 
            = ((((0xe8U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)) 
                 || (0xcaU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                || (0xa2U == (0xe3U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))))
                ? 2U : (((8U == (0xbfU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                         || (0x9aU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))
                         ? 1U : ((((0x88U == (0xbfU 
                                              & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                                   || (0xa4U == (0xe7U 
                                                 & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                                  || (0xa0U == (0xf7U 
                                                & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))))
                                  ? 3U : 0U)));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__src_reg 
            = ((0xbaU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))
                ? 1U : (((((0x86U == (0xe7U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                           || (0x8aU == (0xebU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                          || (0xe0U == (0xf3U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                         || (0xcaU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))
                         ? 2U : (((((0x84U == (0xe7U 
                                               & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                                    || (0x98U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                                   || (0xc0U == (0xf3U 
                                                 & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                                  || (0x88U == (0xbfU 
                                                & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))))
                                  ? 3U : 0U)));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__index_y 
            = (((0x11U == (0x1fU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                || (0x96U == (0xd7U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
               || (9U == (0xfU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__load_only 
            = (0xa0U == (0xe0U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__sei 
            = (0x78U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__cli 
            = (0x58U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__load_reg 
            = (((((((((0xaU == (0x9fU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                      || (1U == (0x83U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                     || (0x88U == (0xedU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                    || (0xa0U == (0xf1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                   || (0xbaU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                  || (0xb4U == (0xf5U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                 || (0xcaU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                || (0xa1U == (0xa3U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
               || (8U == (0x1fU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__clv 
            = (0xb8U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__bit_ins 
            = (0x24U == (0xf7U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__sec 
            = (0x38U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__clc 
            = (0x18U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__shift 
            = ((6U == (0x87U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
               || (0xaU == (0x8fU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__compare 
            = (((0xc0U == (0xdbU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                || (0xccU == (0xdfU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
               || (0xc1U == (0xe3U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))));
    }
    if (vlSelfRef.CoproDrMario__DOT__cpu_rst) {
        __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0U;
        vlSelfRef.CoproDrMario__DOT__lev_done = 0U;
        vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sl_cpw = 0U;
    } else {
        if (((IData)(vlSelfRef.CoproDrMario__DOT__lev_wr_board) 
             & (0U == (IData)(vlSelfRef.CoproDrMario__DOT__lev_wslot)))) {
            __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v0 
                = vlSelfRef.CoproDrMario__DOT__lev_enc;
            __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v0 
                = (0x7fU & (IData)(vlSelfRef.CoproDrMario__DOT__AB));
            __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v0 = 1U;
        }
        if (((((((((0U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st)) 
                   | (0x11U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) 
                  | (0x1cU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) 
                 | (0x1aU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) 
                | (0x1bU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) 
               | (0x12U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) 
              | (0x13U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) 
             | (0x14U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st)))) {
            if ((0U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                if (((IData)(vlSelfRef.CoproDrMario__DOT__lev_start) 
                     | ((IData)(vlSelfRef.CoproDrMario__DOT____VdfgRegularize_hb6d3a560_2_2) 
                        & (0xf4U == (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__AB)))))) {
                    vlSelfRef.CoproDrMario__DOT__lev_done = 0U;
                    if (((IData)(vlSelfRef.CoproDrMario__DOT__lev_start) 
                         | (1U == (0xfU & (IData)(vlSelfRef.CoproDrMario__DOT__DO))))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__maxh = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__holes = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__toprisk = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__spawn = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__setup = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__pollution = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__buried = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__rdy_ext = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__vrdy = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__anyvir = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__wc = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__wr_ = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__seen = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__fillcnt = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 1U;
                    } else if (((2U == (0xfU & (IData)(vlSelfRef.CoproDrMario__DOT__DO))) 
                                | (3U == (0xfU & (IData)(vlSelfRef.CoproDrMario__DOT__DO))))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__cmd_l 
                            = (0xfU & (IData)(vlSelfRef.CoproDrMario__DOT__DO));
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0x11U;
                    } else if ((4U == (0xfU & (IData)(vlSelfRef.CoproDrMario__DOT__DO)))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__node_leaf = 1U;
                        vlSelfRef.CoproDrMario__DOT__lev_legal = 0U;
                        __Vdly__CoproDrMario__DOT__lev_rvc = 0U;
                        __Vdly__CoproDrMario__DOT__lev_rvv = 0U;
                        vlSelfRef.CoproDrMario__DOT__lev_imm = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[0U] = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[1U] = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[2U] = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[3U] = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__anyclear = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0x12U;
                    }
                }
            } else if ((0x11U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp2 = 0U;
                __Vdly__CoproDrMario__DOT__leafeval__DOT__cpw_p = 0U;
                __Vdly__CoproDrMario__DOT__leafeval__DOT__sr_addr 
                    = ((IData)(vlSelfRef.CoproDrMario__DOT__lev_a_sl) 
                       << 7U);
                if ((2U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__cmd_l))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0x1cU;
                } else {
                    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sl_cpw = 1U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0x1bU;
                }
            } else if ((0x1cU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                __Vdly__CoproDrMario__DOT__leafeval__DOT__sr_addr 
                    = (0x1ffU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sr_addr)));
                __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0x1aU;
            } else if ((0x1aU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                __Vdly__CoproDrMario__DOT__leafeval__DOT__sr_addr 
                    = (0x1ffU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sr_addr)));
                __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v1 
                    = (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sl_qb));
                __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v1 
                    = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp2;
                __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v1 = 1U;
                if ((0x7fU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp2))) {
                    vlSelfRef.CoproDrMario__DOT__lev_done = 1U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0U;
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp2 
                        = (0x7fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp2)));
                }
            } else if ((0x1bU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                if ((0x7fU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__cpw_p))) {
                    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sl_cpw = 0U;
                    vlSelfRef.CoproDrMario__DOT__lev_done = 1U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0U;
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__cpw_p 
                        = (0x7fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__cpw_p)));
                }
            } else if ((0x12U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                if (((0x10U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp)) 
                     | vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of
                     [((0x78U & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp) 
                                 << 3U)) | (IData)(vlSelfRef.CoproDrMario__DOT__lev_a_col))])) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__fo1 
                        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp;
                    if ((2U & (IData)(vlSelfRef.CoproDrMario__DOT__lev_a_o4))) {
                        if ((7U == (IData)(vlSelfRef.CoproDrMario__DOT__lev_a_col))) {
                            vlSelfRef.CoproDrMario__DOT__lev_done = 1U;
                            __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0U;
                        } else {
                            __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0x13U;
                        }
                    } else if ((2U <= (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__off_b 
                            = ((0x78U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp) 
                                          - (IData)(1U)) 
                                         << 3U)) | (IData)(vlSelfRef.CoproDrMario__DOT__lev_a_col));
                        vlSelfRef.CoproDrMario__DOT__lev_legal = 1U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0x14U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__off_a 
                            = ((0x78U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp) 
                                          - (IData)(2U)) 
                                         << 3U)) | (IData)(vlSelfRef.CoproDrMario__DOT__lev_a_col));
                    } else {
                        vlSelfRef.CoproDrMario__DOT__lev_done = 1U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0U;
                    }
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp = 0U;
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp 
                        = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp)));
                }
            } else if ((0x13U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                if (((0x10U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp)) 
                     | vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of
                     [((0x78U & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp) 
                                 << 3U)) | (7U & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.CoproDrMario__DOT__lev_a_col))))])) {
                    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fo2b__DOT__fom 
                        = (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fo1) 
                            < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp))
                            ? (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fo1)
                            : (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp));
                    if ((1U <= (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fo2b__DOT__fom))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__off_a 
                            = ((0x78U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fo2b__DOT__fom) 
                                          - (IData)(1U)) 
                                         << 3U)) | (IData)(vlSelfRef.CoproDrMario__DOT__lev_a_col));
                        vlSelfRef.CoproDrMario__DOT__lev_legal = 1U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0x14U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__off_b 
                            = ((0x78U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fo2b__DOT__fom) 
                                          - (IData)(1U)) 
                                         << 3U)) | 
                               (7U & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__lev_a_col))));
                    } else {
                        vlSelfRef.CoproDrMario__DOT__lev_done = 1U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0U;
                    }
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp 
                        = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp)));
                }
            } else {
                if ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__lev_a_o4))) {
                    __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v2 
                        = vlSelfRef.CoproDrMario__DOT__lev_a_cb;
                    __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v3 
                        = vlSelfRef.CoproDrMario__DOT__lev_a_ca;
                } else {
                    __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v2 
                        = vlSelfRef.CoproDrMario__DOT__lev_a_ca;
                    __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v3 
                        = vlSelfRef.CoproDrMario__DOT__lev_a_cb;
                }
                __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v2 
                    = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__off_a;
                __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v2 = 1U;
                __Vdly__CoproDrMario__DOT__leafeval__DOT__li = 0U;
                __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0x15U;
                __Vdly__CoproDrMario__DOT__leafeval__DOT__sstep = 1U;
                __Vdly__CoproDrMario__DOT__leafeval__DOT__scnt = 8U;
                __Vdly__CoproDrMario__DOT__leafeval__DOT__srun = 0U;
                __Vdly__CoproDrMario__DOT__leafeval__DOT__smcol = 0U;
                __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v3 
                    = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__off_b;
                __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v3 = 1U;
                __Vdly__CoproDrMario__DOT__leafeval__DOT__soff 
                    = (0x78U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__off_a));
            }
        } else if (((((((((0x15U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st)) 
                          | (0x16U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) 
                         | (0x17U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) 
                        | (0x18U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) 
                       | (0x19U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) 
                      | (1U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) 
                     | (2U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) 
                    | (3U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st)))) {
            if ((0x15U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                vlSelfRef.CoproDrMario__DOT__leafeval__DOT__scan__DOT__c_ 
                    = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                    [(0x7fU & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__soff))];
                vlSelfRef.CoproDrMario__DOT__leafeval__DOT__scan__DOT__brk 
                    = ((0U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__scan__DOT__c_)) 
                       | ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__scan__DOT__c_) 
                          != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__smcol)));
                if (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__scan__DOT__brk) 
                     & (4U <= (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun)))) {
                    if ((0U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart))));
                    }
                    if ((1U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep)) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep)) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep)))));
                    }
                    if ((2U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep), 1U)) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep), 1U)) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep), 1U)))));
                    }
                    if ((3U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(3U) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(3U) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(3U) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((4U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep), 2U)) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep), 2U)) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep), 2U)))));
                    }
                    if ((5U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(5U) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(5U) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(5U) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((6U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(6U) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(6U) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(6U) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((7U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(7U) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(7U) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(7U) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((8U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep), 3U)) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep), 3U)) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep), 3U)))));
                    }
                    if ((9U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(9U) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(9U) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(9U) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((0xaU < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(0xaU) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(0xaU) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xaU) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((0xbU < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(0xbU) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(0xbU) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xbU) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((0xcU < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(0xcU) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(0xcU) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xcU) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((0xdU < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(0xdU) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(0xdU) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xdU) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((0xeU < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(0xeU) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(0xeU) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xeU) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((0xfU < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(0xfU) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(0xfU) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xfU) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                }
                if ((0U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__scan__DOT__c_))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__srun = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__smcol = 0U;
                } else if (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__scan__DOT__c_) 
                            != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__smcol))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__smcol 
                        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__scan__DOT__c_;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__srstart 
                        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__soff;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__srun = 1U;
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__srun 
                        = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun)));
                }
                if ((1U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__scnt))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0x16U;
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__soff 
                        = (0xffU & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__soff) 
                                    + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep)));
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__scnt 
                        = (0x1fU & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__scnt) 
                                    - (IData)(1U)));
                }
            } else if ((0x16U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                if ((4U <= (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                    if ((0U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart))));
                    }
                    if ((1U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep)) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep)) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep)))));
                    }
                    if ((2U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep), 1U)) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep), 1U)) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep), 1U)))));
                    }
                    if ((3U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(3U) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(3U) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(3U) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((4U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep), 2U)) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep), 2U)) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep), 2U)))));
                    }
                    if ((5U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(5U) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(5U) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(5U) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((6U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(6U) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(6U) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(6U) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((7U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(7U) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(7U) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(7U) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((8U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep), 3U)) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep), 3U)) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      VL_SHIFTL_III(7,32,32, (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep), 3U)))));
                    }
                    if ((9U < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(9U) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(9U) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(9U) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((0xaU < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(0xaU) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(0xaU) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xaU) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((0xbU < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(0xbU) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(0xbU) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xbU) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((0xcU < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(0xcU) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(0xcU) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xcU) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((0xdU < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(0xdU) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(0xdU) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xdU) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((0xeU < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(0xeU) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(0xeU) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xeU) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                    if ((0xfU < (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[(3U 
                                                                         & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                                             + 
                                                                             ((IData)(0xfU) 
                                                                              * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                                                            >> 5U))] 
                            = (__Vdly__CoproDrMario__DOT__leafeval__DOT__markb[
                               (3U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                       + ((IData)(0xfU) 
                                          * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))) 
                                      >> 5U))] | ((IData)(1U) 
                                                  << 
                                                  (0x1fU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart) 
                                                      + 
                                                      ((IData)(0xfU) 
                                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep))))));
                    }
                }
                __Vdly__CoproDrMario__DOT__leafeval__DOT__smcol = 0U;
                __Vdly__CoproDrMario__DOT__leafeval__DOT__srun = 0U;
                if ((0U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__li))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__soff 
                        = (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__off_a));
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__sstep = 8U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__scnt = 0x10U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__li = 1U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0x15U;
                } else if ((1U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__li))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__soff 
                        = (0x78U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__off_b));
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__sstep = 1U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__scnt = 8U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__li = 2U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0x15U;
                } else if ((2U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__li))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__soff 
                        = (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__off_b));
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__sstep = 8U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__scnt = 0x10U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__li = 3U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0x15U;
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp2 = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0x17U;
                }
            } else if ((0x17U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                if ((1U & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__markb[
                           ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp2) 
                            >> 5U)] >> (0x1fU & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp2))))) {
                    __Vdly__CoproDrMario__DOT__lev_rvc 
                        = (0x3fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__lev_rvc)));
                    if (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of
                        [vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp2]) {
                        __Vdly__CoproDrMario__DOT__lev_rvv 
                            = (0xfU & ((IData)(1U) 
                                       + (IData)(vlSelfRef.CoproDrMario__DOT__lev_rvv)));
                    }
                    __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v4 
                        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp2;
                    __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v4 = 1U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__anyclear = 1U;
                }
                if ((0x7fU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp2))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__wc = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__gdest = 0xfU;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp = 0xfU;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st 
                        = (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__anyclear) 
                            | (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__markb[3U] 
                               >> 0x1fU)) ? 0x18U : 0x19U);
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp2 
                        = (0x7fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp2)));
                }
            } else if ((0x18U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                vlSelfRef.CoproDrMario__DOT__leafeval__DOT__grv__DOT__t 
                    = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                    [((0x78U & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp) 
                                << 3U)) | (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))];
                if ((0U != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__grv__DOT__t))) {
                    if ((4U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__grv__DOT__t))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__gdest 
                            = (0x1fU & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp) 
                                        - (IData)(1U)));
                    } else {
                        if (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__gdest) 
                             != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp))) {
                            __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v5 
                                = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__grv__DOT__t;
                            __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v5 
                                = ((0x78U & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__gdest) 
                                             << 3U)) 
                                   | (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)));
                            __VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v5 = 1U;
                            __VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v6 
                                = ((0x78U & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp) 
                                             << 3U)) 
                                   | (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)));
                        }
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__gdest 
                            = (0x1fU & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__gdest) 
                                        - (IData)(1U)));
                    }
                }
                if ((0U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp))) {
                    if ((7U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0x19U;
                    } else {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__wc 
                            = (0xfU & ((IData)(1U) 
                                       + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)));
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__gdest = 0xfU;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp = 0xfU;
                    }
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp 
                        = (0x1fU & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp) 
                                    - (IData)(1U)));
                }
            } else if ((0x19U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                vlSelfRef.CoproDrMario__DOT__lev_imm 
                    = (0xffffU & (((IData)(0xb4U) * (IData)(vlSelfRef.CoproDrMario__DOT__lev_rvv)) 
                                  + ((IData)(0xaU) 
                                     * (IData)(vlSelfRef.CoproDrMario__DOT__lev_rvc))));
                if (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__node_leaf) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__maxh = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__holes = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__toprisk = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__spawn = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__setup = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__pollution = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__buried = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__rdy_ext = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__vrdy = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__anyvir = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__wc = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__wr_ = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__seen = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__fillcnt = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 1U;
                } else {
                    vlSelfRef.CoproDrMario__DOT__lev_done = 1U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0U;
                }
            } else if ((1U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                if (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of
                    [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                       << 3U) | (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))]) {
                    if ((1U & (~ (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__seen)))) {
                        if (((0x1fU & ((IData)(0x10U) 
                                       - (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_))) 
                             > (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__maxh))) {
                            __Vdly__CoproDrMario__DOT__leafeval__DOT__maxh 
                                = (0x1fU & ((IData)(0x10U) 
                                            - (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_)));
                        }
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__seen = 1U;
                    }
                    if (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of
                        [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                           << 3U) | (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))]) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__buried 
                            = (0x3ffU & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__buried) 
                                         + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fillcnt)));
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__anyvir = 1U;
                    }
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__fillcnt 
                        = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fillcnt)));
                    if ((3U > (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__toprisk 
                            = (0xffU & ((IData)(1U) 
                                        + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__toprisk)));
                    }
                    if (((4U > (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_)) 
                         & ((3U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)) 
                            | (4U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc))))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__spawn 
                            = (0xffU & ((IData)(1U) 
                                        + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__spawn)));
                    }
                } else if (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__seen) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__holes 
                        = (0xffU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__holes)));
                }
                if ((0xfU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__wr_ = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__seen = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__fillcnt = 0U;
                    if ((7U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc))) {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__vo = 0U;
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 2U;
                    } else {
                        __Vdly__CoproDrMario__DOT__leafeval__DOT__wc 
                            = (0xfU & ((IData)(1U) 
                                       + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)));
                    }
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__wr_ 
                        = (0xfU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_)));
                }
            } else if ((2U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                if (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of
                    [vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vo]) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__run_h = 1U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__run_v = 1U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__p 
                        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_c;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 3U;
                } else if ((0x7fU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vo))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__wc = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__wr_ = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0xeU;
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__vo 
                        = (0x7fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vo)));
                }
            } else if ((((0U != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p)) 
                         & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                            [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_r) 
                               << 3U) | (7U & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p) 
                                               - (IData)(1U))))] 
                            == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_col))) 
                        & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of
                        [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_r) 
                           << 3U) | (7U & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p) 
                                           - (IData)(1U))))])) {
                __Vdly__CoproDrMario__DOT__leafeval__DOT__run_h 
                    = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__run_h)));
                __Vdly__CoproDrMario__DOT__leafeval__DOT__p 
                    = (0x1fU & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p) 
                                - (IData)(1U)));
            } else {
                __Vdly__CoproDrMario__DOT__leafeval__DOT__span_lo 
                    = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p;
                __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 4U;
            }
        } else if (((((((((4U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st)) 
                          | (5U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) 
                         | (6U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) 
                        | (7U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) 
                       | (8U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) 
                      | (9U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) 
                     | (0xaU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) 
                    | (0xbU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st)))) {
            if ((4U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                if (((0U != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__span_lo)) 
                     & ((~ vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of
                         [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_r) 
                            << 3U) | (7U & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__span_lo) 
                                            - (IData)(1U))))]) 
                        | (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                           [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_r) 
                              << 3U) | (7U & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__span_lo) 
                                              - (IData)(1U))))] 
                           == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_col))))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__span_lo 
                        = (0x1fU & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__span_lo) 
                                    - (IData)(1U)));
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__p 
                        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_c;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 5U;
                }
            } else if ((5U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                if ((((7U != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p)) 
                      & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of
                      [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_r) 
                         << 3U) | (7U & ((IData)(1U) 
                                         + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p))))]) 
                     & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                        [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_r) 
                           << 3U) | (7U & ((IData)(1U) 
                                           + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p))))] 
                        == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_col)))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__run_h 
                        = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__run_h)));
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__p 
                        = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p)));
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__span_hi 
                        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 6U;
                }
            } else if ((6U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                if (((7U != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__span_hi)) 
                     & ((~ vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of
                         [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_r) 
                            << 3U) | (7U & ((IData)(1U) 
                                            + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__span_hi))))]) 
                        | (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                           [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_r) 
                              << 3U) | (7U & ((IData)(1U) 
                                              + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__span_hi))))] 
                           == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_col))))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__span_hi 
                        = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__span_hi)));
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__p 
                        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_r;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 7U;
                }
            } else if ((7U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                if ((((0U != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p)) 
                      & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of
                      [((0x78U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p) 
                                   - (IData)(1U)) << 3U)) 
                        | (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_c))]) 
                     & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                        [((0x78U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p) 
                                     - (IData)(1U)) 
                                    << 3U)) | (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_c))] 
                        == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_col)))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__run_v 
                        = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__run_v)));
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__p 
                        = (0x1fU & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p) 
                                    - (IData)(1U)));
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__vspan_lo 
                        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 8U;
                }
            } else if ((8U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                if (((0U != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vspan_lo)) 
                     & ((~ vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of
                         [((0x78U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vspan_lo) 
                                      - (IData)(1U)) 
                                     << 3U)) | (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_c))]) 
                        | (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                           [((0x78U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vspan_lo) 
                                        - (IData)(1U)) 
                                       << 3U)) | (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_c))] 
                           == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_col))))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__vspan_lo 
                        = (0x1fU & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vspan_lo) 
                                    - (IData)(1U)));
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__p 
                        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_r;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 9U;
                }
            } else if ((9U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                if ((((0xfU != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p)) 
                      & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of
                      [((0x78U & (((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p)) 
                                  << 3U)) | (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_c))]) 
                     & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                        [((0x78U & (((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p)) 
                                    << 3U)) | (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_c))] 
                        == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_col)))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__run_v 
                        = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__run_v)));
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__p 
                        = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p)));
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__vspan_hi 
                        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0xaU;
                }
            } else if ((0xaU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
                if (((0xfU != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vspan_hi)) 
                     & ((~ vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of
                         [((0x78U & (((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vspan_hi)) 
                                     << 3U)) | (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_c))]) 
                        | (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                           [((0x78U & (((IData)(1U) 
                                        + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vspan_hi)) 
                                       << 3U)) | (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_c))] 
                           == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_col))))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__vspan_hi 
                        = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vspan_hi)));
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__p = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0xbU;
                }
            } else {
                if ((((((7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p)) 
                        != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_c)) 
                       & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of
                       [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_r) 
                          << 3U) | (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p)))]) 
                      & (~ vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of
                         [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_r) 
                            << 3U) | (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p)))])) 
                     & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                        [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_r) 
                           << 3U) | (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p)))] 
                        != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_col)))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__pollution 
                        = (0x7ffU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__pollution)));
                }
                if ((7U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__p = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0xcU;
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__p 
                        = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p)));
                }
            }
        } else if ((0xcU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
            if ((((((0xfU & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p)) 
                    != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_r)) 
                   & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of
                   [((0x78U & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p) 
                               << 3U)) | (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_c))]) 
                  & (~ vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of
                     [((0x78U & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p) 
                                 << 3U)) | (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_c))])) 
                 & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                    [((0x78U & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p) 
                                << 3U)) | (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_c))] 
                    != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_col)))) {
                __Vdly__CoproDrMario__DOT__leafeval__DOT__pollution 
                    = (0x7ffU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__pollution)));
            }
            if ((0xfU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p))) {
                __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0xdU;
            } else {
                __Vdly__CoproDrMario__DOT__leafeval__DOT__p 
                    = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p)));
            }
        } else if ((0xdU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
            vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fin__DOT__hq 
                = ((4U <= (0x1fU & ((IData)(1U) + ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__span_hi) 
                                                   - (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__span_lo)))))
                    ? ([&]() {
                        __Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__3__n 
                            = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__run_h;
                        __Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__3__Vfuncout 
                            = (0x1ffU & ((IData)(__Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__3__n) 
                                         * (IData)(__Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__3__n)));
                    }(), (IData)(__Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__3__Vfuncout))
                    : 0U);
            vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fin__DOT__vq 
                = ((4U <= (0x1fU & ((IData)(1U) + ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vspan_hi) 
                                                   - (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vspan_lo)))))
                    ? ([&]() {
                        __Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__4__n 
                            = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__run_v;
                        __Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__4__Vfuncout 
                            = (0x1ffU & ((IData)(__Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__4__n) 
                                         * (IData)(__Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__4__n)));
                    }(), (IData)(__Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__4__Vfuncout))
                    : 0U);
            if ((0x7fU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vo))) {
                __Vdly__CoproDrMario__DOT__leafeval__DOT__wc = 0U;
                __Vdly__CoproDrMario__DOT__leafeval__DOT__wr_ = 0U;
                __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0xeU;
            } else {
                __Vdly__CoproDrMario__DOT__leafeval__DOT__vo 
                    = (0x7fU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vo)));
                __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 2U;
            }
            vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fin__DOT__mx 
                = (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fin__DOT__hq) 
                    > (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fin__DOT__vq))
                    ? (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fin__DOT__hq)
                    : (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fin__DOT__vq));
            __Vdly__CoproDrMario__DOT__leafeval__DOT__rdy_ext 
                = (0xffffU & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__rdy_ext) 
                              + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fin__DOT__mx)));
            __Vdly__CoproDrMario__DOT__leafeval__DOT__vrdy 
                = (0xffffU & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vrdy) 
                              + VL_EXTEND_II(16,9, 
                                             ([&]() {
                                __Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__5__n 
                                    = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__run_v;
                                __Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__5__Vfuncout 
                                    = (0x1ffU & ((IData)(__Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__5__n) 
                                                 * (IData)(__Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__5__n)));
                            }(), (IData)(__Vfunc_CoproDrMario__DOT__leafeval__DOT__sq__5__Vfuncout)))));
        } else if ((0xeU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
            vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suh__DOT__c0 
                = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                   << 3U) | (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))];
            if ((((0U != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suh__DOT__c0)) 
                  & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                     [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                        << 3U) | (7U & ((IData)(1U) 
                                        + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc))))] 
                     == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suh__DOT__c0))) 
                 & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                    [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                       << 3U) | (7U & ((IData)(2U) 
                                       + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc))))] 
                    == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suh__DOT__c0)))) {
                vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suh__DOT__t 
                    = (((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of
                         [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                            << 3U) | (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))] 
                         & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                            [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                               << 3U) | (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))] 
                            == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suh__DOT__c0))) 
                        | (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of
                           [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                              << 3U) | (7U & ((IData)(1U) 
                                              + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc))))] 
                           & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                              [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                                 << 3U) | (7U & ((IData)(1U) 
                                                 + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc))))] 
                              == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suh__DOT__c0)))) 
                       | (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of
                          [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                             << 3U) | (7U & ((IData)(2U) 
                                             + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc))))] 
                          & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                             [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                                << 3U) | (7U & ((IData)(2U) 
                                                + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc))))] 
                             == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suh__DOT__c0))));
                if (((~ (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suh__DOT__t)) 
                     & (0U != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))) {
                    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suh__DOT__t 
                        = (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of
                           [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                              << 3U) | (7U & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc) 
                                              - (IData)(1U))))] 
                           & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                              [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                                 << 3U) | (7U & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc) 
                                                 - (IData)(1U))))] 
                              == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suh__DOT__c0)));
                }
                if (((~ (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suh__DOT__t)) 
                     & (5U > (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))) {
                    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suh__DOT__t 
                        = (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of
                           [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                              << 3U) | (7U & ((IData)(3U) 
                                              + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc))))] 
                           & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                              [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                                 << 3U) | (7U & ((IData)(3U) 
                                                 + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc))))] 
                              == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suh__DOT__c0)));
                }
                if (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suh__DOT__t) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__setup 
                        = (0xffU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__setup)));
                }
            }
            if ((5U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc))) {
                __Vdly__CoproDrMario__DOT__leafeval__DOT__wc = 0U;
                if ((0xfU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__wr_ = 0U;
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0xfU;
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__wr_ 
                        = (0xfU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_)));
                }
            } else {
                __Vdly__CoproDrMario__DOT__leafeval__DOT__wc 
                    = (0xfU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)));
            }
        } else if ((0xfU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
            vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suv__DOT__c0 
                = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                   << 3U) | (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))];
            if ((((0U != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suv__DOT__c0)) 
                  & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                     [((0x78U & (((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_)) 
                                 << 3U)) | (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))] 
                     == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suv__DOT__c0))) 
                 & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                    [((0x78U & (((IData)(2U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_)) 
                                << 3U)) | (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))] 
                    == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suv__DOT__c0)))) {
                vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suv__DOT__t 
                    = (((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of
                         [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                            << 3U) | (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))] 
                         & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                            [(((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                               << 3U) | (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))] 
                            == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suv__DOT__c0))) 
                        | (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of
                           [((0x78U & (((IData)(1U) 
                                        + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_)) 
                                       << 3U)) | (7U 
                                                  & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))] 
                           & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                              [((0x78U & (((IData)(1U) 
                                           + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_)) 
                                          << 3U)) | 
                                (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))] 
                              == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suv__DOT__c0)))) 
                       | (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of
                          [((0x78U & (((IData)(2U) 
                                       + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_)) 
                                      << 3U)) | (7U 
                                                 & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))] 
                          & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                             [((0x78U & (((IData)(2U) 
                                          + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_)) 
                                         << 3U)) | 
                               (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))] 
                             == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suv__DOT__c0))));
                if (((~ (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suv__DOT__t)) 
                     & (0U != (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_)))) {
                    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suv__DOT__t 
                        = (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of
                           [((0x78U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                                        - (IData)(1U)) 
                                       << 3U)) | (7U 
                                                  & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))] 
                           & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                              [((0x78U & (((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_) 
                                           - (IData)(1U)) 
                                          << 3U)) | 
                                (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))] 
                              == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suv__DOT__c0)));
                }
                if (((~ (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suv__DOT__t)) 
                     & (0xdU > (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_)))) {
                    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suv__DOT__t 
                        = (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of
                           [((0x78U & (((IData)(3U) 
                                        + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_)) 
                                       << 3U)) | (7U 
                                                  & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))] 
                           & (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
                              [((0x78U & (((IData)(3U) 
                                           + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_)) 
                                          << 3U)) | 
                                (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)))] 
                              == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suv__DOT__c0)));
                }
                if (vlSelfRef.CoproDrMario__DOT__leafeval__DOT__suv__DOT__t) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__setup 
                        = (0xffU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__setup)));
                }
            }
            if ((0xdU == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_))) {
                __Vdly__CoproDrMario__DOT__leafeval__DOT__wr_ = 0U;
                if ((7U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc))) {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0x10U;
                } else {
                    __Vdly__CoproDrMario__DOT__leafeval__DOT__wc 
                        = (0xfU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc)));
                }
            } else {
                __Vdly__CoproDrMario__DOT__leafeval__DOT__wr_ 
                    = (0xfU & ((IData)(1U) + (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_)));
            }
        } else if ((0x10U == (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st))) {
            vlSelfRef.CoproDrMario__DOT__lev_sco = 
                (0xffffU & ((((((((((IData)(0x1388U) 
                                    - ((IData)(0xcU) 
                                       * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__maxh))) 
                                   - ((IData)(0x14U) 
                                      * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__holes))) 
                                  - ((IData)(0x5aU) 
                                     * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__toprisk))) 
                                 - ((IData)(0x96U) 
                                    * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__spawn))) 
                                + ((IData)(0x3cU) * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__setup))) 
                               - ((IData)(0x1eU) * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__buried))) 
                              + ((IData)(0xcU) * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__rdy_ext))) 
                             + ((IData)(0xcU) * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vrdy))) 
                            - ((IData)(6U) * (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__pollution))));
            vlSelfRef.CoproDrMario__DOT__lev_win = 
                (1U & (~ (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__anyvir)));
            vlSelfRef.CoproDrMario__DOT__lev_done = 1U;
            __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0U;
        } else {
            __Vdly__CoproDrMario__DOT__leafeval__DOT__st = 0U;
        }
    }
    if ((0x27U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__D 
            = (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__DI) 
                     >> 3U));
    } else if ((0xcU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        if (vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__sed) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__D = 1U;
        }
        if (vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__cld) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__D = 0U;
        }
        if (vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__plp) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__D 
                = (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD) 
                         >> 3U));
        }
    }
    if ((0xcU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__sed 
            = (0xf8U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__cld 
            = (0xd8U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__plp 
            = (0x28U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR));
    }
    if (((0xcU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)) 
         | (8U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)))) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__adc_sbc 
            = (0x61U == (0x63U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)));
    }
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__st 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__st;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__maxh 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__maxh;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__holes 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__holes;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__toprisk 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__toprisk;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__spawn 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__spawn;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__setup 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__setup;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__pollution 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__pollution;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__buried 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__buried;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__rdy_ext 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__rdy_ext;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vrdy 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__vrdy;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__anyvir 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__anyvir;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wc 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__wc;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__wr_ 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__wr_;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__seen 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__seen;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fillcnt 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__fillcnt;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__cmd_l 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__cmd_l;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__node_leaf 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__node_leaf;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__markb[0U] 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[0U];
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__markb[1U] 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[1U];
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__markb[2U] 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[2U];
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__markb[3U] 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__markb[3U];
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__anyclear 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__anyclear;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fwp2 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__fwp2;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__fo1 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__fo1;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__off_b 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__off_b;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__off_a 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__off_a;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__li 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__li;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sstep 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__sstep;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__scnt 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__scnt;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srun 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__srun;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__smcol 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__smcol;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__soff 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__soff;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__srstart 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__srstart;
    vlSelfRef.CoproDrMario__DOT__lev_rvc = __Vdly__CoproDrMario__DOT__lev_rvc;
    vlSelfRef.CoproDrMario__DOT__lev_rvv = __Vdly__CoproDrMario__DOT__lev_rvv;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__gdest 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__gdest;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__run_h 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__run_h;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__run_v 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__run_v;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__p = __Vdly__CoproDrMario__DOT__leafeval__DOT__p;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__span_lo 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__span_lo;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__span_hi 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__span_hi;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vspan_lo 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__vspan_lo;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vspan_hi 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__vspan_hi;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__cpw_p 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__cpw_p;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vo 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__vo;
    if (__VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v0) {
        vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell[__VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v0] 
            = __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v0;
    }
    if (__VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v1) {
        vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell[__VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v1] 
            = __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v1;
    }
    if (__VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v2) {
        vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell[__VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v2] 
            = __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v2;
    }
    if (__VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v3) {
        vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell[__VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v3] 
            = __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v3;
    }
    if (__VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v4) {
        vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell[__VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v4] = 0U;
    }
    if (__VdlySet__CoproDrMario__DOT__leafeval__DOT__bcell__v5) {
        vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell[__VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v5] 
            = __VdlyVal__CoproDrMario__DOT__leafeval__DOT__bcell__v5;
        vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell[__VdlyDim0__CoproDrMario__DOT__leafeval__DOT__bcell__v6] = 0U;
    }
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_c 
        = (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vo));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_r 
        = (0xfU & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vo) 
                   >> 3U));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sl_qb 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__slotram__DOT__mem
        [vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sr_addr];
    if (vlSelfRef.CoproDrMario__DOT__lev_wr_arg) {
        if ((1U & (~ ((IData)(vlSelfRef.CoproDrMario__DOT__AB) 
                      >> 2U)))) {
            if ((2U & (IData)(vlSelfRef.CoproDrMario__DOT__AB))) {
                if ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__AB))) {
                    vlSelfRef.CoproDrMario__DOT__lev_a_cb 
                        = vlSelfRef.CoproDrMario__DOT__lev_colenc;
                }
                if ((1U & (~ (IData)(vlSelfRef.CoproDrMario__DOT__AB)))) {
                    vlSelfRef.CoproDrMario__DOT__lev_a_ca 
                        = vlSelfRef.CoproDrMario__DOT__lev_colenc;
                }
            }
            if ((1U & (~ ((IData)(vlSelfRef.CoproDrMario__DOT__AB) 
                          >> 1U)))) {
                if ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__AB))) {
                    vlSelfRef.CoproDrMario__DOT__lev_a_col 
                        = (7U & (IData)(vlSelfRef.CoproDrMario__DOT__DO));
                }
                if ((1U & (~ (IData)(vlSelfRef.CoproDrMario__DOT__AB)))) {
                    vlSelfRef.CoproDrMario__DOT__lev_a_o4 
                        = (3U & (IData)(vlSelfRef.CoproDrMario__DOT__DO));
                }
            }
        }
        if ((4U & (IData)(vlSelfRef.CoproDrMario__DOT__AB))) {
            vlSelfRef.CoproDrMario__DOT__lev_a_sl = 
                (3U & (IData)(vlSelfRef.CoproDrMario__DOT__DO));
        }
    }
    if ((((IData)(vlSelfRef.CoproDrMario__DOT__WE) 
          & (~ (IData)(vlSelfRef.CoproDrMario__DOT__cpu_rst))) 
         & (0x70f3U == (IData)(vlSelfRef.CoproDrMario__DOT__AB)))) {
        vlSelfRef.CoproDrMario__DOT__lev_wslot = (3U 
                                                  & (IData)(vlSelfRef.CoproDrMario__DOT__DO));
    }
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[1U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [1U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[2U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [2U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[3U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [3U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[4U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [4U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[5U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [5U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[6U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [6U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[7U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [7U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[8U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [8U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[9U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [9U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0xaU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0xaU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0xbU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0xbU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0xcU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0xcU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0xdU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0xdU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0xeU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0xeU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0xfU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0xfU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x10U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x10U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x11U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x11U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x12U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x12U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x13U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x13U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x14U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x14U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x15U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x15U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x16U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x16U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x17U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x17U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x18U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x18U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x19U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x19U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x1aU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x1aU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x1bU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x1bU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x1cU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x1cU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x1dU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x1dU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x1eU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x1eU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x1fU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x1fU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x20U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x20U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x21U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x21U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x22U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x22U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x23U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x23U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x24U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x24U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x25U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x25U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x26U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x26U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x27U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x27U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x28U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x28U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x29U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x29U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x2aU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x2aU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x2bU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x2bU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x2cU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x2cU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x2dU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x2dU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x2eU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x2eU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x2fU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x2fU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x30U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x30U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x31U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x31U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x32U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x32U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x33U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x33U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x34U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x34U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x35U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x35U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x36U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x36U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x37U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x37U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x38U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x38U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x39U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x39U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x3aU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x3aU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x3bU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x3bU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x3cU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x3cU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x3dU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x3dU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x3eU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x3eU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x3fU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x3fU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x40U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x40U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x41U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x41U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x42U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x42U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x43U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x43U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x44U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x44U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x45U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x45U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x46U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x46U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x47U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x47U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x48U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x48U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x49U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x49U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x4aU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x4aU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x4bU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x4bU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x4cU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x4cU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x4dU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x4dU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x4eU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x4eU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x4fU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x4fU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x50U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x50U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x51U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x51U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x52U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x52U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x53U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x53U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x54U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x54U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x55U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x55U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x56U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x56U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x57U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x57U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x58U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x58U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x59U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x59U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x5aU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x5aU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x5bU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x5bU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x5cU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x5cU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x5dU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x5dU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x5eU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x5eU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x5fU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x5fU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x60U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x60U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x61U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x61U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x62U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x62U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x63U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x63U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x64U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x64U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x65U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x65U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x66U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x66U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x67U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x67U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x68U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x68U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x69U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x69U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x6aU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x6aU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x6bU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x6bU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x6cU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x6cU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x6dU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x6dU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x6eU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x6eU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x6fU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x6fU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x70U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x70U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x71U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x71U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x72U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x72U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x73U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x73U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x74U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x74U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x75U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x75U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x76U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x76U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x77U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x77U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x78U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x78U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x79U] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x79U]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x7aU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x7aU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x7bU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x7bU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x7cU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x7cU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x7dU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x7dU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x7eU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x7eU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__occ_of[0x7fU] 
        = (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                  [0x7fU]));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                  [0U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[1U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [1U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                  [1U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[2U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [2U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                  [2U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[3U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [3U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                  [3U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[4U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [4U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                  [4U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[5U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [5U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                  [5U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[6U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [6U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                  [6U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[7U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [7U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                  [7U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[8U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [8U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                  [8U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[9U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [9U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                  [9U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0xaU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0xaU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                    [0xaU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0xbU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0xbU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                    [0xbU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0xcU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0xcU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                    [0xcU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0xdU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0xdU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                    [0xdU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0xeU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0xeU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                    [0xeU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0xfU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0xfU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                    [0xfU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x10U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x10U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x10U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x11U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x11U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x11U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x12U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x12U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x12U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x13U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x13U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x13U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x14U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x14U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x14U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x15U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x15U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x15U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x16U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x16U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x16U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x17U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x17U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x17U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x18U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x18U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x18U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x19U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x19U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x19U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x1aU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x1aU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x1aU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x1bU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x1bU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x1bU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x1cU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x1cU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x1cU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x1dU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x1dU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x1dU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x1eU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x1eU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x1eU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x1fU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x1fU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x1fU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x20U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x20U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x20U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x21U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x21U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x21U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x22U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x22U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x22U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x23U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x23U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x23U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x24U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x24U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x24U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x25U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x25U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x25U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x26U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x26U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x26U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x27U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x27U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x27U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x28U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x28U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x28U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x29U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x29U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x29U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x2aU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x2aU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x2aU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x2bU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x2bU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x2bU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x2cU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x2cU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x2cU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x2dU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x2dU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x2dU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x2eU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x2eU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x2eU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x2fU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x2fU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x2fU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x30U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x30U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x30U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x31U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x31U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x31U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x32U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x32U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x32U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x33U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x33U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x33U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x34U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x34U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x34U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x35U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x35U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x35U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x36U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x36U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x36U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x37U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x37U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x37U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x38U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x38U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x38U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x39U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x39U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x39U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x3aU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x3aU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x3aU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x3bU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x3bU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x3bU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x3cU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x3cU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x3cU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x3dU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x3dU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x3dU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x3eU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x3eU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x3eU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x3fU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x3fU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x3fU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x40U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x40U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x40U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x41U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x41U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x41U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x42U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x42U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x42U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x43U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x43U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x43U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x44U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x44U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x44U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x45U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x45U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x45U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x46U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x46U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x46U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x47U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x47U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x47U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x48U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x48U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x48U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x49U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x49U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x49U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x4aU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x4aU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x4aU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x4bU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x4bU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x4bU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x4cU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x4cU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x4cU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x4dU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x4dU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x4dU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x4eU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x4eU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x4eU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x4fU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x4fU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x4fU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x50U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x50U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x50U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x51U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x51U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x51U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x52U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x52U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x52U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x53U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x53U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x53U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x54U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x54U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x54U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x55U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x55U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x55U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x56U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x56U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x56U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x57U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x57U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x57U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x58U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x58U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x58U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x59U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x59U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x59U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x5aU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x5aU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x5aU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x5bU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x5bU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x5bU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x5cU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x5cU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x5cU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x5dU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x5dU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x5dU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x5eU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x5eU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x5eU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x5fU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x5fU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x5fU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x60U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x60U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x60U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x61U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x61U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x61U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x62U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x62U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x62U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x63U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x63U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x63U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x64U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x64U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x64U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x65U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x65U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x65U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x66U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x66U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x66U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x67U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x67U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x67U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x68U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x68U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x68U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x69U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x69U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x69U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x6aU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x6aU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x6aU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x6bU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x6bU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x6bU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x6cU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x6cU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x6cU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x6dU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x6dU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x6dU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x6eU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x6eU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x6eU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x6fU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x6fU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x6fU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x70U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x70U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x70U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x71U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x71U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x71U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x72U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x72U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x72U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x73U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x73U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x73U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x74U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x74U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x74U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x75U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x75U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x75U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x76U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x76U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x76U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x77U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x77U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x77U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x78U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x78U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x78U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x79U] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x79U] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x79U])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x7aU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x7aU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x7aU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x7bU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x7bU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x7bU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x7cU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x7cU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x7cU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x7dU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x7dU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x7dU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x7eU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x7eU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x7eU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vir_of[0x7fU] 
        = ((vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
            [0x7fU] >> 2U) & (0U != (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
                                     [0x7fU])));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[1U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [1U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[2U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [2U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[3U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [3U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[4U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [4U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[5U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [5U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[6U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [6U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[7U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [7U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[8U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [8U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[9U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [9U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0xaU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0xaU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0xbU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0xbU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0xcU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0xcU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0xdU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0xdU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0xeU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0xeU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0xfU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0xfU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x10U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x10U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x11U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x11U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x12U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x12U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x13U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x13U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x14U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x14U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x15U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x15U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x16U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x16U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x17U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x17U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x18U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x18U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x19U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x19U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x1aU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x1aU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x1bU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x1bU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x1cU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x1cU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x1dU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x1dU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x1eU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x1eU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x1fU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x1fU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x20U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x20U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x21U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x21U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x22U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x22U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x23U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x23U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x24U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x24U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x25U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x25U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x26U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x26U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x27U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x27U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x28U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x28U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x29U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x29U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x2aU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x2aU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x2bU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x2bU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x2cU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x2cU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x2dU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x2dU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x2eU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x2eU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x2fU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x2fU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x30U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x30U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x31U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x31U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x32U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x32U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x33U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x33U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x34U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x34U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x35U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x35U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x36U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x36U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x37U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x37U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x38U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x38U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x39U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x39U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x3aU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x3aU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x3bU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x3bU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x3cU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x3cU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x3dU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x3dU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x3eU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x3eU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x3fU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x3fU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x40U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x40U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x41U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x41U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x42U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x42U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x43U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x43U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x44U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x44U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x45U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x45U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x46U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x46U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x47U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x47U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x48U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x48U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x49U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x49U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x4aU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x4aU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x4bU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x4bU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x4cU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x4cU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x4dU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x4dU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x4eU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x4eU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x4fU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x4fU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x50U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x50U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x51U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x51U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x52U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x52U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x53U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x53U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x54U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x54U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x55U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x55U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x56U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x56U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x57U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x57U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x58U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x58U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x59U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x59U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x5aU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x5aU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x5bU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x5bU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x5cU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x5cU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x5dU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x5dU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x5eU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x5eU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x5fU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x5fU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x60U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x60U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x61U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x61U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x62U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x62U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x63U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x63U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x64U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x64U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x65U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x65U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x66U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x66U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x67U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x67U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x68U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x68U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x69U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x69U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x6aU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x6aU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x6bU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x6bU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x6cU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x6cU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x6dU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x6dU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x6eU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x6eU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x6fU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x6fU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x70U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x70U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x71U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x71U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x72U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x72U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x73U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x73U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x74U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x74U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x75U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x75U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x76U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x76U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x77U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x77U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x78U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x78U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x79U] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x79U]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x7aU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x7aU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x7bU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x7bU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x7cU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x7cU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x7dU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x7dU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x7eU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x7eU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of[0x7fU] 
        = (3U & vlSelfRef.CoproDrMario__DOT__leafeval__DOT__bcell
           [0x7fU]);
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sr_addr 
        = __Vdly__CoproDrMario__DOT__leafeval__DOT__sr_addr;
    if (__VdlySet__CoproDrMario__DOT__leafeval__DOT__slotram__DOT__mem__v0) {
        vlSelfRef.CoproDrMario__DOT__leafeval__DOT__slotram__DOT__mem[__VdlyDim0__CoproDrMario__DOT__leafeval__DOT__slotram__DOT__mem__v0] 
            = __VdlyVal__CoproDrMario__DOT__leafeval__DOT__slotram__DOT__mem__v0;
    }
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_col 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
        [vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vo];
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__P = 
        (0x30U | ((((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__N) 
                    << 7U) | ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__V) 
                              << 6U)) | ((((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__D) 
                                           << 3U) | 
                                          ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__I) 
                                           << 2U)) 
                                         | (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__Z) 
                                             << 1U) 
                                            | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__C)))));
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD 
        = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp));
}

VL_INLINE_OPT void VCoproDrMario___024root___nba_sequent__TOP__3(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___nba_sequent__TOP__3\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vdly__CoproDrMario__DOT__cpu6502__DOT__state 
        = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state;
    if (vlSelfRef.CoproDrMario__DOT__cpu_rst) {
        vlSelfRef.__Vdly__CoproDrMario__DOT__cpu6502__DOT__state = 8U;
    } else if (((((((((0xcU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)) 
                      | (0x2fU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                     | (0x30U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                    | (0x31U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                   | (0U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                  | (1U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                 | (2U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                | (3U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)))) {
        if ((0xcU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
            if (((((((((0U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)) 
                       | (0x20U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                      | (0x2cU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                     | (0x40U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                    | (0x4cU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                   | (0x60U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                  | (0x6cU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                 | (8U == (0xbfU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))))) {
                vlSelfRef.__Vdly__CoproDrMario__DOT__cpu6502__DOT__state 
                    = ((0U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))
                        ? 8U : ((0x20U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))
                                 ? 0x1aU : ((0x2cU 
                                             == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))
                                             ? 0U : 
                                            ((0x40U 
                                              == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))
                                              ? 0x25U
                                              : ((0x4cU 
                                                  == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))
                                                  ? 0x16U
                                                  : 
                                                 ((0x60U 
                                                   == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))
                                                   ? 0x2aU
                                                   : 
                                                  ((0x6cU 
                                                    == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))
                                                    ? 0x18U
                                                    : 0x21U)))))));
            } else if (((((((((0x28U == (0xbfU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                              | (0x18U == (0x9fU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                             | (0x80U == (0x9dU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                            | (0x8cU == (0x9fU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                           | (0x88U == (0x8fU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                          | (1U == (0x1fU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                         | (4U == (0x1cU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                        | (9U == (0x1fU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))))) {
                vlSelfRef.__Vdly__CoproDrMario__DOT__cpu6502__DOT__state 
                    = ((0x28U == (0xbfU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))
                        ? 0x1eU : ((0x18U == (0x9fU 
                                              & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))
                                    ? 0x24U : ((0x80U 
                                                == 
                                                (0x9dU 
                                                 & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))
                                                ? 0xdU
                                                : (
                                                   (0x8cU 
                                                    == 
                                                    (0x9fU 
                                                     & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))
                                                    ? 0U
                                                    : 
                                                   ((0x88U 
                                                     == 
                                                     (0x8fU 
                                                      & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))
                                                     ? 0x24U
                                                     : 
                                                    ((1U 
                                                      == 
                                                      (0x1fU 
                                                       & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))
                                                      ? 0xeU
                                                      : 
                                                     ((4U 
                                                       == 
                                                       (0x1cU 
                                                        & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))
                                                       ? 0x2fU
                                                       : 0xdU)))))));
            } else if (((((((((0xdU == (0x1fU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
                              | (0xeU == (0x1fU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                             | (0x10U == (0x1fU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                            | (0x11U == (0x1fU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                           | (0x14U == (0x1cU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                          | (0x19U == (0x1fU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                         | (0x1cU == (0x1cU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))) 
                        | (0xaU == (0xfU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))))) {
                vlSelfRef.__Vdly__CoproDrMario__DOT__cpu6502__DOT__state 
                    = ((0xdU == (0x1fU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))
                        ? 0U : ((0xeU == (0x1fU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))
                                 ? 0U : ((0x10U == 
                                          (0x1fU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))
                                          ? 5U : ((0x11U 
                                                   == 
                                                   (0x1fU 
                                                    & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))
                                                   ? 0x12U
                                                   : 
                                                  ((0x14U 
                                                    == 
                                                    (0x1cU 
                                                     & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))
                                                    ? 0x30U
                                                    : 
                                                   ((0x19U 
                                                     == 
                                                     (0x1fU 
                                                      & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))
                                                     ? 2U
                                                     : 
                                                    ((0x1cU 
                                                      == 
                                                      (0x1cU 
                                                       & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR)))
                                                      ? 2U
                                                      : 0x24U)))))));
            }
        } else {
            vlSelfRef.__Vdly__CoproDrMario__DOT__cpu6502__DOT__state 
                = ((0x2fU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                    ? ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__write_back)
                        ? 0x23U : 0xdU) : ((0x30U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                            ? 0x31U
                                            : ((0x31U 
                                                == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                ? ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__write_back)
                                                    ? 0x23U
                                                    : 0xdU)
                                                : (
                                                   (0U 
                                                    == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                    ? 1U
                                                    : 
                                                   ((1U 
                                                     == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                     ? 
                                                    ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__write_back)
                                                      ? 0x23U
                                                      : 0xdU)
                                                     : 
                                                    ((2U 
                                                      == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                      ? 3U
                                                      : 
                                                     ((((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__CO) 
                                                        | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__store)) 
                                                       | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__write_back))
                                                       ? 4U
                                                       : 0xdU)))))));
        }
    } else if (((((((((4U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)) 
                      | (0xeU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                     | (0xfU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                    | (0x10U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                   | (0x11U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                  | (0x12U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                 | (0x13U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                | (0x14U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)))) {
        vlSelfRef.__Vdly__CoproDrMario__DOT__cpu6502__DOT__state 
            = ((4U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                ? ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__write_back)
                    ? 0x23U : 0xdU) : ((0xeU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                        ? 0xfU : ((0xfU 
                                                   == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                   ? 0x10U
                                                   : 
                                                  ((0x10U 
                                                    == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                    ? 0x11U
                                                    : 
                                                   ((0x11U 
                                                     == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                     ? 0xdU
                                                     : 
                                                    ((0x12U 
                                                      == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                      ? 0x13U
                                                      : 
                                                     ((0x13U 
                                                       == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                       ? 0x14U
                                                       : 
                                                      (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__CO) 
                                                        | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__store))
                                                        ? 0x15U
                                                        : 0xdU))))))));
    } else if (((((((((0x15U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)) 
                      | (0x23U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                     | (0x2eU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                    | (0xdU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                   | (0x24U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                  | (0x21U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                 | (0x22U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                | (0x1eU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)))) {
        vlSelfRef.__Vdly__CoproDrMario__DOT__cpu6502__DOT__state 
            = ((0x15U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                ? 0xdU : ((0x23U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                           ? 0x2eU : ((0x2eU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                       ? 0xdU : ((0xdU 
                                                  == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                  ? 0xcU
                                                  : 
                                                 ((0x24U 
                                                   == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                   ? 0xcU
                                                   : 
                                                  ((0x21U 
                                                    == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                    ? 0x22U
                                                    : 
                                                   ((0x22U 
                                                     == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                     ? 0xcU
                                                     : 0x1fU)))))));
    } else if (((((((((0x1fU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)) 
                      | (0x20U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                     | (0x1aU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                    | (0x1bU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                   | (0x1cU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                  | (0x1dU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                 | (0x25U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                | (0x26U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)))) {
        vlSelfRef.__Vdly__CoproDrMario__DOT__cpu6502__DOT__state 
            = ((0x1fU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                ? 0x20U : ((0x20U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                            ? 0xcU : ((0x1aU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                       ? 0x1bU : ((0x1bU 
                                                   == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                   ? 0x1cU
                                                   : 
                                                  ((0x1cU 
                                                    == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                    ? 0x1dU
                                                    : 
                                                   ((0x1dU 
                                                     == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                     ? 0xdU
                                                     : 
                                                    ((0x25U 
                                                      == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                      ? 0x26U
                                                      : 0x27U)))))));
    } else if (((((((((0x27U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)) 
                      | (0x28U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                     | (0x29U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                    | (0x2aU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                   | (0x2bU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                  | (0x2cU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                 | (0x2dU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                | (5U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)))) {
        vlSelfRef.__Vdly__CoproDrMario__DOT__cpu6502__DOT__state 
            = ((0x27U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                ? 0x28U : ((0x28U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                            ? 0x29U : ((0x29U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                        ? 0xcU : ((0x2aU 
                                                   == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                   ? 0x2bU
                                                   : 
                                                  ((0x2bU 
                                                    == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                    ? 0x2cU
                                                    : 
                                                   ((0x2cU 
                                                     == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                     ? 0x2dU
                                                     : 
                                                    ((0x2dU 
                                                      == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                      ? 0xdU
                                                      : 
                                                     ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__cond_true)
                                                       ? 6U
                                                       : 0xcU))))))));
    } else if (((((((((6U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)) 
                      | (7U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                     | (0x16U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                    | (0x17U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                   | (0x18U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                  | (0x19U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                 | (8U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) 
                | (9U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)))) {
        vlSelfRef.__Vdly__CoproDrMario__DOT__cpu6502__DOT__state 
            = ((6U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                ? (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__CO) 
                    ^ (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__backwards))
                    ? 7U : 0xcU) : ((7U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                     ? 0xcU : ((0x16U 
                                                == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                ? 0x17U
                                                : (
                                                   (0x17U 
                                                    == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                    ? 0xcU
                                                    : 
                                                   ((0x18U 
                                                     == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                     ? 0x19U
                                                     : 
                                                    ((0x19U 
                                                      == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                      ? 0x16U
                                                      : 
                                                     ((8U 
                                                       == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                       ? 9U
                                                       : 0xaU)))))));
    } else if ((0xaU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        vlSelfRef.__Vdly__CoproDrMario__DOT__cpu6502__DOT__state = 0xbU;
    } else if ((0xbU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        vlSelfRef.__Vdly__CoproDrMario__DOT__cpu6502__DOT__state = 0x16U;
    }
}

VL_INLINE_OPT void VCoproDrMario___024root___nba_sequent__TOP__4(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___nba_sequent__TOP__4\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__VdlySet__CoproDrMario__DOT__wram__DOT__mem__v0) {
        vlSelfRef.CoproDrMario__DOT__wram__DOT__mem[vlSelfRef.__VdlyDim0__CoproDrMario__DOT__wram__DOT__mem__v0] 
            = vlSelfRef.__VdlyVal__CoproDrMario__DOT__wram__DOT__mem__v0;
    }
    if (vlSelfRef.__VdlySet__CoproDrMario__DOT__wram__DOT__mem__v1) {
        vlSelfRef.CoproDrMario__DOT__wram__DOT__mem[vlSelfRef.__VdlyDim0__CoproDrMario__DOT__wram__DOT__mem__v1] 
            = vlSelfRef.__VdlyVal__CoproDrMario__DOT__wram__DOT__mem__v1;
    }
}

extern const VlUnpacked<CData/*0:0*/, 128> VCoproDrMario__ConstPool__TABLE_h2335744c_0;

VL_INLINE_OPT void VCoproDrMario___024root___nba_sequent__TOP__5(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___nba_sequent__TOP__5\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*6:0*/ __Vtableidx8;
    __Vtableidx8 = 0;
    // Body
    __Vtableidx8 = ((((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__N) 
                      << 6U) | ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__V) 
                                << 5U)) | (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__C) 
                                            << 4U) 
                                           | (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__Z) 
                                               << 3U) 
                                              | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__cond_code))));
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__cond_true 
        = VCoproDrMario__ConstPool__TABLE_h2335744c_0
        [__Vtableidx8];
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__backwards 
        = (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__DI) 
                 >> 7U));
    if ((0xcU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__store 
            = ((0x84U == (0xe5U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
               || (0x81U == (0xe3U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))));
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__write_back 
            = ((6U == (0x87U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
               || (0xc6U == (0xc7U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))));
    }
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__CO = 
        (1U & (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp) 
                >> 8U) | ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT____Vcellinp__ALU__BCD) 
                          & (5U <= (7U & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_h) 
                                          >> 1U))))));
    vlSelfRef.CoproDrMario__DOT__cpu_rst = vlSelfRef.CoproDrMario__DOT__rst_m;
    vlSelfRef.CoproDrMario__DOT__DI = ((IData)(vlSelfRef.CoproDrMario__DOT__sel_vec_d)
                                        ? ((IData)(vlSelfRef.CoproDrMario__DOT__ab0_d)
                                            ? 0xbfU
                                            : 0x80U)
                                        : ((IData)(vlSelfRef.CoproDrMario__DOT__sel_rom_d)
                                            ? (IData)(vlSelfRef.CoproDrMario__DOT__rom_q)
                                            : ((IData)(vlSelfRef.CoproDrMario__DOT__sel_lev_d)
                                                ? (IData)(vlSelfRef.CoproDrMario__DOT__lev_q)
                                                : ((IData)(vlSelfRef.CoproDrMario__DOT__sel_ram_d)
                                                    ? (IData)(vlSelfRef.CoproDrMario__DOT__ram_a_q)
                                                    : 0xffU))));
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR = 
        ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__NMI_edge)
          ? 0U : ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IRHOLD_valid)
                   ? (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IRHOLD)
                   : (IData)(vlSelfRef.CoproDrMario__DOT__DI)));
    vlSelfRef.CoproDrMario__DOT__rst_m = ((0U != (IData)(vlSelfRef.CoproDrMario__DOT__rst_cnt)) 
                                          | (IData)(vlSelfRef.CoproDrMario__DOT__parked));
}

VL_INLINE_OPT void VCoproDrMario___024root___nba_sequent__TOP__6(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___nba_sequent__TOP__6\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state 
        = vlSelfRef.__Vdly__CoproDrMario__DOT__cpu6502__DOT__state;
}

VL_INLINE_OPT void VCoproDrMario___024root___nba_sequent__TOP__7(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___nba_sequent__TOP__7\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.CoproDrMario__DOT__rst_cnt = vlSelfRef.__Vdly__CoproDrMario__DOT__rst_cnt;
    if ((((IData)(vlSelfRef.ce) & (IData)(vlSelfRef.prg_write)) 
         & (IData)(vlSelfRef.copro_sel))) {
        if ((0x84U == (0x1ffU & (IData)(vlSelfRef.prg_ain)))) {
            vlSelfRef.CoproDrMario__DOT__parked = 0U;
        }
    }
}

extern const VlUnpacked<CData/*0:0*/, 256> VCoproDrMario__ConstPool__TABLE_hf9320a1f_0;
extern const VlUnpacked<CData/*0:0*/, 512> VCoproDrMario__ConstPool__TABLE_hafeef89d_0;
extern const VlUnpacked<CData/*0:0*/, 128> VCoproDrMario__ConstPool__TABLE_h3046dbb4_0;
extern const VlUnpacked<CData/*0:0*/, 8192> VCoproDrMario__ConstPool__TABLE_hc377d77d_0;
extern const VlUnpacked<CData/*3:0*/, 2048> VCoproDrMario__ConstPool__TABLE_h00ffe440_0;
extern const VlUnpacked<CData/*1:0*/, 2048> VCoproDrMario__ConstPool__TABLE_h8ffa5a2b_0;

VL_INLINE_OPT void VCoproDrMario___024root___nba_comb__TOP__0(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___nba_comb__TOP__0\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*7:0*/ CoproDrMario__DOT__cpu6502__DOT__BI;
    CoproDrMario__DOT__cpu6502__DOT__BI = 0;
    CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__CI;
    CoproDrMario__DOT__cpu6502__DOT__CI = 0;
    CData/*7:0*/ CoproDrMario__DOT__cpu6502__DOT__regfile;
    CoproDrMario__DOT__cpu6502__DOT__regfile = 0;
    CData/*0:0*/ CoproDrMario__DOT__cpu6502__DOT__alu_shift_right;
    CoproDrMario__DOT__cpu6502__DOT__alu_shift_right = 0;
    CData/*3:0*/ CoproDrMario__DOT__cpu6502__DOT__alu_op;
    CoproDrMario__DOT__cpu6502__DOT__alu_op = 0;
    SData/*15:0*/ CoproDrMario__DOT__cpu6502__DOT____VdfgExtracted_hdce86eaa__0;
    CoproDrMario__DOT__cpu6502__DOT____VdfgExtracted_hdce86eaa__0 = 0;
    SData/*8:0*/ CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_logic;
    CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_logic = 0;
    CData/*4:0*/ CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_l;
    CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_l = 0;
    SData/*8:0*/ __Vtableidx1;
    __Vtableidx1 = 0;
    CData/*6:0*/ __Vtableidx2;
    __Vtableidx2 = 0;
    CData/*7:0*/ __Vtableidx3;
    __Vtableidx3 = 0;
    SData/*10:0*/ __Vtableidx4;
    __Vtableidx4 = 0;
    SData/*10:0*/ __Vtableidx5;
    __Vtableidx5 = 0;
    SData/*12:0*/ __Vtableidx6;
    __Vtableidx6 = 0;
    // Body
    __Vtableidx3 = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__plp) 
                     << 7U) | (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__load_reg) 
                                << 6U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)));
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__write_register 
        = VCoproDrMario__ConstPool__TABLE_hf9320a1f_0
        [__Vtableidx3];
    __Vtableidx1 = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__backwards) 
                     << 8U) | (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__CO) 
                                << 7U) | (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__NMI_edge) 
                                           << 6U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))));
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_inc 
        = VCoproDrMario__ConstPool__TABLE_hafeef89d_0
        [__Vtableidx1];
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT____Vcellinp__ALU__BCD 
        = ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__adc_bcd) 
           & (0xdU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)));
    __Vtableidx2 = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__store) 
                     << 6U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state));
    vlSelfRef.CoproDrMario__DOT__WE = VCoproDrMario__ConstPool__TABLE_h3046dbb4_0
        [__Vtableidx2];
    CoproDrMario__DOT__cpu6502__DOT__alu_shift_right 
        = (((0xdU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)) 
            | ((0x24U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)) 
               | (0x23U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)))) 
           & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__shift_right));
    __Vtableidx6 = (((((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__load_only) 
                       << 0xcU) | ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__compare) 
                                   << 0xbU)) | (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__CO) 
                                                 << 0xaU) 
                                                | ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__inc) 
                                                   << 9U))) 
                    | (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__shift) 
                        << 8U) | (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__C) 
                                   << 7U) | (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__rotate) 
                                              << 6U) 
                                             | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)))));
    CoproDrMario__DOT__cpu6502__DOT__CI = VCoproDrMario__ConstPool__TABLE_hc377d77d_0
        [__Vtableidx6];
    __Vtableidx5 = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__backwards) 
                     << 0xaU) | (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__op) 
                                  << 6U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)));
    CoproDrMario__DOT__cpu6502__DOT__alu_op = VCoproDrMario__ConstPool__TABLE_h00ffe440_0
        [__Vtableidx5];
    __Vtableidx4 = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__dst_reg) 
                     << 9U) | (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__index_y) 
                                << 8U) | (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__src_reg) 
                                           << 6U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))));
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__regsel 
        = VCoproDrMario__ConstPool__TABLE_h8ffa5a2b_0
        [__Vtableidx4];
    vlSelfRef.CoproDrMario__DOT____VdfgRegularize_hb6d3a560_2_3 
        = ((~ (IData)(vlSelfRef.CoproDrMario__DOT__cpu_rst)) 
           & (IData)(vlSelfRef.CoproDrMario__DOT__WE));
    CoproDrMario__DOT__cpu6502__DOT____VdfgExtracted_hdce86eaa__0 
        = (0x100U | vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AXYS
           [vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__regsel]);
    CoproDrMario__DOT__cpu6502__DOT__regfile = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AXYS
        [vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__regsel];
    if ((0x20U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        if ((0x10U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp 
                = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
            CoproDrMario__DOT__cpu6502__DOT__BI = (0xffU 
                                                   & (IData)(vlSelfRef.CoproDrMario__DOT__DI));
            if ((8U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                vlSelfRef.CoproDrMario__DOT__AB = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                    = (0xffU & 0U);
            } else if ((4U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                vlSelfRef.CoproDrMario__DOT__AB = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                    = (0xffU & 0U);
            } else if ((2U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                vlSelfRef.CoproDrMario__DOT__AB = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                    = (0xffU & 0U);
            } else if ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                vlSelfRef.CoproDrMario__DOT__AB = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD;
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                    = (0xffU & 0U);
            } else {
                vlSelfRef.CoproDrMario__DOT__AB = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                    = (0xffU & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
            }
            vlSelfRef.CoproDrMario__DOT__DO = (0xffU 
                                               & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
        } else if ((8U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp 
                = ((2U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                    ? (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC)
                    : ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                        ? (((IData)(vlSelfRef.CoproDrMario__DOT__DI) 
                            << 8U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD))
                        : (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC)));
            if ((4U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                CoproDrMario__DOT__cpu6502__DOT__BI 
                    = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__DI));
                if ((2U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                    if ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                        vlSelfRef.CoproDrMario__DOT__AB 
                            = vlSelfRef.CoproDrMario__DOT__DI;
                        vlSelfRef.CoproDrMario__DOT__DO 
                            = (0xffU & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
                    } else {
                        vlSelfRef.CoproDrMario__DOT__AB 
                            = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ABH) 
                                << 8U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ABL));
                        vlSelfRef.CoproDrMario__DOT__DO 
                            = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD));
                    }
                } else {
                    vlSelfRef.CoproDrMario__DOT__AB 
                        = ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                            ? (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC)
                            : (0x100U | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD)));
                    vlSelfRef.CoproDrMario__DOT__DO 
                        = (0xffU & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
                }
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                    = (0xffU & 0U);
            } else {
                if ((2U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                    CoproDrMario__DOT__cpu6502__DOT__BI 
                        = (0xffU & 0U);
                    if ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                        vlSelfRef.CoproDrMario__DOT__AB 
                            = (0x100U | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD));
                        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                            = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD));
                    } else {
                        vlSelfRef.CoproDrMario__DOT__AB 
                            = CoproDrMario__DOT__cpu6502__DOT____VdfgExtracted_hdce86eaa__0;
                        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                            = (0xffU & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
                    }
                } else {
                    CoproDrMario__DOT__cpu6502__DOT__BI 
                        = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__DI));
                    vlSelfRef.CoproDrMario__DOT__AB 
                        = ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                            ? (((IData)(vlSelfRef.CoproDrMario__DOT__DI) 
                                << 8U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD))
                            : (0x100U | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD)));
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & 0U);
                }
                vlSelfRef.CoproDrMario__DOT__DO = (0xffU 
                                                   & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
            }
        } else {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp 
                = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
            if ((4U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                CoproDrMario__DOT__cpu6502__DOT__BI 
                    = (0xffU & 0U);
                if ((2U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                    vlSelfRef.CoproDrMario__DOT__AB 
                        = (0x100U | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD));
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD));
                } else {
                    vlSelfRef.CoproDrMario__DOT__AB 
                        = ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                            ? (IData)(CoproDrMario__DOT__cpu6502__DOT____VdfgExtracted_hdce86eaa__0)
                            : (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ABH) 
                                << 8U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ABL)));
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
                }
                vlSelfRef.CoproDrMario__DOT__DO = (0xffU 
                                                   & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
            } else if ((2U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                CoproDrMario__DOT__cpu6502__DOT__BI 
                    = (0xffU & 0U);
                if ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                    vlSelfRef.CoproDrMario__DOT__AB 
                        = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ABH) 
                            << 8U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ABL));
                    vlSelfRef.CoproDrMario__DOT__DO 
                        = (0xffU & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__DI));
                } else {
                    vlSelfRef.CoproDrMario__DOT__AB 
                        = CoproDrMario__DOT__cpu6502__DOT____VdfgExtracted_hdce86eaa__0;
                    vlSelfRef.CoproDrMario__DOT__DO 
                        = (0xffU & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__php)
                                     ? (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__P)
                                     : (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD)));
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
                }
            } else {
                if ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                    CoproDrMario__DOT__cpu6502__DOT__BI 
                        = (0xffU & 0U);
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
                } else {
                    CoproDrMario__DOT__cpu6502__DOT__BI 
                        = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__DI));
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & 0U);
                }
                vlSelfRef.CoproDrMario__DOT__AB = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
                vlSelfRef.CoproDrMario__DOT__DO = (0xffU 
                                                   & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
            }
        }
    } else if ((0x10U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        if ((8U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp 
                = ((2U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                    ? (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC)
                    : ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                        ? (((IData)(vlSelfRef.CoproDrMario__DOT__DI) 
                            << 8U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD))
                        : (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC)));
            if ((4U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                if ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                    CoproDrMario__DOT__cpu6502__DOT__BI 
                        = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__DI));
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & 0U);
                } else {
                    CoproDrMario__DOT__cpu6502__DOT__BI 
                        = (0xffU & 0U);
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
                }
                vlSelfRef.CoproDrMario__DOT__AB = (
                                                   (2U 
                                                    & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                     ? 
                                                    (0x100U 
                                                     | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD))
                                                     : (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC))
                                                    : (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC));
                vlSelfRef.CoproDrMario__DOT__DO = (0xffU 
                                                   & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
            } else if ((2U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                CoproDrMario__DOT__cpu6502__DOT__BI 
                    = (0xffU & 0U);
                if ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                    vlSelfRef.CoproDrMario__DOT__AB 
                        = (0x100U | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD));
                    vlSelfRef.CoproDrMario__DOT__DO 
                        = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC));
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD));
                } else {
                    vlSelfRef.CoproDrMario__DOT__AB 
                        = CoproDrMario__DOT__cpu6502__DOT____VdfgExtracted_hdce86eaa__0;
                    vlSelfRef.CoproDrMario__DOT__DO 
                        = (0xffU & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC) 
                                    >> 8U));
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
                }
            } else {
                CoproDrMario__DOT__cpu6502__DOT__BI 
                    = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__DI));
                vlSelfRef.CoproDrMario__DOT__AB = (
                                                   (1U 
                                                    & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                    ? 
                                                   (((IData)(vlSelfRef.CoproDrMario__DOT__DI) 
                                                     << 8U) 
                                                    | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD))
                                                    : (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC));
                vlSelfRef.CoproDrMario__DOT__DO = (0xffU 
                                                   & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                    = (0xffU & 0U);
            }
        } else {
            if ((4U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                if ((2U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                    if ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp 
                            = (((IData)(vlSelfRef.CoproDrMario__DOT__DI) 
                                << 8U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD));
                        vlSelfRef.CoproDrMario__DOT__AB 
                            = (((IData)(vlSelfRef.CoproDrMario__DOT__DI) 
                                << 8U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD));
                    } else {
                        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp 
                            = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
                        vlSelfRef.CoproDrMario__DOT__AB 
                            = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
                    }
                } else {
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp 
                        = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
                    vlSelfRef.CoproDrMario__DOT__AB 
                        = ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                            ? (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD) 
                                << 8U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ABL))
                            : (((IData)(vlSelfRef.CoproDrMario__DOT__DI) 
                                << 8U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD)));
                }
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                    = (0xffU & 0U);
            } else {
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp 
                    = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
                if ((2U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                    if ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                        vlSelfRef.CoproDrMario__DOT__AB 
                            = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD;
                        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                            = (0xffU & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
                    } else {
                        vlSelfRef.CoproDrMario__DOT__AB 
                            = vlSelfRef.CoproDrMario__DOT__DI;
                        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                            = (0xffU & 0U);
                    }
                } else {
                    vlSelfRef.CoproDrMario__DOT__AB 
                        = ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                            ? (((IData)(vlSelfRef.CoproDrMario__DOT__DI) 
                                << 8U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD))
                            : (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD));
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & 0U);
                }
            }
            CoproDrMario__DOT__cpu6502__DOT__BI = (0xffU 
                                                   & (IData)(vlSelfRef.CoproDrMario__DOT__DI));
            vlSelfRef.CoproDrMario__DOT__DO = (0xffU 
                                               & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
        }
    } else if ((8U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
        if ((4U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
            if ((2U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp 
                    = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
                if ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                    CoproDrMario__DOT__cpu6502__DOT__BI 
                        = (0xffU & 0U);
                    vlSelfRef.CoproDrMario__DOT__AB 
                        = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD;
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD));
                } else {
                    CoproDrMario__DOT__cpu6502__DOT__BI 
                        = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__DI));
                    vlSelfRef.CoproDrMario__DOT__AB 
                        = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
                }
            } else {
                if ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp 
                        = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
                    CoproDrMario__DOT__cpu6502__DOT__BI 
                        = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__DI));
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__load_only)
                                     ? 0U : (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile)));
                } else {
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp 
                        = ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__NMI_edge)
                            ? (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ABH) 
                                << 8U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ABL))
                            : (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC));
                    CoproDrMario__DOT__cpu6502__DOT__BI 
                        = (0xffU & 0U);
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & 0U);
                }
                vlSelfRef.CoproDrMario__DOT__AB = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
            }
            vlSelfRef.CoproDrMario__DOT__DO = (0xffU 
                                               & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
        } else if ((2U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
            if ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp 
                    = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
                CoproDrMario__DOT__cpu6502__DOT__BI 
                    = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__DI));
                vlSelfRef.CoproDrMario__DOT__AB = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
                vlSelfRef.CoproDrMario__DOT__DO = (0xffU 
                                                   & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                    = (0xffU & 0U);
            } else {
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp 
                    = ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__res)
                        ? 0xfffcU : ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__NMI_edge)
                                      ? 0xfffaU : 0xfffeU));
                CoproDrMario__DOT__cpu6502__DOT__BI 
                    = (0xffU & 0U);
                vlSelfRef.CoproDrMario__DOT__AB = (0x100U 
                                                   | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD));
                vlSelfRef.CoproDrMario__DOT__DO = (0xffU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__NMI_edge)
                                                       ? 
                                                      (0xefU 
                                                       & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__P))
                                                       : (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__P)));
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                    = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD));
            }
        } else {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp 
                = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
            CoproDrMario__DOT__cpu6502__DOT__BI = (0xffU 
                                                   & 0U);
            if ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                vlSelfRef.CoproDrMario__DOT__AB = (0x100U 
                                                   | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD));
                vlSelfRef.CoproDrMario__DOT__DO = (0xffU 
                                                   & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC));
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                    = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD));
            } else {
                vlSelfRef.CoproDrMario__DOT__AB = CoproDrMario__DOT__cpu6502__DOT____VdfgExtracted_hdce86eaa__0;
                vlSelfRef.CoproDrMario__DOT__DO = (0xffU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC) 
                                                      >> 8U));
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                    = (0xffU & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
            }
        }
    } else {
        if ((4U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
            if ((2U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                if ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp 
                        = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD) 
                            << 8U) | (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC)));
                    CoproDrMario__DOT__cpu6502__DOT__BI 
                        = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__DI));
                    vlSelfRef.CoproDrMario__DOT__AB 
                        = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD) 
                            << 8U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ABL));
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & 0U);
                } else {
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp 
                        = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ABH) 
                            << 8U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD));
                    CoproDrMario__DOT__cpu6502__DOT__BI 
                        = (0xffU & 0U);
                    vlSelfRef.CoproDrMario__DOT__AB 
                        = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ABH) 
                            << 8U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD));
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ABH));
                }
            } else {
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp 
                    = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
                if ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                    CoproDrMario__DOT__cpu6502__DOT__BI 
                        = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC));
                    vlSelfRef.CoproDrMario__DOT__AB 
                        = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__DI));
                } else {
                    CoproDrMario__DOT__cpu6502__DOT__BI 
                        = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__DI));
                    vlSelfRef.CoproDrMario__DOT__AB 
                        = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD) 
                            << 8U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ABL));
                    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                        = (0xffU & 0U);
                }
            }
        } else {
            vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC_temp 
                = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC;
            if ((2U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))) {
                CoproDrMario__DOT__cpu6502__DOT__BI 
                    = (0xffU & (IData)(vlSelfRef.CoproDrMario__DOT__DI));
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                    = (0xffU & ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                 ? 0U : (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile)));
            } else {
                CoproDrMario__DOT__cpu6502__DOT__BI 
                    = (0xffU & ((1U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                 ? 0U : (IData)(vlSelfRef.CoproDrMario__DOT__DI)));
                vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI 
                    = (0xffU & 0U);
            }
            vlSelfRef.CoproDrMario__DOT__AB = ((1U 
                                                & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))
                                                ? (
                                                   ((IData)(vlSelfRef.CoproDrMario__DOT__DI) 
                                                    << 8U) 
                                                   | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ADD))
                                                : (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__PC));
        }
        vlSelfRef.CoproDrMario__DOT__DO = (0xffU & (IData)(CoproDrMario__DOT__cpu6502__DOT__regfile));
    }
    vlSelfRef.CoproDrMario__DOT__a_ram = ((0U == (0xfU 
                                                  & ((IData)(vlSelfRef.CoproDrMario__DOT__AB) 
                                                     >> 0xcU))) 
                                          | (0x61U 
                                             == (0xffU 
                                                 & ((IData)(vlSelfRef.CoproDrMario__DOT__AB) 
                                                    >> 8U))));
    vlSelfRef.CoproDrMario__DOT__a_addr = (0xfffU & 
                                           ((0x61U 
                                             == (0xffU 
                                                 & ((IData)(vlSelfRef.CoproDrMario__DOT__AB) 
                                                    >> 8U)))
                                             ? (0x800U 
                                                | (0xffU 
                                                   & (IData)(vlSelfRef.CoproDrMario__DOT__AB)))
                                             : (IData)(vlSelfRef.CoproDrMario__DOT__AB)));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sl_wa 
        = ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__sl_cpw)
            ? (((IData)(vlSelfRef.CoproDrMario__DOT__lev_a_sl) 
                << 7U) | (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__cpw_p))
            : (((IData)(vlSelfRef.CoproDrMario__DOT__lev_wslot) 
                << 7U) | (0x7fU & (IData)(vlSelfRef.CoproDrMario__DOT__AB))));
    vlSelfRef.CoproDrMario__DOT____VdfgRegularize_hb6d3a560_2_2 
        = ((IData)(vlSelfRef.CoproDrMario__DOT____VdfgRegularize_hb6d3a560_2_3) 
           & (0x7000U == (0xff00U & (IData)(vlSelfRef.CoproDrMario__DOT__AB))));
    vlSelfRef.CoproDrMario__DOT__lev_colenc = ((0U 
                                                == 
                                                (3U 
                                                 & (IData)(vlSelfRef.CoproDrMario__DOT__DO)))
                                                ? 1U
                                                : (
                                                   (1U 
                                                    == 
                                                    (3U 
                                                     & (IData)(vlSelfRef.CoproDrMario__DOT__DO)))
                                                    ? 2U
                                                    : 3U));
    CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_logic 
        = ((2U & (IData)(CoproDrMario__DOT__cpu6502__DOT__alu_op))
            ? ((1U & (IData)(CoproDrMario__DOT__cpu6502__DOT__alu_op))
                ? (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI)
                : ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI) 
                   ^ (IData)(CoproDrMario__DOT__cpu6502__DOT__BI)))
            : ((1U & (IData)(CoproDrMario__DOT__cpu6502__DOT__alu_op))
                ? ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI) 
                   & (IData)(CoproDrMario__DOT__cpu6502__DOT__BI))
                : ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI) 
                   | (IData)(CoproDrMario__DOT__cpu6502__DOT__BI))));
    if (CoproDrMario__DOT__cpu6502__DOT__alu_shift_right) {
        CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_logic 
            = ((0x100U & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI) 
                          << 8U)) | (((IData)(CoproDrMario__DOT__cpu6502__DOT__CI) 
                                      << 7U) | (0x7fU 
                                                & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI) 
                                                   >> 1U))));
    }
    vlSelfRef.CoproDrMario__DOT__lev_wr_arg = ((IData)(vlSelfRef.CoproDrMario__DOT____VdfgRegularize_hb6d3a560_2_2) 
                                               & (IData)(
                                                         (0xe0U 
                                                          == 
                                                          (0xf8U 
                                                           & (IData)(vlSelfRef.CoproDrMario__DOT__AB)))));
    vlSelfRef.CoproDrMario__DOT__lev_wr_board = ((~ 
                                                  ((IData)(vlSelfRef.CoproDrMario__DOT__AB) 
                                                   >> 7U)) 
                                                 & (IData)(vlSelfRef.CoproDrMario__DOT____VdfgRegularize_hb6d3a560_2_2));
    vlSelfRef.CoproDrMario__DOT__lev_start = ((IData)(vlSelfRef.CoproDrMario__DOT____VdfgRegularize_hb6d3a560_2_2) 
                                              & (0xf8U 
                                                 == 
                                                 (0xffU 
                                                  & (IData)(vlSelfRef.CoproDrMario__DOT__AB))));
    vlSelfRef.CoproDrMario__DOT__lev_enc = ((0xffU 
                                             == (IData)(vlSelfRef.CoproDrMario__DOT__DO))
                                             ? 0U : 
                                            (((0xdU 
                                               == (0xfU 
                                                   & ((IData)(vlSelfRef.CoproDrMario__DOT__DO) 
                                                      >> 4U))) 
                                              << 2U) 
                                             | (IData)(vlSelfRef.CoproDrMario__DOT__lev_colenc)));
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_BI 
        = (0xffU & ((8U & (IData)(CoproDrMario__DOT__cpu6502__DOT__alu_op))
                     ? ((4U & (IData)(CoproDrMario__DOT__cpu6502__DOT__alu_op))
                         ? 0U : (IData)(CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_logic))
                     : ((4U & (IData)(CoproDrMario__DOT__cpu6502__DOT__alu_op))
                         ? (~ (IData)(CoproDrMario__DOT__cpu6502__DOT__BI))
                         : (IData)(CoproDrMario__DOT__cpu6502__DOT__BI))));
    CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_l 
        = (0x1fU & (((0xfU & (IData)(CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_logic)) 
                     + (0xfU & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_BI))) 
                    + ((~ ((IData)(CoproDrMario__DOT__cpu6502__DOT__alu_shift_right) 
                           | (3U == (3U & ((IData)(CoproDrMario__DOT__cpu6502__DOT__alu_op) 
                                           >> 2U))))) 
                       & (IData)(CoproDrMario__DOT__cpu6502__DOT__CI))));
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_HC 
        = (1U & (((IData)(CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_l) 
                  >> 4U) | ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT____Vcellinp__ALU__BCD) 
                            & (5U <= (7U & ((IData)(CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_l) 
                                            >> 1U))))));
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_h 
        = (0x1fU & ((((IData)(CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_logic) 
                      >> 4U) + (0xfU & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_BI) 
                                        >> 4U))) + (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_HC)));
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp 
        = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_h) 
            << 4U) | (0xfU & (IData)(CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_l)));
}

void VCoproDrMario___024root___eval_triggers__act(VCoproDrMario___024root* vlSelf);

bool VCoproDrMario___024root___eval_phase__act(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___eval_phase__act\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    VlTriggerVec<3> __VpreTriggered;
    CData/*0:0*/ __VactExecute;
    // Body
    VCoproDrMario___024root___eval_triggers__act(vlSelf);
    __VactExecute = vlSelfRef.__VactTriggered.any();
    if (__VactExecute) {
        __VpreTriggered.andNot(vlSelfRef.__VactTriggered, vlSelfRef.__VnbaTriggered);
        vlSelfRef.__VnbaTriggered.thisOr(vlSelfRef.__VactTriggered);
        VCoproDrMario___024root___eval_act(vlSelf);
    }
    return (__VactExecute);
}

bool VCoproDrMario___024root___eval_phase__nba(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___eval_phase__nba\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = vlSelfRef.__VnbaTriggered.any();
    if (__VnbaExecute) {
        VCoproDrMario___024root___eval_nba(vlSelf);
        vlSelfRef.__VnbaTriggered.clear();
    }
    return (__VnbaExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VCoproDrMario___024root___dump_triggers__ico(VCoproDrMario___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void VCoproDrMario___024root___dump_triggers__nba(VCoproDrMario___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void VCoproDrMario___024root___dump_triggers__act(VCoproDrMario___024root* vlSelf);
#endif  // VL_DEBUG

void VCoproDrMario___024root___eval(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___eval\n"); );
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
            VCoproDrMario___024root___dump_triggers__ico(vlSelf);
#endif
            VL_FATAL_MT("CoproDrMario.sv", 21, "", "Input combinational region did not converge.");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        __VicoContinue = 0U;
        if (VCoproDrMario___024root___eval_phase__ico(vlSelf)) {
            __VicoContinue = 1U;
        }
        vlSelfRef.__VicoFirstIteration = 0U;
    }
    __VnbaIterCount = 0U;
    __VnbaContinue = 1U;
    while (__VnbaContinue) {
        if (VL_UNLIKELY((0x64U < __VnbaIterCount))) {
#ifdef VL_DEBUG
            VCoproDrMario___024root___dump_triggers__nba(vlSelf);
#endif
            VL_FATAL_MT("CoproDrMario.sv", 21, "", "NBA region did not converge.");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        __VnbaContinue = 0U;
        vlSelfRef.__VactIterCount = 0U;
        vlSelfRef.__VactContinue = 1U;
        while (vlSelfRef.__VactContinue) {
            if (VL_UNLIKELY((0x64U < vlSelfRef.__VactIterCount))) {
#ifdef VL_DEBUG
                VCoproDrMario___024root___dump_triggers__act(vlSelf);
#endif
                VL_FATAL_MT("CoproDrMario.sv", 21, "", "Active region did not converge.");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
            vlSelfRef.__VactContinue = 0U;
            if (VCoproDrMario___024root___eval_phase__act(vlSelf)) {
                vlSelfRef.__VactContinue = 1U;
            }
        }
        if (VCoproDrMario___024root___eval_phase__nba(vlSelf)) {
            __VnbaContinue = 1U;
        }
    }
}

#ifdef VL_DEBUG
void VCoproDrMario___024root___eval_debug_assertions(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___eval_debug_assertions\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY((vlSelfRef.clk & 0xfeU))) {
        Verilated::overWidthError("clk");}
    if (VL_UNLIKELY((vlSelfRef.clk_cpu & 0xfeU))) {
        Verilated::overWidthError("clk_cpu");}
    if (VL_UNLIKELY((vlSelfRef.ce & 0xfeU))) {
        Verilated::overWidthError("ce");}
    if (VL_UNLIKELY((vlSelfRef.enable & 0xfeU))) {
        Verilated::overWidthError("enable");}
    if (VL_UNLIKELY((vlSelfRef.prg_read & 0xfeU))) {
        Verilated::overWidthError("prg_read");}
    if (VL_UNLIKELY((vlSelfRef.prg_write & 0xfeU))) {
        Verilated::overWidthError("prg_write");}
}
#endif  // VL_DEBUG
