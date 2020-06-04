"""
Module to control which strategy to run

# Here's what our code should do
# Given a ticker,
# training period, test period
# it should train a classifier using the training period and
# run a backtest on the test period
# The result should be the Sharpe Ratio of our strategy in the test period
# and the other metrics we might need to evaluate the strategy


# We should be able to run this backtest with different options
# The frequency (daily/weekly/monthly) , the features to be used
# which kind of ticker - NSE vs international
# which price is used - open , close, high or low etc

# all these options are captured in a dictionary that will be passed
# from our main function down to any function that needs it

# We'll keep adding to this dict as needed, the first set of options is the
# one that specifies from which tables and how the raw data we need will be fetched.
"""


#from src.model.setup import *
from analysis.src.testAndTrain import *


def main():
    algorithms = {
                'MLlibrary':[KNeighborsRegressor,RandomForestClassifier,GaussianNB,SVC],
                'MLlibParams':[{'n_neighbors':5},{"n_estimators":100,"random_state":2},{},{}]
    }
    options =  {'qtype':'adjclose',# qtype specifies the price type we are running our model on
                'tables':["stockProd","tradingDays"],# tables are those which hold the data for our ticker
                'freq':1, # The frequency of trading, daily=0, monthly=1,weekly=2
                'offset':1, # The offset if the period > 1day, ie which trading day in the month/week the strategy will be executed
                'pure':1, # from here we have the features , the returns as is
                'cal':1, # Calendar features
                'history':0, # last 3 periods returns
                'momentum':1, # momentum features
                'jump':1, # jump features
                'value':1, # long term reversal features
                'prevWeeks':1,# Now by turning this to 1 we can run a model which includes previous weeks
                'algo':algorithms['MLlibrary'][1],
                'algo_params':algorithms['MLlibParams'][1]
               }



    # We've written a function that can construct the features for our datapoints,
    # But we also might want to construct similar features for tickers that might
    # be related and use them as input features

    supportTickers= None #[("AORD",{'pure':0,'momentum':1,'jump':0,'prevWeeks':0})]

    ticker="BHP"
    trainStart="2015-01-01"
    testPeriod=["2017-06-01","2019-04-01"]
    if options['algo'] == KNeighborsRegressor:
        result=backtestResults(ticker,trainStart,testPeriod,options,supportTickers,predictFn=getPredictionsNN)
    elif options['algo'] == RandomForestClassifier:
        result=backtestResults(ticker,trainStart,testPeriod,options,supportTickers,predictFn=getPredictions)
    elif options['algo'] == GaussianNB:
        result=backtestResults(ticker,trainStart,testPeriod,options,supportTickers,predictFn=getPredictions)
    else:
        result=backtestResults(ticker,trainStart,testPeriod,options,supportTickers,predictFn=getPredictions)

if __name__ == "__main__":
    main()












