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
dataSetGN = filt.excludeRun(dataSetGN,6)  # remove spurious last read
dataSetGP = imp.extractConditionData(path,'AST-GP67/Data')
dataSetGP_train = filt.selectedRuns(imp.extractConditionData(path,'AST-GP67/Data'),range(1,9))
dataSetGP_crossVal = filt.selectedRuns(imp.extractConditionData(path,'AST-GP67/Data'),range(9,16))
#lower index
for j, i in enumerate(dataSetGP_crossVal):
    replaceWith = i._replace(runNum=i.runNum-8)
    dataSetGP_crossVal[j] = replaceWith

dataSetDOE_ID =filt.selectedRuns(imp.extractConditionData(path,'DOE_ID_AST'),range(1,6))
dataSetDOE_AST =filt.selectedRuns(imp.extractConditionData(path,'DOE_ID_AST'),range(6,11))
for j, i in enumerate(dataSetDOE_AST):
    replaceWith = i._replace(runNum=i.runNum-5)
    dataSetDOE_AST[j] = replaceWith
#extract data from DOE white cardSet
dataSetWhite = imp.extractWhiteCardDOE(path)

#prediction code
fullAvePredictDict = {}
avePredictWellDict = {}
fullAveResultDict = {}
aveResultWellDict = {}
fullAveTestDict = {}
aveTestWellDict = {}
selectWell=7
wellRange=range(0,64)
#wellRange=range(selectWell,selectWell+1)
for i in range(1,2):
    well=i
    predictMatrix=np.zeros((4,4))
    for indexPredict, opticPredict in enumerate(['OS3', 'OS4', 'OS5','OS6']):
        for indexResult, opticResult in enumerate(['OS3', 'OS4', 'OS5','OS6']):
            
            module='TX1'
            #get predictor set
            predictorSet = filt.getSet(dataSetWhite, 'White Card', module, opticPredict, None)            

            #get result Set
            resultSet    = filt.getSet(dataSetGP_train, 'Normal', module, opticResult, None)
            testSet      = filt.getSet(dataSetGP_crossVal, 'Normal', module, opticResult, None)
            #testSet      = filt.getSet(dataSetGN, 'Normal', module, opticResult, None)
            #resultSet    = filt.getSet(dataSetDOE_ID, 'Normal', module, opticResult, None)
            #resultSet    = filt.getSet(dataSetDOE_AST, 'Normal', module, opticResult, None)
            #resultSet    = filt.getSet(dataSetGN, 'Normal', module, opticResult, None)
            
            averageVec=[]
            for i in predictorSet:
                #calcualte average over each read results in 64 well vector
                averageVec.append(i[0].mean(0))
            #calcuate average over each run results in 64 well vector    
            avePredictor=np.array(averageVec).mean(0)
            #store average for each wellin vector for indexing later by optic set
            avePredictWellDict[opticPredict] = avePredictor
            #calculate and store total average
            fullAvePredictDict[opticPredict]=np.array(averageVec).mean()           
            stdPredictor=np.array(averageVec).std(0)
            
            averageVec=[]
            for i in resultSet:
                averageVec.append(i[0].mean(0))
            aveResult=np.array(averageVec).mean(0)
            aveResultWellDict[opticResult] = aveResult
            fullAveResultDict[opticResult]=np.array(averageVec).mean()
            stdResult=np.array(averageVec).std(0)         

            averageVec=[]
            for i in testSet:
                averageVec.append(i[0].mean(0))
            aveTest=np.array(averageVec).mean(0)
            aveTestWellDict[opticResult] = aveTest
            fullAveTestDict[opticResult]=np.array(averageVec).mean()
            stdTest=np.array(averageVec).std(0)         

     
    absPredict=np.array([[fullAvePredictDict['OS3'],
                fullAvePredictDict['OS4'],
                fullAvePredictDict['OS5'],
                fullAvePredictDict['OS6']]])

    absResult=np.array([[fullAveResultDict['OS3'],
                fullAveResultDict['OS4'],
                fullAveResultDict['OS5'],
                fullAveResultDict['OS6']]])
                
    absTest = np.array([[fullAveTestDict['OS3'],
                fullAveTestDict['OS4'],
                fullAveTestDict['OS5'],
                fullAveTestDict['OS6']]])

    
    theta_array = [None]*64
    train_error = []
    for i in wellRange:
        X = np.array([avePredictWellDict['OS3'][i],
                        avePredictWellDict['OS4'][i],
                        avePredictWellDict['OS5'][i],
                        avePredictWellDict['OS6'][i]])
        #add bias term
        X = np.vstack([np.ones(len(X)),X]).T
        y = np.matrix([[aveResultWellDict['OS3'][i],
                        aveResultWellDict['OS4'][i],
                        aveResultWellDict['OS5'][i],
                        aveResultWellDict['OS6'][i]]]).T
        # least squares to find prediction theta variables using average values

        theta0 , theta1 = np.linalg.lstsq(X,y)[0]
        theta = np.matrix([theta0[0,0],theta1[0,0]])
        prediction = (theta * X.T).T
        train_error.append(np.abs(prediction-y).sum()/4)
        
        #plt.figure()
        #find min values for trend line
        Xmin=X[:,1].min() - 50
        Xmax=X[:,1].max() + 50
        
        x=np.matrix(np.arange(Xmin,Xmax,0.01))
        x=np.concatenate((np.ones((1,x.shape[1])),x),axis=0).T
        trendLine = (theta * x.T).T
        plt.scatter(x[:,1],trendLine,marker='s',c='b',alpha=1,s=1)
        plt.scatter(X[:,1],np.array(y.T)[0,:],c='r',marker='o',s=100, alpha=1)    
        theta_array[i] = theta  

    #plot againt test set
    
    plt.figure()
    
    test_error=[]
    for i in wellRange:
        X = np.array([avePredictWellDict['OS3'][i],
                        avePredictWellDict['OS4'][i],
                        avePredictWellDict['OS5'][i],
                        avePredictWellDict['OS6'][i]])
        #add bias term
        X = np.vstack([np.ones(len(X)),X]).T
        y = np.matrix([[aveTestWellDict['OS3'][i],
                        aveTestWellDict['OS4'][i],
                        aveTestWellDict['OS5'][i],
                        aveTestWellDict['OS6'][i]]]).T
        # least squares to find prediction theta variables using average values
        prediction = (theta_array[i] * X.T).T
        test_error.append(np.abs(prediction-y).sum()/4)
        #plt.figure()
        #find min values for trend line
        Xmin=X[:,1].min() - 50
        Xmax=X[:,1].max() + 50
        
        x=np.matrix(np.arange(Xmin,Xmax,0.01))
        x=np.concatenate((np.ones((1,x.shape[1])),x),axis=0).T
        trendLine = (theta_array[i] * x.T).T
        plt.scatter(x[:,1],trendLine,marker='s',c='b',alpha=1,s=1)
        plt.scatter(X[:,1],np.array(y.T)[0,:],c='r',marker='o',s=100)
        
    print('Training Error  ' + str(np.array(train_error).mean()))
    print('TestSet  Error  ' + str(np.array(test_error).mean()))


    
    plt.figure()
    
    
    plt.pcolor(np.concatenate((absPredict,absResult),axis=0),cmap='gray')
    #plt.pcolor(np.concatenate((np.array([[0, 0, 0, 0]]),np.array([[1, 1, 1, 1]])),axis=0),cmap='gray')
    
    plt.colorbar()
    pylab.yticks([0.5,1.5],['predict','result'])
    pylab.xticks([0.5,1.5,2.5,3.5],['OS3','OS4','OS5','OS6'])

 #   sys.exit()        
    #project results for each combo and find least square error
    # use each optic WC to predict for each result and compare errors
    Err=np.zeros((4,4))
    prediction=np.array(np.zeros((4,4,64)))
    for indexPredict, opticPredict in enumerate(['OS3', 'OS4', 'OS5','OS6']):
        for indexResult, opticResult in enumerate(['OS3', 'OS4', 'OS5','OS6']):
            for well in wellRange:
                X=np.matrix([1, avePredictWellDict[opticPredict][well]]).transpose()
                y=aveResultWellDict[opticResult][well]
                prediction[indexPredict,indexResult,well]=(theta_array[well] * X)[0,0]
                squareError = np.square(y-prediction)
            
            Err[indexPredict,indexResult] = np.abs(prediction[indexPredict,indexResult,:] - aveResultWellDict[opticResult]).mean()
    plt.figure()
    plt.pcolor(Err,cmap='gray')#,vmin=0.8,vmax=1) 
    plt.colorbar()
    pylab.yticks([0.5,1.5,2.5,3.5],['OS3','OS4','OS5','OS6'])
    pylab.xticks([0.5,1.5,2.5,3.5],['OS3','OS4','OS5','OS6'])         
    pylab.xlabel('white')
    pylab.ylabel('result')       
    
    
module='TX1'
#get predictor set
predictorSet = filt.getSet(dataSetWhite, 'White Card', module, opticPredict, None)            
#get result Set
resultSet    = filt.getSet(dataSetDOE_AST, 'Normal', module, opticResult, None)
    


 
plt.figure()
plt.figure(figsize=(10, 10))
  
#apply model using each white card predictor
#get y min and max to put all plots on the same scale
xMins=[]
xMaxes=[]
yMaxes=[]
yMins=[]
for i in avePredictWellDict:
    xMaxes.append(max(avePredictWellDict[i]))
    xMins.append(min(avePredictWellDict[i]))
for i in aveResultWellDict:
    yMaxes.append(max(aveResultWellDict[i]))
    yMins.append(min(aveResultWellDict[i]))
for i in aveTestWellDict:
    yMaxes.append(max(aveTestWellDict[i]))
    yMins.append(min(aveTestWellDict[i]))
xMax = max(xMaxes)
xMin = min(xMins) 
yMax = max(yMaxes)
yMin = min(yMins) 



#sys.exit()
      


for i in wellRange:
    ax = plt.subplot2grid((8,8),(-(i+1)%8,int((i)/8)))        
    if i%8 > 0: 
        ax.set_xticklabels([])
    if i > 7:
        ax.set_yticklabels([])
    ax.set_title(str(i+1),y=0.5)
    
    x=np.matrix(np.arange(3100,3400,0.01))
    x=np.concatenate((np.ones((1,x.shape[1])),x),axis=0).T
    trendLine = (theta_array[i] * x.T).T  
    ax.scatter(x[:,1],trendLine,marker='s',c='b',alpha=1,s=1)
   
    X = np.array([avePredictWellDict['OS3'][i],
                    avePredictWellDict['OS4'][i],
                    avePredictWellDict['OS5'][i],
                    avePredictWellDict['OS6'][i]])
                    
    yTrain = np.array([[aveResultWellDict['OS3'][i],
                    aveResultWellDict['OS4'][i],
                    aveResultWellDict['OS5'][i],
                    aveResultWellDict['OS6'][i]]])

    yTest = np.array([[aveTestWellDict['OS3'][i],
                    aveTestWellDict['OS4'][i],
                    aveTestWellDict['OS5'][i],
                    aveTestWellDict['OS6'][i]]])

    plt.scatter(X,yTrain,c='r',marker='o',s=30)    
    plt.scatter(X,yTest, c='g',marker='o',s=30, alpha=0.5)    
    plt.ylim(yMin,yMax)
    plt.xlim(xMin,xMax)
    xticks=[int(float(k)) for k in np.linspace(xMin, xMax, 4)]
    plt.xticks(xticks)
    plt.setp(plt.xticks()[1], rotation=-45)

plt.savefig("trendsbyWell" + ".png", dpi=300)
            
            
    