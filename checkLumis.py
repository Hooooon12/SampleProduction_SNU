from CRABClient.UserUtilities import config, getUsernameFromCRIC, getLumiListInValidFiles
from WMCore.DataStructs.LumiList import LumiList

processedLumis = getLumiListInValidFiles(dataset='/DYTypeI_NLO_SF_M1100_2016/jihunk-DRPremix_step2__CMSSW_8_0_31-f7b11725a86c799f51ca60747917325e/USER', dbsurl='phys03') #Get lumilist of valid files on DAS
print processedLumis
Njobs=0
lumilist = processedLumis.getCompactList()["1"]
for i in lumilist:
  Njobs+=len(range(i[0],i[1]+1))
print Njobs/5 #modify this to proper value
