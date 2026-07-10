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
    SData/*13:0*/ __Vtableidx7;
    __Vtableidx7 = 0;
    CData/*7:0*/ __VdlyVal__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0;
    __VdlyVal__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0 = 0;
    CData/*1:0*/ __VdlyDim0__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0;
    __VdlyDim0__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0 = 0;
    CData/*0:0*/ __VdlySet__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0;
    __VdlySet__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0 = 0;
    // Body
    __VdlySet__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0 = 0U;
    if (vlSelfRef.CoproDrMario__DOT____Vcellinp__wram__wren_a) {
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
    if (__VdlySet__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AXYS[__VdlyDim0__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0] 
            = __VdlyVal__CoproDrMario__DOT__cpu6502__DOT__AXYS__v0;
    }
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__HC = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_HC;
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__adj_bcd 
        = ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__adc_sbc) 
           & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__D));
    if (((0xcU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)) 
         | (8U == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)))) {
        vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__adc_bcd 
            = ((0x61U == (0xe3U & (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR))) 
               && (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__D));
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
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AN = 
        (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp) 
               >> 7U));
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__BI7 
        = (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_BI) 
                 >> 7U));
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__AI7 
        = (1U & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AI) 
                 >> 7U));
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
    vlSelfRef.CoproDrMario__DOT__cpu_rst = vlSelfRef.CoproDrMario__DOT__rst_m;
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__CO = 
        (1U & (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp) 
                >> 8U) | ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT____Vcellinp__ALU__BCD) 
                          & (5U <= (7U & ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_h) 
                                          >> 1U))))));
    vlSelfRef.CoproDrMario__DOT__DI = ((IData)(vlSelfRef.CoproDrMario__DOT__sel_vec_d)
                                        ? ((IData)(vlSelfRef.CoproDrMario__DOT__ab0_d)
                                            ? 0xbfU
                                            : 0x80U)
                                        : ((IData)(vlSelfRef.CoproDrMario__DOT__sel_rom_d)
                                            ? (IData)(vlSelfRef.CoproDrMario__DOT__rom_q)
                                            : ((IData)(vlSelfRef.CoproDrMario__DOT__sel_ram_d)
                                                ? (IData)(vlSelfRef.CoproDrMario__DOT__ram_a_q)
                                                : 0xffU)));
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
extern const VlUnpacked<CData/*1:0*/, 2048> VCoproDrMario__ConstPool__TABLE_h8ffa5a2b_0;
extern const VlUnpacked<CData/*3:0*/, 2048> VCoproDrMario__ConstPool__TABLE_h00ffe440_0;

VL_INLINE_OPT void VCoproDrMario___024root___nba_comb__TOP__0(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___nba_comb__TOP__0\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ CoproDrMario__DOT__WE;
    CoproDrMario__DOT__WE = 0;
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
    __Vtableidx2 = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__store) 
                     << 6U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state));
    CoproDrMario__DOT__WE = VCoproDrMario__ConstPool__TABLE_h3046dbb4_0
        [__Vtableidx2];
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT____Vcellinp__ALU__BCD 
        = ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__adc_bcd) 
           & (0xdU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)));
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
    __Vtableidx4 = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__dst_reg) 
                     << 9U) | (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__index_y) 
                                << 8U) | (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__src_reg) 
                                           << 6U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state))));
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__regsel 
        = VCoproDrMario__ConstPool__TABLE_h8ffa5a2b_0
        [__Vtableidx4];
    __Vtableidx5 = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__backwards) 
                     << 0xaU) | (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__op) 
                                  << 6U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)));
    CoproDrMario__DOT__cpu6502__DOT__alu_op = VCoproDrMario__ConstPool__TABLE_h00ffe440_0
        [__Vtableidx5];
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
    vlSelfRef.CoproDrMario__DOT__a_addr = (0xfffU & 
                                           ((0x61U 
                                             == (0xffU 
                                                 & ((IData)(vlSelfRef.CoproDrMario__DOT__AB) 
                                                    >> 8U)))
                                             ? (0x800U 
                                                | (0xffU 
                                                   & (IData)(vlSelfRef.CoproDrMario__DOT__AB)))
                                             : (IData)(vlSelfRef.CoproDrMario__DOT__AB)));
    vlSelfRef.CoproDrMario__DOT__a_ram = ((0U == (0xfU 
                                                  & ((IData)(vlSelfRef.CoproDrMario__DOT__AB) 
                                                     >> 0xcU))) 
                                          | (0x61U 
                                             == (0xffU 
                                                 & ((IData)(vlSelfRef.CoproDrMario__DOT__AB) 
                                                    >> 8U))));
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
    vlSelfRef.CoproDrMario__DOT____Vcellinp__wram__wren_a 
        = ((IData)(CoproDrMario__DOT__WE) & ((~ (IData)(vlSelfRef.CoproDrMario__DOT__cpu_rst)) 
                                             & (IData)(vlSelfRef.CoproDrMario__DOT__a_ram)));
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
