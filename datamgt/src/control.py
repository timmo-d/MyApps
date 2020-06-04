"""
This module is the controller for getting, munging, cleaning, staging and loading into the database

"""

import os
import csv
from datetime import datetime
import mysql.connector

from datamgt.src.globals import *
from datamgt.src.common import *
from datamgt.src.download import *
from datamgt.src.stage import *
from datamgt.src.load import *


def main():
	# create local variables from global dictionary
	end_date = str(int(datetime.now().timestamp())) #globals['end_date']
	freq = globals['freq']
	localExtractFilePath = globals['dataFilesPath']
	symbolsNamesURL = globals['symbolsNamesURL']
	fileName = globals['symbolsFileName']
	symChangesFileName = globals['dataFilesPath']+'/'+globals['symbolChangesFileName']
	symbolsFilePath = globals['dataFilesPath']+'/'+fileName
	dataFilesPath = globals['dataFilesPath']
	createDBFilePath = globals['sqlFilesPath']+'/'+globals['createDB']
	createSTFilePath = globals['sqlFilesPath']+'/'+globals['createStage']
	createPTFilePath = globals['sqlFilesPath']+'/'+globals['createProd']
	createCFFilePath = globals['sqlFilesPath']+'/'+globals['createCalFeature']


	# Toggle the options below to control which functionality is executed when running this module.
	to_execute = {
		'stageTableSetup':False,	# Setup staging tables to store data from retrieved files
		'getCom':False,				# Download a list of companies trading on the ASX
		'stageCom':False,			# Load CSV file that was downloaded into the companies staging table
		'stageChanges':False,		# !!!FOR TEN YEARS WORTH, TAKES ABOUT 3 HOURS TO COMPLETE!!! Load CSV file that determines changes in symbols over the price history period
		'getIndicies':False,		# Download historical price data for each of the ASX indexes for date range specified in global options
		'stageIndicies':False,		# Load CSV file that was downloaded into the indicies staging table
		'getPrices':False,			# Download historical price data for each of the ASX companies for date range specified in global options
		'stagePrices':False,		# Load prices CSV files that were downloaded into the prices staging table
		'loadProdTables':False,		# Load the data from the prices staging table into prices production table
		'buildCalFeatures':False,	# Execute sql file to build calendar features for model
		'testing':True
	}

	###############################################################
	# As per control options above, execute selected functionality
	###############################################################

	# Build staging tables to store all data
	if to_execute['stageTableSetup']:
		print('Starting to build staging tables')
		executeSQLFromFile(createSTFilePath)
		print ('Staging tables configured.')

	start_date = getQuery('SELECT lastupdate FROM updates ORDER BY lastupdate DESC LIMIT 1','')
	print (''.join(start_date[0]))

	# Manage companies (symbols and names) that operate on ASX
	if to_execute['getCom']:
		print('Starting to retrieve company list from ASX URL')
		download(symbolsFilePath, symbolsNamesURL)
		print ('Company codes retrieved')

	if to_execute['stageCom']:
		print('Starting to load ASX companies into staging table')
		stageSymbols(symbolsFilePath)
		print ('Company symbols staged')

	# Manage common indexes that operate on ASX
	if to_execute['getIndicies']:
		print('Starting to retrieve indicies from URL')
		getIndicies(start_date,end_date,freq)
		print ('ASX indicies retrieved')

	if to_execute['stageIndicies']:
		print('Starting to load indicies into staging tables')
		for file in os.listdir(dataFilesPath):
			if file.endswith(".csv") & file.startswith("0"):
				stageIndicies(dataFilesPath+"/"+file)
				print("Loaded file " + dataFilesPath+"/"+file + " into database")
		print ('Index data staged')

	# Manage historical price data for stocks listed on ASX
	if to_execute['getPrices']:
		print('Starting to retrieve stock prices history from URL')
		getPrices(start_date,end_date,freq)
		setQuery('insert into updates values (' + str(end_date) + ')')
		print ('Stock price data retrieved')

	if to_execute['stagePrices']:
		print('Starting to load historical stock prices into staging tables')
		for file in os.listdir(dataFilesPath):
			if file.endswith(".csv") & file.startswith("1"):
				stagePrices(dataFilesPath+"/"+file)
				print("Loaded file " + file + " into database")
		print ('Stock data staged')

	if to_execute['stageChanges']:
		print('Starting to update historical symbol changes')
		print (symChangesFileName)
		stageSymbolChanges(symChangesFileName)
		print ('Company symbols staged')

	if to_execute['loadProdTables']:
		print('Loading data from staging tables into production tables')
		## May need to change C:\ProgramData\MySQL\MySQL Server 8.0\my.ini, set system variable innodb_buffer_pool_size to 256M
		executeSQLFromFile(createPTFilePath)
		print('Stock data loaded into Prod')

	if to_execute['buildCalFeatures']:
		print('Building calendar features')
		executeSQLFromFile(createCFFilePath)
		print ('Calendar features built')

	if to_execute['testing']:
		print ('running testing stuff')
		# params=''
		# lastUpdate = getQuery('SELECT lastupdate FROM updates ORDER BY lastupdate DESC LIMIT 1',params)
		# newUpdate = int(datetime.now().timestamp())
		#
		# setQuery('insert into updates values (' + str(end_date) + ')')
		# print (''.join(lastUpdate[0]))
		# print (str(newUpdate))



		# print ('old stuff')
		# start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
		# end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
		# reference_date = datetime.strptime("2010-01-01", "%Y-%m-%d").date()
		# reference_index = 1262304000  # 2010-01-01
		# s_date = str(int(reference_index + (start_date - reference_date).total_seconds()))
		# e_date = str(int(reference_index + (end_date - reference_date).total_seconds()))
		# print (s_date)
		# print (e_date)
		# setQuery('insert into updates values (' + str(s_date) + ')')
		# print ('tests complete')

if __name__ == "__main__":
	main()