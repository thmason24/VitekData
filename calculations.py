# -*- coding: utf-8 -*-
"""
Created on Wed May  6 10:05:55 2015

@author: 10016928
"""
import numpy as np

"calculates percent change from raw values"
def calcPC(raw):
    pcntChange=np.zeros(raw.shape)
    for i in range(1,len(raw)+1):
        #calculate an array of max values for current and all past reads
        maxArray=raw[0:i,:].max(0)
        pcntChange[i-1,:]=100 * (maxArray-raw[i-1,:])/maxArray
    return pcntChange


def negCalcPC(raw):
    pcntChange=np.zeros(raw.shape)
    for i in range(1,len(raw)+1):
        #calculate an array of min values for current and all past reads
        minArray=raw[0:i,:].min(0)
        pcntChange[i-1,:]=100 * (minArray-raw[i-1,:])/minArray
    return pcntChange

#Calculates sum of percent change
def calcSum(read,numReads):
    return read[0:numReads,:].sum(0)
    
#Calculates range
def calcRange(raw):
    return raw.max(0)-raw.min(0) 
    
#Calculates max
def calcMax(raw):
    return raw.max(0)
    
#Calculates min
def calcMin(raw):
    return raw.min(0) 