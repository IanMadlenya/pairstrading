#!/usr/bin/env python
#This program moves through all combinations of variables for a pair trade
#and creates an optimized set of variables for profitable correlated pairs.
from processFuncs import *
from pairsObjects import *
from createPairs import getRatios
from createCorr import getCorr
from flask import Flask, Response, redirect, request, url_for
from random import random,randrange
from analyzePairs import analyzePairs
import sys

try:
    import cpickle as pickle
except ImportError:
    import pickle as pickle

#pairStats is the individual stats 
#stats is for all stats

#Not sure we can do this at all if move to google apps
def predictTrade(env,stats,predictValues,model):
    from sklearn.naive_bayes import BernoulliNB
    from numpy import array
    
    prediction=0
    if not stats.tradeDetails:
        return 1

    predictValues=array(predictValues)
    prediction=stats.model.predict(predictValues) #Predict the last row in the array - should be 1 or 0

    #BernoulliNB(alpha=1.0, binarize=0.0, class_prior=None, fit_prior=True)
    #print(clf.predict(X[2]))

    return prediction

def trainModel(env,trainValues):
    from numpy import array
    from sklearn.naive_bayes import BernoulliNB
    if not trainValues:
        return 1
    model = BernoulliNB()
    X=array(map(lambda x:[x[0],x[1],x[2],x[3]],trainValues))
    Y=array(map(lambda x:x[4],trainValues))
    model.fit(X, Y)
    stats.model=model
    return model

if __name__ == "__main__":
    from createHistory import getHistory
    from datetime import datetime,timedelta

    trainValues=[]
    correlation=0.00
    stopProcessing=0
    currPair=''
    
    env=Environment() #Temp space specific to the current pair
    stats=Stats()
    env.priceQueue=getHistory()
    
    calibration=Calibration()
    pairStats=PairStats()
    optimizedPairs=PairStats()
    
    # The proces is for each combination, run the process and see which parameters create 
    # profitable trades.
    
    #The system should converge and tell me when the trade confidence is high.
    #These are all starting points
    #we will use a standard 10% incremental steps
    env.startDaysMA=5 #calendar days starting point
    env.startCorrMin=.3
    env.startCVMin=.005
    env.startMinStd=1 #alter based on the history of the pair. Maybe 3 maybe 1.5...
    
    env.endDaysMA=30
    env.endCorrMin=1
    env.endCVMin=.01
    env.endMinStd=5
    
    corrData=getCorr()
    fullRatioQueue=getRatios() #for every pair
    startDate=datetime(2013, 5, 1, 0, 0)
    stats.MA=env.startDaysMA
    stats.corrMin=env.startCorrMin
    stats.CVMin=env.startCVMin
    stats.minStd=env.startMinStd
    priorTotalProfit=0
    #calibration.pairStats[pair]={}
    processed=[]
    trackingConv={}
    # The original system sequences through the data in find pairs
    # in this system, I am sending over an object and the system
    # should just know what to do with it.
    for corrMin in arange(env.startCorrMin,env.endCorrMin,env.startCorrMin*.25):
        env.corrData=filter(lambda x:avgRange(corrData[x])>corrMin,corrData) #Not properly filtering

        if not env.corrData:
            #stopProcessing=True
            continue

        for pair in corrData:
            
            #had to add check of corrmin because filter above is not working
            if pair in processed or median(map(lambda x:x[0],corrData[pair]))<corrMin: #Since a pair can be higher than the min, we don't want to process the pair twice
                continue
            else:
                processed.append(pair)
               
                env.corrMin=avgRange(takeCol(corrData[pair],0)) # corrData is stored as tuple correlation and probability [(.5,.002),(.7,.02)]
                correlation=env.corrMin

            broadCast("Processing pair:%s"%(pair,))
            stopProcessing=False
            currPair=pair
            converged=False
            pricesExist=False
            priorRatio=0
            converged=False
            
            while not converged:

                initPairs(pairStats,pair)
                #pairsStats is for each session
                #stats is for total performance
                
                env.startDate=startDate
                
                for minStd in arange(env.startMinStd,env.endMinStd,.5):
                    
                    env.minStd=minStd
                
                    for CVMin in arange(env.startCVMin,env.endCVMin,.05):    
                
                        env.CVMin=CVMin
                        ratioQueue=fullRatioQueue[pair] #all ratio data for just this pair
                        
                        for daysMA in arange(env.startDaysMA,env.endDaysMA,1.0):

                            broadCast('New parameters: %s MA:%d CV:%.4f Std:%.3f' % (pair,daysMA,CVMin,minStd))
                            env.daysMA=daysMA

                            #env.prices ={Symbol:[(date,open,high,low,close),...,(date,open,high,low,close)]
                            env.prices=sliceData(env.priceQueue,env.startDate,env.startDate+timedelta(days=env.daysMA))

                            env.ratioData=sliceData(ratioQueue,env.startDate,env.startDate+timedelta(days=env.daysMA))

                            if not env.ratioData:
                                continue

                            #This process should only sends 1 pair over at a time.
                            env.timesProcessed=0
                            #env.prices contains a dictionary of prices for each symbol of length daysMA
                            
                            
                            while len(env.prices[max(env.prices)]):
                                pricesExist=True

                                result=analyzePairs(env,pairStats,pair)
                                env.startDate+=timedelta(days=env.daysMA)
                                env.prices=sliceData(env.priceQueue,env.startDate,env.startDate+timedelta(days=env.daysMA))
                                env.ratioData=sliceData(ratioQueue,env.startDate,env.startDate+timedelta(days=env.daysMA))
                                
                                if not env.ratioData:
                                    #broadCast('Breaking out')
                                    break
                            env.startDate=startDate

                converged=True
            dateOfMax=None
            env.timesProcessed=0
            maxProfit,maxDaysMA,maxCorrMin,maxMinStd,maxCVMin=0,0,0,0,0

            if pricesExist:
                for row in pairStats.stats[pair]['tradeDetails']:
                    for key,value in row.iteritems():
                        if row['totalProfit']>=maxProfit: 
                            #If the date and profit are always the same, which one is the winner?
                            #The highest value should be used. This will create a more reliable trade.
                            maxProfit=row['totalProfit']
                            dateOfMax=row['currDate']
                            maxDaysMA=row['daysMA']
                            maxCorrMin=correlation #This is the correlation of the pair on that max day. Not the min
                            maxMinStd=row['minStd']
                            maxCVMin=row['CVMin']
                            
                #The maximum results will be added to stats.tradeDetails for each pair
                if maxProfit>0:
                    stats.totalProfit=pairStats.stats[pair]['totalProfit']
                    writeLog (("%s enters=%i exits=%i early=%i long=%.2f short=%.2f total=%.2f") % \
                        (pair,pairStats.stats[pair]['enters'],pairStats.stats[pair]['exits'],\
                        pairStats.stats[pair]['earlyExit'], pairStats.stats[pair]['longProfit'],\
                        pairStats.stats[pair]['shortProfit'], pairStats.stats[pair]['totalProfit']))

                    writeLog ("Max params %s Date=%s profit=%f MA=%.3f CorrMin=%.3f Std=%.3f CV=%.3f" % (pair,dateOfMax,maxProfit,maxDaysMA,maxCorrMin,maxMinStd,maxCVMin))       
                    
                    broadCast("Saving to memory maximized pair parameters for: %s"%(pair,))
                    #Need to save the maximums to a dictionary with the pair as the key
                    optimizedPairs.stats[pair]={}
                    optimizedPairs.stats[pair]['maxDaysMA']=maxDaysMA
                    optimizedPairs.stats[pair]['maxCorrMin']=maxCorrMin
                    optimizedPairs.stats[pair]['maxMinStd']=maxMinStd
                    optimizedPairs.stats[pair]['maxCVMin']=maxCVMin
                    broadCast("Saved...%s"%(pair,))
                
    optimizedFile = "calibratedPairs.d"
    pickle.dump(optimizedPairs, open(optimizedFile, "wb" ))

    #if currPair and pricesExist:
    #    calibration.models[currPair].model=trainModel(env,trainValues)
    
    #After the optimized pairs are created prior to the open, we will
    #then go through all the pairs and use the real time last function to create a real time
    #price queue. The price queue will get appened with the last every 5 mins.
    #Total of 84 prices will be in the queue at the close.
    
    #So, after we retrieve the last price we need to check that the queue is as long as the moving avg. 
    #otherwise we wait for the next update until the queue is equal to the moving average.
    

