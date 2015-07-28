#VITEK data analysis
#Tim Mason
#5-5-2015
#Analyzes a bunch of VITEK-Data


import sys
import os
import pylab
import importData as imp
import numpy as np
import matplotlib.pyplot as plt
import multiPlots as mp
import calculations as calcs
import dataFilters as filt


#creat path to data
path=os.path.dirname(__file__)
dataDir=os.path.join(path,'Data')


#extract data from condition set
dataSetGN = imp.extractConditionData(path,'AST-GN/Data')
dataSetGN = filt.excludeRun(dataSetGN,6)
dataSetGP = imp.extractConditionData(path,'AST-GP67/Data')
dataSetDOE_AST =filt.selectedRuns(imp.extractConditionData(path,'DOE_ID_AST'),range(1,6))
dataSetDOE_ID =filt.selectedRuns(imp.extractConditionData(path,'DOE_ID_AST'),range(6,11))

#extract data from DOE white cardSet
dataSetWhite = imp.extractWhiteCardDOE(path)


#add filter
#filteredSets = filt.removeSixth(dataSet)   
#filteredSets = filt.removeSixth(dataSet)   
#filteredSets = filt.allRuns(dataSet)   
#filteredSets = filt.filterMod(dataSet,'TX1')

filteredSets = []

TestDataSet = dataSetGP
module = 'TX1'

filteredSet = ['white', filt.filterCondition(dataSetWhite,'White Card')]
filteredSets.append(filteredSet)

resultSet   = ['Unfilled ' , filt.getSet(TestDataSet, 'Unfilled' , module, None , None)]
filteredSets.append(resultSet)

resultSet   = ['HeaterOff ', filt.getSet(TestDataSet, 'HeaterOff' , module, None , None)]
filteredSets.append(resultSet)

resultSet   = ['unsealed ',  filt.getSet(TestDataSet, 'Unsealed' , module, None , None)]
filteredSets.append(resultSet)

resultSet   = ['Normal ',    filt.getSet(TestDataSet, 'Normal' , module, None , None)]
filteredSets.append(resultSet)





#set this to inhibit plots
#filteredSets=[]

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
    mp.rowOfPlots(aveRaw,aveRange,None,None,aveSumPcnt,aveSumNegPcnt,len(j[1]),'Ave ' + j[0]);
    #plot std deviation
    #mp.rowOfPlots(rawStd,rangeStd,minStd,maxStd,sumPcntStd,sumNegPcntStd,len(j[1]),'Std ' + j[0]);
    #plot std range
    #mp.rowOfPlots(rawRange,rangeRange,minRange,maxRange,sumPcntRange,sumNegPcntRange,len(j[1]),'Rng ' + j[0]);
    
    #multiplot
    #multiPlot(read)    


for i in range(1,2):
    selectedSet=filt.selRun(dataSetGN,'Data_Normal','Optic5','TX1',i)
    #mp.multiPlot(selectedSet,0,4095)
    mp.multiPlot(calcs.calcPC(selectedSet),0,10)
    plt.figure()
    mp.layoutPlot(calcs.calcSum(calcs.calcPC(selectedSet),7),grayMin=None,grayMax=None)
    plt.title('Sum')

    