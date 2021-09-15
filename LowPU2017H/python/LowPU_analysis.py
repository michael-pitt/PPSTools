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
        #self.out.branch("nIsoTracks"     , "I");

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def selectElectrons(self, event):
        ## access a collection in nanoaod and create a new collection based on this

        event.selectedElectrons = []
        electrons = Collection(event, "Electron")
        for el in electrons:
            el.etaSC = el.eta + el.deltaEtaSC
            if el.pt > 15 and abs(el.eta) < 2.4 and abs(el.dxy) < 0.05 and abs(el.dz) < 0.2 and el.pfRelIso03_all < 0.4:
                if el.mvaFall17V2noIso_WP90:
                    event.selectedElectrons.append(el)

        event.selectedElectrons.sort(key=lambda x: x.pt, reverse=True)
        

    def selectMuons(self, event):
        ## access a collection in nanoaod and create a new collection based on this

        event.selectedMuons = []
        muons = Collection(event, "Muon")
        for mu in muons:
            if mu.pt > 15 and abs(mu.eta) < 2.4 and abs(mu.dxy) < 0.5 and abs(mu.dz) < 1.0 and mu.pfRelIso04_all < 0.4:
                if mu.looseId:
                    event.selectedMuons.append(mu)

        event.selectedMuons.sort(key=lambda x: x.pt, reverse=True)


    def selectAK4Jets(self, event):
        ## access a collection in nanoaod and create a new collection based on this
        ## apply bitwise selection on some ID e.g., here is the jetID [similar for EG ids bla..]
        
        event.selectedAK4Jets = []
        ak4jets = Collection(event, "Jet")
        for j in ak4jets:
            if not (j.pt > 25 and abs(j.eta) < 2.4 and (j.jetId & 2)):
                continue
            event.selectedAK4Jets.append(j)
            
        event.selectedAK4Jets.sort(key=lambda x: x.pt, reverse=True)


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        #apply selection depending on the channel:
        if self.channel=="mu":
            self.selectMuons(event)
            
            if len(event.selectedMuons)==0: return False
            if len(event.selectedMuons)>2: return False
            
            #DY selection
            if len(event.selectedMuons)==2:
                if event.selectedMuons[0].charge==event.selectedMuons[1].charge: return False
        

        if self.channel=="el":
            self.selectElectrons(event)

            if len(event.selectElectrons)==0: return False
            if len(event.selectElectrons)>2: return False
            
            #DY selection
            if len(event.selectElectrons)==2:
                if event.selectElectrons[0].charge==event.selectElectrons[1].charge: return False

        if self.channel=="mj":
            self.selectAK4Jets(event)

            if len(event.selectedAK4Jets)==0: return False
            if len(event.selectedAK4Jets[0].pt)<140: return False
                   
        ## leptons
        #self.out.fillBranch("nIsoTracks"  , event.nIsoTrack)
    
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
analysis_mu = lambda : Analysis(channel="mu")
analysis_el = lambda : Analysis(channel="el")
analysis_mj = lambda : Analysis(channel="mj")

