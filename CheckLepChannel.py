import math

with open('pLHE_1.lhe') as f:
  lines = f.readlines()

events = []
OSevents = []
SSevents = []
MuMuevents = []
EEevents = []
EMuevents = []
lpairs = []

for i in range(len(lines)):
  if '<event>' in lines[i]:
    this_ev = []
    for j in range(20):
      if not 'amcatnlo' in lines[i+2+j]:
        this_ev.append(lines[i+2+j].strip())
      else:
        break
    events.append(this_ev)

for i in range(len(events)):
  lpair = []
  for ptcl in events[i]:
    if abs(int(ptcl.split(' ')[0]))==13 or abs(int(ptcl.split(' ')[0]))==11:
      lpair.append(int(ptcl.split(' ')[0]))
  lpairs.append(lpair)

isSSMuMu = 0
isSSEE = 0
isSSMuE = 0
isSSEMu = 0
isOSMuMu = 0
isOSEE = 0
isOSMuE = 0
isOSEMu = 0
for lpair in lpairs:
  if abs(lpair[0])==13 and abs(lpair[1])==11 and lpair[0]*lpair[1]>0:
	  isSSMuE+=1
  if abs(lpair[0])==11 and abs(lpair[1])==13 and lpair[0]*lpair[1]>0:
	  isSSEMu+=1
  if abs(lpair[0])==13 and abs(lpair[1])==13 and lpair[0]*lpair[1]>0:
	  isSSMuMu+=1
  if abs(lpair[0])==11 and abs(lpair[1])==11 and lpair[0]*lpair[1]>0:
	  isSSEE+=1
  if abs(lpair[0])==13 and abs(lpair[1])==11 and lpair[0]*lpair[1]<0:
	  isOSMuE+=1
  if abs(lpair[0])==11 and abs(lpair[1])==13 and lpair[0]*lpair[1]<0:
	  isOSEMu+=1
  if abs(lpair[0])==13 and abs(lpair[1])==13 and lpair[0]*lpair[1]<0:
	  isOSMuMu+=1
  if abs(lpair[0])==11 and abs(lpair[1])==11 and lpair[0]*lpair[1]<0:
	  isOSEE+=1

results = {}
results['SSMuE']=isSSMuE
results['SSEMu']=isSSEMu
results['SSMuMu']=isSSMuMu
results['SSEE']=isSSEE
results['OSMuE']=isOSMuE
results['OSEMu']=isOSEMu
results['OSMuMu']=isOSMuMu
results['OSEE']=isOSEE

results['Mu_X'] = isSSMuMu+isSSMuE+isOSMuMu+isOSMuE
results['E_X'] = isSSEMu+isSSEE+isOSEMu+isOSEE
results['X_Mu'] = isSSMuMu+isSSEMu+isOSMuMu+isOSEMu
results['X_E'] = isSSEE+isSSMuE+isOSEE+isOSMuE

results = sorted(results.items())

total = len(events)
print "total Nevents:",total
for i in range(len(results)):
  print results[i][0]+" Nevents:",results[i][1]
  print "eff:",float(results[i][1])/total,"+-",(float(results[i][1])/total) * math.sqrt(1./total + 1./(float(results[i][1])+10e-07)) #JH : to avoid ZeroDivision
