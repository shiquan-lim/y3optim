from docplex.cp.model import *
from scipy import *
import psycopg2

hostname = 'y3optim.cnlc0eowtsp7.ap-southeast-1.rds.amazonaws.com'
user = 'limshiq'
password = 'awesomeSQ'
dbname = 'y3optim'
port = 5432

def doQuery( conn ) :
    cur = conn.cursor()

    # cur.execute()

    # for firstname, lastname in cur.fetchall() :
    #     print firstname, lastname

def writeData(conn):
	cur = conn.cursor()
	f = open(r'/Users/limshiquan/Desktop/outlet.csv', 'r')
	cur.copy_from(f, "outlets", sep=',')
	f.close()

print ("Hello world")
myConnection = psycopg2.connect( host=hostname, user=user, password=password, dbname=dbname )
# doQuery( myConnection )
writeData(myConnection)
myConnection.commit()
myConnection.close()
