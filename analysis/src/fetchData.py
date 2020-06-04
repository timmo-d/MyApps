"""
This module fetches the data for a ticker given the options and a start_date, end_date

"""
#
from analysis.src.setup import *
from analysis.src.common import getQuery

def getRawData(ticker, start_date, end_date, options, buf=300):
    """This function does something.

	:param name: The name to use
	:type name: None
	:param state: None
	:type state: None
	:returns: None
	:raises: None
	"""
    #print('in getrawdata')
    # The buf variable will be the extra number of days behind the start date that need to be fetched.
    # This is required to get trailing data that might be required to compute momentum, reversal, jump etc

    qtype = options['qtype']
    stockTable = options['tables'][0]
    daysTable = options['tables'][1]

    query = 'select c.datestamp, c.' + qtype + ', t.month, t.day, t.dayOfWeek, t.tDaysLeftMonth, t.tDayinMonth, t.tDayinWeek' \
    		' from ' + stockTable + ' c left join ' + daysTable + ' t on c.datestamp=t.tDay' \
    		' where c.symbol=%s and c.datestamp<%s and t.id>=(select min(id) from tradingDays where tDay>=%s)-%s order by datestamp desc'
    params = (ticker, end_date, start_date, buf)

    rawData = getQuery(query, params)

    tickerDataRaw = pd.DataFrame(rawData, columns=["Datestamp", "Price", "Month", "Day", "DayofWeek", "tDaysleftMonth",
                                                   "tDayinMonth", "tDayinWeek"])
    #print('retrieved raw data')
    #print(tickerDataRaw.head(5))

    # Let's make the index of the data frame the date, this will help easily sort, filter  by date
    tickerDataRaw.index = tickerDataRaw["Datestamp"]
    del tickerDataRaw["Datestamp"]

    return tickerDataRaw
