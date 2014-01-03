def analyzePairs(env,pairStats,pair='',saveTotal={}):
    from processFuncs import savePair,score,writeLog,average,std
    #This routine gets called until the change in profit to losses doesn't change
    #Called for only one pair at a time.
    #env: stores the variables that are used to keep track of the progress and position of the pairs
    #pairStats: is for keeping stats on the price, entry and exit positions
    #pair: is the current pair being processed
    #positions: 0=watching, 1=Crossed up, 2=Dropped below after crossing up - Entered into trade
    #Don't need to import from numpy, these are now implemented in python
    #from numpy import average,isnan,std
    
    #The routine expects an environment, a place to store stats and a pair
    #Could check to make sure the env and pairStats are the correct structure
    #and if not, convert or create them.
    
    currMavg,currMavg2,currStdDevMA,trigger,ratioStdev,position,longPrice,shortPrice,CV,currCV,longStart,shortStart,longEnd,shortEnd=\
        0.00,0.00,0.00,0.00,0.00,0,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00
    currDate,currDate2,longSymbol,shortSymbol,symbol1,symbol2=None,None,None,None,None,None
    profitable=0
    save=True
    maxStdev=0.00
    CVDelta=0.00
    maRatio=0.00
    trackTrans=False #log all ups and downs
    ratio=env.ratioData

    if not ratio or not pair:
        save=False #Nothing to process
    else:
        if not env.timesProcessed: #first time looking
            env.timesProcessed=1
            currMavg=round(average(map(lambda x:x[1], ratio)),3)
            currDate=ratio[-1][0]
            currMavg2=round(average(map(lambda x:x[1], ratio[:-1])),3) #using one less day Moving avg
            #Ratio structure is [(date,ratio),(date,ratio)...]
            if currMavg<>0: #11/16/13
                ratioStdev=std(map(lambda x:x[1],ratio))
                if ratioStdev==0:
                    ratioStdev=1

                trigger=currMavg+(env.minStd*ratioStdev)
                
                #coefficient of variation = stdev/mean is unitless and the more correlated, the smaller the number
                CV=ratioStdev/float(currMavg)
                #writeLog(('%s %s %s %.3f CV=%.3f') % ('Trig Calcd:',pair,currDate,trigger,CV))
                save=True
        else:
            #This is where we do the looking
            env.timesProcessed+=1
            
            longSymbol=""
            shortSymbol=""
            #pair looks like this: AAPL GOOG
            symbol1=pair.split()[0]
            symbol2=pair.split()[1]
            
            if not env.prices[symbol1]: #This symbol doesn't have a price history for some reason
                save=False
            
            if not env.prices[symbol2]: #This symbol doesn't have a price history for some reason
                save=False
                
            if not ratio:
                save=False

            #The price array is for each day: date,open,high,low,close
            #So, this is taking the close from the last day
            close1=env.prices[symbol1][-1][4]
            close2=env.prices[symbol2][-1][4]
            #calculates the change in the closing prices
            #This could be a more sophisticated scoring routine.
            score1=score(map(lambda x:x[4],env.prices[symbol1]),env.daysMA)
            score2=score(map(lambda x:x[4],env.prices[symbol2]),env.daysMA)
            #Get the stored values
            #Take the saved values from the environment and don't overwrite them.
            CV=env.pairs['CV']
            ratioStdev=env.pairs['ratioStdev']
            longSymbol=env.pairs['longSymbol']
            shortSymbol=env.pairs['shortSymbol']
            longStart=env.pairs['longStart']
            shortStart=env.pairs['shortStart']
            trigger=env.pairs['trigger']
            position=env.pairs['position']
            currDate=ratio[-1][0]
            
            currMavg=round(average(map(lambda x:x[1], ratio)),3)
            currMavg2=round(average(map(lambda x:x[1], ratio[:-1])),3)

            currDate=ratio[-1][0]
            
            if position==1 and currMavg<trigger and currMavg<>0:

                currCV=ratioStdev/float(currMavg)
                CVDelta=currCV-CV
                maRatio=currMavg/(currMavg2 if currMavg2 else 1)
                pairStats.stats[pair]['enterDate']=currDate #temp holding spot

                longStart=env.prices[longSymbol][-1][4]
                shortStart=env.prices[shortSymbol][-1][4]
                position=2
                
                pairStats.stats[pair]['enters']+=1
                pairStats.stats[pair]['sumCV']+=currCV
                pairStats.stats[pair]['totalProfit']=pairStats.stats[pair]['totalProfit']

                if trackTrans:
                    writeLog('Enter: %s %s L=%s %.2f S=%s %.2f CV=%.3f CV Delta=%.5f Std=%.3f Trig:%.3f' % (pair,currDate,longSymbol,longStart,shortSymbol,shortStart,env.CVMin,currCV-CV,env.minStd,trigger))
               
            elif position==0 and currMavg>trigger and currMavg<>0:# and (ratioStdev/float(currMavg))>env.CVMin:
            
                #This is the case of the ratio moving past (above) the trigger enough to indicate 
                #a rare event. 
                #Use the change in CV to be an indication of volatility
                #Use the current CV to indicate the potential of the trade: Higher = more range and more potential
                if (ratioStdev/float(currMavg))>env.CVMin:
                    CV=ratioStdev/float(currMavg) #Value that was checked against the min
                    
                    env.maxStdev= ratioStdev #max(ratioStdev,env.maxStdev)
                    
                    if score1>score2:
                        longSymbol=symbol2
                        shortSymbol=symbol1
                    else:
                        longSymbol=symbol1
                        shortSymbol=symbol2

                    if trackTrans:
                        writeLog('Crossed up: %s %.1f %s %s %s L=%s S=%s trig=%.3f CV=%.3f Trig:%.3f' % (pair,env.minStd,'std dev',pair,currDate,longSymbol,shortSymbol,trigger,CV,trigger))
                    position=1
                    save=True
            elif position==2 and currMavg>currMavg2:  #round(average(map(lambda x:x[1], ratio[:-1])),3)
                
                longEnd=env.prices[longSymbol][-1][4]
                shortEnd=env.prices[shortSymbol][-1][4]
                longStart=env.pairs['longStart']
                shortStart=env.pairs['shortStart']
                longProfit=(longEnd-longStart)
                shortProfit=(shortStart-shortEnd)
                profit=longProfit+shortProfit
                
                pairStats.stats[pair]['exits']+=1

                pairStats.stats[pair]['longProfit']+=(longProfit)
                pairStats.stats[pair]['shortProfit']+=(shortProfit)
                #longProfit=pairStats.stats[pair]['longProfit']
                #shortProfit=pairStats.stats[pair]['shortProfit']
                pairStats.stats[pair]['totalProfit']+=((longProfit+shortProfit))
                
                if profit>0:
                    profitable=1 #This is for the model
                    pairStats.stats[pair]['profitable']+=1
                    pairStats.stats[pair]['sumCVProfit']+=env.pairs['CV']
                else:
                    profitable=0
                    pairStats.stats[pair]['losses']+=1
                    pairStats.stats[pair]['sumCVLoss']+=env.pairs['CV']
                    
                if trackTrans:
                    writeLog('Exit: %s %s L=%s %.3f S=%s %.3f P=%.3f PRCTP=%.3f CV=%.3f MA=%.3f Stdev=%.3f corr=%.3f Trig:%.3f' % \
                        (pair,currDate,longSymbol,longProfit,shortSymbol,shortProfit,profit,\
                        profit/(longStart+shortStart),env.CVMin,env.daysMA,env.minStd,env.corrMin,trigger))
                        
                #These details need to reflect the state prior to entering the trade
                #Since that is what will be available to model prior to entering the trade.
                #The symbol will be used to get any other details before modeling
                pairStats.stats[pair]['tradeDetails'].append({})
                enterDate=pairStats.stats[pair]['enterDate']

                pairStats.stats[pair]['tradeDetails'].append(savePair(pairStats.stats[pair]['tradeDetails'][-1],\
                    enterDate=enterDate,currDate=currDate,pair=pair,daysMA=env.daysMA,CVMin=env.CVMin,\
                    minStd=env.minStd,corrMin=env.corrMin,longSymbol=longSymbol,longStart=longStart,longProfit=longProfit,\
                    shortSymbol=shortSymbol,shortStart=shortStart,shortProfit=shortProfit,totalProfit=shortProfit+longProfit,\
                    CVDelta=env.CVDelta,trigger=trigger,profitable=profitable))

                #removePair(env,pair) #start from the beginning - need to recalc trigger, etc.
                position=0
                env.timesProcessed=0
                env.pairs['position']=0
                save=False
            elif position==2 and currMavg>trigger: #the ratio moved back under and now it went back over - the ratio is diverging
                longEnd=env.prices[longSymbol][-1][4]
                shortEnd=env.prices[shortSymbol][-1][4]
                longStart=env.pairs['longStart']
                shortStart=env.pairs['shortStart']
                longProfit=(longEnd-longStart)
                shortProfit=(shortStart-shortEnd)
                profit=longProfit+shortProfit
                
                pairStats.stats[pair]['earlyExit']+=1
                pairStats.stats[pair]['exits']+=1
                pairStats.stats[pair]['longProfit']+=(longProfit)
                pairStats.stats[pair]['shortProfit']+=(shortProfit)
                longProfit=pairStats.stats[pair]['longProfit']
                shortProfit=pairStats.stats[pair]['shortProfit']
                pairStats.stats[pair]['totalProfit']+=((longProfit+shortProfit))
                
                if profit>0:
                    profitable=1 #This is for the model
                    pairStats.stats[pair]['profitable']+=1
                    pairStats.stats[pair]['sumCVProfit']+=env.pairs['CV']
                else:
                    profitable=0
                    pairStats.stats[pair]['losses']+=1
                    pairStats.stats[pair]['sumCVLoss']+=env.pairs['CV']
                    
                if trackTrans:
                    writeLog('%s %s %s L=%s %.3f S=%s %.3f P=%.3f PRCTP=%.3f CV=%.3f MA=%.3f Stdev=%.3f corr=%.3f Trig:%.3f' % \
                        ('Early Exit:',pair,currDate,longSymbol,longProfit,shortSymbol,shortProfit,profit,\
                        profit/(longStart+shortStart),env.CVMin,env.daysMA,env.minStd,env.corrMin, trigger))
                        
                #These details need to reflect the state prior to entering the trade
                #Since that is what will be available to model prior to entering the trade.
                #The symbol will be used to get any other details before modeling
                pairStats.stats[pair]['tradeDetails'].append({})
                enterDate=pairStats.stats[pair]['enterDate']
                pairStats.stats[pair]['tradeDetails'].append(savePair(pairStats.stats[pair]['tradeDetails'][-1],\
                    enterDate=enterDate,currDate=currDate,pair=pair,daysMA=env.daysMA,CVMin=env.CVMin,\
                    minStd=env.minStd,corrMin=env.corrMin,longSymbol=longSymbol,longStart=longStart,longProfit=longProfit,\
                    shortSymbol=shortSymbol,shortStart=shortStart,shortProfit=shortProfit,totalProfit=shortProfit+longProfit,\
                    CVDelta=env.CVDelta,trigger=trigger,profitable=profitable))

                #removePair(env,pair) #start from the beginning - need to recalc trigger, etc.
                position=0
                env.timesProcessed=0
                env.pairs['position']=0
                save=False
                #env.pairs is a dictionary that holds the Pair object, first pass create, otherwise get
                
        if save:
            savePair(env.pairs,pair=pair,currMavg=currMavg,ratioStdev=ratioStdev,\
            longSymbol=longSymbol,shortSymbol=shortSymbol,currDate=currDate,trigger=trigger,\
            position=position,CV=CV,longStart=longStart,shortStart=shortStart,maxStdev=maxStdev,\
            CVDelta=CVDelta,maRatio=maRatio,currMavg2=currMavg2)
            
        if position>0 and save:
            #print position,"***",env.pairs
            saveTotal[pair]['position']=position #env.pairs
            saveTotal[pair]['longSymbol']=longSymbol
            saveTotal[pair]['shortSymbol']=shortSymbol
            saveTotal[pair]['currDate']=currDate
            saveTotal[pair]['currMavg']=currMavg
            saveTotal[pair]['currMavg2']=currMavg2
            saveTotal[pair]['maxStdev']=maxStdev
            saveTotal[pair]['maRatio']=maRatio
            saveTotal[pair]['trigger']=trigger
            saveTotal[pair]['CV']=CV
            saveTotal[pair]['ratioStdev']=ratioStdev
        else:
            saveTotal[pair]={}
            
            #print env.pairs
            
            #raw_input()
    
        pair,currMavg,trigger,position,CV,currCV,profit=0.00,0.00,0.00,0.00,0.00,0.00,0.00
        longSymbol,shortSymbol='',''
        
        profitable=0
        save=True
                

