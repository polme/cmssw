from __future__ import print_function
import FWCore.ParameterSet.Config as cms
from DQMServices.Core.DQMEDHarvester import DQMEDHarvester
import DQMServices.Components.test.checkBooking as booking
import DQMServices.Components.test.createElements as c
import sys

process = cms.Process("TESTHARV")

folder = "TestFolder/"

process.load('Configuration.StandardSequences.EDMtoMEAtRunEnd_cff')
process.load("DQMServices.Components.DQMFileSaver_cfi")

# Input source
process.source = cms.Source("PoolSource",
                            secondaryFileNames = cms.untracked.vstring(),
                            fileNames = cms.untracked.vstring('file:dqm_file1_oldf.root',
                                                              'file:dqm_file2_oldf.root',
                                                              'file:dqm_file3_oldf.root'),
                            processingMode = cms.untracked.string('RunsAndLumis')
)

elements = c.createElements()

process.harvester = cms.EDAnalyzer("DummyHarvestingClient",
                                   folder   = cms.untracked.string(folder),
                                   elements = cms.untracked.VPSet(*elements),
                                   cumulateRuns = cms.untracked.bool(False),
                                   cumulateLumis = cms.untracked.bool(True))

process.eff = DQMEDHarvester("DQMGenericClient",
                             efficiency = cms.vstring("eff1 \'Eff1\' Bar0 Bar1"),
                             resolution = cms.vstring(),
                             subDirs = cms.untracked.vstring(folder))

process.dqmSaver.workflow = cms.untracked.string("/Test/File1_File2_File3_oldf/DQM")
process.dqmSaver.saveByLumiSection = cms.untracked.int32(1)
process.dqmSaver.saveByRun = cms.untracked.int32(1)

process.p = cms.Path(process.EDMtoME + process.harvester + process.eff)
process.o = cms.EndPath(process.dqmSaver)

process.add_(cms.Service("DQMStore"))
#process.DQMStore.verbose = cms.untracked.int32(3)
#process.add_(cms.Service("Tracer"))

if len(sys.argv) > 2:
    if sys.argv[2] == "Collate": 
        print("Collating option for multirunH")
        process.DQMStore.collateHistograms = cms.untracked.bool(True)
        process.dqmSaver.saveAtJobEnd = cms.untracked.bool(True)
        process.dqmSaver.forceRunNumber = cms.untracked.int32(999999)

