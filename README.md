# PPSTools

## Installation instructions

```
cmsrel CMSSW_10_6_24
cd CMSSW_10_6_24/src
cmsenv

#This package
cd $CMSSW_BASE/src
git clone git@github.com:michael-pitt/PPSTools.git
scram b -j 8
```

## Table of content

The repository contains several tools/packages to do analysis with PPS protons.

### 1. EfficiencyCorrection
The package is used to extract proton efficiency corrections from the data, it runs with [CMSSW](https://cms-sw.github.io/) on AOD files (in development)

### 2. Low PU analysis
This package contain modules and codes used with 2017H datasample.

