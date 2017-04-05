import sys
import psycopg2
import cgi
import datetime
from psycopg2.extensions import AsIs

hostname = 'y3optim.cnlc0eowtsp7.ap-southeast-1.rds.amazonaws.com'
user = 'limshiq'
password = 'awesomeSQ'
dbname = 'y3optim'
port = 5432

def knapsack(items, maxweight, ilist):
    bestvalues = [[0] * (maxweight + 1)
                  for i in range(len(items) + 1)]

    for i, (value, weight) in enumerate(items):
        i += 1
        for capacity in range(maxweight + 1):
            if weight > capacity:
                bestvalues[i][capacity] = bestvalues[i - 1][capacity]
            else:
                candidate1 = bestvalues[i - 1][capacity]
                candidate2 = bestvalues[i - 1][capacity - weight] + value
                bestvalues[i][capacity] = max(candidate1, candidate2)

    reconstruction = []
    i = len(items)
    j = maxweight

    while i > 0:
        if bestvalues[i][j] != bestvalues[i - 1][j]:
            reconstruction.append(ilist[i - 1])
            j -= int(ilist[i - 1][1])
        i -= 1

    reconstruction.reverse()

    return bestvalues[len(items)][maxweight], reconstruction

def get_table_name(age, time, groupNum, weather):
	if(age < 18):
		age = 'YOUTH'
	elif(age < 35):
		age = 'ADULT'
	elif(age < 50):
		age = 'MIDDLE'
	else:
		age = 'SENIOR'

	if(time < 6):
		time = 'SUPPER'
	elif(time < 12):
		time = 'BREAKFAST'
	elif(time < 18):
		time = 'LUNCH'
	else:
		time = 'DINNER'

	if(groupNum == 1):
		groupNum = 'SOLO'
	elif(groupNum == 2):
		groupNum = 'COUPLE'
	else:
		groupNum = 'GROUP'

	return(age+'_'+time+'_'+groupNum+'_'+weather.upper())


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print('Please enter: main.py [budget] [group size] [your age] [dietary restrictions (x,y,z)] [weather]')
        with open('messages/welcome.txt') as f:
        	lines = f.readlines()
        for line in lines:
        	print(line)
        sys.exit(1)

    d = datetime.datetime.now().time().hour

    profile = get_table_name(int(sys.argv[3]), d, int(sys.argv[2]), sys.argv[5])
    print("Extracting from profile...",profile)

    myConnection = psycopg2.connect( host=hostname, user=user, password=password, dbname=dbname )
    cur = myConnection.cursor()
    cur.execute('SELECT * FROM "%(table)s"', {"table": AsIs(profile)})
    dbitems = cur.fetchall()

    maxweight = int(sys.argv[1]) * 100
    choice = sys.argv[4]

    if(choice != '-'):
    	cList = choice.split(',')
    	for c in cList:
    		for i in dbitems:
    			if (i[2]=='Main' or i[2]=='Side') and i[3].find(c):
    				print (i[2], i[3])

    items = [map(int, line[0:2]) for line in dbitems]

    bestvalue, reconstruction = knapsack(items, maxweight, dbitems)

    # print('Best possible value: {0}'.format(bestvalue))
    print('Cost: $', sum(int(row[1]) for row in reconstruction)/100)
    print('Items:')
    for value, weight, itype, cat, desc in reconstruction:
        print('V: {0}, W: {1}, T: {2}, C: {3}, D: {4}'.format(value, weight, itype, cat, desc))


