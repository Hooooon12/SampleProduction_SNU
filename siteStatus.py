#Get the result files of checkSites.py. Run this at each CRABJOB directory

import commands as cmd
import os

samples = cmd.getoutput('ls | grep Heavy').split('\n')
siteLog = open("siteLog.txt","w")

for sample in samples:
  crabdir = cmd.getoutput('ls '+sample+'/crab_projects')
  if sample+'/siteLog_'+crabdir+'.txt':
    with open(sample+'/siteLog_'+crabdir+'.txt') as f:
      lines = f.readlines()
    for line in lines:
      siteLog.write(line)
      siteLog.write('\n')

siteLog.close()

s = set()

with open('siteLog.txt') as g:
  sites = g.readlines()

for site in sites:
  if site != '\n':
    s.add([v for v in site.split(' ') if v][2])

s = list(s)

print s

results = {}

total=0
for site in sites:
  if site!='\n':
    total+=1
print total # This is the real number of total jobs. If a failed job's exit code is Unknown then it can confuse the value of 'a' below

for i in s:
  results[i] = [0,0,0]
  for site in sites:
    if i in site and 'finished' in site:
      results[i][0]+=1
    elif ((i in site) and (('Retry' in site) or ('failed' in site))):
      results[i][1]+=1
    elif i in site:
      results[i][2]+=1

a=0
b=0
c=0
d=0

for i in results.keys():
  a+=int(results[i][0])
  a+=int(results[i][1])
  a+=int(results[i][2])

for j in results.values():
  b+=int(j[0])
  c+=int(j[1])
  d+=int(j[2])

p = "==out of "+str(a)+" jobs=="
print '%-21s'%p,"finished :",b,", failed :",c,", etc :",d

for i,j in results.items():
  print '%-21s'%i,"finished :",'%-3s'%j[0],", failed :",j[1]

print "blacklist candidates:"
for i,j in results.items():
  if j[0]==0 and j[1]!=0:
    print '%-21s'%i,"finished :",'%-3s'%j[0],", failed :",j[1]
