""" This file is for creating a history array prior to the open
"""

def openData(dbName):
    from pymongo import Connection
    connection = Connection()
    connection = Connection('localhost', 27017)
    
    #db.nasdaq.ensure_index('Date')
    # Since I am the only one using this I am not trying to protect from eval.
    return eval( ("connection.%s") % (dbName,) )# connection.stockData

def useIndex(dbConn,dataBase,*indexes):
    #This isn't final - should create the command
    dbConn.nasdaq.ensure_index([('Date','Symbol')])

def getHistory(): #add the

    try:
        import cpickle as pickle
    except ImportError:
        import pickle as pickle

    import datetime
    import time
    historyFile = "stockHist.d"
    try:
        histDict=pickle.load( open( historyFile, "rb" ) )
        # Need to check if the data files have changed and if so recreate
        # Check the max date in the database against the retrieved array
    except IOError:
        from sys import getsizeof
        from symbols import symbolList
        from processFuncs import writeLog
        
        histDict={}
        recHistory=[]
        
        dateSearch = datetime.datetime(2013, 1, 2, 0, 0) #We know this is the starting date. Should probably use the tradingDates.py
        
        db=openData('stockData')
        useIndex(db,'nasdaq','Date','Symbol')
        #db.nasdaq.ensure_index([('Date','Symbol')])
        writeLog("Creating Price History")

        #Symbol,Date,Open,High,Low,Close,Volume
        #prices={'AAPL':[('20130201',433.45,434.30,432.33,436.3,2030400),('20130202',433.55,434.50,432.33,436.3,2030400)]}
        #.strftime("%Y%m%d")
        for symbol in symbolList:
            recHistory = map(lambda x: (x['Date'].combine(x['Date'].date(),datetime.time(0,0,0)),x['Open'],x['High'],x['Low'],x['Close']),\
                db.nasdaq.find({'Symbol':symbol},{'Date':1,'Open': 1,'High':1,'Low':1,'Close': 1, '_id':0 }).sort('Date',1))
            #print recHistory
            #raw_input()
            histDict[symbol]=recHistory
            recHistory=[]
        pickle.dump( histDict, open( historyFile, "wb" ))
        

    
    return histDict

if __name__ == "__main__":
    historyData=getHistory()
