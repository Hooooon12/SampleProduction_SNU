#This resubmits all failed jobs. Run this at each CRABJOB directory.

import os
import commands as cmd

cwd = os.getcwd()
samples = cmd.getoutput('ls | grep Heavy').split('\n')
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
    os.system('crab resubmit --jobids='+index)

doneTxt.close()