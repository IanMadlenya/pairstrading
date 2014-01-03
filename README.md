The source code for this pairs trading depends on data from eoddata.com. The data is imported into the MongoDB and then initialized from the main program: realTimePairs.py

The system creates optimized pairs based on what parameters (days MA, standard deviations,...) created profitable trades.

We first look at what we will use to describe and track a pair.
1)The individual price stock histories
2)The ratio of the prices. (The ratio is simply one price divided by the other.)
3)The standard deviation of the ratio.
4)The moving average of the ratio.
5)The correlation of the price history of the two stocks
6)Though not a requirement we will be using the coefficient of variation - the standard deviation divided by the average.

Generally, when the ratio exceeds 2 standard deviations and is returning to correlation the trade is entered and when 
the correlation is near the original level, the trade is exited. 
But many arbitrary assumptions immediately come in view. 

For example, decisions need to be made for determining if the pair is correlated at all. 
From which time period of the price history do we use to calculate the correlation?
And for how long? Can't be too long ago since the landscape may have changed and is no longer valid. Can't be too recent since 
the overlap of the divergence will invalidate the calculation and we need that breakdown of correlation to make the 
pair trade. Thus, we would never find a correlated pair.Also, how correlated do we need the pair to be? 70%? 90%? 
Remember that the more correlated the pair the smaller 2 standard deviations will be and make the trade very short.

The point is that a pairs behavior is unique to each pair. For some, 2 standard deviations will create an opportunity.
For others, 3 standard deviations is a better opportunity and some 1.75 standard deviations will be optimal. If we
were to vary every variable listed above and move through the history we could classify the values used for the 
history as a profitable or not-profitable parameter set. At the end of the "calibration" step, we would keep only 
the most profitable parameters and use those for future searches. 

Of course with any trading system, use at your own risk.

If you need more info, please contact me. 
