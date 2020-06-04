import mysql.connector
from datamgt.src.globals import config

# May need to run the following code in MySQL workbench...
# SET GLOBAL local_infile = 1;
# SHOW VARIABLES LIKE 'local_infile';
def getQuery(query, params):
    #print (query)
    #print (params)
    conn =mysql.connector.connect(**config)
    c = conn.cursor(prepared=True)
    c.execute('set autocommit=1')
    c.execute('set global max_allowed_packet=1073741824;')
    c.execute(query,params)
    data = c.fetchall()
    #print (data)
    conn.close()
    return data

def setQuery(query):
    print (query)

    conn = mysql.connector.connect(**config)
    c = conn.cursor()
    c.execute('set autocommit=1')
    c.execute('set global max_allowed_packet=1073741824;')
    c.execute(query)
    conn.close()

def executeSQLFromFile(filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # connect to database
    conn = mysql.connector.connect(**config)
    c = conn.cursor()
    c.execute('set autocommit=1')
    c.execute('set global max_allowed_packet=1073741824;')

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        try:

            c.execute(command)
        except:
            print(command)
            print ("Command skipped")

    conn.close()