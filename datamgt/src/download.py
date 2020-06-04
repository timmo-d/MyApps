"""
The purpose of this module is to download stock details and prices from internet.
These files are ASX companies listings, along with ticker changes and price data.

"""
#Downloads Management
#.. module:: download
#   :platform: Windows
#   :synopsis: Module to download stock details and prices from internet

#.. moduleauthor:: Tim Davies <td_gen@westnet.com.au>


import os
from datetime import datetime
from csv import writer
from csv import reader

from datamgt.src.common import getQuery
from datamgt.src.globals import *



def constructYFURL(ticker,s_date,e_date,freq):
	"""This function constructs the correct URL string to download from Yahoo Finance.

	:param name: The name to use
	:type name: None
	:param state: None
	:type state: None
	:returns:  str -- URL for downloading from Yahoo Finance
	:raises: None
	"""

	#crypto: https://query1.finance.yahoo.com/v7/finance/download/BTC-AUD?period1=1557468908&period2=1589091308&interval=1d&events=history
	#stock: https://query1.finance.yahoo.com/v7/finance/download/BHP.AX?period1=1262304000&period2=1589155200&interval=1d&events=history
	#index: https://query1.finance.yahoo.com/v7/finance/download/^AORD?period1=1420070400&period2=1451606400&interval=1d&events=history
	# another site to retrieve data: https://www.marketindex.com.au/data-downloads

	ticker=ticker.replace("^","%5E")
	yfURL = "https://query1.finance.yahoo.com/v7/finance/download/" + ticker + "?period1=" + str(''.join(s_date[0])) + "&period2=" + str(e_date) + "&interval=1" + freq + "&events=history"
	print (yfURL)
	return yfURL

def download(filePath,urlOfFile):
	"""This function downloads a csv file from the internet and saves to local machine.

	:param name: The name to use
	:type name: None
	:param state: None
	:type state: None
	:returns: None
	:raises: HTTPError
	"""

	import urllib3
	urllib3.disable_warnings()

	# get my user agent header string from www.whatsmyuseragent.com
	hdr = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1 RuxitSynthetic/1.0 v1100525156 t4690183951324214268 smf=0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Language':'en-US,en;q=0.8',
		'Accept-Encoding':'none',
		'Connection':'keep-alive'}

	http = urllib3.PoolManager()
	try:
		page = http.request('GET', urlOfFile, headers=hdr)
		content=page.data

		with open(filePath,"wb") as output:
			output.write(bytearray(content))

	except urllib3.exceptions.HTTPError as e:
		# Let's print out the error, if any resulted
		print (e.fp.read())

def add_column_in_csv(input_file, output_file, transform_row):
	"""Append a column in existing csv using csv.reader / csv.writer classes.

	:param name: The name to use
	:type name: None
	:param state: None
	:type state: None
	:returns: None
	:raises: None
	"""

	# Open the input_file in read mode and output_file in write mode
	with open(input_file, 'r') as read_obj, open(output_file, 'w', newline='') as write_obj:

		csv_reader = reader(read_obj)	# Create a csv.reader object from the input file object
		csv_writer = writer(write_obj)	# Create a csv.writer object from the output file object
		for row in csv_reader:			# Read each row of the input csv file as list
			transform_row(row, csv_reader.line_num)	# Pass the list / row in the transform function to add column text for this row
			csv_writer.writerow(row)	# Write the updated row / list to the output file

def getPrices(start_date,end_date,freq):
	"""Get prices for all tickers in database for time period between start and finish dates at the selected frequency.

	:param name: The name to use
	:type name: None
	:param state: None
	:type state: None
	:returns: None
	:raises: None
	"""

	query = "SELECT symbol FROM companyStaging"
	symbols =getQuery(query, '')
	i=0

	for symbol in symbols:
		i= i + 1
		totalNum = len(symbols)
		ticker= ' '.join(symbol)
		localFilePath= globals['dataFilesPath'] + ticker + ".AX.csv"
		yfURL = constructYFURL(ticker,start_date,end_date,freq)
		print (str(i) + " of " + str(totalNum) + " - " + yfURL)
		try:
			download(localFilePath,yfURL)
			#print(yfURL)
		# Add the column in csv file with header
			add_column_in_csv(localFilePath, globals['dataFilesPath']+"/1" + ticker + ".csv", lambda row, line_num: row.append('Symbol') if line_num == 1 else row.append(ticker))
			os.remove(localFilePath)
		except:
			print('download failed')

def getIndicies(start_date,end_date,freq):
	"""Get prices for all indicies in database for time period between start and finish dates at the selected frequency.

	:param name: The name to use
	:type name: None
	:param state: None
	:type state: None
	:returns: None
	:raises: None
	"""

	#indicies=['^AORD','^AXJO']
	indicies = globals['indicies']
	localDir=globals['dataFilesPath']
	for index in indicies:

		url=constructYFURL(index,start_date,end_date,freq)
		index = str(index[1: 5: 1])
		print(localDir+'/'+index+'.csv')
		try:
			download(localDir+'/'+index+'.csv', url)
			add_column_in_csv(localDir+'/'+index+'.csv', localDir+"/0" + index + ".csv", lambda row, line_num: row.append('Symbol') if line_num == 1 else row.append(index))
			os.remove(localDir+'/'+index+'.csv')
		except:
			print('download failed')
