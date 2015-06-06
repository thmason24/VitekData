# -*- coding: utf-8 -*-
"""
Created on Wed May 20 11:24:31 2015

@author: 10016928
"""

import os
import numpy as np
import collections

#extract data from a folder structure

#extract from condition study

cardRun = collections.namedtuple('CardRun', 'data runNum Optic TXmod condition')


def extractConditionData(path,subDir):
    dataSet=[]
    dataDir=os.path.join(path,subDir)
    for condition in os.listdir(dataDir):     
        #print(dir)
        conditionPath=os.path.join(dataDir,condition)
        #print(condition)
    
        for optic in os.listdir(conditionPath):
            #print(optic)
            opticDir=os.path.join(conditionPath,optic)
            TX1count = 0
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
    return dataSet
    
def extractWhiteCardDOE(path):
    dataSet=[]
    dataDir=os.path.join(path,'DOEwhiteCardData')
    for optic in os.listdir(dataDir):
        opticDir=os.path.join(dataDir,optic)
        TX1count = 0
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
                dataSet.append(cardRun(np.loadtxt(file)[:,1:],runNum, optic,TXmod,"White Card"))
                file.close() 
    return dataSet
    