from docplex.cp.model import *
from scipy import *
import psycopg2

hostname = 'y3optim.cnlc0eowtsp7.ap-southeast-1.rds.amazonaws.com'
user = 'limshiq'
password = 'awesomeSQ'
dbname = 'y3optim'

def doQuery( conn ) :
    cur = conn.cursor()

    # cur.execute()

    # for firstname, lastname in cur.fetchall() :
    #     print firstname, lastname

print ("Hello world")
myConnection = psycopg2.connect( host=hostname, user=user, password=password, dbname=dbname )
doQuery( myConnection )
myConnection.close()