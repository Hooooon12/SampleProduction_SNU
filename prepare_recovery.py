#Prepare to submit recovery jobs

import os
import commands as cmd

cwd = os.getcwd()
samples = cmd.getoutput('ls | grep -e DYTypeI_NLO_SF_M700_2016 -e DYTypeI_NLO_SF_M1000_2016').split('\n')
with open('doneList.txt') as f:
  doneLists = f.readlines()

for sample in samples:
  if sample+'\n' in doneLists:
    print "In",sample+":"
    print "Completed job. Skipping..."
    continue

  os.chdir(cwd+"/"+sample)
  crabdir = cmd.getoutput('ls crab_projects')

  status = cmd.getoutput('crab status -d crab_projects/'+crabdir)
  status = status.split('\n')
  for out in status:
    if 'Output dataset:' in out:
      myDataSet = out.split('\t')[-1]

  os.system('crab report -d crab_projects/'+crabdir)
  os.system('cp crab_projects/'+crabdir+'/results/processedLumis.json crab_projects/'+crabdir+'/results/myinputLumis.json')
  realpath = cmd.getoutput('realpath crab_projects/'+crabdir+'/results/myinputLumis.json')
  os.system('cp crab.py crab_recovery.py')
  with open('crab_recovery.py') as f:
    lines = f.readlines()
  newlines = []
  for line in lines:
    if 'CRABClient.UserUtilities' in line:
      line = line.strip()+', getLumiListInValidFiles\nfrom WMCore.DataStructs.LumiList import LumiList\n'
      newlines.append(line)
    elif 'requestName' in line:
      line = 'config.General.requestName = "recovery"\n'
      newlines.append(line)
    elif 'workArea' in line:
      pass
    else:
      newlines.append(line)

  with open('crab_recovery.py','w') as new_f:
    for newline in newlines:
      new_f.write(newline)
    new_f.write('\n')
    new_f.write('inputLumis = LumiList(filename=\''+realpath+'\') #### modify this lumilist to the full lumisection by yourself\n')
    new_f.write('processedLumis = getLumiListInValidFiles(dataset=\''+myDataSet+'\', dbsurl=\'phys03\')\n')
    new_f.write('newLumis = inputLumis - processedLumis\n')
    new_f.write('newLumis.writeJSON(\'my_lumi_mask.json\')\n')
    new_f.write('config.Data.lumiMask = \'my_lumi_mask.json\'\n')
    new_f.write('#### Now do: crab submit -c crab_recovery.py')
