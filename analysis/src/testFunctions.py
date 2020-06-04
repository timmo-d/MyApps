"""
Test function

"""

from analysis.src.fetchData import getRawData

def main():
    ticker ="BHP"
    start_date="2015-01-01"
    end_date="2020-01-01"
    options={'qtype':'adjclose',
             'tables':['stockProd','tradingDays']
             }

    tickerDataRaw=getRawData(ticker,start_date,end_date,options)

    print (tickerDataRaw.head())

if __name__ == "__main__":
    main()