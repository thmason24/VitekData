# -*- coding: utf-8 -*-
"""
Created on Wed May  6 10:05:55 2015

@author: 10016928
"""
import numpy as np

"calculates percent change from raw values"
def calcPC(raw,numReads):
    pcntChange=np.zeros(raw.shape)
    for i in range(1,len(raw)+1):
        #calculate an array of max values for current and all past reads
        maxArray=raw[0:i,:].max(0)
        pcntChange[i-1,:]=100 * (maxArray-raw[i-1,:])/maxArray

    return pcntChange


