#include "PPSTools/EfficiencyCorrection/interface/MiniEvent.h"
#include <iostream>

void createMiniEventTree(TTree *t,MiniEvent_t &ev)
{

  //event header
  t->Branch("run",       &ev.run,      "run/i");
  t->Branch("event",     &ev.event,    "event/l");
  t->Branch("betaStar",     &ev.betaStar,    "betaStar/F");
  t->Branch("fill",     &ev.fill,    "fill/i");
  t->Branch("lumi",      &ev.lumi,     "lumi/i");
  t->Branch("beamXangle",  &ev.beamXangle,   "beamXangle/F");
  t->Branch("instLumi",    &ev.instLumi,     "instLumi/F");

}

void attachToMiniEventTree(TTree *t,MiniEvent_t &ev)
{

  //event header

  t->SetBranchAddress("run",       &ev.run);
  t->SetBranchAddress("event",     &ev.event);
  t->SetBranchAddress("fill",      &ev.fill);
  t->SetBranchAddress("lumi",      &ev.lumi);
  t->SetBranchAddress("betaStar",      &ev.betaStar);
  t->SetBranchAddress("beamXangle",  &ev.beamXangle);
  t->SetBranchAddress("instLumi",    &ev.instLumi);

}

