// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VLeafEval.h for the primary calling header

#include "VLeafEval__pch.h"
#include "VLeafEval___024root.h"

VL_ATTR_COLD void VLeafEval___024root___eval_static(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___eval_static\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void VLeafEval___024root___eval_initial(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___eval_initial\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
}

VL_ATTR_COLD void VLeafEval___024root___eval_final(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___eval_final\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VLeafEval___024root___dump_triggers__stl(VLeafEval___024root* vlSelf);
#endif  // VL_DEBUG
VL_ATTR_COLD bool VLeafEval___024root___eval_phase__stl(VLeafEval___024root* vlSelf);

VL_ATTR_COLD void VLeafEval___024root___eval_settle(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___eval_settle\n"); );
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
            VLeafEval___024root___dump_triggers__stl(vlSelf);
#endif
            VL_FATAL_MT("LeafEval.sv", 14, "", "Settle region did not converge.");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        __VstlContinue = 0U;
        if (VLeafEval___024root___eval_phase__stl(vlSelf)) {
            __VstlContinue = 1U;
        }
        vlSelfRef.__VstlFirstIteration = 0U;
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VLeafEval___024root___dump_triggers__stl(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___dump_triggers__stl\n"); );
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

VL_ATTR_COLD void VLeafEval___024root___stl_sequent__TOP__0(VLeafEval___024root* vlSelf);

VL_ATTR_COLD void VLeafEval___024root___eval_stl(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___eval_stl\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VstlTriggered.word(0U))) {
        VLeafEval___024root___stl_sequent__TOP__0(vlSelf);
    }
}

VL_ATTR_COLD void VLeafEval___024root___stl_sequent__TOP__0(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___stl_sequent__TOP__0\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.LeafEval__DOT__v_c = (7U & (IData)(vlSelfRef.LeafEval__DOT__vo));
    vlSelfRef.LeafEval__DOT__v_r = (0xfU & ((IData)(vlSelfRef.LeafEval__DOT__vo) 
                                            >> 3U));
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
    vlSelfRef.LeafEval__DOT__v_col = vlSelfRef.LeafEval__DOT__col_of
        [vlSelfRef.LeafEval__DOT__vo];
}

VL_ATTR_COLD void VLeafEval___024root___eval_triggers__stl(VLeafEval___024root* vlSelf);

VL_ATTR_COLD bool VLeafEval___024root___eval_phase__stl(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___eval_phase__stl\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VstlExecute;
    // Body
    VLeafEval___024root___eval_triggers__stl(vlSelf);
    __VstlExecute = vlSelfRef.__VstlTriggered.any();
    if (__VstlExecute) {
        VLeafEval___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VLeafEval___024root___dump_triggers__act(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___dump_triggers__act\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VactTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 0 is active: @(posedge clk)\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void VLeafEval___024root___dump_triggers__nba(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___dump_triggers__nba\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VnbaTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 0 is active: @(posedge clk)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void VLeafEval___024root___ctor_var_reset(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___ctor_var_reset\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelf->clk = VL_RAND_RESET_I(1);
    vlSelf->rst = VL_RAND_RESET_I(1);
    vlSelf->wr = VL_RAND_RESET_I(1);
    vlSelf->waddr = VL_RAND_RESET_I(7);
    vlSelf->wdata = VL_RAND_RESET_I(3);
    vlSelf->wslot = VL_RAND_RESET_I(2);
    vlSelf->start = VL_RAND_RESET_I(1);
    vlSelf->cmd = VL_RAND_RESET_I(4);
    vlSelf->cmd_go = VL_RAND_RESET_I(1);
    vlSelf->a_sl = VL_RAND_RESET_I(2);
    vlSelf->a_o4 = VL_RAND_RESET_I(2);
    vlSelf->a_col = VL_RAND_RESET_I(3);
    vlSelf->a_ca = VL_RAND_RESET_I(2);
    vlSelf->a_cb = VL_RAND_RESET_I(2);
    vlSelf->done = VL_RAND_RESET_I(1);
    vlSelf->sco = VL_RAND_RESET_I(16);
    vlSelf->win = VL_RAND_RESET_I(1);
    vlSelf->legal = VL_RAND_RESET_I(1);
    vlSelf->rv_cells = VL_RAND_RESET_I(6);
    vlSelf->rv_vir = VL_RAND_RESET_I(4);
    vlSelf->imm = VL_RAND_RESET_I(16);
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->LeafEval__DOT__bcell[__Vi0] = VL_RAND_RESET_I(3);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->LeafEval__DOT__s_live[__Vi0] = VL_RAND_RESET_I(3);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->LeafEval__DOT__s_w1[__Vi0] = VL_RAND_RESET_I(3);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->LeafEval__DOT__s_w2[__Vi0] = VL_RAND_RESET_I(3);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->LeafEval__DOT__col_of[__Vi0] = VL_RAND_RESET_I(2);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->LeafEval__DOT__occ_of[__Vi0] = VL_RAND_RESET_I(1);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->LeafEval__DOT__vir_of[__Vi0] = VL_RAND_RESET_I(1);
    }
    vlSelf->LeafEval__DOT__st = VL_RAND_RESET_I(5);
    vlSelf->LeafEval__DOT__node_leaf = VL_RAND_RESET_I(1);
    vlSelf->LeafEval__DOT__fo1 = VL_RAND_RESET_I(5);
    vlSelf->LeafEval__DOT__fwp = VL_RAND_RESET_I(5);
    vlSelf->LeafEval__DOT__off_a = VL_RAND_RESET_I(7);
    vlSelf->LeafEval__DOT__off_b = VL_RAND_RESET_I(7);
    VL_RAND_RESET_W(128, vlSelf->LeafEval__DOT__markb);
    vlSelf->LeafEval__DOT__li = VL_RAND_RESET_I(2);
    vlSelf->LeafEval__DOT__soff = VL_RAND_RESET_I(8);
    vlSelf->LeafEval__DOT__sstep = VL_RAND_RESET_I(4);
    vlSelf->LeafEval__DOT__scnt = VL_RAND_RESET_I(5);
    vlSelf->LeafEval__DOT__srun = VL_RAND_RESET_I(5);
    vlSelf->LeafEval__DOT__smcol = VL_RAND_RESET_I(2);
    vlSelf->LeafEval__DOT__srstart = VL_RAND_RESET_I(8);
    vlSelf->LeafEval__DOT__fwp2 = VL_RAND_RESET_I(7);
    vlSelf->LeafEval__DOT__gdest = VL_RAND_RESET_I(5);
    vlSelf->LeafEval__DOT__anyclear = VL_RAND_RESET_I(1);
    vlSelf->LeafEval__DOT__wc = VL_RAND_RESET_I(4);
    vlSelf->LeafEval__DOT__wr_ = VL_RAND_RESET_I(4);
    vlSelf->LeafEval__DOT__maxh = VL_RAND_RESET_I(5);
    vlSelf->LeafEval__DOT__holes = VL_RAND_RESET_I(8);
    vlSelf->LeafEval__DOT__toprisk = VL_RAND_RESET_I(8);
    vlSelf->LeafEval__DOT__spawn = VL_RAND_RESET_I(8);
    vlSelf->LeafEval__DOT__setup = VL_RAND_RESET_I(8);
    vlSelf->LeafEval__DOT__pollution = VL_RAND_RESET_I(11);
    vlSelf->LeafEval__DOT__buried = VL_RAND_RESET_I(10);
    vlSelf->LeafEval__DOT__rdy_ext = VL_RAND_RESET_I(16);
    vlSelf->LeafEval__DOT__vrdy = VL_RAND_RESET_I(16);
    vlSelf->LeafEval__DOT__anyvir = VL_RAND_RESET_I(1);
    vlSelf->LeafEval__DOT__seen = VL_RAND_RESET_I(1);
    vlSelf->LeafEval__DOT__fillcnt = VL_RAND_RESET_I(5);
    vlSelf->LeafEval__DOT__vo = VL_RAND_RESET_I(7);
    vlSelf->LeafEval__DOT__v_r = VL_RAND_RESET_I(4);
    vlSelf->LeafEval__DOT__v_c = VL_RAND_RESET_I(3);
    vlSelf->LeafEval__DOT__v_col = VL_RAND_RESET_I(2);
    vlSelf->LeafEval__DOT__run_h = VL_RAND_RESET_I(5);
    vlSelf->LeafEval__DOT__run_v = VL_RAND_RESET_I(5);
    vlSelf->LeafEval__DOT__p = VL_RAND_RESET_I(5);
    vlSelf->LeafEval__DOT__span_lo = VL_RAND_RESET_I(5);
    vlSelf->LeafEval__DOT__span_hi = VL_RAND_RESET_I(5);
    vlSelf->LeafEval__DOT__vspan_lo = VL_RAND_RESET_I(5);
    vlSelf->LeafEval__DOT__vspan_hi = VL_RAND_RESET_I(5);
    vlSelf->LeafEval__DOT__i = VL_RAND_RESET_I(32);
    vlSelf->LeafEval__DOT__fo2b__DOT__fom = VL_RAND_RESET_I(5);
    vlSelf->LeafEval__DOT__scan__DOT__brk = VL_RAND_RESET_I(1);
    vlSelf->LeafEval__DOT__scan__DOT__c_ = VL_RAND_RESET_I(2);
    vlSelf->LeafEval__DOT__grv__DOT__t = VL_RAND_RESET_I(3);
    vlSelf->LeafEval__DOT__fin__DOT__hq = VL_RAND_RESET_I(9);
    vlSelf->LeafEval__DOT__fin__DOT__vq = VL_RAND_RESET_I(9);
    vlSelf->LeafEval__DOT__fin__DOT__mx = VL_RAND_RESET_I(9);
    vlSelf->LeafEval__DOT__suh__DOT__c0 = VL_RAND_RESET_I(2);
    vlSelf->LeafEval__DOT__suh__DOT__t = VL_RAND_RESET_I(1);
    vlSelf->LeafEval__DOT__suv__DOT__c0 = VL_RAND_RESET_I(2);
    vlSelf->LeafEval__DOT__suv__DOT__t = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__clk__0 = VL_RAND_RESET_I(1);
}
