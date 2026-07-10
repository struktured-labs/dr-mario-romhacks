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
extern const VlUnpacked<CData/*1:0*/, 2048> VCoproDrMario__ConstPool__TABLE_h8ffa5a2b_0;
extern const VlUnpacked<CData/*3:0*/, 2048> VCoproDrMario__ConstPool__TABLE_h00ffe440_0;

VL_ATTR_COLD void VCoproDrMario___024root___stl_sequent__TOP__0(VCoproDrMario___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    VCoproDrMario__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VCoproDrMario___024root___stl_sequent__TOP__0\n"); );
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
    CData/*6:0*/ __Vtableidx8;
    __Vtableidx8 = 0;
    // Body
    vlSelfRef.prg_dout = vlSelfRef.CoproDrMario__DOT__ram_b_q;
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
    __Vtableidx2 = (((IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__store) 
                     << 6U) | (IData)(vlSelfRef.CoproDrMario__DOT__cpu6502__DOT__state));
    CoproDrMario__DOT__WE = VCoproDrMario__ConstPool__TABLE_h3046dbb4_0
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
    vlSelfRef.CoproDrMario__DOT__DI = ((IData)(vlSelfRef.CoproDrMario__DOT__sel_vec_d)
                                        ? ((IData)(vlSelfRef.CoproDrMario__DOT__ab0_d)
                                            ? 0xbfU
                                            : 0x80U)
                                        : ((IData)(vlSelfRef.CoproDrMario__DOT__sel_rom_d)
                                            ? (IData)(vlSelfRef.CoproDrMario__DOT__rom_q)
                                            : ((IData)(vlSelfRef.CoproDrMario__DOT__sel_ram_d)
                                                ? (IData)(vlSelfRef.CoproDrMario__DOT__ram_a_q)
                                                : 0xffU)));
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
    vlSelf->CoproDrMario__DOT__rst_cnt = VL_RAND_RESET_I(5);
    vlSelf->CoproDrMario__DOT__parked = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__rst_m = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__cpu_rst = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__DI = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__a_ram = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__a_addr = VL_RAND_RESET_I(12);
    for (int __Vi0 = 0; __Vi0 < 16384; ++__Vi0) {
        vlSelf->CoproDrMario__DOT__rom[__Vi0] = VL_RAND_RESET_I(8);
    }
    vlSelf->CoproDrMario__DOT__rom_q = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__ram_a_q = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__ram_b_q = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT____Vcellinp__wram__wren_a = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__sel_ram_d = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__sel_rom_d = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__sel_vec_d = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__ab0_d = VL_RAND_RESET_I(1);
    vlSelf->CoproDrMario__DOT__hb_addr = VL_RAND_RESET_I(12);
    vlSelf->CoproDrMario__DOT__hb_din = VL_RAND_RESET_I(8);
    vlSelf->CoproDrMario__DOT__hb_we = VL_RAND_RESET_I(1);
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
