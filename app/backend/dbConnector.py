import MySQLdb as mariadb
from db_credentials import host, user, passwd, db

''' Connects to database and returns database object'''
def connectDB(host = host, user = user, passwd = passwd, db = db):
    connection = mariadb.connect(host, user, passwd, db)
    return connection

'''Executes passed SQL query with passed db connection and returns a Cursor object'''
def executeQuery(dbConnection = None, query = None, query_params = ()):
    if dbConnection is None:
        print("No connection to database")
        return None
    
    if query is None or len(query.strip()) == 0:
        print("Empty query. Please pass a SQL query")
        return None

    #create cursor to execute query
    cursor = dbConnection.cursor()

    '''
    #Create tuple of parameters to send with query
    params = tuple()
    for i in query_params:
        params = params + (i)
    '''

    #Commit changes to database
    cursor.execute(query, query_params)

    dbConnection.commit()
    return cursor
