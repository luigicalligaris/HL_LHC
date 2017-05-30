#########
#
# Example script to run the python extractor on MC events
# for the skimmed geometry
# 
# Usage: cmsRun SLHC_Extr.py
#
# Author: S.Viret (s.viret@ipnl.in2p3.fr)
# Date  : 24/05/2017
#
# Script tested with release CMSSW_9_2_0 (works either for Tilted of Flat geometries)
#
#########
#
# Here you choose if you want flat (True) or tilted (False) geometry
#

flat=False

###################

import FWCore.ParameterSet.Config as cms

process = cms.Process("MIBextractor")

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('L1Trigger.TrackTrigger.TrackTrigger_cff')
process.load('SimTracker.TrackTriggerAssociation.TrackTriggerAssociator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# Global tag for PromptReco
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('ProductNotFound')
)

# Number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# The file you want to extract
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring('file:PGun_example.root'),       
                            #fileNames = cms.untracked.vstring('file:PU_sample.root'),
			    #fileNames = cms.untracked.vstring('file:TT_example.root'),       
			    #fileNames = cms.untracked.vstring('file:QCD_example.root'),       
                            duplicateCheckMode = cms.untracked.string( 'noDuplicateCheck' )
)

# Load the extractor
process.load("Extractors.RecoExtractor.MIB_extractor_cff")

# Tune some options (see MIB_extractor_cfi.py for details)

process.MIBextraction.doMC             = True
process.MIBextraction.doSTUB           = True
process.MIBextraction.doPixel          = True
process.MIBextraction.doMatch          = True
process.MIBextraction.flatBarrel       = flat

process.p = cms.Path(process.MIBextraction)

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.combinedCustoms

if flat:
	print 'You choose the flat geometry'
	process.load('L1Trigger.TrackTrigger.TkOnlyFlatGeom_cff') # Special config file for TkOnly geometry
else:
	print 'You choose the tilted geometry'
	process.load('L1Trigger.TrackTrigger.TkOnlyTiltedGeom_cff') # Special config file for TkOnly geometry

# End of customisation functions
