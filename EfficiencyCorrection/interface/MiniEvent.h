#ifndef _minievent_h_
#define _minievent_h_

#include "TTree.h"

struct MiniEvent_t
{
  MiniEvent_t(){}
  
  static const int MAXPROTONS   =  50;

  UInt_t run,lumi,fill;
  ULong64_t event;
  Float_t beamXangle, instLumi, betaStar;

};

void createMiniEventTree(TTree *t,MiniEvent_t &ev);
void attachToMiniEventTree(TTree *t, MiniEvent_t &ev);

#endif
