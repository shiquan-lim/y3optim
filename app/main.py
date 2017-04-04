import sys
import psycopg2
import cgi

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


if __name__ == '__main__':
    # if len(sys.argv) != 5:
    #     print('Please enter: main.py [budget] [group size] [your age] [dietary restrictions (x,y,z)]')
    #     sys.exit(1)

    myConnection = psycopg2.connect( host=hostname, user=user, password=password, dbname=dbname )
    cur = myConnection.cursor()
    cur.execute("""SELECT * from adult_breakfast_couple""")
    dbitems = cur.fetchall()
    # print(dbitems[0][1])

    maxweight = 1000
    items = [map(int, line[0:2]) for line in dbitems]

    bestvalue, reconstruction = knapsack(items, maxweight, dbitems)

    # print('Best possible value: {0}'.format(bestvalue))
    print('Cost:', sum(int(row[1]) for row in reconstruction))
    print('Items:')
    for value, weight, itype, cat, desc in reconstruction:
        print('V: {0}, W: {1}, T: {2}, C: {3}, D: {4}'.format(value, weight, itype, cat, desc))


