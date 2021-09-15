# Low PU analysis

Contains scripts to post-process nanoAOD files with PPS content.

## CMSSW setup
```
cmsrel CMSSW_10_6_27
cd CMSSW_10_6_27/src
cmsenv

#setup nanoAOD-tools
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
scram b -j

#This package
git clone https://github.com/michael-pitt/PPSTools.git
scram b -j
```

## Analysis

Analysis code is in [LowPU_analysis.py](https://github.com/michael-pitt/PPSTools/blob/main/LowPU2017H/python/produce_ntuple.py) which select events, compute central variables and write a skimmed output tree

### Running on a single file:
```
$CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py -c "HLT_HIMu15==1" --bi $CMSSW_BASE/src/PPSTools/LowPU2017H/scripts/keep_and_drop.txt output root://cms-xrd-global.cern.ch//store/data/Run2017H/SingleMuon/NANOAOD/UL2017_MiniAODv2_NanoAODv9-v1/100000/00E28CF6-5CDE-A644-A390-40F2F6613888.root -I PPSTools.LowPU2017H.LowPU_analysis analysis
```

### Submitting to condor

To submit condor jobs for entire data set:


