# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 13:09:08 2015

@author: 10016928
"""


import sys
import os
import importData as imp
import numpy as np
import matplotlib.pyplot as plt
import dataFilters as filt


#creat path to data
path=os.path.dirname(__file__)
dataDir=os.path.join(path,'Data')


#extract data from condition set
dataSetWhite = imp.extractWhiteCardDOE(path)
EngCards =   filt.filterCondition(imp.extractConditionData(path,'DOE_ID_AST'),'Eng_Data')
ZJGP = filt.filterCondition(imp.extractConditionData(path,'AST-GP67/Data'),'Normal')
DOE_ID =  filt.filterCondition(filt.selectedRuns(imp.extractConditionData(path,'DOE_ID_AST'),range(1,6)),'Normal')
DOE_AST = filt.filterCondition(filt.selectedRuns(imp.extractConditionData(path,'DOE_ID_AST'),range(6,11)),'Normal')
#adjust down AST run tags because they are the last files in the directories after the first 5 which are ID runs
for j, i in enumerate(DOE_AST):
    replaceWith = i._replace(runNum=i.runNum-5)
    DOE_AST[j] = replaceWith

xDataSet=  dataSetWhite
#yDataSet = DOE_AST
yDataSet = ZJGP

#yDataSet = EngCards
#yDataSet = dataSetDOE_AST

    
#for i in dataSetDOE_ID:
#    print(i['runNum'])


opticPop = [  'OS1', 'OS2', 'OS3', 'OS4', 'OS5', 'OS6']

opticPop = [  'OS3', 'OS4', 'OS5', 'OS6']


#exclude wells with analine blue
analine = [3,8,9,10,11,63,64]

include = [i-1 for i in range(1,65) if i not in analine]
exclude = [i-1 for i in range(1,65) if i in analine]



for module in ['TX1', 'TX3']:
    plt.figure()
    xVec=[]
    xData=[]
    for i in opticPop:
        run=[]
        for j in range(1,6):
            run.append(filt.getSet(xDataSet, 'White Card', module, i, [j])[0][0].mean(0))
        xVec.append(run)
        xData.append(np.array(run).mean(0))    
    #print(xData[0])

    yVec=[]
    yData=[]
    for i in opticPop:
        run=[]
        for j in range(1,6):
            run.append(filt.getSet(yDataSet, None, module, i, [j])[0][0].mean(0))
        yVec.append(run)
        yData.append(np.array(run).mean(0))
    #print(yData[0])
    
    
    color = [ '0.75', 'm', 'b', 'g' , 'r', 'y' ]
    #remove exclusion wells
    
    xTotal=[]
    yTotal=[]
    for i, j in enumerate(opticPop):
        #remove exclusion wells
        x=xData[i]#[include]
        y=yData[i]#[include]
        xTotal.append(x)
        yTotal.append(y)
        plt.scatter(x,y,c=color[i],marker='o',s=40, label = j, alpha=0.6 )#'optic' + str(i+1)) 
        plt.title(module)
        plt.xlabel('White')
        plt.ylabel('Result')
    xmin,xmax = plt.xlim()
    plt.legend(bbox_to_anchor=(1.3,1))

    
    xTotal=[]
    yTotal=[]
    #remove the [] and comment to see individual optics plotted
    for i, j in []: #enumerate(opticPop):
        #remove exclusion wells
        plt.figure()
        x=xData[i]#[include]
        y=yData[i]#[include]
        xTotal.append(x)
        yTotal.append(y)
        plt.scatter(x,y,c=color[i],marker='o',s=40, label = j )#'optic' + str(i+1)) 
        plt.title(module)
        plt.xlabel('White')
        plt.ylabel('Result')
        plt.xlim(xmin,xmax)
        plt.legend(bbox_to_anchor=(1.3,1))