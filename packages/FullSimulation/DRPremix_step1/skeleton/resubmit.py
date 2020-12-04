#########################################################################################################
#
#  This resubmits all failed jobs in CRABJOB directory.
#  Place this at CRABJOB directory and do 'python resubmit.py' at times.
#  If the same number of jobs fails repeatedly,
#  you may need to check 'crab status -d <sample_name>/crab_projects/<requestName> [--long]' by yourself.
#  If you are under CMSSW_7_* and getting 'Error contacting CRIC',
#  see https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3FAQ#crab_commands_fails_with_Error_U
#
#########################################################################################################

import os, sys
import commands as cmd

try: os.environ["CMSSW_VERSION"]
except:
  print "Please run this after setting CMSSW. Exiting..."
  sys.exit()

blacklists = ''
with open('###BLACKLIST') as f:
  lines = f.readlines()
  for line in lines:
    blacklists+=line.strip()+','

blacklists = blacklists[:-1]

cwd = os.getcwd()
samples = cmd.getoutput("ls -l | grep ^d | awk '{print $9}'").split('\n') #Use 'ls | grep <sample_name>' if needed.
doneTxt = open('doneList.txt','a')
with open('doneList.txt') as f:
  doneLists = f.readlines()

for sample in samples:
  if sample+'\n' in doneLists:
    print "In",sample+":"
    print "Completed job. Skipping..."
    continue
  lines = []
  index = ''
  Nfailed = 0

  os.chdir(cwd+"/"+sample)
  crabdir = cmd.getoutput('ls crab_projects')

  out = cmd.getoutput('crab status -d crab_projects/'+crabdir+' --long | grep -e finished -e failed -e toRetry -e transferring -e running -e COMPLETED | grep -e T2 -e T3 -e COMPLETED')
  if 'COMPLETED' in out:
    print "In",sample+":"
    print "Completed job. Skipping..."
    doneTxt.write(sample+'\n')
    continue
  lines = out.split('\n')

  for line in lines:
    if 'failed' in line:
      index+=line.strip().split(' ')[0]+','
      Nfailed+=1

  index = index[:-1]
  
  if Nfailed == 0:
    print "In",sample+":"
    print "0 job failed. Skipping..."
  else:
    print "In",sample+":"
    print Nfailed,"job(s) failed. Resubmitting..."
    os.system('crab resubmit --siteblacklist='+blacklists+' --jobids='+index)

doneTxt.close()
