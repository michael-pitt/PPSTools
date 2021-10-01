#!/bin/bash

input=${1}
output=${2}
cmssw=${3}

cd ${cmssw}/src
eval `scram r -sh`
export X509_USER_PROXY=${cmssw}/src/PPSTools/LowPU2017H/data/voms_proxy.txt
cd -

$CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py output ${input} \
    --json $CMSSW_BASE/src/PPSTools/LowPU2017H/data/combined_RPIN_CMS_LOWMU.json \
    --bi $CMSSW_BASE/src/PPSTools/LowPU2017H/scripts/keep_and_drop_in.txt \
    --bo $CMSSW_BASE/src/PPSTools/LowPU2017H/scripts/keep_and_drop_out.txt \
    -c "HLT_HIMu15" \
    -I PPSTools.LowPU2017H.LowPU_analysis analysis_mu

mv -v output/*.root ${output}
