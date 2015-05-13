#!/usr/bin/env python
import matplotlib.pyplot as plt
import sys
import os
from numpy import arange
# gather data into a reads X wells matrix

def multiPlot(read):
    plotRange = range(0,len(read))
    path=os.path.dirname(__file__)
    dataDir=os.path.join(path,'Data')
    plt.axis('off')
    plt.figure(figsize=(10, 10))

    for i in range (1,65):
        #place read to match the layout of a card
        ax = plt.subplot(8,8,((i-1)%8)*8 + int((i-1)/8) + 1)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_title(str(i),y=0.5)
        ax.plot(plotRange,read[:,i-1]) #,plotRange,plotRange)
    plt.savefig(dataDir + "test" + ".png")
    

def layoutPlot(read,grayMin= None,grayMax= None):
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
    figureSize=2.6;
    plt.figure(figsize=(figureSize*8, figureSize))

    #calcuate and plot average for each well
    plt.subplot(1,6,1)
    layoutPlot(Sum/Num,grayMin=None,grayMax=None)
    plt.title(title + 'raw')
    #plot range    
    plt.subplot(1,6,2)
    layoutPlot(Range/Num,grayMin=None,grayMax=None)
    plt.title(title + 'Range')
    #plot min    
    plt.subplot(1,6,3)
    layoutPlot(Min/Num,grayMin=None,grayMax=None)
    plt.title(title + 'Min')
    #plot max    
    plt.subplot(1,6,4)
    layoutPlot(Max/Num,grayMin=None,grayMax=None)
    plt.title(title + 'Max')
    #plot percent change
    plt.subplot(1,6,5)
    layoutPlot(Pcnt/Num,grayMin=0,grayMax=None)
    plt.title(title + '%change')
    #plot negative percent change    
    plt.subplot(1,6,6)
    layoutPlot(NegPcnt/Num,grayMin=0,grayMax=None)
    plt.title(title + 'Neg %change')