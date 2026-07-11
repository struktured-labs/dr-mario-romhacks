// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VCoproDrMario.h for the primary calling header

#include "VCoproDrMario__pch.h"
#include "VCoproDrMario___024root.h"

VL_ATTR_COLD void VCoproDrMario___024root___eval_static__TOP(VCoproDrMario___024root* vlSelf);

VL_ATTR_COLD void VCoproDrMario___024root___eval_static(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___eval_static\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    VCoproDrMario___024root___eval_static__TOP(vlSelf);
}

VL_ATTR_COLD void VCoproDrMario___024root___eval_static__TOP(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___eval_static__TOP\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.CoproDrMario__DOT__rst_cnt = 0x1fU;
    vlSelfRef.CoproDrMario__DOT__parked = 1U;
    vlSelfRef.CoproDrMario__DOT__rst_m = 1U;
    vlSelfRef.CoproDrMario__DOT__cpu_rst = 1U;
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__C = 0U;
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__Z = 0U;
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__I = 0U;
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__D = 0U;
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__V = 0U;
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__N = 0U;
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__NMI_edge = 0U;
}

VL_ATTR_COLD void VCoproDrMario___024root___eval_initial__TOP(VCoproDrMario___024root* vlSelf);

VL_ATTR_COLD void VCoproDrMario___024root___eval_initial(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___eval_initial\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    VCoproDrMario___024root___eval_initial__TOP(vlSelf);
    vlSelfRef.__Vtrigprevexpr___TOP__clk_cpu__0 = vlSelfRef.clk_cpu;
    vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__CoproDrMario__DOT__cpu_rst__0 
        = vlSelfRef.CoproDrMario__DOT__cpu_rst;
}

VL_ATTR_COLD void VCoproDrMario___024root___eval_initial__TOP(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___eval_initial__TOP\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    VlWide<4>/*127:0*/ __Vtemp_1;
    // Body
    __Vtemp_1[0U] = 0x2e686578U;
    __Vtemp_1[1U] = 0x5f726f6dU;
    __Vtemp_1[2U] = 0x6f70726fU;
    __Vtemp_1[3U] = 0x63U;
    VL_READMEM_N(true, 8, 16384, 0, VL_CVT_PACK_STR_NW(4, __Vtemp_1)
                 ,  &(vlSelfRef.CoproDrMario__DOT__rom)
                 , 0, ~0ULL);
}

VL_ATTR_COLD void VCoproDrMario___024root___eval_final(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___eval_final\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VCoproDrMario___024root___dump_triggers__stl(VCoproDrMario___024root* vlSelf);
#endif  // VL_DEBUG
VL_ATTR_COLD bool VCoproDrMario___024root___eval_phase__stl(VCoproDrMario___024root* vlSelf);

VL_ATTR_COLD void VCoproDrMario___024root___eval_settle(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___eval_settle\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    IData/*31:0*/ __VstlIterCount;
    CData/*0:0*/ __VstlContinue;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    __VstlContinue = 1U;
    while (__VstlContinue) {
        if (VL_UNLIKELY((0x64U < __VstlIterCount))) {
#ifdef VL_DEBUG
            VCoproDrMario___024root___dump_triggers__stl(vlSelf);
#endif
            VL_FATAL_MT("CoproDrMario.sv", 21, "", "Settle region did not converge.");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        __VstlContinue = 0U;
        if (VCoproDrMario___024root___eval_phase__stl(vlSelf)) {
            __VstlContinue = 1U;
        }
        vlSelfRef.__VstlFirstIteration = 0U;
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VCoproDrMario___024root___dump_triggers__stl(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___dump_triggers__stl\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VstlTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VstlTriggered.word(0U))) {
        VL_DBG_MSGF("         'stl' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void VCoproDrMario___024root___stl_sequent__TOP__0(VCoproDrMario___024root* vlSelf);

VL_ATTR_COLD void VCoproDrMario___024root___eval_stl(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___eval_stl\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VstlTriggered.word(0U))) {
        VCoproDrMario___024root___stl_sequent__TOP__0(vlSelf);
    }
}

extern const VlUnpacked<CData/*0:0*/, 256> VCoproDrMario__ConstPool__TABLE_hf9320a1f_0;
extern const VlUnpacked<CData/*0:0*/, 512> VCoproDrMario__ConstPool__TABLE_hafeef89d_0;
extern const VlUnpacked<CData/*0:0*/, 128> VCoproDrMario__ConstPool__TABLE_h2335744c_0;
extern const VlUnpacked<CData/*0:0*/, 128> VCoproDrMario__ConstPool__TABLE_h3046dbb4_0;
extern const VlUnpacked<CData/*0:0*/, 8192> VCoproDrMario__ConstPool__TABLE_hc377d77d_0;
extern const VlUnpacked<CData/*3:0*/, 2048> VCoproDrMario__ConstPool__TABLE_h00ffe440_0;
extern const VlUnpacked<CData/*1:0*/, 2048> VCoproDrMario__ConstPool__TABLE_h8ffa5a2b_0;

VL_ATTR_COLD void VCoproDrMario___024root___stl_sequent__TOP__0(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___stl_sequent__TOP__0\n"); );
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
    CData/*6:0*/ __Vtableidx8;
    __Vtableidx8 = 0;
    // Body
    vlSelfRef.prg_dout = vlSelfRef.CoproDrMario__DOT__ram_b_q;
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_c 
        = (7U & (IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vo));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_r 
        = (0xfU & ((IData)(vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vo) 
                   >> 3U));
    vlSelfRef.copro_sel = ((IData)(vlSelfRef.enable) 
                           & (0x5000U == (0xfe00U & (IData)(vlSelfRef.prg_ain))));
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
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT____Vcellinp__ALU__BCD 
        = ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__adc_bcd) 
           & (0xdU == (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state)));
    __Vtableidx2 = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__store) 
                     << 6U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state));
    vlSelfRef.CoproDrMario__DOT__WE = VCoproDrMario__ConstPool__TABLE_h3046dbb4_0
        [__Vtableidx2];
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
    vlSelfRef.CoproDrMario__DOT____VdfgRegularize_hb6d3a560_2_3 
        = ((~ (IData)(vlSelfRef.CoproDrMario__DOT__cpu_rst)) 
           & (IData)(vlSelfRef.CoproDrMario__DOT__WE));
    vlSelfRef.CoproDrMario__DOT__leafeval__DOT__v_col 
        = vlSelfRef.CoproDrMario__DOT__leafeval__DOT__col_of
        [vlSelfRef.CoproDrMario__DOT__leafeval__DOT__vo];
    CoproDrMario__DOT__cpu6502__DOT____VdfgExtracted_hdce86eaa__0 
        = (0x100U | vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AXYS
           [vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__regsel]);
    CoproDrMario__DOT__cpu6502__DOT__regfile = vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__AXYS
        [vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__regsel];
    vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IR = 
        ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__NMI_edge)
          ? 0U : ((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IRHOLD_valid)
                   ? (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__IRHOLD)
                   : (IData)(vlSelfRef.CoproDrMario__DOT__DI)));
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

VL_ATTR_COLD void VCoproDrMario___024root___eval_triggers__stl(VCoproDrMario___024root* vlSelf);

VL_ATTR_COLD bool VCoproDrMario___024root___eval_phase__stl(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___eval_phase__stl\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VstlExecute;
    // Body
    VCoproDrMario___024root___eval_triggers__stl(vlSelf);
    __VstlExecute = vlSelfRef.__VstlTriggered.any();
    if (__VstlExecute) {
        VCoproDrMario___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VCoproDrMario___024root___dump_triggers__ico(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___dump_triggers__ico\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VicoTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VicoTriggered.word(0U))) {
        VL_DBG_MSGF("         'ico' region trigger index 0 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void VCoproDrMario___024root___dump_triggers__act(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___dump_triggers__act\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VactTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 0 is active: @(posedge clk_cpu)\n");
    }
    if ((2ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 1 is active: @(posedge clk)\n");
    }
    if ((4ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 2 is active: @(posedge CoproDrMario.cpu_rst)\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void VCoproDrMario___024root___dump_triggers__nba(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___dump_triggers__nba\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VnbaTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 0 is active: @(posedge clk_cpu)\n");
    }
    if ((2ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 1 is active: @(posedge clk)\n");
    }
    if ((4ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 2 is active: @(posedge CoproDrMario.cpu_rst)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void VCoproDrMario___024root___ctor_var_reset(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___ctor_var_reset\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelf->clk = VL_RAND_RESET_I(1);
    vlSelf->clk_cpu = VL_RAND_RESET_I(1);
    vlSelf->ce = VL_RAND_RESET_I(1);
    vlSelf->enable = VL_RAND_RESET_I(1);
    vlSelf->prg_ain = VL_RAND_RESET_I(16);
    vlSelf->prg_read = VL_RAND_RESET_I(1);
    vlSelf->prg_write = VL_RAND_RESET_I(1);
    vlSelf->prg_din = VL_RAND_RESET_I(8);
    vlSelf->prg_dout = VL_RAND_RESET_I(8);
    vlSelf->copro_sel = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__AB = VL_RAND_RESET_I(16);
    vlSelf->CoproDrMario__DOT__DO = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__WE = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__rst_cnt = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__parked = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__rst_m = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu_rst = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__DI = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__a_ram = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__a_addr = VL_RAND_RESET_I(12);
    vlSelf->CoproDrMario__DOT__lev_start = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__lev_wr_arg = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__lev_enc = VL_RAND_RESET_I(3);
    vlSelf->CoproDrMario__DOT__lev_colenc = VL_RAND_RESET_I(2);
    vlSelf->CoproDrMario__DOT__lev_wslot = VL_RAND_RESET_I(2);
    vlSelf->CoproDrMario__DOT__lev_a_o4 = VL_RAND_RESET_I(2);
    vlSelf->CoproDrMario__DOT__lev_a_sl = VL_RAND_RESET_I(2);
    vlSelf->CoproDrMario__DOT__lev_a_ca = VL_RAND_RESET_I(2);
    vlSelf->CoproDrMario__DOT__lev_a_cb = VL_RAND_RESET_I(2);
    vlSelf->CoproDrMario__DOT__lev_a_col = VL_RAND_RESET_I(3);
    vlSelf->CoproDrMario__DOT__lev_done = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__lev_win = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__lev_legal = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__lev_sco = VL_RAND_RESET_I(16);
    vlSelf->CoproDrMario__DOT__lev_imm = VL_RAND_RESET_I(16);
    vlSelf->CoproDrMario__DOT__lev_rvc = VL_RAND_RESET_I(6);
    vlSelf->CoproDrMario__DOT__lev_rvv = VL_RAND_RESET_I(4);
    vlSelf->CoproDrMario__DOT__lev_q = VL_RAND_RESET_I(8);
    for (int __Vi0 = 0; __Vi0 < 16384; ++__Vi0) {
        vlSelf->CoproDrMario__DOT__rom[__Vi0] = VL_RAND_RESET_I(8);
    }
    vlSelf->CoproDrMario__DOT__rom_q = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__ram_a_q = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__ram_b_q = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__sel_ram_d = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__sel_rom_d = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__sel_vec_d = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__sel_lev_d = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__ab0_d = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__hb_addr = VL_RAND_RESET_I(12);
    vlSelf->CoproDrMario__DOT__hb_din = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__hb_we = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT____VdfgRegularize_hb6d3a560_2_2 = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT____VdfgRegularize_hb6d3a560_2_3 = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__PC = VL_RAND_RESET_I(16);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__ABL = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__ABH = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__ADD = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__IRHOLD = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__IRHOLD_valid = VL_RAND_RESET_I(1);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->CoproDrMario__DOT__cpu6502__DOT__AXYS[__Vi0] = VL_RAND_RESET_I(8);
    }
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__C = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__Z = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__I = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__D = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__V = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__N = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__AN = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__HC = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__AI = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__IR = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__CO = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__NMI_edge = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__regsel = VL_RAND_RESET_I(2);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__P = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__state = VL_RAND_RESET_I(6);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__PC_inc = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__PC_temp = VL_RAND_RESET_I(16);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__src_reg = VL_RAND_RESET_I(2);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__dst_reg = VL_RAND_RESET_I(2);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__index_y = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__load_reg = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__inc = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__write_back = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__load_only = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__store = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__adc_sbc = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__compare = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__shift = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__rotate = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__backwards = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__cond_true = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__cond_code = VL_RAND_RESET_I(3);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__shift_right = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__op = VL_RAND_RESET_I(4);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__adc_bcd = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__adj_bcd = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__bit_ins = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__plp = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__php = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__clc = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__sec = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__cld = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__sed = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__cli = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__sei = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__clv = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__res = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__write_register = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT____Vcellinp__ALU__BCD = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__AI7 = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__BI7 = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_BI = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_h = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp = VL_RAND_RESET_I(9);
    vlSelf->CoproDrMario__DOT__cpu6502__DOT__ALU__DOT__temp_HC = VL_RAND_RESET_I(1);
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->CoproDrMario__DOT__leafeval__DOT__bcell[__Vi0] = VL_RAND_RESET_I(3);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->CoproDrMario__DOT__leafeval__DOT__s_live[__Vi0] = VL_RAND_RESET_I(3);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->CoproDrMario__DOT__leafeval__DOT__s_w1[__Vi0] = VL_RAND_RESET_I(3);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->CoproDrMario__DOT__leafeval__DOT__s_w2[__Vi0] = VL_RAND_RESET_I(3);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->CoproDrMario__DOT__leafeval__DOT__col_of[__Vi0] = VL_RAND_RESET_I(2);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->CoproDrMario__DOT__leafeval__DOT__occ_of[__Vi0] = VL_RAND_RESET_I(1);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->CoproDrMario__DOT__leafeval__DOT__vir_of[__Vi0] = VL_RAND_RESET_I(1);
    }
    vlSelf->CoproDrMario__DOT__leafeval__DOT__st = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__node_leaf = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__fo1 = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__fwp = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__off_a = VL_RAND_RESET_I(7);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__off_b = VL_RAND_RESET_I(7);
    VL_RAND_RESET_W(128, vlSelf->CoproDrMario__DOT__leafeval__DOT__markb);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__li = VL_RAND_RESET_I(2);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__soff = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__sstep = VL_RAND_RESET_I(4);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__scnt = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__srun = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__smcol = VL_RAND_RESET_I(2);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__srstart = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__fwp2 = VL_RAND_RESET_I(7);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__gdest = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__anyclear = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__wc = VL_RAND_RESET_I(4);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__wr_ = VL_RAND_RESET_I(4);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__maxh = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__holes = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__toprisk = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__spawn = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__setup = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__pollution = VL_RAND_RESET_I(11);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__buried = VL_RAND_RESET_I(10);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__rdy_ext = VL_RAND_RESET_I(16);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__vrdy = VL_RAND_RESET_I(16);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__anyvir = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__seen = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__fillcnt = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__vo = VL_RAND_RESET_I(7);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__v_r = VL_RAND_RESET_I(4);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__v_c = VL_RAND_RESET_I(3);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__v_col = VL_RAND_RESET_I(2);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__run_h = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__run_v = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__p = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__span_lo = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__span_hi = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__vspan_lo = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__vspan_hi = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__i = VL_RAND_RESET_I(32);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__fo2b__DOT__fom = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__scan__DOT__brk = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__scan__DOT__c_ = VL_RAND_RESET_I(2);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__grv__DOT__t = VL_RAND_RESET_I(3);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__fin__DOT__hq = VL_RAND_RESET_I(9);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__fin__DOT__vq = VL_RAND_RESET_I(9);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__fin__DOT__mx = VL_RAND_RESET_I(9);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__suh__DOT__c0 = VL_RAND_RESET_I(2);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__suh__DOT__t = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__suv__DOT__c0 = VL_RAND_RESET_I(2);
    vlSelf->CoproDrMario__DOT__leafeval__DOT__suv__DOT__t = VL_RAND_RESET_I(1);
    for (int __Vi0 = 0; __Vi0 < 4096; ++__Vi0) {
        vlSelf->CoproDrMario__DOT__wram__DOT__mem[__Vi0] = VL_RAND_RESET_I(8);
    }
    vlSelf->__Vdly__CoproDrMario__DOT__rst_cnt = VL_RAND_RESET_I(5);
    vlSelf->__Vdly__CoproDrMario__DOT__cpu6502__DOT__state = VL_RAND_RESET_I(6);
    vlSelf->__VdlyVal__CoproDrMario__DOT__wram__DOT__mem__v0 = VL_RAND_RESET_I(8);
    vlSelf->__VdlyDim0__CoproDrMario__DOT__wram__DOT__mem__v0 = VL_RAND_RESET_I(12);
    vlSelf->__VdlySet__CoproDrMario__DOT__wram__DOT__mem__v0 = 0;
    vlSelf->__VdlyVal__CoproDrMario__DOT__wram__DOT__mem__v1 = VL_RAND_RESET_I(8);
    vlSelf->__VdlyDim0__CoproDrMario__DOT__wram__DOT__mem__v1 = VL_RAND_RESET_I(12);
    vlSelf->__VdlySet__CoproDrMario__DOT__wram__DOT__mem__v1 = 0;
    vlSelf->__Vtrigprevexpr___TOP__clk_cpu__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__CoproDrMario__DOT__cpu_rst__0 = VL_RAND_RESET_I(1);
}
