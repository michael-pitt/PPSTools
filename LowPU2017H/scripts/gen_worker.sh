#!/bin/bash
#instructions from  https://twiki.cern.ch/twiki/bin/view/CMS/PdmVLegacy2017Analysis#Example_of_cmsDriver_AN1
#run.sh card

startMsg='Job started on '`date`
echo $startMsg

# check number of arguments
if [ "$#" -ne 6 ]; then
  echo "Usage: $0 proxy card seed output cmssw Nevents" >&2
  echo "Example: $0 /tmp/x509up_u58751 ${CMSSW_BASE}/data/cards/dijet_Pt100_TuneCP5_13TeV 1 /eos/home-m/mpitt/LowMu/MC/nanoAOD/dijet_Pt100_TuneCP5_13TeV ${CMSSW_BASE} 50" >&2
  exit 1
fi

####### INPUT SETTINGS ###########
proxy=${1}
card=${2}
idx=$(printf "%03d" `expr ${3} + 0`)
outfolder=${4}
cmssw=${5}
EVENTS=${6}
##################################

echo ./gen_worker.sh $1 $2 $3 $4 $5 $6

setup10() {
    echo scram p CMSSW CMSSW_10_6_20
    export SCRAM_ARCH=slc7_amd64_gcc700
    if [ -r CMSSW_10_6_20/src ] ; then
       echo release CMSSW_10_6_20 already exists
    else
      scram p CMSSW CMSSW_10_6_20
    fi
    cd CMSSW_10_6_20/src
    eval `scram runtime -sh`
    curl file://${card} --retry 2 --create-dirs -o Configuration/GenProduction/python/My-fragment.py
    scram b -j
    cd ../../
}

echo "create temporary folder to run the job"
tmpfolder=`echo ${card} | rev | cut -d/ -f1 | rev`
mkdir -pv /tmp/$USER/${tmpfolder}_${idx}; cd /tmp/$USER/${tmpfolder}_${idx}

echo mkdir -p $outfolder
mkdir -p $outfolder

echo "Setup CMSSW"
setup10

echo "GEN-SIM starting"
seed=`expr 123456 + ${EVENTS} \* ${3}`
#https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/BTV-RunIISummer20UL17wmLHEGEN-00001
#https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/BTV-RunIISummer20UL17SIM-00003
echo "cmsDriver.py Configuration/GenProduction/python/My-fragment.py --python_filename step1_cfg.py --eventcontent RAWSIM --datatier GEN-SIM --fileout file:stepSIM.root --conditions 106X_mc2017_realistic_v6 --beamspot Realistic25ns13TeVEarly2017Collision --customise_commands process.RandomNumberGeneratorService.generator.initialSeed=\"cms.untracked.uint32(${seed})\" --step GEN,SIM --geometry DB:Extended --era Run2_2017 --no_exec --mc -n ${EVENTS}"
cmsDriver.py Configuration/GenProduction/python/My-fragment.py --python_filename step1_cfg.py \
--eventcontent RAWSIM --datatier GEN-SIM --fileout file:stepSIM.root --conditions 106X_mc2017_realistic_v6 \
--beamspot Realistic25ns13TeVEarly2017Collision --customise_commands process.RandomNumberGeneratorService.generator.initialSeed="cms.untracked.uint32(${seed})" \
--step GEN,SIM --geometry DB:Extended --era Run2_2017 --no_exec --mc -n ${EVENTS}
if [[ `echo $card | rev | cut -d"/" -f1 | rev | cut -d"_" -f 1` == 'DPE' ]]; then
  sed -i "/# Output definition/a process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(50000)" step1_cfg.py
  moreEvents=`expr ${EVENTS} \* 50000`
  sed -i "/# Output definition/a process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(${moreEvents}))" step1_cfg.py  
fi  
echo INFO: step1_cfg.py
cat step1_cfg.py
cmsRun step1_cfg.py


echo "DIGI-RAW starting"
#https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/BTV-RunIISummer20UL17DIGIPremix-00003
cmsDriver.py step2 --python_filename step2_cfg.py --eventcontent RAWSIM --datatier GEN-SIM-RAW --fileout file:stepRAW.root \
--pileup 'E7TeV_AVE_2_BX2808,{"N": 3.0}'  --pileup_input "dbs:/MinBias_TuneCP5_13TeV-pythia8/RunIISummer20UL17SIM-106X_mc2017_realistic_v6-v2/GEN-SIM" \
--beamspot Realistic25ns13TeVEarly2017Collision --conditions 106X_mc2017_realistic_v6 --step DIGI,L1,DIGI2RAW,HLT:@fake2 \
--geometry DB:Extended --filein file:stepSIM.root --era Run2_2017 --no_exec --mc -n -1
sed -i "/process.mix.input.fileNames/a process.mix.input.seed = cms.untracked.int32(${seed})" step2_cfg.py
cmsRun step2_cfg.py

if [ ! -f stepRAW.root ]; then
  echo "stepRAW.root was not generated, break."
  cd ../
  rm -rf ${tmpfolder}_${idx}
  exit 1;
fi

echo "RAW-AOD starting"
#https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/BTV-RunIISummer20UL17RECO-00003
cmsDriver.py step3 --filein file:stepRAW.root --fileout file:stepAOD.root --mc --eventcontent AODSIM \
--datatier AODSIM --runUnscheduled --conditions 106X_mc2017_realistic_v6 --step RAW2DIGI,L1Reco,RECO,RECOSIM \
--nThreads 8 --geometry DB:Extended --era Run2_2017 --python_filename step3_cfg.py --runUnscheduled --no_exec -n -1
echo INFO\: step3_cfg.py
cat step3_cfg.py
cmsRun step3_cfg.py

echo "AOD-MINIAOD starting"
#https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/BTV-RunIISummer20UL17MiniAODv2-00003
cmsDriver.py step4 --filein file:stepAOD.root --fileout file:miniAOD.root --mc --eventcontent MINIAODSIM \
--datatier MINIAODSIM --runUnscheduled --conditions 106X_mc2017_realistic_v9 --step PAT --procModifiers run2_miniAOD_UL \
--nThreads 8 --geometry DB:Extended --era Run2_2017 --runUnscheduled --python_filename step4_cfg.py --no_exec -n -1
echo INFO\: step4_cfg.py
cat step4_cfg.py
cmsRun step4_cfg.py

echo "running proton simulation on miniAOD file:"
echo "Setting up ${cmssw}"
cd ${cmssw}/src
eval `scram r -sh`
cd -

cmsRun $cmssw/src/PPSTools/NanoTools/test/addProtons_miniaod.py inputFiles=file:miniAOD.root instance="" outputFile=miniAOD_withProtons.root

echo "MINIAOD-NANOAOD starting"
# note this step is done with customized nanoAOD tools
cmsRun $cmssw/src/PPSTools/NanoTools/test/produceNANO.py inputFiles=file:miniAOD_withProtons.root

# https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/BTV-RunIISummer20UL17NanoAODv9-00018
#cmsDriver.py step5 --filein file:miniAOD_withProtons.root --fileout file:nanoAOD.root --mc --eventcontent NANOEDMAODSIM \
--datatier NANOAODSIM --runUnscheduled --conditions 106X_mc2017_realistic_v9 --step NANO \
--nThreads 8 --geometry DB:Extended --era Run2_2017,run2_nanoAOD_106Xv2 --python_filename step5_cfg.py --no_exec -n -1
#sed -i 's/PoolOutputModule/NanoAODOutputModule/g' step5_cfg.py
#echo INFO\: step5_cfg.py
#cat step5_cfg.py
#cmsRun step5_cfg.py

echo "Analysis starting"
for channel in mu el mj; do
  echo 'Processing '$channel

  $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py $PWD output_nano.root \
  --bi $CMSSW_BASE/src/PPSTools/LowPU2017H/scripts/keep_and_drop_in.txt \
  --bo $CMSSW_BASE/src/PPSTools/LowPU2017H/scripts/keep_and_drop_out.txt \
  -I PPSTools.LowPU2017H.LowPU_analysis analysis_${channel}  
  
  mv output_nano_Skim.root output_nano_Skim_${channel}.root
done


echo "Copying to storage"
for channel in mu el mj; do
  mkdir -p ${outfolder}/${tmpfolder}_${channel}
  echo coutput_nano_Skim_${channel}.root  ${outfolder}/${tmpfolder}_${channel}/skim_events_${idx}.root
  cp output_nano_Skim_${channel}.root  ${outfolder}/${tmpfolder}_${channel}/skim_events_${idx}.root
done

echo "clean output"
cd ../
rm -rf ${tmpfolder}_${idx}

echo $startMsg
echo job finished on `date`



