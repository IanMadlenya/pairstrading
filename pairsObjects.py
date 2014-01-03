class Calibration(object):
    def __init__(self):
        #Each pair will have its own dictionary
        self.models={} #calibrate.models['AAPL GOOG'].model
        #The model is calibrated when the avg percent of profitable to non-profitables doesn't change
        #by more then .01
        #Each pair has a model
        
class PairStats(object): #Pair Statistics
    def __init__(self): #Holds a dictionary of Stats objects
        self.stats={}

class Stats(object): #Total statistics
    def __init__(self):
        self.enters=0
        self.exits=0
        self.sumCV=0
        self.avgCV=0
        self.sumCVProfit=0
        self.sumCVLoss=0
        self.avgCVProfit=0
        self.avgCVLoss=0        
        self.longProfit=0.00
        self.shortProfit=0.00
        self.totalProfit=0.00
        self.MA=0
        self.corrMin=0.00
        self.CVMin=0.00
        self.minStd=0.00
        self.profitable=0
        self.losses=0
        self.tradeDetails=[] #This will be fed to the model with a flag for profit or loss 
        # The model will need a description of the history of the ratios, CV, how many std devs it exceeded the trigger, etc.
        # A classification model will use these details to determine if a new trade has a
        # high probability to be profitable. 
             
class Environment(object):
    def __init__(self):
        self.startDate=None
        self.pairs={}
        self.priceQueue={}
        self.prices={}
        self.pairQueue=[]
        self.corrData=[]
        self.ratioData={}
        self.dataInfo=[]
        self.daysMA=0 #Varying the moving average
        self.exitPeriod=0
        self.corrMin=0
        self.minStrength=0
        self.minStd=0.00
        self.maxStdev=0.00
        self.CVDelta=0.00
        self.maRatio=0.00
        self.timesProcessed=0
        self.startDaysMA=0
        self.startCorrMin=0.00
        self.startCVMin=0.00
        self.startMinStd=0.00
        
