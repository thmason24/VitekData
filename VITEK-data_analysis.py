#VITEK data analysis
#Tim Mason
#5-5-2015
#Analyzes a bunch of VITEK-Data


import sys
import os
import collections
import numpy as np
import matplotlib.pyplot as plt
import multiPlots as mp
import calculations as calcs
import dataFilters as filt

#creat path to data
path=os.path.dirname(__file__)
dataDir=os.path.join(path,'Data')

cardRun = collections.namedtuple('CardRun', 'data runNum Optic TXmod condition')

dataSet=[]
for condition in os.listdir(dataDir):     
    #print(dir)
    conditionPath=os.path.join(dataDir,condition)
    #print(condition)

    for optic in os.listdir(conditionPath):
        #print(optic)
        opticDir=os.path.join(conditionPath,optic)
        TX1count = 0;
        TX3count = 0
        for testRun in os.listdir(opticDir):
            #print(testRun)
            #add this to database
            TXmod=testRun.split()[0]
            if TXmod == 'TX1':
                TX1count += 1
                runNum = TX1count
            elif TXmod == 'TX3':
                TX3count += 1
                runNum = TX3count  
            with open(os.path.join(opticDir,testRun), 'r') as file:
                #load data into numpy array
                dataSet.append(cardRun(np.loadtxt(file)[:,1:],runNum, optic,TXmod,condition))
                file.close() 


#add filter
#filteredSets = filt.removeSixth(dataSet)   
#filteredSets = filt.removeSixth(dataSet)   
#filteredSets = filt.allRuns(dataSet)   
#filteredSets = filt.filterMod(dataSet,'TX1')

filteredSets = []

filteredSet = ['', filt.condition(dataSet,'Data_Unfilled')]
filteredSet = ['', filt.excludeRun(filteredSet[1],6)]
filteredSet = ['Unfilled ', filt.filterMod(filteredSet[1],'TX1')]
filteredSets.append(filteredSet)

filteredSet = ['', filt.condition(dataSet,'Data_Unsealed')]
filteredSet = ['', filt.excludeRun(filteredSet[1],6)]
filteredSet = ['UnSealed ', filt.filterMod(filteredSet[1],'TX1')]
filteredSets.append(filteredSet)

filteredSet = ['', filt.condition(dataSet,'Data_HeaterOff')]
filteredSet = ['', filt.excludeRun(filteredSet[1],6)]
filteredSet = ['HeaterOff ', filt.filterMod(filteredSet[1],'TX1')]
filteredSets.append(filteredSet)
#
filteredSet = ['', filt.condition(dataSet,'Data_Normal')]
filteredSet = ['', filt.excludeRun(filteredSet[1],6)]
filteredSet = ['Normal ', filt.filterMod(filteredSet[1],'TX1')]
filteredSets.append(filteredSet)



for j in filteredSets:
    sumAll=np.zeros(64,)
    sumPcnt=np.zeros(64,)
    sumNegPcnt=np.zeros(64,)
    sumRange=np.zeros(64,)
    sumMin=np.zeros(64,)
    sumMax=np.zeros(64,)
    maxVec=[]
    minVec=[]
    rangeVec=[]
    averageVec=[]
    sumPcntVec=[]
    sumNegPcntVec=[]
    print()
    for i in j[1]:   #loop through the data in the Jth filtered set
        #print(i[1:]);
        #mp.multiPlot(data[0])
        #convert to percent change
        pcnt=calcs.calcPC(i[0])
        negPcnt=calcs.negCalcPC(i[0])
        #sum all from this filter
        sumPcntVec.append(calcs.calcSum(pcnt,7))
        sumNegPcntVec.append(np.absolute(calcs.calcSum(negPcnt,7)))
        averageVec.append(calcs.calcSum(i[0],len(i[0]))/len(i[0]))
        rangeVec.append(calcs.calcRange(i[0]))        
        minVec.append(calcs.calcMin(i[0]))
        maxVec.append(calcs.calcMax(i[0]))

#calculate average values             
    aveSumPcnt=np.array(sumPcntVec).sum(0)
    aveSumNegPcnt=np.array(sumNegPcntVec).sum(0)
    aveRaw=np.array(averageVec).sum(0)
    aveRange=np.array(rangeVec).sum(0)       
    aveMin=np.array(minVec).sum(0)
    aveMax=np.array(maxVec).sum(0)
#calculate std deviations
    sumPcntStd=np.array(sumPcntVec).std(0)
    sumNegPcntStd=np.array(sumNegPcntVec).std(0)
    rawStd=np.array(averageVec).std(0)
    rangeStd=np.array(rangeVec).std(0)       
    minStd=np.array(minVec).std(0)
    maxStd=np.array(maxVec).std(0)
#calculate ranges
    sumPcntRange     = np.array(sumPcntVec).max(0)    - np.array(sumPcntVec).min(0)
    sumNegPcntRange  = np.array(sumNegPcntVec).max(0) - np.array(sumNegPcntVec).min(0)
    rawRange      = np.array(averageVec).max(0)    - np.array(averageVec).min(0)
    rangeRange    = np.array(rangeVec).max(0)      - np.array(rangeVec).min(0)      
    minRange      = np.array(minVec).max(0)        - np.array(minVec).min(0)
    maxRange      = np.array(maxVec).max(0)        - np.array(maxVec).min(0)

    #plot average
    #mp.rowOfPlots(aveRaw,aveRange,aveMin,aveMax,aveSumPcnt,aveSumNegPcnt,len(j[1]),'Ave ' + j[0]);
    #plot std deviation
  #  mp.rowOfPlots(rawStd,rangeStd,minStd,maxStd,sumPcntStd,sumNegPcntStd,len(j[1]),'Std ' + j[0]);
  #  #plot std range
  #  mp.rowOfPlots(rawRange,rangeRange,minRange,maxRange,sumPcntRange,sumNegPcntRange,len(j[1]),'Rng ' + j[0]);
    
    #multiplot
 #   multiPlot(read)    
selectedSet=filt.selRun(dataSet,'Data_Normal','Optic3','TX1',1)
mp.multiPlot(selectedSet)