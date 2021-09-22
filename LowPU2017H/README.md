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
git clone git@github.com:michael-pitt/PPSTools.git
scram b -j
```

## Analysis

Analysis code is in [LowPU_analysis.py](https://github.com/michael-pitt/PPSTools/blob/main/LowPU2017H/python/LowPU_analysis.py), which select events, compute high level variables and write a skimmed output tree

Three analysis modules can be executed:
- `analysis_mu`: HLT_HIMu15, 1 or 2 muons, mu0_pt>15GeV, Electron veto. If 2 muons are selected, only OS events are stored.
- `analysis_el`: HLT_HIEle15_WPLoose_Gsf, 1 or 2 electrons, el0_pt>15GeV, Muon veto. If 2 electrons are selected, only OS events are stored.
- `analysis_mj`: HLT_HIPFJet140 || HLT_HIPFJetFwd140, selecting events with at least 2 jets, where the leading jet has pt > 140 GeV.

For each event selection:
- An appropriate `keep_and_drop` files can be chosen (see list of files [here](https://github.com/michael-pitt/PPSTools/tree/main/LowPU2017H/scripts))
- A corresponding trigger should be set

json file with low-pu luminosity blocks: [combined_RPIN_CMS_LOWMU.json](https://github.com/michael-pitt/PPSTools/blob/main/LowPU2017H/data/combined_RPIN_CMS_LOWMU.json)

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
