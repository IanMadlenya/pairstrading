#After the optimized pairs are created prior to the open, we will
#then open the previous saved pairs and check their status and position 
#then go through all the optimized pairs and create the positions from the existing close prices: watching, trending, inposition
#save them to an updated pairs.d file prior to the open.
#
#Then at the open, open the pairs.d file and use the real time last function to create a real time
#price queue. The price queue will get appeneded with the last every 5 mins.
#Total of 84 prices will be in the queue at the close.

#So, after we retrieve the last price we need to check that the queue is as long as the moving avg. 
#otherwise we wait for the next update until the queue is equal to the moving average.

#RealTime

#We do the same steps as calibrate, but now the optimized pairs file: calibratedPairs.d
#drives the process and the price queue comes from google current prices.
#in the future, this could come from a data feed.

#Check if an update (NASDAQ and INDEX) file is in the update folder. If so, append to the nasdaq database.
from processFuncs import *
from pairsObjects import *
from createPairs import getRatios
from createCorr import getCorr
from analyzePairs import analyzePairs

from datetime import datetime
from pairsObjects import *

from createHistory import getHistory
from datetime import datetime,timedelta
    
import os

#*** Starts here ***
def openDfile(fileName):
    return getObj(fileName)

def savePairs(historyData,fileName):
    return saveObj(fileName,historyData)

if __name__ == "__main__":
    #these will be populated from the calibrated values
    writeLog('Starting realTimePairs.py...')
    env=Environment() #Temp space specific to the current pair
    startDate=datetime(2013, 5, 1, 0, 0)
    pairStats=Stats()
    env.priceQueue=getHistory()
    fullRatioQueue=getRatios() #for every pair
    pairs=openDfile('pairsStatus.d') #inprogress optimized pairs
    pairStats=PairStats()
    optPairs=openDfile('calibratedPairs.d') #Optimized pairs parameters
    #Only looking based on optPairs
    #And then storing the status in pairs
    #listObjProps(optPairs)
    symbolList={}

    print "****"
    for row in pairs:
        #print row,pairs[row]
        if pairs[row]: # and pairs[row]['position']==2 : #and 'IDX' in pairs[row]['shortSymbol']:
            
            print optPairs.stats[row]
            print row,pairs[row]['position'],pairs[row]['currDate'],pairs[row]['longSymbol']\
            ,pairs[row]['shortSymbol'],pairs[row]['currMavg'],pairs[row]['trigger'],pairs[row]['CV']
    print "****"
    allPairs=[]
    #Three groups - 
    #Optimized pairs
    #Pairs in progress
    #Pairs not in progress - just being watched
    #Could be overlap between optimized and in progress
    
    #Put the optimized pairs and
    
    #initalize parameters from optimized pairs
    #calPairs is a dictionary
    
    #The inprogress pairs will have a date for the as-of date. 
    #When the price passes that date, then the ratio needs to be checked, etc.
    #for a change in the status.
    #Create a summary view that shows the ongoing statistics. 
    #Profit/Loss, etc.
    saveTotal={}
    broadCast('Starting...')
    for pair in optPairs.stats:
        
        ratioQueue=fullRatioQueue[pair]
        #This process should only sends 1 pair over at a time.
        env.timesProcessed=0
        env.startDate=startDate
        initPairs(pairStats,pair)
        env.startDaysMA=0 #calendar days starting point
        env.startCorrMin=0
        env.startCVMin=0
        env.startMinStd=1 #alter based on the history of the pair. Maybe 3 maybe 1.5...
        
        env.endDaysMA=0
        env.endCorrMin=0
        env.endCVMin=0

        env.startDate=startDate
        env.daysMA=optPairs.stats[pair]['maxDaysMA']
        env.CVMin=optPairs.stats[pair]['maxCVMin']
        env.endMinStd=optPairs.stats[pair]['maxMinStd']
        env.maxStdev=optPairs.stats[pair]['maxMinStd']
        env.ratioData=sliceData(ratioQueue,env.startDate,env.startDate+timedelta(days=env.daysMA))
        env.prices=sliceData(env.priceQueue,env.startDate,env.startDate+timedelta(days=env.daysMA))
        
        if not env.ratioData:
            continue
            
        saveTotal[pair]={}
        
        while len(env.prices[max(env.prices)]):

            analyzePairs(env,pairStats,pair,saveTotal)
            env.startDate+=timedelta(days=3)
            env.prices=sliceData(env.priceQueue,env.startDate,env.startDate+timedelta(days=3))
            env.ratioData=sliceData(ratioQueue,env.startDate,env.startDate+timedelta(days=3))
            #After the end we need to start adding the intraday values to the end of the queue.
        
    savePairs(pairStats,'pairStats.d')

    savePairs(saveTotal,'pairsStatus.d')
