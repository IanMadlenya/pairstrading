## {{{ http://code.activestate.com/recipes/52308/ (r2)
from stat import *

class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

def listObjProps(obj):
    from pprint import pprint
    if hasattr(obj,'__dict__'):
        pprint (vars(obj))

    #if type(obj) is dict:
    #    for key,value in obj.iteritems(): broadcast("%s %s"% (key,value))
    #else:
    #    for key,value in obj.dict.iteritems(): print key,value

def writeLog(message):
    import datetime
    with open("history.log", "a") as text_file:
        text_file.write("%s %s\n" % (message,datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),))
    print message

def broadCast(msg):
    print msg
    
def isValue(x): #Checks if a variable is a number
    from math import isnan
    result = 0
    if not isnan(x):
        result= x if isinstance(x, (long, int, float) ) else 0
    else:
        result = 0
    return result

def findDate(num):
    # Trading dates is created at the beginning of the year for the whole year
    from tradingDates import getDates
    dateList=getDates()
    length=len(dateList)
    if length<num:
        num=length+1
    return dateList[num-1] if dateList[num-1] else None #Since the length starts at 1 and the lists are 0 indexed have subtract 1

def movingAvg(data=[],period=1):
    tempMA=0.00
    MA=0.00
    counter=0
    maArray=[]
    if len(data)>period:

        for c in reversed(data):
            if isValue(c):
                counter += 1
                tempMA += c
                if not (counter % period):
                    maArray.insert(0,round(tempMA/period,2))
                    tempMA=0.00
                    counter=0
        #Have to add the last values that were left over if the total array is not divisible by MA number
        if tempMA > 0: #Something was left over
            maArray.insert(0,round(tempMA/(counter if counter else 1),2))
            
    return maArray
    
def strictly_increasing(L):
    return all(x<y for x, y in zip(L, L[1:]))

def strictly_decreasing(L):
    return all(x>y for x, y in zip(L, L[1:]))

def non_increasing(L):
    return all(x>=y for x, y in zip(L, L[1:]))

def non_decreasing(L):
    return all(x<=y for x, y in zip(L, L[1:]))
    
def score(dataArray,cmpLength):
    #from numpy import average
    #Right now just returning the change of the avg from 2 periods back,
    #but a more sophisticated scoring will be implemented later
    if len(dataArray)<=cmpLength:
        cmpLength=len(dataArray)/2
        
    if not dataArray:
        return 0
    return (dataArray[cmpLength:][-1]-dataArray[cmpLength:][0])/dataArray[cmpLength:][0]
    #return (dataArray[-1]-dataArray[0])/dataArray[0]
    #return round((average(dataArray[-cmpLength:])-average(dataArray[-(2*cmpLength):-cmpLength]))\
    #        /average(dataArray[-(2*cmpLength):-cmpLength]),3)

def getObj(dataFile=None):
    try:
        import cpickle as pickle
    except ImportError:
        import pickle as pickle

    dataObj={}
    try:
        dataObj=pickle.load( open( dataFile, "rb" ) )
    except IOError:
        return dataObj    
    return dataObj

def saveObj(dataFile=None,dataObj={}):
    try:
        import cpickle as pickle
    except ImportError:
        import pickle as pickle
        
    try:
        pickle.dump( dataObj, open(dataFile, "wb" ))
    except IOError:
        return -1
    
    return 1
    
def manhattanDistance(array1,array2):
    #from numpy import average
#First normalize the array
    norm1=[]
    norm2=[]
    distance=[]
    times=0
    
    times=len(array1)
    for j in range(1,times):
        norm1.append((array1[j]-min(array1))/(max(array1)-min(array1)))
        
    times=len(array2)
    for j in range(1,times):
        norm2.append((array2[j]-min(array2))/(max(array2)-min(array2)))

    if len(norm1)<len(norm2):
        times=len(norm1)
    else:
        times=len(norm2)
        
    for j in range(1,times):
        distance.append(abs(norm1[j]-norm2[j]))
    if not distance:
        return 0
    return (distance[-1]-min(distance))/(max(distance)-min(distance)) #reduce(lambda x,y:x+y,distance)

def countAbove(data=[],numToCheck=0):
    return sum(map(lambda x:x>numToCheck,data))

def countBelow(data=[],numToCheck=0):
    return sum(map(lambda x:x<=numToCheck,data))
    
def slope(dataArray):
    return len(dataArray)/(dataArray[-1]-dataArray[0])
    
def arange(start,end,step=1):
    j=start
    while j<=end:
	    yield j
	    j+=step

def std(arry):
    from math import sqrt
    return sqrt(average(variance(arry)))
    
def variance(arry):
    return map(lambda x: (x - average(arry))**2, arry)
    
def average(s):
    if not len(s):
        return 0
    return sum(s) * 1.0 / len(s)
        

def median(arry):
    return sorted(arry)[int(round(len(arry)/2))]

def takeCol(a,col=0):
    return map(lambda x:x[col],a)
    
def convertDate(dateStr): #expected format 2-12-2013 should make more generic
    from datetime import datetime

    return datetime.strptime(dateStr, '%m-%d-%Y') 
     
#These should be more generic - send the structure
def convertToISODate(dateStr): #expected format '12-Jun-2013' should make more generic
    from datetime import datetime

    return datetime.strptime(dateStr, '%d-%b-%Y').isoformat()
    
def avgRange(arry):
    #from numpy import median
    if len(arry):
        return median(arry)
        #return median(map(lambda x:x[0],arry))
    else:
        return [0]

def sliceData(data,minDate,maxDate):
    #list to dictionary
    #import itertools
    #d = dict(itertools.izip_longest(*[iter(a)] * 2, fillvalue=""))
    tempValues={}
    tempData=[]

    if isinstance(data,list): #Then it's just a single data list
        return filter(lambda x:(x[0]>=minDate and x[0]<=maxDate),data)
    elif isinstance(data,dict):

        for key,value in data.iteritems():
            tempData=filter(lambda x:(x[0]>=minDate and x[0]<=maxDate),data[key])
            #for row in data[key]:
            #    if row[0]>=minDate and row[0]<=maxDate:
            #        tempData.append(row)
            tempValues[key]=tempData

    return tempValues
    
def savePair(pairDict,**kwargs):
    for key,value in kwargs.iteritems():
        pairDict[key]=value
    return pairDict

def getRealTimeLast(symbol):
    from stockquote import stockquote
    import os
    
    h = stockquote.from_google(symbol)

    priceData={}

    symbol=k['symbol']

    if symbol not in priceData:
        priceData[symbol]=[]

    priceData[symbol].append((datetime.strptime(k['price_last_datetime'], '%b %d, %H:%M%p %Z'),0,0,0,k['price_last']))

    return priceData
    
def findPos(matchList,matchChar):
    return filter(lambda x:(x[1]==matchChar),enumerate(list(dateStr)))[0][0]
    
def insertText(tempStr,position=0,textVal=''):
    if len(tempStr)<position:
        return tempStr

    temp=list(tempStr)
    temp.insert(position,textVal)
    return "".join(temp)
    
def openFileType(**args): #not using this function
    #Check: {'fileName': 'log.txt', 'filetType': 'txt'}
    #Expecting fileName and the type to check against
    fileName=''
    fileType=''
    if 'fileName' in args:
        fileName=args['fileName']
        fileType=args['fileType']
        if file.endswith(fileType):
            try:
               with open(fileName): pass
            except IOError:
               return None

def getArgs(**args):
    #getArgs(var1=1,var2=2)
    for j in range(0,len(zip(args))):
    	print zip(args)[j][0],args[zip(args)[j][0]]
    	
def walktree(top, callback, walkDir=False):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''
    import os, sys
    
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname).st_mode
        if S_ISDIR(mode) and walkDir:
            # It's a directory, recurse into it
            walktree(pathname, callback)
            
        elif S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print 'Skipping %s' % pathname

def importFile(file):
    import sys
    records=None
    dataBase='stockData'
    collection='nasdaq'
    result=None
    if file.endswith('csv'):
        if (file.find('NASDAQ')>=0) or (file.find('INDEX')>=0): #Returns position found
            broadCast('Importing %s' % file)
            records=createRecords(file)
            result=importMongo(dataBase,collection,records)
            if not result: #number of records imported
               sys.exit(('Error importing records %s'% (file,)))
            else:
                return result

def createRecords(file):
    import csv
    #file=r'/home/webmaster/Documents/Source/Python/mongoDB/stockData/NASDAQ_20130417.csv'
    #The records have to be formatted for import for the database
    #The dot has to be removed from the index name and the data has to be formatted to an ISO date.
    
    #Symbol,Date,Open,High,Low,Close,Volume
    #AAIT,19-Jun-2013,28.2,28.2,27.94,27.94,1100
    #post = {"author": "Mike","text": "My first blog post!","tags": ["mongodb", "python", "pymongo"],
    dataDict=[]
    data = csv.reader(open(file, "rb"))
    header=[]
    #Expects header
    #This process should be more generic
    j=0

    for row in data:
        #row is a list
        if j == 0:
            #header.append(row) #if it were a comma sep string: map(str.strip, row.split(','))
            header=row
        else:
            #store the header row as the fields
            dataDict.append({header[0]:row[0],header[1]:convertToISODate(row[1]),header[2]:row[2],header[3]:row[3],header[4]:row[4],header[5]:row[5],header[6]:row[6]})
        j+=1
    return dataDict
    
def importMongo(dataBase,collection,records):
    from pymongo import MongoClient
    client = MongoClient()
    db = client[dataBase]
    recsInserted=0
    #import datetime
    #post = {"author": "Mike","text": "My first blog post!","tags": ["mongodb", "python", "pymongo"],"date": datetime.datetime.utcnow()}
    collectionId = db[collection] #Collection
    #print db.collection_names()
    for row in records:
        collection_id = collectionId.insert(row)        
        recsInserted +=1
    #db.collection_names()

def initPairs(pairStats,pair=''):
    pairStats.stats[pair]={}
    pairStats.stats[pair]['enterDate']=None
    pairStats.stats[pair]['enters']=0
    pairStats.stats[pair]['sumCV']=0
    pairStats.stats[pair]['totalProfit']=0
    pairStats.stats[pair]['exits']=0
    pairStats.stats[pair]['earlyExit']=0
    pairStats.stats[pair]['longProfit']=0
    pairStats.stats[pair]['shortProfit']=0
    pairStats.stats[pair]['totalProfit']=0
    pairStats.stats[pair]['profitable']=0
    pairStats.stats[pair]['losses']=0
    pairStats.stats[pair]['sumCVProfit']=0
    pairStats.stats[pair]['sumCVLoss']=0
    pairStats.stats[pair]['tradeDetails']=[] #This array holds dictionaries.

