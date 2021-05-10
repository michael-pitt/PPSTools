// -*- C++ -*-
//
// Package:    PPSTools/EfficiencyCorrection
// Class:      EfficiencyCorrection
//
/**\class EfficiencyCorrection EfficiencyCorrection.cc PPSTools/EfficiencyCorrection/plugins/EfficiencyCorrection.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Michael Pitt
//         Created:  Sun, 09 May 2021 21:55:38 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "CondFormats/RunInfo/interface/LHCInfo.h"
#include "CondFormats/DataRecord/interface/LHCInfoRcd.h"

// package helpers
#include "PPSTools/EfficiencyCorrection/interface/MiniEvent.h"

// ROOT related
#include "TTree.h"
#include "TLorentzVector.h"

//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<>
// This will improve performance in multithreaded jobs.

using namespace std;


class EfficiencyCorrection : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit EfficiencyCorrection(const edm::ParameterSet&);
      ~EfficiencyCorrection();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      // ----------member data ---------------------------
      //edm::EDGetTokenT<TrackCollection> tracksToken_;  //used to select what tracks to read from configuration file
	  
	  TTree *tree_;
	  MiniEvent_t ev_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
EfficiencyCorrection::EfficiencyCorrection(const edm::ParameterSet& iConfig)
 //:
 // tracksToken_(consumes<TrackCollection>(iConfig.getUntrackedParameter<edm::InputTag>("tracks")))

{
   //now do what ever initialization is needed
   
   edm::Service<TFileService> fs;
   tree_ = fs->make<TTree>("tree","PPS efficiency variables");
   createMiniEventTree(tree_,ev_);
   
}


EfficiencyCorrection::~EfficiencyCorrection()
{

   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
EfficiencyCorrection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;

    //get beam-crossing angle and LHC conditions
      ESHandle<LHCInfo> hLHCInfo;
      string lhcInfoLabel("");
    try{
      //ESHandle<LHCInfo> hLHCInfo;
      iSetup.get<LHCInfoRcd>().get(lhcInfoLabel, hLHCInfo);
	  cout << "hLHCInfo.isValid() = " << hLHCInfo.isValid()<< endl;
      if(hLHCInfo.isValid()){
        ev_.beamXangle=hLHCInfo->crossingAngle();
        ev_.instLumi=hLHCInfo->instLumi(); // instantaneous luminosity in ub-1
        ev_.betaStar=hLHCInfo->betaStar();
        ev_.fill=hLHCInfo->fillNumber();
      }
    }
    catch(...){
      ev_.beamXangle=0;
      ev_.instLumi=0;
      ev_.betaStar=0;
      ev_.fill=0;
    }
   
    //analyze the event
    bool isData = iEvent.isRealData();
    ev_.run     = isData ? iEvent.id().run() : -1;
    ev_.lumi    = iEvent.luminosityBlock();
    ev_.event   = iEvent.id().event();   
   
	tree_->Fill();
}


// ------------ method called once each job just before starting event loop  ------------
void
EfficiencyCorrection::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void
EfficiencyCorrection::endJob()
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
EfficiencyCorrection::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);

  //Specify that only 'tracks' is allowed
  //To use, remove the default given above and uncomment below
  //ParameterSetDescription desc;
  //desc.addUntracked<edm::InputTag>("tracks","ctfWithMaterialTracks");
  //descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(EfficiencyCorrection);
