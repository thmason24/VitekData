# -*- coding: utf-8 -*-
"""
Created on Thu May  7 09:50:11 2015

@author: 10016928
"""

import sys
import os
import collections
import numpy as np
import pylab as p
import matplotlib as plt
#creat path to data
path=os.path.dirname(__file__)
dataDir=os.path.join(path,'WhiteCardModel2/Data')


cardRun = collections.namedtuple('CardRun', 'data TXmod set cavity control barCode')

dataSet=[]
sets = []
for set in os.listdir(dataDir):     
    setPath=os.path.join(dataDir,set)
    TX1count = 0;
    TX3count = 0
    sets.append(set)
    if set == 'Control':
        control = True
    else:
        control = False


    for run in os.listdir(setPath):
        TXmod = run.split()[0]
        cavity = run.split()[1]
        barCode = run.split()[3]
        if TXmod == 'TX1':
            TX1count += 1
        elif TXmod == 'TX3':
            TX3count += 1
                                               
        #map run number to cavity

        #run numbers greater than 8 are control

                                  
                               
        with open(os.path.join(setPath,run), 'r') as file:
            #load data into numpy array
            dataSet.append(cardRun(np.loadtxt(file)[:,1:],TXmod,set,cavity,control, barCode))
            file.close() 
            

#compute stats for the following filters

filteredSets = []
for mod in ['TX1' , 'TX3']:
    filteredSets.append([mod + ' only:           ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod]])
    filteredSets.append([mod + ' no control:     ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and not dataSet[j].control]])
    filteredSets.append([mod + ' P4S2:     ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].barCode == "0090123101002509" ]])
    filteredSets.append([mod + ' control:     ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].control]])

    
#    filteredSets.append([mod + ' control:        ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].control]])

#for mod in ['TX1' , 'TX3']:
#    for set in sets:
#        filteredSets.append([mod + ' ' +  set + ' only:           ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].set == set]])

for j in filteredSets:
    meanArray=[]
    stdDevArray=[]
    params=[]
    for i in j[1]:
        data=dataSet[i]
        #print(data[1:])
        #generate sub Data set
        meanArray.append(data[0].mean())
        #sys.exit()
        stdDevArray.append(data[0].std())

    #calculate range as max - min of the means    
    Range = np.array(meanArray).max() - np.array(meanArray).min()  
    Min = np.array(meanArray).min()
    Max = np.array(meanArray).max()
#    print(j[0] + 'Average ' + str(int(np.array(meanArray).mean().round())) + ' STDDEV ' + str(int(np.array(meanArray).std().round()))  + ' Range ' + str(int(Range.round())))
    print('{0:<30s}Average: {1:4d}    STDDEV:{2:4d}    Range:{3:4d}  Min: {4:4d} Max: {5:4d} '.format(j[0], int(np.array(meanArray).mean().round()) ,  int(np.array(meanArray).std().round()) , int(Range.round()), int(Min.round()), int(Max.round()) ))
#    print()
    #print("test" , len(meanArray))
    #p.figure()
    
    #p.hist(meanArray,50)
    #sys.exit()