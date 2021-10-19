#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
##soon to be deprecated
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
##new way of using jme uncertainty
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *

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
        self.out.branch("nano_LepID",     "I");
        self.out.branch("nano_LepPT",     "F");
        self.out.branch("nano_LepEta",    "F");
        self.out.branch("nano_LepPhi",    "F");
        self.out.branch("nano_LepIso",    "F");
        self.out.branch("nano_LepIsIso",  "O");
        self.out.branch("nano_LepDxy",    "F");
        self.out.branch("nano_LepDz",     "F");
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


    def selectElectrons(self, event):
        ## access a collection in nanoaod and create a new collection based on this

        event.selectedElectrons = []
        electrons = Collection(event, "Electron")
        for el in electrons:
            isEBEE = True if abs(el.eta)>1.4442 and abs(el.eta)<1.5660 else False
            if el.pt > 20 and abs(el.eta) < 2.4 and not isEBEE and abs(el.dxy) < 0.05 and abs(el.dz) < 0.2:

                isiso=el.mvaFall17V2Iso_WP80
                setattr(el,'isiso', isiso)

                isnoniso_sideband = el.mvaFall17V2noIso_WP80 and not isiso 
                if not isiso and not isnoniso_sideband : continue
                event.selectedElectrons.append(el)

        event.selectedElectrons.sort(key=lambda x: x.pt, reverse=True)
        

    def selectMuons(self, event):
        ## access a collection in nanoaod and create a new collection based on this

        event.selectedMuons = []
        muons = Collection(event, "Muon")
        for mu in muons:
            if mu.pt > 20 and abs(mu.eta) < 2.4 and mu.pfRelIso04_all<0.4 and abs(mu.dxy) < 0.5 and abs(mu.dz) < 1.0:
                if mu.tightId:
                    setattr(mu,'isiso', True if mu.pfRelIso04_all<0.15 else False)
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

    def selectProtons(self, event):
        ## access a collection of protons and create a new collection based on this
        
        event.selectedProtons = []
        protons = Collection(event, "Proton_multiRP")
        for j in protons:
            event.selectedProtons.append(j)
            
        event.selectedProtons.sort(key=lambda x: x.xi, reverse=True)


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        # apply object selection
        self.selectMuons(event)
        self.selectElectrons(event)
        self.selectAK4Jets(event)
        self.selectProtons(event)
        
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

        # leading lepton and jet pt/eta
        leading_lep_id=0
        leading_lep_pt=-1; leading_lep_eta=-999; leading_lep_phi=-999; leading_lep_iso=-999;
        leading_lep_isiso=False
        leading_lep_dxy=-999
        leading_lep_dz=-999
        if len(event.selectedElectrons):
            leading_lep_id=11
            leading_lep_pt=event.selectedElectrons[0].pt
            leading_lep_eta=event.selectedElectrons[0].eta
            leading_lep_phi=event.selectedElectrons[0].phi
            leading_lep_iso=event.selectedElectrons[0].pfRelIso03_all
            leading_lep_isiso=event.selectedElectrons[0].isiso
            leading_lep_dxy=event.selectedElectrons[0].dxy
            leading_lep_dz=event.selectedElectrons[0].dz
        if len(event.selectedMuons) and event.selectedMuons[0].pt>leading_lep_pt: 
            leading_lep_id=13
            leading_lep_pt=event.selectedMuons[0].pt
            leading_lep_eta=event.selectedMuons[0].eta
            leading_lep_phi=event.selectedMuons[0].phi
            leading_lep_iso=event.selectedMuons[0].pfRelIso04_all
            leading_lep_isiso=event.selectedMuons[0].isiso
            leading_lep_dxy=event.selectedMuons[0].dxy
            leading_lep_dz=event.selectedMuons[0].dz

        leading_jet_pt=-1; leading_jet_eta=-999; leading_jet_phi=-999
        if len(event.selectedAK4Jets):
            leading_jet_pt=event.selectedAK4Jets[0].pt
            leading_jet_eta=event.selectedAK4Jets[0].eta
            leading_jet_phi=event.selectedAK4Jets[0].phi
                
        #W boson transverse mass,pt and phi
        MET_pt=event.MET_pt
        MET_phi=event.MET_phi
        w_mT =  2.*leading_lep_pt*MET_pt*(1.-ROOT.TMath.Cos(ROOT.TVector2.Phi_mpi_pi(leading_lep_phi-MET_phi)))
        if w_mT>0: 
            w_mT=ROOT.TMath.Sqrt(w_mT)
        else:
            w_mT=-999.
        w_ptvec=ROOT.TVector2(leading_lep_pt*ROOT.TMath.Cos(leading_lep_phi)+MET_pt*ROOT.TMath.Cos(MET_phi),
                              leading_lep_pt*ROOT.TMath.Sin(leading_lep_phi)+MET_pt*ROOT.TMath.Sin(MET_phi))
        w_pt=w_ptvec.Mod()
        w_phi=w_ptvec.Phi()
        
        #di-lepton 4-vector
        lepSum = ROOT.TLorentzVector()
        if len(event.selectedElectrons)==2:
            for lep in event.selectedElectrons:
                lepSum+=lep.p4()
                if lep.isiso : continue
                leading_lep_isiso=False

        if len(event.selectedMuons)==2:
            for lep in event.selectedMuons:
                lepSum+=lep.p4()
                if lep.isiso : continue
                leading_lep_isiso=False

        if self.channel=='emu':
            lepSum=event.selectedMuons[0].p4()+event.selectedElectrons[0].p4()
            leading_lep_isiso = event.selectedMuons[0].isiso & event.selectedElectrons[0].isiso
            leading_lep_id=11*13

                
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
        self.out.fillBranch("nano_nLeptons",  len(event.selectedElectrons)+len(event.selectedMuons))
        self.out.fillBranch("nano_LepID" ,    leading_lep_id)
        self.out.fillBranch("nano_LepPT" ,    leading_lep_pt)
        self.out.fillBranch("nano_LepEta" ,   leading_lep_eta)
        self.out.fillBranch("nano_LepPhi" ,   leading_lep_phi)
        self.out.fillBranch("nano_LepIso" ,   leading_lep_iso)
        self.out.fillBranch("nano_LepIsIso" , leading_lep_isiso)
        self.out.fillBranch("nano_LepDxy" ,   leading_lep_dxy)
        self.out.fillBranch("nano_LepDz" ,    leading_lep_dz)
        self.out.fillBranch("nano_JetPT" ,    leading_jet_pt)
        self.out.fillBranch("nano_JetEta" ,   leading_jet_eta)
        self.out.fillBranch("nano_JetPhi" ,   leading_jet_phi)
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
