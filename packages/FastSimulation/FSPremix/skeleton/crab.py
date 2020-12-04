from CRABClient.UserUtilities import config, getUsernameFromCRIC

config = config()

###REQUESTNAME
config.General.workArea = 'crab_projects'
config.General.transferLogs = True
config.General.transferOutputs = True

config.JobType.pluginName = 'PrivateMC'
###PSETNAME
config.JobType.maxMemoryMB = 4000
config.JobType.numCores = 4

###OUTPUTDATASET
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromCRIC())
###OUTPUTTAG
config.Data.splitting = 'EventBased'
###UNITSPERJOB
###NJOBS
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True

config.Site.storageSite = 'T3_KR_KNU'
