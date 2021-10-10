import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

# MC configuration
# 2017:  https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/BTV-RunIISummer20UL17NanoAODv9-00018

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register('isData', False,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.bool,
                 "is data"
                 )
options.register('era', 'era2017',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "choose era"
                 )			 
options.register('runProtonFastSim', None,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Run proton fastsim for this angle"
                 )
options.register('doPUProtons', True,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.bool,
                 "Include PU protons"
                 )
options.register('instance', 'genPUProtons',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "productInstanceName for PU protons"
                 )		                 
options.register('outFilename', 'output_nano.root',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Output file name"
                 )                 
options.parseArguments()

print "INFO: Era set to", options.era
print "INFO: isData set to", options.isData


if '2016preVFP' in options.era:
    process = cms.Process('NANO',eras.Run2_2016_HIPM,eras.run2_nanoAOD_106Xv2)
elif '2016' in options.era:
    process = cms.Process('NANO',eras.Run2_2016,eras.run2_nanoAOD_106Xv2)
elif '2017' in options.era:
    process = cms.Process('NANO',eras.Run2_2017,eras.run2_nanoAOD_106Xv2)
elif '2018' in options.era:
    process = cms.Process('NANO',eras.Run2_2018,eras.run2_nanoAOD_106Xv2)

#get the configuration to apply
from PPSTools.NanoTools.EraConfig import getEraConfiguration
globalTag, ppscff = getEraConfiguration(era=options.era,isData=options.isData)
print("INFO: globalTag set to "+globalTag)


# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
if options.runProtonFastSim:
  process.load(ppscff)

# process stdout
process.MessageLogger.cerr.threshold = cms.untracked.string('')
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)

#process options

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

# Input source
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(options.inputFiles),
                            inputCommands = cms.untracked.vstring('keep *', 
                            # drop the old event content, since it is empty
                            'drop recoForwardProtons_ctppsProtons_multiRP_RECO', 
                            'drop recoForwardProtons_ctppsProtons_singleRP_RECO'),
                            duplicateCheckMode = cms.untracked.string('noDuplicateCheck') 
                            )

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(False) 
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('--python_filename nevts:-1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition
process.NANOEDMAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:'+options.outFilename),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

# Additional output definition

# Other statements
# global tag
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, globalTag, '')

# Need this modifications to use fitVtxY=False option (not recommended by POG)
#print('FIXME MultiRP proton reco: filteredProtons->ctppsProtons')
#process.protonTable.tagRecoProtonsMulti=cms.InputTag("ctppsProtons", "multiRP")
#process.multiRPTable.src=cms.InputTag("ctppsProtons","multiRP")

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequenceMC)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOEDMAODSIMoutput_step = cms.EndPath(process.NANOEDMAODSIMoutput)
nanoSteps = [process.nanoAOD_step, process.endjob_step, process.NANOEDMAODSIMoutput_step]

#schedule execution
toSchedule=[]

#proton reconstruction
if options.runProtonFastSim:
  print 'INFO:\t Run proton simulation with xangle = ',options.runProtonFastSim,'murad'
  from PPSTools.NanoTools.protonReco_cfg import setupProtonSim
  setupProtonSim(process,options.runProtonFastSim,withPU=options.doPUProtons,instance=options.instance)
  toSchedule.append(process.pps_fastsim)

# Schedule definition
process.schedule=cms.Schedule( (p for p in toSchedule + nanoSteps) )
print process.schedule
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeMC 

#call to customisation function nanoAOD_customizeMC imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeMC(process)
process.genProtonTable.srcPUProtons = cms.InputTag('genPUProtons', options.instance)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
