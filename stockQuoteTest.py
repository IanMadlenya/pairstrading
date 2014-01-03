from stockquote import stockquote
from datetime import datetime
import os

#Jul 11, 10:33AM EDT

def convertDate(dateStr): #2010-01-07
    from datetime import datetime

    return datetime.strptime(dateStr, '%Y-%m-%d')

#h = stockquote.historical_quotes("GOOG", "20130710", "20130711")
k = stockquote.from_google("GOOG")
#{'price_last_datetime': u'Jul 11, 10:33AM EDT', 'price_last': u'915.35', 'exchange': u'NASDAQ', 
#'symbol': u'GOOG', 'source_url': 'http://www.google.com/finance/info?q=GOOG', u'GOOGLE_CODE_s': u'0',
#'source': 'Google', 'price_last_time': u'10:33AM EDT', u'GOOGLE_CODE_l_cur': u'915.35', u'GOOGLE_CODE_id': u'694653', 
#'price_close': u'1.03', 'change': u'+9.36', u'GOOGLE_CODE_ccol': u'chg'}

priceData={}
if False:
    for row in h:
        symbol=row['symbol']
        if symbol not in priceData:
            priceData[symbol]=[]

        priceData[symbol].append((convertDate(row['Date']),row['Open'],row['High'],row['Low'],row['Close']))


symbol=k['symbol']
if symbol not in priceData:
    priceData[symbol]=[]

priceData[symbol].append((datetime.strptime(k['price_last_datetime'], '%b %d, %H:%M%p %Z'),0,0,0,k['price_last']))


print priceData[symbol]
    
    #for key,value in row.iteritems():

    #    print key,value


#pairs structure is:
#{Symbol:[(date,open,high,low,close),...,(date,open,high,low,close)]
    
#print os.linesep.join(["%25s: %s" % (k, h[0][k]) for k in sorted(h[0].keys())])
