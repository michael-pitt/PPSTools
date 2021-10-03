# NanoTools

Contains scripts to post-process nanoAOD files with PPS content.

## CMSSW setup
```
cmsrel CMSSW_10_6_27
cd CMSSW_10_6_27/src
cmsenv

#This package
git clone git@github.com:michael-pitt/PPSTools.git
scram b -j
```

## Processing files

MINIAOD -> PROTONRECO -> NANOAOD

### Running on a single file:

example of running on a file from `SingleMuon` stream
```
$CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py \
output root://cms-xrd-global.cern.ch//store/data/Run2017H/SingleMuon/NANOAOD/UL2017_MiniAODv2_NanoAODv9-v1/100000/00E28CF6-5CDE-A644-A390-40F2F6613888.root \
--json $CMSSW_BASE/src/PPSTools/LowPU2017H/data/combined_RPIN_CMS_LOWMU.json \
--bi $CMSSW_BASE/src/PPSTools/LowPU2017H/scripts/keep_and_drop_in.txt \
--bo $CMSSW_BASE/src/PPSTools/LowPU2017H/scripts/keep_and_drop_out.txt \
-c "HLT_HIMu15" -I PPSTools.LowPU2017H.LowPU_analysis analysis_mu
```

### Submitting to condor

To submit condor jobs for the entire data set:
