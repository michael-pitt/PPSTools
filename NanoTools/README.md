# NanoTools

Contains scripts to produce nanoAOD files with PPS content.

## CMSSW setup
```
cmsrel CMSSW_10_6_27
cd CMSSW_10_6_27/src
cmsenv

#This package
git clone git@github.com:michael-pitt/PPSTools.git
scram b -j
```

As a default, the proton nanoAOD content is not stored for MC. To enable it add `protonTablesTask` to the `nanoTableTaskCommon` in [PhysicsTools.NanoAOD.nano_cff](https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/NanoAOD/python/nano_cff.py), after downloading the NanoAOD package: 
```
cd CMSSW_10_6_27/src
git cms-addpkg PhysicsTools/NanoAOD
```
To retrieve PU protons from `GenParticle` container, add to [genparticles_cff.py](https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/NanoAOD/python/genparticles_cff.py) the following code:
```python
finalGenProtons = cms.EDProducer("GenParticlePruner",
    src = cms.InputTag("genPUProtons","genPUProtons"),
    select = cms.vstring(
	"drop *",
    "keep ((pdgId == 2212) && (abs(pz) > 5200) && (abs(pz) < 6467.5))", #keep LHC protons with xi in (1.5% - 20%)
   )
)

genProtonTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("finalGenProtons"),
    cut = cms.string(""), #we should not filter after pruning
    name= cms.string("GenProton"),
    doc = cms.string("diffractive protons"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the taus
    variables = cms.PSet(
         pt  = Var("pt",  float, precision=8),
         pz = Var("pz", float,precision=8),
    )
)

genProtonSequence = cms.Sequence(finalGenProtons)
genProtonTables = cms.Sequence(genProtonTable)
```

## Processing files

### Testing proton reconstruction

To test proton reconstruction before producing NANOAODs, one can run the following sequence: MINIAOD -> PROTONRECO -> MINIAOD. The example will run the simulation using the 2017 post-TS2 PPS configuration, with a crossing-angle of 150urad.

```
file=/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/240000/C070EFE9-646E-2D4C-BFEA-4011B96BBCC9.root
cmsRun $CMSSW_BASE/src/PPSTools/NanoTools/test/addProtons_miniaod.py maxEvents=500 inputFiles=$file
```

The output file - `output_numEvent500.root` is a MINIAOD which contain 500 events with reconstructed protons from `genPUProtons` container.

### Producing nanoAODs

The following sequence - MINIAOD -> PROTONRECO -> NANOAOD - can be executed using the following command:
```
cmsRun $CMSSW_BASE/src/PPSTools/NanoTools/test/produceNANO.py inputFiles=$file maxEvents=500 runProtonFastSim=150
```

Where the `runProtonFastSim` is the input parameter indicates the simulated crossing angle.

### Submitting to condor

To submit condor jobs for the entire data set:
