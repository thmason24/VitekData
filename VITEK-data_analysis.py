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
import percentchange as pc

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


sumAll=np.zeros(64,)

filteredSets = []
for mod in ['TX1', 'TX3']:
    #filteredSets.append([mod + ' only:           ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].condition == 'Data_Unsealed']])
    #filteredSets.append([mod + ' only:           ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].condition == 'Data_Unsealed']])
    filteredSets.append([mod + ' only:           ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].condition == 'Data_Unfilled' and dataSet[j].runNum < 6 ]])
    filteredSets.append([mod + ' only:           ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].condition == 'Data_Unsealed' and dataSet[j].runNum < 6 ]])
    filteredSets.append([mod + ' only:           ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].condition == 'Data_HeaterOff' and dataSet[j].runNum < 6 ]])
    filteredSets.append([mod + ' only:           ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].condition == 'Data_Normal' and dataSet[j].runNum < 6 ]])

   
for j in filteredSets:
    for i in j[1]:   #loop through the data in the Jth filtered set
        data=dataSet[i]
        print(data[1:])
        #mp.multiPlot(data[0])
        pcnt=pc.calcPC(data[0])
        print(np.minimum(pc.calcSumPC(pcnt,7),30*np.ones(64)))
        sumAll += np.minimum(pc.calcSumPC(pcnt,7),30*np.ones(64))
        
        #plt.figure()
        #plot sum percent change for first 7 reads
        #mp.pcntChangeLayout(pc.calcSumPC(pcnt,7),30)
        #plot maximum percent change
        #plt.figure()
        #mp.pcntChangeLayout(pcnt.max(0),8)
    plt.figure()
    print(len(j[1]))
    average=sumAll/len(j[1])
    print(sumAll)
    print(average)
    mp.pcntChangeLayout(average,40)    


