# -*- coding: utf-8 -*-
"""
Created on Thu May  7 09:50:11 2015

@author: 10016928
"""

import sys
import os
import collections
import numpy as np

#creat path to data
path=os.path.dirname(__file__)
dataDir=os.path.join(path,'WhiteCardModel/Data')

cardRun = collections.namedtuple('CardRun', 'data set optic TXmod run runNum cavity control')

dataSet=[]
for set in os.listdir(dataDir):     
    setPath=os.path.join(dataDir,set)
    TX1count = 0;
    TX3count = 0
    for run in os.listdir(setPath):
        TXmod = run.split()[0]
        setNum = set.split('_')[0]
        opticSN = set.split('_')[1]
        if TXmod == 'TX1':
            TX1count += 1
            runNum = TX1count
        elif TXmod == 'TX3':
            TX3count += 1
            runNum = TX3count     
                                               
        #map run number to cavity
        cavDict = {1:'W1F6',
                   2:'W1A8',
                   3:'W1A2',
                   4:'W1F4',
                   5:'W3A5',
                   6:'W3F7',
                   7:'W3F3',
                   8:'W3A8',
                   9:'P-4S2',
                   10:'P-4S2',
                   11:'P-4S2'}
        #run numbers greater than 8 are control
        if runNum > 8:
            control = True
        else:
            control = False
                                  
                               
        with open(os.path.join(setPath,run), 'r') as file:
            #load data into numpy array
            dataSet.append(cardRun(np.loadtxt(file)[:,1:],setNum,opticSN,TXmod,run,runNum,cavDict[runNum],control))
            file.close() 

#compute stats for the following filters

filteredSets = []
for mod in ['TX1' , 'TX3']:
    filteredSets.append([mod + ' only:           ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod]])
    filteredSets.append([mod + ' no control:     ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and not dataSet[j].control]])
    filteredSets.append([mod + ' control:        ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].control]])
    filteredSets.append([mod + ' OS4:            ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].optic == 'OS4' ]])
    filteredSets.append([mod + ' OS5             ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].optic == 'OS5' ]])
    filteredSets.append([mod + ' OS4 control:    ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].optic == 'OS4' and dataSet[j].control]])
    filteredSets.append([mod + ' OS5 control:    ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].optic == 'OS5' and dataSet[j].control]])
    filteredSets.append([mod + ' OS4 no control: ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].optic == 'OS4' and not dataSet[j].control]])
    filteredSets.append([mod + ' OS5 no control: ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].optic == 'OS5' and not dataSet[j].control]])




for j in filteredSets:
    meanArray=[]
    stdDevArray=[]
    params=[]
    for i in j[1]:
        data=dataSet[i]
        #print(data[1:])
        #generate sub Data set
        meanArray.append(data[0].mean())
        stdDevArray.append(data[0].std())

    #calculate range as max - min of the means    
    Range = np.array(meanArray).max() - np.array(meanArray).min()        
#    print(j[0] + 'Average ' + str(int(np.array(meanArray).mean().round())) + ' STDDEV ' + str(int(np.array(meanArray).std().round()))  + ' Range ' + str(int(Range.round())))
    print('{0:s}Average: {1:4d}    STDDEV:{2:4d}    Range:{3:4d} '.format(j[0], int(np.array(meanArray).mean().round()) ,  int(np.array(meanArray).std().round()) , int(Range.round())) )
#    print()