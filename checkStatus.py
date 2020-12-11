#This resubmits all failed jobs. Run this at each CRABJOB directory.

import os
import commands as cmd

cwd = os.getcwd()
samples = cmd.getoutput('ls | grep Mu').split('\n')

with open('doneList.txt') as f:
  doneLists = f.readlines()

for sample in samples:

  if sample+'\n' in doneLists:
    print "In",sample+":"
    print "Completed job. Skipping..."
    continue

  os.chdir(cwd+"/"+sample)
  crabdir = cmd.getoutput('ls crab_projects')

  out = cmd.getoutput('crab status -d crab_projects/'+crabdir)
  lines = out.split('\n')
  for line in lines:
    print line

  out = cmd.getoutput('crab status -d crab_second')
  lines = out.split('\n')
  for line in lines:
    print line
