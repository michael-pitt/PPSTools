import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("ProcPPS")

options = VarParsing.VarParsing('python')

options.parseArguments()


# import of standard configurations
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load('Configuration.StandardSequences.Services_cff')
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)

#process options
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )
process.source = cms.Source("PoolSource",fileNames = cms.untracked.vstring(options.inputFiles))

# setup output file name
process.TFileService = cms.Service("TFileService",fileName = cms.string(options.outputFile))

#select plugin
process.analysis = cms.EDAnalyzer('EfficiencyCorrection')

process.p = cms.Path(process.analysis)
