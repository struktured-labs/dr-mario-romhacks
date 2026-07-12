// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VLeafEval.h for the primary calling header

#include "VLeafEval__pch.h"
#include "VLeafEval__Syms.h"
#include "VLeafEval___024root.h"

#ifdef VL_DEBUG
VL_ATTR_COLD void VLeafEval___024root___dump_triggers__ico(VLeafEval___024root* vlSelf);
#endif  // VL_DEBUG

void VLeafEval___024root___eval_triggers__ico(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___eval_triggers__ico\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VicoTriggered.set(0U, (IData)(vlSelfRef.__VicoFirstIteration));
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        VLeafEval___024root___dump_triggers__ico(vlSelf);
    }
#endif
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VLeafEval___024root___dump_triggers__act(VLeafEval___024root* vlSelf);
#endif  // VL_DEBUG

void VLeafEval___024root___eval_triggers__act(VLeafEval___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VLeafEval__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VLeafEval___024root___eval_triggers__act\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VactTriggered.set(0U, ((IData)(vlSelfRef.clk) 
                                       & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk__0))));
    vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        VLeafEval___024root___dump_triggers__act(vlSelf);
    }
#endif
}
