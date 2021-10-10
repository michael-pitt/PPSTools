import FWCore.ParameterSet.Config as cms
'''
An example file to run proton simulation + reconstruction on MC events. 
All protons from "genPUProtons" will be processed
'''
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')
options.register('instance', 'genPUProtons',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "productInstanceName for PU protons"
                 )	 
options.register('xangle', 150,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "set crossing angle"
                 )	                                       
options.parseArguments()

#start process
from Configuration.StandardSequences.Eras import eras
from Configuration.ProcessModifiers.run2_miniAOD_UL_cff import run2_miniAOD_UL

process = cms.Process("CTPPS", eras.Run2_2017, run2_miniAOD_UL)
 
# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

#pps simulation settings (load them before the source):
#process.load('Validation.CTPPS.simu_config.year_2017_preTS2_cff')
process.load('Validation.CTPPS.simu_config.year_2017_postTS2_cff')

#message logger
process.MessageLogger.cerr.threshold = ''
process.MessageLogger.cerr.FwkReport.reportEvery = 100


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

# Input source
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(options.inputFiles),
                            duplicateCheckMode = cms.untracked.string('noDuplicateCheck') 
                            )
                            
# Output definition
process.MINIAODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('miniAOD_withProtons.root'),
    outputCommands = process.MINIAODSIMEventContent.outputCommands
)
# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mc2017_realistic_v9')

# Path and EndPath definitions
process.endjob_step = cms.EndPath(process.endOfProcess)
process.MINIAODSIMoutput_step = cms.EndPath(process.MINIAODSIMoutput)

outputSteps = [process.endjob_step, process.MINIAODSIMoutput_step]

#schedule execution
toSchedule=[]

#setup proton simulation:
xangle=options.xangle
print('INFO: Run proton simulation for PostTS2 2017 configuration and crossing-angle of %d urad'%xangle)
process.beamDivergenceVtxGenerator.src = cms.InputTag("")
process.beamDivergenceVtxGenerator.srcGenParticle = cms.VInputTag(
   #cms.InputTag("genPUProtons","genPUProtons"), # works with step2_premix modifier
   cms.InputTag("genPUProtons",options.instance),
   #cms.InputTag("prunedGenParticles"), # when ~premix_stage2 signal protons proporate to genPUProtons
)

# do not apply vertex smearing again
process.ctppsBeamParametersESSource.vtxStddevX = 0
process.ctppsBeamParametersESSource.vtxStddevY = 0
process.ctppsBeamParametersESSource.vtxStddevZ = 0
  
#undo CMS vertex shift (example)
process.ctppsBeamParametersESSource.vtxOffsetX45 = +0.2475 * 1E-1
process.ctppsBeamParametersESSource.vtxOffsetY45 = -0.6924 * 1E-1
process.ctppsBeamParametersESSource.vtxOffsetZ45 = -8.1100 * 1E-1
  
# set up Xangle  
process.ctppsLHCInfoESSource.xangle = cms.double(xangle)
process.ctppsBeamParametersESSource.halfXangleX45 = xangle * 1E-6
process.ctppsBeamParametersESSource.halfXangleX56 = xangle * 1E-6
  
# for multiRP fit, set if you want to use x* and y* as free parameters or set them to zero
process.ctppsProtons.fitVtxY = False

process.pps_fastsim = cms.Path(process.beamDivergenceVtxGenerator
    * process.ctppsDirectProtonSimulation
    * process.reco_local
    * process.ctppsProtons
)

toSchedule.append(process.pps_fastsim)

                           
process.schedule=cms.Schedule( (p for p in toSchedule + outputSteps) )
print process.schedule
