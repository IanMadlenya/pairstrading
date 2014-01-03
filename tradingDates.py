
def checkDate(dateObj):
        #Returns the number in the date array which will define where the symbols close is in the history
        #0 means it is not a valid date.
        return 1

def okDate(dateObj):
    import datetime
    holidays = [datetime.datetime(2013, 1, 1, 0, 0),
        datetime.datetime(2013, 1, 21, 0, 0),
        datetime.datetime(2013, 2, 18, 0, 0),
        datetime.datetime(2013, 3, 29, 0, 0),
        datetime.datetime(2013, 5, 27, 0, 0),
        datetime.datetime(2013, 7, 4, 0, 0),
        datetime.datetime(2013, 9, 2, 0, 0),
        datetime.datetime(2013, 11, 28, 0, 0),
        datetime.datetime(2013, 12, 25, 0, 0),]
    if dateObj not in holidays and dateObj.weekday()<5:
        return dateObj

def getDates():
    try:
        import cpickle as pickle
    except ImportError:
        import pickle as pickle

    import datetime

    
    dateList=[]

    dateHistFile = "dateList.d"

    try:
        dateList=pickle.load( open( dateHistFile, "rb" ) )
    except IOError:

        #Change this to the min date instead of a fixed date
        #But then we need to consider if the holiday dates are in the same range

        dateList = map(okDate,[ datetime.datetime(2012, 12, 31, 0, 0) + datetime.timedelta(days=x) for x in range(0,365)])

        dateList = [dateVal for dateVal in dateList if dateVal is not None]
        #If this file is being run or loaded, then we need to recreate the pickled dateList
        pickle.dump( dateList, open( dateHistFile, "wb" ))

    return dateList

if __name__ == "__main__":
    dateList=getDates()
