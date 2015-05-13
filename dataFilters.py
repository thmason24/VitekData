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

def condition(dataSet,condition):
    filteredSet = []
    for i in [j for j in range(0,len(dataSet)) if dataSet[j].condition == condition ]:
        filteredSet.append(dataSet[i])
    return filteredSet  
    
def selRun(dataSet,condition,optic,mod,runNum):
    filteredSet = []
    for i in [j for j in range(0,len(dataSet)) if dataSet[j].condition == condition and dataSet[j].Optic == optic and dataSet[j].TXmod == mod and dataSet[j].runNum == runNum ]:
        filteredSet.append(dataSet[i])
    if len(filteredSet) == 0:
        print('ERROR:  empty set')
        sys.exit()
        return
    else:
        return filteredSet[0][0]  