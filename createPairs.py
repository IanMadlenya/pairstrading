""" This file is for creating a price ratio history array prior to the open
"""
def getRatios():
    
    try:
        import cpickle as pickle
    except ImportError:
        import pickle as pickle

    import datetime
    pairsFile = "ratioHistory.d"

    try:
        pairsDict=pickle.load( open( pairsFile, "rb" ) )
    except IOError:
        from sys import getsizeof
        from symbols import symbolList
        import numpy as np
        from processFuncs import writeLog
        from math import log
        #Then we need to create the file
        # Structure {Symbol:[12.12,13,13.2...],...]
        # In our program, we need to retrieve the history array of open,close values and then append the latest values for each 
        # symbol
        # For testing, just retrieve the latest history
        from createHistory import getHistory
        
        # This is how we get the price ratio
        # This will get us the average price and then divide them
        # np.divide(np.average(histDict['AAPL']),np.average(histDict['AMZN']))
        
        # This will create an array that shows the history of the price ratios
        # np.divide(histDict['AAPL'],histDict['AMZN'])

        # Find the standard deviation of the price ratios
        # np.std(np.divide(histDict['AAPL'],histDict['AMZN']))
        pairsDict={}
        pairsHistory=[]
        symbol1Arry=[]
        symbol2Arry=[]
        savePair=0
        dupeList=symbolList[:]
        stockHist = getHistory() #This will be the entire history in a dictionary with key=symbol the dates are based on order
        writeLog("Creating Pairs")
        for symbol in symbolList:
            # Don't need to do this since we already have a history function
            #symbolArry = stockHist[symbol]#map(lambda x: x['Close'],db.nasdaq.find({'Symbol':symbol},{'Close': 1, '_id':0 }))
            symbolArry = map(lambda x:(x[0],x[4]),stockHist[symbol]) 
            for symbol2 in dupeList:
                symbol2Arry=[]
                if symbol2 == symbol:
                    savePair=0
                    continue

                #symbol2Arry = stockHist[symbol2] #map(lambda x: x['Close'],db.nasdaq.find({'Symbol':symbol2},{'Close': 1, '_id':0 }))
                symbol2Arry=map(lambda x:(x[0],x[4]),stockHist[symbol2])

                minLen=min(len(symbolArry),len(symbol2Arry))
                
                if minLen>0:
                    symbolArry=symbolArry[-minLen:]
                    symbol2Arry=symbol2Arry[-minLen:]
                    savePair=1

                #if len(symbolArry)==len(symbol2Arry):
                #    savePair=1
                
                if savePair:
                    # Need to create another dictionary that stores the average and standard deviation
                    # Also, need to keep track of correlation
                    # For each day we need to divide
                    symbol2dict=dict(symbol2Arry)
                    doPairAppend=pairsHistory.append
                    for day in symbolArry:
                        dayDate=day[0]
                        dayClose=day[1]
                        if dayDate not in symbol2dict:
                            continue
                        day2Close=symbol2dict[dayDate]
                        
                        doPairAppend((dayDate,log(round(np.divide(float(dayClose),float(day2Close)),5))))
                    
                    #print pairsHistory
                    #print symbol,symbol2
                    #raw_input()
                    pairsDict[("%s %s")%(symbol,symbol2)]=pairsHistory
                        
                    if False:
                        for day in symbolArry:
                            dayDate=day[0]
                            day2Close=day[1]
                            #The date is stored in GMT time, so sometimes it has standard time and sometimes it's daylight
                            #time. Have to remove the GMT portion. Not sure if in import or when creating history.
                            if dayDate not in symbol2dict:
                                continue
                            dayClose=symbol2dict[dayDate]
                            pairsHistory.append((dayDate,round(np.divide(day2Close,dayClose),5)))
                       
                        pairsDict[("%s %s")%(symbol2,symbol)]=pairsHistory
                    #pairsHistory=np.divide(symbol2Arry,symbolArry,)
                    #pairsDict[("%s %s")%(symbol2,symbol)]=pairsHistory

                
                pairsHistory=[]
                symbol1Arry=[]
                symbol2Arry=[]
                savePair=0
                
            #if len(dupeList):
            #    dupeList.pop(0) 
            #else:
            #    break
            
        pickle.dump( pairsDict, open(pairsFile, "wb" ))
    return pairsDict

if __name__ == "__main__":
    historyPairs=getRatios()
