#!/usr/bin/env python
import matplotlib.pyplot as plt
import sys
import os
from numpy import arange
# gather data into a reads X wells matrix

def multiPlot(read,min = None, max = None):
    plotRange = range(0,len(read))
    path=os.path.dirname(__file__)
    dataDir=os.path.join(path,'Data')
    #plt.axis('off')
    plt.figure(figsize=(10, 10))

    for i in range (1,65):
        #place read to match the layout of a card
        #ax = plt.subplot(8,8,((i-1)%8)*8 + int((i-1)/8) + 1)
        ax = plt.subplot2grid((8,8),(-i%8,int((i-1)/8)))        
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_title(str(i),y=0.5)
        ax.set_ylim(min,max)
        ax.plot(plotRange,read[:,i-1]) #,plotRange,plotRange)
    plt.savefig(dataDir + "test" + ".png")
    

def layoutPlot(read,grayMin= None,grayMax= None):
    """Test"""
    #sumPcntChange=read[0:numReads,:].sum(0).reshape(8,8).transpose()
    data=read.reshape(8,8).transpose()
    plt.pcolor(data,cmap='gray',vmin=grayMin,vmax=grayMax)
    #plt.pcolor(data,cmap='gray')
    plt.colorbar()
    plt.xticks(arange(0.5,8.5),range(1,9),fontsize=10)
    plt.yticks(arange(0.5,8.5),range(1,9),fontsize=10)

    #plt.axis('off')
    #annotate each well
    for i in range(1,65):
        plt.text(int((i-1)/8) + 0.5,(i-1)%8 + 0.5,i,color = 'orange',horizontalalignment = 'center',verticalalignment = 'center')
    
    
def rowOfPlots(Sum,Range,Min,Max,Pcnt,NegPcnt,Num,title):
        #new figure


    plotCount = 6
    if Sum is None:
        plotCount -=1
    if Range is None:
        plotCount -=1
    if Min is None:
        plotCount -=1
    if Max is None:
        plotCount -=1
    if Pcnt is None:
        plotCount -=1
    if NegPcnt is None:
        plotCount -=1

    figureSize=2.6;
    plt.figure(figsize=(figureSize*8*(plotCount/6), figureSize))

    #calcuate and plot average for each well
    plotNum=0
    if Sum is not None:
        plotNum += 1
        plt.subplot(1,plotCount,plotNum)
        layoutPlot(Sum/Num,grayMin=None,grayMax=None)
        plt.title(title + 'raw')
    #plot range    
    if Range is not None:
        plotNum += 1
        plt.subplot(1,plotCount,plotNum)
        layoutPlot(Range/Num,grayMin=None,grayMax=None)
        plt.title(title + 'Range')
    #plot min    
    if Min is not None:
        plotNum += 1
        plt.subplot(1,plotCount,plotNum)
        layoutPlot(Min/Num,grayMin=None,grayMax=None)
        plt.title(title + 'Min')
    #plot max    
    if Max is not None:
        plotNum += 1
        plt.subplot(1,plotCount,plotNum)    
        layoutPlot(Max/Num,grayMin=None,grayMax=None)
        plt.title(title + 'Max')
    #plot percent change
    if Pcnt is not None:
        plotNum += 1
        plt.subplot(1,plotCount,plotNum)
        layoutPlot(Pcnt/Num,grayMin=0,grayMax=None)
        plt.title(title + '%change')
    #plot negative percent change    
    if NegPcnt is not None:
        plotNum += 1
        plt.subplot(1,plotCount,plotNum)
        layoutPlot(NegPcnt/Num,grayMin=0,grayMax=None)
        plt.title(title + 'Neg %change')
        
    
