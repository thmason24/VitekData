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
    

def pcntChangeLayout(read,grayMax):
    #sumPcntChange=read[0:numReads,:].sum(0).reshape(8,8).transpose()
    data=read.reshape(8,8).transpose()
    plt.pcolor(data,cmap='gray',vmin=0,vmax=grayMax)
    plt.colorbar()
    plt.xticks(arange(0.5,8.5),range(1,9),fontsize=10)
    plt.yticks(arange(0.5,8.5),range(1,9),fontsize=10)

    #plt.axis('off')
    #annotate each well
    for i in range(1,65):
        plt.text(int((i-1)/8) + 0.4,(i-1)%8 + 0.4,i,color = 'orange')
    
    
