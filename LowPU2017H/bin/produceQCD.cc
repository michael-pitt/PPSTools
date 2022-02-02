#include <iostream>
#include <algorithm>

/*
Code was developed for LowPU analysis
Code will read data file and generate data-driven QCD estimation in two steps:

1. Calculate the fake-factors (FF)
2. generate a new output file with weights replaced by the FF
Example:
produceQCD /eos/cms/store/cmst3/group/top/low_mu_data/nano_output_22_01_26/data/SingleMuon_mu.root
*/

#include <TString.h>
#include <TFile.h>
#include <TTree.h>
#include <TChain.h>
#include <TH1F.h>
#include <TDirectory.h>
#include <TBranch.h>
#include <TRandom3.h>
#include <TMath.h>
#include "TSystem.h"

#define MAXLEP 5

#include <time.h>
using namespace std;

int main(int argc, char* argv[])
{
	
  // CMSSW settings  
  //const char* CMSSW_BASE = getenv("CMSSW_BASE");

  
  // Check arguments
  if (argc != 2) {
    cout << "ERROR: missing input file!" << endl
         << "Usage: " << argv[0] << " <inputfile> " << endl;
    return 0;
  }
  
  // Check input files
  if(gSystem->AccessPathName(argv[1])){
	  cout << "ERROR! Missing input file: " << argv[1] << endl;
	  return 0;
  }
  
  string inFileName = argv[1];
  string outFileName = inFileName.substr(inFileName.find_last_of('/') + 1, inFileName.find_last_of('.') - inFileName.find_last_of('/') - 1) + "_FakeLepton.root";
  //bool isSignal = TString(inFileName.c_str()).Contains("excl_ttbar") || TString(inFileName.c_str()).Contains("ExclusiveTTbar");
  
  // Load the input file:
  TFile *file = new TFile(inFileName.c_str());
  TTree * Events = (TTree *)file->Get("Events");
  
  
  // Calculate FF from the sample:
  float FF_nom=0, FF_denom=0;
  
  // variables used in the sample:
  int nlep;
  float lep_isolation[MAXLEP];
  bool lep_isIso[MAXLEP];
  int lep_id[MAXLEP];
  float mt;
  Events->SetBranchAddress("nano_WMT",&mt);
  Events->SetBranchAddress("nano_LepID",lep_id);
  Events->SetBranchAddress("nano_LepIsIso",lep_isIso);
  Events->SetBranchAddress("nano_LepIso",lep_isolation);
  Events->SetBranchAddress("nano_nLeptons",&nlep);
  
  int times,timed;
  times=time(NULL);  
  
  cout << "Calculate FF from the sample"<<endl;
  int iEntry; int nEntries = Events->GetEntries();
  for (iEntry = 0; iEntry < nEntries; iEntry++) {
	  if(iEntry%1000==0) printf ("\r [%3.0f%%] done", 100.*(float)iEntry/(float)nEntries);
	  Events->GetEntry(iEntry);
	  
	  // event selection
	  if (nlep!=1) continue;
	  if (mt>10) continue;
	  
	  // compute FF
	  bool pass = (inFileName.find("mu") != std::string::npos) ? lep_isIso[0] : (lep_id[0]==4);
	  if (!pass) FF_denom++;
	  else FF_nom++;
  }
  
  cout <<  endl << "Computed FF = " << FF_nom/FF_denom << endl;
  
  // Construct a new sample, with inverted lepton ISO and add appropriate weight
  TFile* fOut = new TFile(outFileName.c_str(), "RECREATE");
  TTree* tout = Events->CloneTree(0);
  
  // add weight 
  float weight = FF_nom/FF_denom;
  tout->Branch("nano_weight", &weight);

  cout << "Write new sample with updated event info"<<endl;
  for (iEntry = 0; iEntry < nEntries; iEntry++) {
	  if(iEntry%1000==0) printf ("\r [%3.0f%%] done", 100.*(float)iEntry/(float)nEntries);
	  Events->GetEntry(iEntry);
	  
	  // event selection
	  if (nlep!=1) continue;
	  if (mt<10) continue;
	  
	  // updated isolation and write the event
	  bool pass = (inFileName.find("mu") != std::string::npos) ? lep_isIso[0] : (lep_id[0]==4);
	  if (pass) continue;
	  if((inFileName.find("mu") != std::string::npos)){
		lep_isIso[0]=1;
		lep_isolation[0]=0;
	  }
	  else{
		  lep_id[0]=4;
	  }
	  
	  tout->Fill();
  }
  
  
  cout << "\nDone. " << iEntry << " events processed." << endl;
      timed=time(NULL);
    times=timed-times;
    cout << "time from start to end = " << times << "sec"<< endl;
	
  // Write mixed tree to file and close everything
  fOut->cd();
  cout << "Writes " << fOut->GetName() << endl;
  tout->Write();
  fOut->Close();
  
  return iEntry;

}
