""" This file is for creating a correlation history array prior to the open
    array should be: "EBAY DELL":[.4,.5,.6,.8...] <-- Relates to daily history
    The average of the cumulative correaltion
"""
def getCorr():

    try:
        import cpickle as pickle
    except ImportError:
        import pickle as pickle
        
    import datetime
    corrFile = "corrHistory.d"

    try:
        corrDict=pickle.load( open( corrFile, "rb" ) )
    except IOError:
        from sys import getsizeof
        from symbols import symbolList
        import numpy as np
        from math import log 
        #import scipy as sp
        from scipy import stats as sp
        from numpy import average,std
        from createHistory import getHistory
        from processFuncs import writeLog,movingAvg
       
        # This is how we get the price ratio
        # This will get us the average price and then divide them
        # np.divide(np.average(histDict['AAPL']),np.average(histDict['AMZN']))
        
        # This will create an array that shows the history of the price ratios
        # np.divide(histDict['AAPL'],histDict['AMZN'])

        # Find the standard deviation of the price ratios
        # np.std(np.divide(histDict['AAPL'],histDict['AMZN']))
        corrDict={}
        corrHistory=[]
        corrHistory2=[]
        symbol1Arry=[]
        symbol2Arry=[]
        savePair=0
        logArry=[]
        logArry2=[]
        
        stockHist = getHistory() #This will be the entire history in a dictionary with key=symbol the dates are based on order
        writeLog("Creating Correlations")
        dupeList=symbolList[:]
        for symbol in symbolList:

            symbolArry = map(lambda x:x[4],stockHist[symbol])
            #actual structure
            #prices={'AAPL':[('20130201',433.45,434.30,432.33,436.3),('20130202',433.55,434.50,432.33,436.3)]}
            for symbol2 in dupeList:
                symbol2Arry=[]
                if symbol2 == symbol:
                    savePair=0
                    continue
                
                symbol2Arry = map(lambda x:x[4],stockHist[symbol2]) #map(lambda x: x['Close'],db.nasdaq.find({'Symbol':symbol2},{'Close': 1, '_id':0 }))

                minLen=min(len(symbolArry),len(symbol2Arry))

                if minLen>0:
                    symbolArry=symbolArry[-minLen:]
                    symbol2Arry=symbol2Arry[-minLen:]
                    savePair=1
                    
                if savePair and symbolArry and symbol2Arry:
                    #weighting the correlation based on how varied the two prices are
                    #if they are very varied, then any correlation may not be accurate

                    # Need to create another dictionary that stores the average and standard deviation
                    # Also, need to keep track of correlation
                    # May use log normal returns - log(price1/price0)
                    #Have to weight the data so recent correlations are counted more
                    #summ=0
                    #k=0
                    #for j in reversed(x):
	                #    k+=1
	                #    summ=summ+(j/(float(k)))
                    logArry=[]
                    logArry2=[]
                    symbolArry= map(lambda x:float(x),symbolArry)
                    symbol2Arry= map(lambda x:float(x),symbol2Arry)

                    for j in range(3,len(symbolArry)):
                        if j>0:
                            #print (float(j))*symbolArry[j-1]+(1-(float(j)))*((float(j-1))*symbolArry[j-1]+(1-(float(j-2))))
                            #The issue is that the division is only 1 day difference. 
                            #Not enough change
                            if j % 5 == 0:
                                logArry.append(log(symbolArry[j]/float(symbolArry[j-5])))
                                logArry2.append(log(symbol2Arry[j]/float(symbol2Arry[j-5])))

                    corrHistory.append(sp.stats.pearsonr(logArry,logArry2))
                    corrHistory2.append(sp.stats.pearsonr(logArry2,logArry))

                    #corrHistory.append(sp.stats.pearsonr(symbolArry,symbol2Arry))
                    #corrHistory2.append(sp.stats.pearsonr(symbol2Arry,symbolArry))
                                            
                    if corrHistory:
                        corrDict[("%s %s")%(symbol,symbol2)]=corrHistory
                        corrDict[("%s %s")%(symbol2,symbol)]=corrHistory2
                        corrHistory=[]
                        corrHistory2=[]
            logArry=[]
            logArry2=[]
            corrHistory=[]
            corrHistory2=[]
            symbol1Arry=[]
            symbol2Arry=[]
            savePair=0

            if len(dupeList):
                dupeList.pop(0)
            else:
                continue

        pickle.dump( corrDict, open(corrFile, "wb" ))
    return corrDict

if __name__ == "__main__":
    historycorr=getCorr()
