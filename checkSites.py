#Run this at your CRABJOB/Sample directory

import commands as cmd

crabdir = cmd.getoutput('ls crab_projects')

a = cmd.getoutput('crab status -d crab_projects/'+crabdir+' --long | grep -e finished -e failed -e toRetry -e transferring -e running | grep -e T2 -e T3 -e Unknown')

siteLog = open("siteLog_"+crabdir+".txt", "w")
siteLog.write(a)
siteLog.close()
