globals = {
		'dataFilesPath':'../../data',
		'outputFilesPath':'../../outputs',
		'symbolsNamesURL':'https://www.asx.com.au/asx/research/ASXListedCompanies.csv',
		'symbolsFileName':'ASXListedCompanies.csv',
		'symbolChangesFileName':'TickerChanges.csv',
		'start_date':'2010-01-01',
		'end_date':'2020-05-13',
		'freq':'d',
		'indicies':['^AORD','^AXJO'],
		'sqlFilesPath':'../data/SQL',
		'createDB':'0_createStagingDB.sql',
		'createStage':'1_createStagingTables.sql',
		'createProd':'2_createProdTables.sql',
		'createCalFeature':'4_tradingDays.sql'
}

config = {
		'user':'root',
		'password':'Xanglesprat',
		'host':'127.0.0.1',
		'database':'asx',
		'port':'33066',
		'allow_local_infile':True
}