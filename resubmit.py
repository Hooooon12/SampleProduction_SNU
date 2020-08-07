#This gets the output of checkSites.py and resubmit failed jobs

import os
import commands as cmd

sites = cmd.getoutput('ls | grep site')

with open(sites) as f:
  lines = f.readlines()

a = ''
n = 0

for line in lines:
  if 'failed' in line:
    a+=line.strip().split(' ')[0]+','
    n+=1

a = a[:-1]

print n,"job(s) failed. Resubmitting..."
os.system('crab resubmit --jobids='+a)
