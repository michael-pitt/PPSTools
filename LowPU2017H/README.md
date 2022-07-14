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
- `analysis_mu`: HLT_HIMu15, 1 or 2 loose muons, mu_pt>15(10)GeV, Electron veto. If 2 muons are selected, only OS events are stored.
- `analysis_el`: HLT_HIEle15_WPLoose_Gsf, 1 or 2 LooseID electrons, el_pt>15(10)GeV, Muon veto. If 2 electrons are selected, only OS events are stored.
- `analysis_emu`: HLT_HIEle15_WPLoose_Gsf || HLT_HIMu15, 1 looseID muon, 1 looseID electron, lep_pt>10GeV, and OS.
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
--json data/combined_RPIN_CMS_LOWMU.json \
--bi scripts/keep_Data.txt --bo scripts/keep_and_drop_Data_out.txt \
-c "HLT_HIMu15" -I PPSTools.LowPU2017H.LowPU_analysis analysis_mu
```

### Submitting to condor

To submit condor jobs for an entire data set.
Start a local proxy under the data directory:

```
voms-proxy-init --voms cms --valid 172:00 --out data/voms_proxy.txt
```

Then call:

```
python scripts/processDataset.py  -i /SingleMuon/Run2017H-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD -o /eos/user/p/psilva/data/sdanalysis/SingleMuon/Chunks
```

## Simulation of signal and background

In [LowPU2017H/data/cards](https://github.com/michael-pitt/PPSTools/blob/main/LowPU2017H/data/cards) pythia fragments of the inclusive and diffractive event can be found. 

### MINIAOD

Generation of the MINIAOD using pythia fragments can be done using the [gen_miniaod.sh](https://github.com/michael-pitt/PPSTools/blob/main/LowPU2017H/scripts/gen_miniaod.sh) script.
```
gen_miniaod.sh $card $seed
```
Example:
```
voms-proxy-init --voms cms
scripts/gen_miniaod.sh data/cards/dijet_Pt100_TuneCP5_13TeV 0
```
### NANOAOD
To produce NANOAODs the following sequence should be executed: MINIAOD->MINIAOD+Protons->NANOAOD:

   1. Proton simulation: the code will propagate all final state protons within the RP acceptance, simulate PPS hits, and run the proton reconstruction module.
```
cmsRun $CMSSW_BASE/src/PPSTools/NanoTools/test/addProtons_miniaod.py inputFiles=file:miniAOD.root instance=""
```
NOTE: Check the input file which collection is used to store the pileup protons.
   2. MINIAOD->NANOAOD step
To produce nanoAOD from miniAOD run:
```
cmsRun $CMSSW_BASE/src/PPSTools/NanoTools/test/produceNANO.py inputFiles=file:miniAOD_withProtons.root instance=""
```
### Submitting to condor
To produce all steps in one shot, you can run the following script:
```
python scripts/submitMC.py -c data/cards/DYtoLL_Pt12_TuneCP5_13TeV
```
   - add `-s` if you wish to submit the code to condor.
   - add `-j` to set the number of jobs.
   - add `-n` to set the number of events per job.
   
### Backgrpund estimation

We use the data-driven method to model backgrounds with fake leptons (mainly QCD processes). The following code will compute Fake-Factors (FF) to Fake-lepton background:
```
produceQCD datafilename.root
```

The code will compute the FF (=N(iso)/N(non-iso)) and store it in the event weight.

## Notebooks

### Table of contents

The `notebooks` folder contains a few useful notebooks:

  * [Proton tag rates](https://nbviewer.org/github/michael-pitt/PPSTools/blob/main/LowPU2017H/notebooks/ProtonTagRate.ipynb)  
  
### Running the notebooks

Click the icon to open a [SWAN session](https://swan.cern.ch) (default is good): [![SWAN](https://swanserver.web.cern.ch/swanserver/images/badge_swan_white_150.png)](https://cern.ch/swanserver/cgi-bin/go/?projurl=https://github.com/michael-pitt/PPSTools.git)

Goto PPSTools/LowPU2017H/notebooks/
