# Low PU analysis

Contains scripts to post-process nanoAOD files with PPS content.

### CMSSW setup
```
cmsrel CMSSW_10_6_27
cd CMSSW_10_6_27/src
cmsenv
```

### Examples:
Running on a single file:
```
cmsrel CMSSW_10_6_24
cd CMSSW_10_6_24/src
cmsenv

#This package
cd $CMSSW_BASE/src
git clone https://github.com/michael-pitt/PPSTools.git
scram b -j 8
```
