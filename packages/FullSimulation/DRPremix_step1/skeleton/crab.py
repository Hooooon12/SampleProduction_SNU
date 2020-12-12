from CRABClient.UserUtilities import config, getUsernameFromCRIC

config = config()

###REQUESTNAME
config.General.workArea = 'crab_projects'
config.General.transferLogs = True
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
###PSETNAME
config.JobType.maxMemoryMB = 4000
config.JobType.numCores = 2

###INPUTDATASET
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromCRIC())
###OUTPUTTAG
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = True
config.Data.ignoreLocality = True

config.Site.storageSite = 'T3_KR_KNU'
config.Site.whitelist = ['T2_*','T3_*']
###BLACKLIST
