"""
Module to stage downloads into database

"""

import csv
import mysql.connector
from datamgt.src.globals import config
from datamgt.src.common import *

def stageSymbols(fileName):
	"""This function does something.

	:param name: The name to use
	:type name: None
	:param state: None
	:type state: None
	:returns: None
	:raises: None
	"""
	delimiter = r','  # The file need to be csv files
	encloseChar = '"'

	conn = mysql.connector.connect(**config)
	c = conn.cursor()
	c.execute("LOAD DATA LOCAL INFILE %s"
			  " INTO TABLE companyStaging"
			  " FIELDS TERMINATED BY %s"
			  " ENCLOSED BY %s"
			  " IGNORE 3 LINES"
			  " (name, symbol, gicsgroup)"
			  , (fileName, delimiter, encloseChar))
	conn.commit()
	c.close()
	conn.close()

def stageSymbolChanges(fileName):
	"""This function does something.

	:param name: The name to use
	:type name: None
	:param state: None
	:type state: None
	:returns: None
	:raises: None
	"""
	conn = mysql.connector.connect(**config)
	c = conn.cursor()
	lineNum = 0

	with open(fileName, newline='') as csvfile:
		linereader = csv.reader(csvfile, delimiter=',', quotechar="\"")

		for row in linereader:
			lineNum = lineNum + 1
			if lineNum == 1:
				continue

			oldSymbol = row[1]
			newSymbol = row[3]

			try:
				print(oldSymbol, newSymbol)
				c.execute("Update stockStaging set symbol=%s where symbol = %s;", (newSymbol, oldSymbol))
			except:
				continue
			finally:
				conn.commit()

	c.close()
	conn.close()

def stagePrices(fileName):
	"""This function does something.

	:param name: The name to use
	:type name: None
	:param state: None
	:type state: None
	:returns: None
	:raises: None
	"""
	delimiter = r','  # The files need to be csv files
	terminator = '\r'
	conn = mysql.connector.connect(**config)
	c = conn.cursor()
	c.execute("LOAD DATA LOCAL INFILE %s"
			  " INTO TABLE stockStaging"
			  " FIELDS TERMINATED BY %s"
			  " LINES TERMINATED BY %s"
			  " IGNORE 1 LINES"
			  " (datestamp,open,high,low,close,adjclose,volume,symbol)"
			  , (fileName, delimiter, terminator))
	conn.commit()
	c.close()
	conn.close()
#			  " LINES TERMINATED BY '\r\n'"

def stageIndicies(fileName):
	"""This function does something.

	:param name: The name to use
	:type name: None
	:param state: None
	:type state: None
	:returns: None
	:raises: None
	"""
	delimiter = r','  # The files need to be csv files
	terminator = '\r'
	conn = mysql.connector.connect(**config)
	c = conn.cursor()
	c.execute("LOAD DATA LOCAL INFILE %s"
			  " INTO TABLE indiciesStaging"
			  " FIELDS TERMINATED BY %s"
			  " LINES TERMINATED BY %s"
			  " IGNORE 1 LINES"
			  " (datestamp,open,high,low,close,adjclose,volume,symbol)"
			  , (fileName, delimiter, terminator))
	conn.commit()
	c.close()
	conn.close()