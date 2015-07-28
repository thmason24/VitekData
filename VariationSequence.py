# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 12:44:57 2015

@author: 10016928
"""
import sys
import os
import pylab
import importData as imp
import numpy as np
import matplotlib.pyplot as plt
import multiPlots as mp
import calculations as calcs
import dataFilters as filt
import pylab as p


#creat path to data
path=os.path.dirname(__file__)
dataDir=os.path.join(path,'Data')

dataSetWhite = imp.extractWhiteCardDOE(path)
dataSetEng = filt.filterCondition(imp.extractConditionData(path,'DOE_ID_AST'),'Eng_Data')

dataSetGN = imp.extractConditionData(path,'AST-GN/Data')
dataSetGN = filt.excludeRun(dataSetGN,6)  # remove spurious last read
dataSetGP = imp.extractConditionData(path,'AST-GP67/Data')


dataSetDOE_ID =filt.selectedRuns(imp.extractConditionData(path,'DOE_ID_AST'),range(1,6))
dataSetDOE_ID =filt.filterCondition(dataSetDOE_ID,'Normal')

dataSetDOE_AST = filt.selectedRuns(imp.extractConditionData(path,'DOE_ID_AST'),range(6,11))
dataSetDOE_AST =filt.filterCondition(dataSetDOE_AST,'Normal')

#adjust down AST run tags because they are the last files in the directories after the first 5 which are ID runs
for j, i in enumerate(dataSetDOE_AST):
    replaceWith = i._replace(runNum=i.runNum-5)
    dataSetDOE_AST[j] = replaceWith



#choose one optic
module = 'TX1'


#opticPop1 = ['OS3', 'OS4', 'OS5', 'OS6' ]



stepArray1=[]
stepArray1.append(dataSetWhite)
stepArray1.append(dataSetEng)
stepArray1.append(dataSetDOE_ID)
stepArray1.append(dataSetDOE_AST)
opticPop1 = ['OS1', 'OS2', 'OS3', 'OS4', 'OS5', 'OS6' ]
colors1 = [ 'b', 'g', 'r', 'c', 'm', 'y']
positions1 = [0,1,2,3]
labels1 = ['white', 'Eng', 'FilledID', 'filledAST']
title1 =  'White Card Capa DOE'
inputs1=[opticPop1, stepArray1, positions1, labels1, title1, colors1]




stepArray2=[]
stepArray2.append(dataSetWhite)
stepArray2.append(dataSetEng)
stepArray2.append(filt.getSet(dataSetGN, 'Unfilled'  , module, None , None))
stepArray2.append(filt.getSet(dataSetGN, 'Unsealed' , module, None , None))
stepArray2.append(filt.getSet(dataSetGN, 'HeaterOff' , module, None , None))
stepArray2.append(filt.getSet(dataSetGN, 'Normal' , module, None , None))
opticPop2 = ['OS3', 'OS4', 'OS5', 'OS6' ]
colors2 = [ 'r', 'c', 'm', 'y']
positions2 = [0,1,2,3,4,5]
labels2 = ['white', 'Eng', 'unfilled', 'Unsealed', 'HeaterOff', 'Normal']
title2  = 'GN variance study'
inputs2=[opticPop2, stepArray2, positions2, labels2, title2, colors2]


stepArray3=[]
stepArray3.append(dataSetWhite)
stepArray3.append(dataSetEng)
stepArray3.append(filt.getSet(dataSetGP, 'Unfilled'  , module, None , None))
stepArray3.append(filt.getSet(dataSetGP, 'Unsealed' , module, None , None))
stepArray3.append(filt.getSet(dataSetGP, 'HeaterOff' , module, None , None))
stepArray3.append(filt.getSet(dataSetGP, 'Normal' , module, None , None))
opticPop3 = ['OS3', 'OS4', 'OS5', 'OS6' ]
colors3 = [ 'r', 'c', 'm', 'y']
positions3 = [0,1,2,3,4,5]
labels3 = ['white', 'Eng', 'unfilled', 'Unsealed', 'HeaterOff', 'Normal']
title3  = 'GP variance study'
colors3 = [ 'r', 'c', 'm', 'y']

inputs3=[opticPop3, stepArray3, positions3, labels3, title3, colors3]






#inputs=inputs2

for inputs in [inputs1, inputs2, inputs3]:
    opticPop= inputs[0]
    stepArray = inputs[1]
    labels = inputs[2]
    plt.figure()
    for opticIndex, optic in enumerate(opticPop):
        stdPlt=[]
        for step in stepArray:
            #filter optic
            data = filt.filterOptic(step,optic)
            #filter module
            data = filt.filterMod(data,module)
            stdVec =[]
            aveVec = []
            totalVec = []
            for i in data:
                #calcualte std over each read results in 64 well vector
                stdVec.append(i[0].std(0))
                #calculate average over each read results in 64 well vector
                aveVec.append(i[0].mean(0))
                #stack array for total std dev
                totalVec.append(i[0])
            
            #calcuate std over each average results in 64 well vector
            aveStd=np.array(aveVec).std(0)
            #std between reads
            readStd = np.array(stdVec).mean(0)
            #total stdDev
            totalStd = np.array(totalVec).std() 

            listOfData = np.array(aveVec).flatten()
            #p.figure()
            #p.hist(listOfData,50)
            #plt.draw()
            #plt.title(optic  )
            #input("Press Enter to continue...")
            
            #wait = input("PRESS ENTER TO CONTINUE.")
            #the goal is to find the average of standard deviations of each well
            stdPlt.append(np.array(aveVec).std(0).mean())

        
            
        plt.plot(stdPlt, lw = 5,label = optic, c = inputs[5][opticIndex] )
        pylab.xticks(inputs[2],inputs[3])
        plt.ylabel('average sigma (RTU)')
        plt.title(inputs[4] +  '\nstd dev of all reads and runs, averaged over all wells')
        plt.legend(bbox_to_anchor=(1.3,1))
        plt.ylim((0,700))
# 