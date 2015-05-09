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

cardRun = collections.namedtuple('CardRun', 'data OpticSN opticMod condition')

dataSet=[]
for condition in os.listdir(dataDir):     
    #print(dir)
    conditionPath=os.path.join(dataDir,condition)
    #print(condition)

    for optic in os.listdir(conditionPath):
        #print(optic)
        opticDir=os.path.join(conditionPath,optic)
        
        for testRun in os.listdir(opticDir):
            #print(testRun)
            #add this to database
            opticMod=testRun.split()[0]
                            
            with open(os.path.join(opticDir,testRun), 'r') as file:
                #load data into numpy array
                dataSet.append(cardRun(np.loadtxt(file)[:,1:],optic,opticMod,dir))
                file.close() 


sumAll=np.zeros(64,)
for i in range(0,12):
    data=dataSet[i]
    print(data[1:])
    #mp.multiPlot(data[0])
    pcnt=pc.calcPC(data[0])
    print(pc.calcSumPC(pcnt,7).shape)
    sumAll += pc.calcSumPC(pcnt,7)
    #plt.figure()
    #plot sum percent change for first 7 reads
    #mp.pcntChangeLayout(pc.calcSumPC(pcnt,7),30)
    #plot maximum percent change
    #plt.figure()
    #mp.pcntChangeLayout(pcnt.max(0),8)
mp.pcntChangeLayout(sumAll,430)    


