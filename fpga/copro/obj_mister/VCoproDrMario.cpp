// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "VCoproDrMario__pch.h"

//============================================================
// Constructors

VCoproDrMario::VCoproDrMario(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new VCoproDrMario__Syms(contextp(), _vcname__, this)}
    , clk{vlSymsp->TOP.clk}
    , clk_cpu{vlSymsp->TOP.clk_cpu}
    , ce{vlSymsp->TOP.ce}
    , enable{vlSymsp->TOP.enable}
    , prg_read{vlSymsp->TOP.prg_read}
    , prg_write{vlSymsp->TOP.prg_write}
    , prg_din{vlSymsp->TOP.prg_din}
    , prg_dout{vlSymsp->TOP.prg_dout}
    , copro_sel{vlSymsp->TOP.copro_sel}
    , prg_ain{vlSymsp->TOP.prg_ain}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

VCoproDrMario::VCoproDrMario(const char* _vcname__)
    : VCoproDrMario(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

VCoproDrMario::~VCoproDrMario() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void VCoproDrMario___024root___eval_debug_assertions(VCoproDrMario___024root* vlSelf);
#endif  // VL_DEBUG
void VCoproDrMario___024root___eval_static(VCoproDrMario___024root* vlSelf);
void VCoproDrMario___024root___eval_initial(VCoproDrMario___024root* vlSelf);
void VCoproDrMario___024root___eval_settle(VCoproDrMario___024root* vlSelf);
void VCoproDrMario___024root___eval(VCoproDrMario___024root* vlSelf);

void VCoproDrMario::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate VCoproDrMario::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    VCoproDrMario___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        vlSymsp->__Vm_didInit = true;
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        VCoproDrMario___024root___eval_static(&(vlSymsp->TOP));
        VCoproDrMario___024root___eval_initial(&(vlSymsp->TOP));
        VCoproDrMario___024root___eval_settle(&(vlSymsp->TOP));
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    VCoproDrMario___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool VCoproDrMario::eventsPending() { return false; }

uint64_t VCoproDrMario::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* VCoproDrMario::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void VCoproDrMario___024root___eval_final(VCoproDrMario___024root* vlSelf);

VL_ATTR_COLD void VCoproDrMario::final() {
    VCoproDrMario___024root___eval_final(&(vlSymsp->TOP));
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* VCoproDrMario::hierName() const { return vlSymsp->name(); }
const char* VCoproDrMario::modelName() const { return "VCoproDrMario"; }
unsigned VCoproDrMario::threads() const { return 1; }
void VCoproDrMario::prepareClone() const { contextp()->prepareClone(); }
void VCoproDrMario::atClone() const {
    contextp()->threadPoolpOnClone();
}
