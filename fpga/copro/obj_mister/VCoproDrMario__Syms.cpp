// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "VCoproDrMario__pch.h"
#include "VCoproDrMario.h"
#include "VCoproDrMario___024root.h"

// FUNCTIONS
VCoproDrMario__Syms::~VCoproDrMario__Syms()
{
}

VCoproDrMario__Syms::VCoproDrMario__Syms(VerilatedContext* contextp, const char* namep, VCoproDrMario* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup module instances
    , TOP{this, namep}
{
        // Check resources
        Verilated::stackCheck(337);
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-12);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscope_CoproDrMario__leafeval.configure(this, name(), "CoproDrMario.leafeval", "leafeval", "<null>", 0, VerilatedScope::SCOPE_OTHER);
    // Setup export functions
    for (int __Vfinal = 0; __Vfinal < 2; ++__Vfinal) {
        __Vscope_CoproDrMario__leafeval.varInsert(__Vfinal,"bcell", &(TOP.CoproDrMario__DOT__leafeval__DOT__bcell), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RD,2 ,2,0 ,0,127);
        __Vscope_CoproDrMario__leafeval.varInsert(__Vfinal,"buried", &(TOP.CoproDrMario__DOT__leafeval__DOT__buried), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RD,1 ,9,0);
        __Vscope_CoproDrMario__leafeval.varInsert(__Vfinal,"holes", &(TOP.CoproDrMario__DOT__leafeval__DOT__holes), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RD,1 ,7,0);
        __Vscope_CoproDrMario__leafeval.varInsert(__Vfinal,"maxh", &(TOP.CoproDrMario__DOT__leafeval__DOT__maxh), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RD,1 ,4,0);
        __Vscope_CoproDrMario__leafeval.varInsert(__Vfinal,"pollution", &(TOP.CoproDrMario__DOT__leafeval__DOT__pollution), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RD,1 ,10,0);
        __Vscope_CoproDrMario__leafeval.varInsert(__Vfinal,"rdy_ext", &(TOP.CoproDrMario__DOT__leafeval__DOT__rdy_ext), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RD,1 ,15,0);
        __Vscope_CoproDrMario__leafeval.varInsert(__Vfinal,"setup", &(TOP.CoproDrMario__DOT__leafeval__DOT__setup), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RD,1 ,7,0);
        __Vscope_CoproDrMario__leafeval.varInsert(__Vfinal,"spawn", &(TOP.CoproDrMario__DOT__leafeval__DOT__spawn), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RD,1 ,7,0);
        __Vscope_CoproDrMario__leafeval.varInsert(__Vfinal,"toprisk", &(TOP.CoproDrMario__DOT__leafeval__DOT__toprisk), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RD,1 ,7,0);
        __Vscope_CoproDrMario__leafeval.varInsert(__Vfinal,"vrdy", &(TOP.CoproDrMario__DOT__leafeval__DOT__vrdy), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RD,1 ,15,0);
    }
}
