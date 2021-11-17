#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection

### Proton selector be replaced by preprocessing module
from PPSTools.LowPU2017H.objectSelector import ProtonSelector
from PPSTools.LowPU2017H.objectSelector import ElectronSelector, MuonSelector

class Analysis(Module):
    def __init__(self, channel):
        self.channel = channel
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    
        self.out = wrappedOutputTree
        self.out.branch("nano_nJets",     "I");
        self.out.branch("nano_nProtons",  "I");
        self.out.branch("nano_nLeptons",  "I");
        self.out.branch("nano_LepID",     "I",  lenVar = "nano_nLeptons");
        self.out.branch("nano_LepPT",     "F",  lenVar = "nano_nLeptons");
        self.out.branch("nano_LepEta",    "F",  lenVar = "nano_nLeptons");
        self.out.branch("nano_LepPhi",    "F",  lenVar = "nano_nLeptons");
        self.out.branch("nano_LepIso",    "F",  lenVar = "nano_nLeptons");
        self.out.branch("nano_LepIsIso",  "O",  lenVar = "nano_nLeptons");
        self.out.branch("nano_LepDxy",    "F",  lenVar = "nano_nLeptons");
        self.out.branch("nano_LepDz",     "F",  lenVar = "nano_nLeptons");
        self.out.branch("nano_mll",       "F");
        self.out.branch("nano_Yll",       "F");
        self.out.branch("nano_Ptll",      "F");
        self.out.branch("nano_Etall",     "F");
        self.out.branch("nano_Phill",     "F");
        self.out.branch("nano_mjets",     "F");
        self.out.branch("nano_Yjets",     "F");
        self.out.branch("nano_Phijets",   "F");
        self.out.branch("nano_PTjets",    "F");
        self.out.branch("nano_JetPT",     "F");
        self.out.branch("nano_JetEta",    "F");
        self.out.branch("nano_JetPhi",    "F");
        self.out.branch("nano_WMT",       "F");
        self.out.branch("nano_WPT",       "F");
        self.out.branch("nano_WPhi",      "F");
        self.out.branch("nano_xip",       "F");
        self.out.branch("nano_xin",       "F");
        self.out.branch("nano_tp",        "F");
        self.out.branch("nano_tn",        "F");
        self.out.branch("nano_mX",        "F");
        self.out.branch("nano_YX",        "F");
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def selectElectrons(self, event, elSel):

        event.selectedElectrons = []
        electrons = Collection(event, "Electron")
        for el in electrons:
            if not elSel.evalElectron(el): continue
            isiso=el.mvaFall17V2Iso_WP80
            setattr(el, 'isiso', isiso)
            setattr(el, 'iso', el.pfRelIso03_all)
            setattr(el, 'id', 11)
            event.selectedElectrons.append(el)
        event.selectedElectrons.sort(key=lambda x: x.pt, reverse=True)
        

    def selectMuons(self, event, muSel):
        ## access a collection in nanoaod and create a new collection based on this

        event.selectedMuons = []
        muons = Collection(event, "Muon")
        for mu in muons:
            if not muSel.evalMuon(mu): continue
            setattr(mu, 'isiso', True if mu.pfRelIso04_all<0.15 else False)
            setattr(mu, 'iso', mu.pfRelIso04_all)
            setattr(mu, 'id', 13)
            event.selectedMuons.append(mu)

        event.selectedMuons.sort(key=lambda x: x.pt, reverse=True)


    def selectAK4Jets(self, event):
        ## Selected jets: pT>25, |eta|<4.7, pass tight ID
        
        event.selectedAK4Jets = []
        ak4jets = Collection(event, "Jet")
        for j in ak4jets:

            if j.pt<25 : 
                continue

            if abs(j.eta) > 4.7:
                continue
            
            #require tight (2^1) or tightLepVeto (2^2) [https://twiki.cern.ch/twiki/bin/view/CMS/JetID#nanoAOD_Flags]
            if j.jetId<2 : 
                continue
                
            #check overlap with selected leptons which are considered to be isolated 
            #(isiso attribute set by the select{Electrons,Muons} methods
            deltaR_to_leptons=[ j.p4().DeltaR(lep.p4()) for lep in event.selectedMuons+event.selectedElectrons if lep.isiso ]
            hasLepOverlap=sum( [dR<0.4 for dR in deltaR_to_leptons] )
            if hasLepOverlap>0: continue

            event.selectedAK4Jets.append(j)
            
        event.selectedAK4Jets.sort(key=lambda x: x.pt, reverse=True)

    def selectProtons(self, event, prSel):
        ## access a collection of protons and create a new collection based on this
        
        event.selectedProtons = []
        protons = Collection(event, "Proton_multiRP")
        tracks = Collection(event, "PPSLocalTrack")

        for idx, pr in enumerate(protons):
            #find associated tracks:
            for tr in tracks:
              if idx != tr.multiRPProtonIdx: continue
              if tr.decRPId // 10 % 10 == 0:  # second digit of RPId is 0 or 2 for near or far detector
                setattr(pr, 'xnear', tr.x)
                setattr(pr, 'ynear', tr.y)
              else:
                setattr(pr, 'xfar', tr.x)
                setattr(pr, 'yfar', tr.y)
            
            #store accepted protons
            if prSel.evalProton(pr): event.selectedProtons.append(pr)
        
        #sort selected protons
        event.selectedProtons.sort(key=lambda x: x.xi, reverse=True)


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        #initiate proton selector tools:
        prSel = ProtonSelector('2017H')
        elSel = ElectronSelector()
        muSel = MuonSelector()
        
        # apply object selection
        self.selectMuons(event, muSel)
        self.selectElectrons(event, elSel)
        self.selectAK4Jets(event)
        self.selectProtons(event, prSel)
        
        #apply event selection depending on the channel:
        if self.channel=="mu":
            
            # veto events with electrons
            if len(event.selectedElectrons): return False
            
            # veto events with 0 or >2 muons
            if len(event.selectedMuons)==0: return False
            if len(event.selectedMuons)>2: return False
            
            #DY selection (2 OS muons)
            if len(event.selectedMuons)==2:
                if event.selectedMuons[0].charge==event.selectedMuons[1].charge: return False

        if self.channel=="el":

            # veto events with muons
            if len(event.selectedMuons): return False
            
            # veto events with 0 or >2 electrons
            if len(event.selectedElectrons)==0: return False
            if len(event.selectedElectrons)>2: return False

            #DY selection (2 OS electrons)
            if len(event.selectedElectrons)==2:
                if event.selectedElectrons[0].charge==event.selectedElectrons[1].charge: return False

        if self.channel=='emu':
            nmu=len(event.selectedMuons)
            nele=len(event.selectedElectrons)
            if nmu==0 or nele==0 : return False
            if nmu+nele!=2 : return False
            if event.selectedMuons[0].charge==event.selectedElectrons[0].charge : return False

        if self.channel=="mj":
            
            #select events with at least 2 jets
            if len(event.selectedAK4Jets)<2: return False
            
            #leading jet pT >140 (trigger treshold)
            if event.selectedAK4Jets[0].pt<140: return False
        
        ######################################################
        ##### HIGH LEVEL VARIABLES FOR SELECTED EVENTS   #####
        ######################################################
        
        event.selectedLeptons=event.selectedElectrons+event.selectedMuons
        event.selectedLeptons.sort(key=lambda x: x.pt, reverse=True)
        
        lep_id=[lep.id for lep in event.selectedLeptons]
        lep_pt=[lep.pt for lep in event.selectedLeptons]
        lep_eta=[lep.eta for lep in event.selectedLeptons]
        lep_phi=[lep.phi for lep in event.selectedLeptons]
        lep_iso=[lep.iso for lep in event.selectedLeptons]
        lep_isiso=[lep.isiso for lep in event.selectedLeptons]
        lep_dxy=[lep.dxy for lep in event.selectedLeptons]
        lep_dz=[lep.dz for lep in event.selectedLeptons]
        
        jet_pt=-1; jet_eta=-999; jet_phi=-999
        if len(event.selectedAK4Jets):
            jet_pt=event.selectedAK4Jets[0].pt
            jet_eta=event.selectedAK4Jets[0].eta
            jet_phi=event.selectedAK4Jets[0].phi
                
        #W boson transverse mass,pt and phi
        MET_pt=event.MET_pt
        MET_phi=event.MET_phi
        if len(event.selectedLeptons):
          w_mT =  2.*lep_pt[0]*MET_pt*(1.-ROOT.TMath.Cos(ROOT.TVector2.Phi_mpi_pi(lep_phi[0]-MET_phi)))
          w_mT=ROOT.TMath.Sqrt(w_mT)
          w_ptvec=ROOT.TVector2(lep_pt[0]*ROOT.TMath.Cos(lep_phi[0])+MET_pt*ROOT.TMath.Cos(MET_phi),
                              lep_pt[0]*ROOT.TMath.Sin(lep_phi[0])+MET_pt*ROOT.TMath.Sin(MET_phi))
          w_pt=w_ptvec.Mod()
          w_phi=w_ptvec.Phi()
        else:
          w_mT = w_pt = 1; w_phi = -999
        
        #di-lepton 4-vector
        lepSum = ROOT.TLorentzVector()
        if len(event.selectedLeptons)==2:
            for lep in event.selectedLeptons:
                lepSum+=lep.p4()
                
        #multi-jet 4-vector:
        jetSum = ROOT.TLorentzVector()
        for jet in event.selectedAK4Jets:
            jetSum+=jet.p4()

        #proton xi
        xip = xin = tp = tn = -1
        for pr in event.selectedProtons:
            if pr.arm==0: xip=pr.xi; tp=pr.t
            if pr.arm==1: xin=pr.xi; tn=pr.t

        ## store branches
        self.out.fillBranch("nano_nJets" ,    len(event.selectedAK4Jets))
        self.out.fillBranch("nano_nProtons",  len(event.selectedProtons))
        self.out.fillBranch("nano_nLeptons",  len(event.selectedLeptons))
        self.out.fillBranch("nano_LepID" ,    lep_id)
        self.out.fillBranch("nano_LepPT" ,    lep_pt)
        self.out.fillBranch("nano_LepEta" ,   lep_eta)
        self.out.fillBranch("nano_LepPhi" ,   lep_phi)
        self.out.fillBranch("nano_LepIso" ,   lep_iso)
        self.out.fillBranch("nano_LepIsIso" , lep_isiso)
        self.out.fillBranch("nano_LepDxy" ,   lep_dxy)
        self.out.fillBranch("nano_LepDz" ,    lep_dz)
        self.out.fillBranch("nano_JetPT" ,    jet_pt)
        self.out.fillBranch("nano_JetEta" ,   jet_eta)
        self.out.fillBranch("nano_JetPhi" ,   jet_phi)
        self.out.fillBranch("nano_WMT" ,      w_mT)
        self.out.fillBranch("nano_WPT" ,      w_pt)
        self.out.fillBranch("nano_WPhi" ,     w_phi)
        self.out.fillBranch("nano_mll" ,      lepSum.M())
        self.out.fillBranch("nano_Yll" ,      lepSum.Rapidity())
        self.out.fillBranch("nano_Ptll" ,     lepSum.Pt())
        self.out.fillBranch("nano_Etall",     lepSum.Eta())
        self.out.fillBranch("nano_Phill",     lepSum.Phi())
        self.out.fillBranch("nano_mjets",     jetSum.M())
        self.out.fillBranch("nano_Yjets",     jetSum.Rapidity())
        self.out.fillBranch("nano_Phijets",   jetSum.Phi())
        self.out.fillBranch("nano_PTjets",    jetSum.Pt())
        self.out.fillBranch("nano_xip",       xip)
        self.out.fillBranch("nano_xin",       xin)
        self.out.fillBranch("nano_tp",        tp)
        self.out.fillBranch("nano_tn",        tn)
        self.out.fillBranch("nano_mX",        (jetSum+lepSum).M())
        self.out.fillBranch("nano_YX",        (jetSum+lepSum).Rapidity())

        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
analysis_mu  = lambda : Analysis(channel="mu")
analysis_el  = lambda : Analysis(channel="el")
analysis_emu = lambda : Analysis(channel="emu")
analysis_mj  = lambda : Analysis(channel="mj")
