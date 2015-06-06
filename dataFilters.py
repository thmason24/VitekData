# -*- coding: utf-8 -*-
"""
Created on Mon May 11 09:54:29 2015

@author: 10016928
"""
import sys

def allRuns(dataSet):
    filteredSet = []
    for mod in ['TX1', 'TX3']:
        filteredSet.append([mod + ' Unfilled    ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].condition == 'Data_Unfilled'  ]])
        filteredSet.append([mod + ' Unsealed:   ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].condition == 'Data_Unsealed'  ]])
        filteredSet.append([mod + ' Heater off: ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].condition == 'Data_HeaterOff' ]])
        filteredSet.append([mod + ' Normal:     ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].condition == 'Data_Normal'    ]])
    return filteredSet
    
def removeSixth(dataSet):
    filteredSet = []
    for mod in ['TX1', 'TX3']:
        filteredSet.append([mod + ' Unfilled    ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].condition == 'Data_Unfilled' and dataSet[j].runNum < 6 ]])
        filteredSet.append([mod + ' Unsealed:   ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].condition == 'Data_Unsealed' and dataSet[j].runNum < 6 ]])
        filteredSet.append([mod + ' Heater off: ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].condition == 'Data_HeaterOff' and dataSet[j].runNum < 6 ]])
        filteredSet.append([mod + ' Normal:     ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].condition == 'Data_Normal' and dataSet[j].runNum < 6 ]])
    return filteredSet
        
def removeSixthTX1(dataSet):
    filteredSet = []
    for mod in ['TX1']:
        filteredSet.append([mod + ' Unfilled    ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].condition == 'Data_Unfilled' and dataSet[j].runNum < 6 ]])
        filteredSet.append([mod + ' Unsealed:   ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].condition == 'Data_Unsealed' and dataSet[j].runNum < 6 ]])
        filteredSet.append([mod + ' Heater off: ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].condition == 'Data_HeaterOff' and dataSet[j].runNum < 6 ]])
        filteredSet.append([mod + ' Normal:     ',[j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod and dataSet[j].condition == 'Data_Normal' and dataSet[j].runNum < 6 ]])
    return filteredSet    
    
def filterOptic(dataSet,Optic):
    filteredSet = []
    for i in [j for j in range(0,len(dataSet)) if dataSet[j].Optic == Optic ]:
        filteredSet.append(dataSet[i])
    return filteredSet

def filterMod(dataSet,mod):
    filteredSet = []
    for i in [j for j in range(0,len(dataSet)) if dataSet[j].TXmod == mod ]:
        filteredSet.append(dataSet[i])
    return filteredSet    

def excludeRun(dataSet,run):
    filteredSet = []
    for i in [j for j in range(0,len(dataSet)) if dataSet[j].runNum != run ]:
        filteredSet.append(dataSet[i])
    return filteredSet    
    
def selectedRuns(dataSet,runs):
    filteredSet = []
    for i in [j for j in range(0,len(dataSet)) if dataSet[j].runNum in runs ]:
        filteredSet.append(dataSet[i])
    return filteredSet 

def filterCondition(dataSet,condition):
    filteredSet = []
    for i in [j for j in range(0,len(dataSet)) if dataSet[j].condition == condition ]:
        filteredSet.append(dataSet[i])
    return filteredSet  
    
def selRun(dataSet,condition,optic,mod,runNum):
    filteredSet = []
    for i in [j for j in range(0,len(dataSet)) if dataSet[j].condition == condition and dataSet[j].Optic == optic and dataSet[j].TXmod == mod and dataSet[j].runNum == runNum ]:
        filteredSet.append(dataSet[i])
    if len(filteredSet) == 0:
        print('ERROR:  empty set from SelRun')
        sys.exit()
        return
    else:
        return filteredSet[0][0]  

def getSet(dataSet,condition,mod,optic,runs):
    filteredSet = dataSet
    if ( condition != None ):
        filteredSet = filterCondition(filteredSet,condition)
    if ( mod != None ):
        filteredSet = filterMod(filteredSet,mod)
    if ( optic != None ): 
        filteredSet = filterOptic(filteredSet,optic)
    if ( runs != None ):
        filteredSet = selectedRuns(filteredSet,runs)
        

    return filteredSet    
    
