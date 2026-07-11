// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "VLeafEval__pch.h"
#include "VLeafEval.h"
#include "VLeafEval___024root.h"

// FUNCTIONS
VLeafEval__Syms::~VLeafEval__Syms()
{
}

VLeafEval__Syms::VLeafEval__Syms(VerilatedContext* contextp, const char* namep, VLeafEval* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup module instances
    , TOP{this, namep}
{
        // Check resources
        Verilated::stackCheck(204);
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-12);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscope_LeafEval.configure(this, name(), "LeafEval", "LeafEval", "<null>", 0, VerilatedScope::SCOPE_OTHER);
    // Setup export functions
    for (int __Vfinal = 0; __Vfinal < 2; ++__Vfinal) {
        __Vscope_LeafEval.varInsert(__Vfinal,"bcell", &(TOP.LeafEval__DOT__bcell), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RD,2 ,2,0 ,0,127);
        __Vscope_LeafEval.varInsert(__Vfinal,"buried", &(TOP.LeafEval__DOT__buried), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RD,1 ,9,0);
        __Vscope_LeafEval.varInsert(__Vfinal,"holes", &(TOP.LeafEval__DOT__holes), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RD,1 ,7,0);
        __Vscope_LeafEval.varInsert(__Vfinal,"maxh", &(TOP.LeafEval__DOT__maxh), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RD,1 ,4,0);
        __Vscope_LeafEval.varInsert(__Vfinal,"pollution", &(TOP.LeafEval__DOT__pollution), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RD,1 ,10,0);
        __Vscope_LeafEval.varInsert(__Vfinal,"rdy_ext", &(TOP.LeafEval__DOT__rdy_ext), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RD,1 ,15,0);
        __Vscope_LeafEval.varInsert(__Vfinal,"setup", &(TOP.LeafEval__DOT__setup), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RD,1 ,7,0);
        __Vscope_LeafEval.varInsert(__Vfinal,"spawn", &(TOP.LeafEval__DOT__spawn), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RD,1 ,7,0);
        __Vscope_LeafEval.varInsert(__Vfinal,"toprisk", &(TOP.LeafEval__DOT__toprisk), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RD,1 ,7,0);
        __Vscope_LeafEval.varInsert(__Vfinal,"vrdy", &(TOP.LeafEval__DOT__vrdy), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RD,1 ,15,0);
    }
}
