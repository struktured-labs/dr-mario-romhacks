// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "VLeafEval__pch.h"

//============================================================
// Constructors

VLeafEval::VLeafEval(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new VLeafEval__Syms(contextp(), _vcname__, this)}
    , clk{vlSymsp->TOP.clk}
    , rst{vlSymsp->TOP.rst}
    , wr{vlSymsp->TOP.wr}
    , waddr{vlSymsp->TOP.waddr}
    , wdata{vlSymsp->TOP.wdata}
    , wslot{vlSymsp->TOP.wslot}
    , start{vlSymsp->TOP.start}
    , cmd{vlSymsp->TOP.cmd}
    , cmd_go{vlSymsp->TOP.cmd_go}
    , a_sl{vlSymsp->TOP.a_sl}
    , a_o4{vlSymsp->TOP.a_o4}
    , a_col{vlSymsp->TOP.a_col}
    , a_ca{vlSymsp->TOP.a_ca}
    , a_cb{vlSymsp->TOP.a_cb}
    , done{vlSymsp->TOP.done}
    , win{vlSymsp->TOP.win}
    , legal{vlSymsp->TOP.legal}
    , rv_cells{vlSymsp->TOP.rv_cells}
    , rv_vir{vlSymsp->TOP.rv_vir}
    , sco{vlSymsp->TOP.sco}
    , imm{vlSymsp->TOP.imm}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

VLeafEval::VLeafEval(const char* _vcname__)
    : VLeafEval(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

VLeafEval::~VLeafEval() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void VLeafEval___024root___eval_debug_assertions(VLeafEval___024root* vlSelf);
#endif  // VL_DEBUG
void VLeafEval___024root___eval_static(VLeafEval___024root* vlSelf);
void VLeafEval___024root___eval_initial(VLeafEval___024root* vlSelf);
void VLeafEval___024root___eval_settle(VLeafEval___024root* vlSelf);
void VLeafEval___024root___eval(VLeafEval___024root* vlSelf);

void VLeafEval::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate VLeafEval::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    VLeafEval___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        vlSymsp->__Vm_didInit = true;
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        VLeafEval___024root___eval_static(&(vlSymsp->TOP));
        VLeafEval___024root___eval_initial(&(vlSymsp->TOP));
        VLeafEval___024root___eval_settle(&(vlSymsp->TOP));
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    VLeafEval___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool VLeafEval::eventsPending() { return false; }

uint64_t VLeafEval::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* VLeafEval::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void VLeafEval___024root___eval_final(VLeafEval___024root* vlSelf);

VL_ATTR_COLD void VLeafEval::final() {
    VLeafEval___024root___eval_final(&(vlSymsp->TOP));
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* VLeafEval::hierName() const { return vlSymsp->name(); }
const char* VLeafEval::modelName() const { return "VLeafEval"; }
unsigned VLeafEval::threads() const { return 1; }
void VLeafEval::prepareClone() const { contextp()->prepareClone(); }
void VLeafEval::atClone() const {
    contextp()->threadPoolpOnClone();
}
