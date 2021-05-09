# PPSTools

## Installation instructions

```
cmsrel CMSSW_10_6_24
cd CMSSW_10_6_24/src
cmsenv

#This package
cd $CMSSW_BASE/src
git clone https://github.com/michael-pitt/PPSTools.git
scram b -j 8
```

## Table of content

The repository contains several tools to do analysis with PPS protons with [CMSSW](https://cms-sw.github.io/)

### 1. EfficiencyCorrection
The package is used to extract proton efficiency corrections from the data
