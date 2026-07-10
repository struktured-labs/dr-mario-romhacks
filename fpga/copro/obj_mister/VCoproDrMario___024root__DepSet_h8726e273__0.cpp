// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VCoproDrMario.h for the primary calling header

#include "VCoproDrMario__pch.h"
#include "VCoproDrMario__Syms.h"
#include "VCoproDrMario___024root.h"

#ifdef VL_DEBUG
VL_ATTR_COLD void VCoproDrMario___024root___dump_triggers__ico(VCoproDrMario___024root* vlSelf);
#endif  // VL_DEBUG

void VCoproDrMario___024root___eval_triggers__ico(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___eval_triggers__ico\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VicoTriggered.set(0U, (IData)(vlSelfRef.__VicoFirstIteration));
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        VCoproDrMario___024root___dump_triggers__ico(vlSelf);
    }
#endif
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VCoproDrMario___024root___dump_triggers__act(VCoproDrMario___024root* vlSelf);
#endif  // VL_DEBUG

void VCoproDrMario___024root___eval_triggers__act(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___eval_triggers__act\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VactTriggered.set(0U, ((IData)(vlSelfRef.clk_cpu) 
                                       & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk_cpu__0))));
    vlSelfRef.__VactTriggered.set(1U, ((IData)(vlSelfRef.clk) 
                                       & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk__0))));
    vlSelfRef.__VactTriggered.set(2U, ((IData)(vlSelfRef.CoproDrMario__DOT__cpu_rst) 
                                       & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__CoproDrMario__DOT__cpu_rst__0))));
    vlSelfRef.__Vtrigprevexpr___TOP__clk_cpu__0 = vlSelfRef.clk_cpu;
    vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__CoproDrMario__DOT__cpu_rst__0 
        = vlSelfRef.CoproDrMario__DOT__cpu_rst;
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        VCoproDrMario___024root___dump_triggers__act(vlSelf);
    }
#endif
}
