import sys

def knapsack(items, maxweight):
    # @memoized
    def bestvalue(i, j):
        if i == 0: return 0
        value, weight = items[i - 1]
        if weight > j:
            return bestvalue(i - 1, j)
        else:
            return max(bestvalue(i - 1, j),
                       bestvalue(i - 1, j - weight) + value)

    j = maxweight
    result = []
    for i in range(len(items), 0, -1):
        if bestvalue(i, j) != bestvalue(i - 1, j):
            result.append(items[i - 1])
            j -= items[i - 1][1]
    result.reverse()
    return bestvalue(len(items), maxweight), result


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: multi_knap.py [file]')
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename) as f:
        lines = f.readlines()

    maxweight = int(lines[0])
    items = [map(int, line.split()) for line in lines[1:]]
    ilist = [map(int, line.split()) for line in lines[1:]]

    bestvalue, reconstruction = knapsack(items, maxweight)

    print('Best possible value: {0}'.format(bestvalue))
    print('Items:')
    for value, weight in reconstruction:
        print('V: {0}, W: {1}'.format(value, weight))

import sys

def knapsack(items, maxweight, ilist):
    # Create an (N+1) by (W+1) 2-d list to contain the running values
    # which are to be filled by the dynamic programming routine.
    #
    # There are N+1 rows because we need to account for the possibility
    # of choosing from 0 up to and including N possible items.
    # There are W+1 columns because we need to account for possible
    # "running capacities" from 0 up to and including the maximum weight W.
    bestvalues = [[0] * (maxweight + 1)
                  for i in range(len(items) + 1)]

    # Enumerate through the items and fill in the best-value table
    for i, (value, weight) in enumerate(items):
        # Increment i, because the first row (0) is the case where no items
        # are chosen, and is already initialized as 0, so we're skipping it
        # print(i)
        i += 1
        for capacity in range(maxweight + 1):
            # Handle the case where the weight of the current item is greater
            # than the "running capacity" - we can't add it to the knapsack
            if weight > capacity:
                bestvalues[i][capacity] = bestvalues[i - 1][capacity]
            else:
                # Otherwise, we must choose between two possible candidate values:
                # 1) the value of "running capacity" as it stands with the last item
                #    that was computed; if this is larger, then we skip the current item
                # 2) the value of the current item plus the value of a previously computed
                #    set of items, constrained by the amount of capacity that would be left
                #    in the knapsack (running capacity - item's weight)
                candidate1 = bestvalues[i - 1][capacity]
                candidate2 = bestvalues[i - 1][capacity - weight] + value

                # Just take the maximum of the two candidates; by doing this, we are
                # in effect "setting in stone" the best value so far for a particular
                # prefix of the items, and for a particular "prefix" of knapsack capacities
                bestvalues[i][capacity] = max(candidate1, candidate2)

    # Reconstruction
    # Iterate through the values table, and check
    # to see which of the two candidates were chosen. We can do this by simply
    # checking if the value is the same as the value of the previous row. If so, then
    # we say that the item was not included in the knapsack (this is how we arbitrarily
    # break ties) and simply move the pointer to the previous row. Otherwise, we add
    # the item to the reconstruction list and subtract the item's weight from the
    # remaining capacity of the knapsack. Once we reach row 0, we're done
    reconstruction = []

    i = len(items)
    j = maxweight

    # print(ilist)
    # temp = []

    # for o in ilist:
    #     temp.append(list(o))
    # print(temp)

    # while i > 0:
    #     if bestvalues[i][j] != bestvalues[i - 1][j]:
    #         reconstruction.append(temp[i - 1])
    #         j -= temp[i - 1][1]
    #     i -= 1

    while i > 0:
        if bestvalues[i][j] != bestvalues[i - 1][j]:
            reconstruction.append(ilist[i - 1])
            j -= int(ilist[i - 1][1])
        i -= 1

    # Reverse the reconstruction list, so that it is presented
    # in the order that it was given
    reconstruction.reverse()

    # print(bestvalues)

    # Return the best value, and the reconstruction list
    return bestvalues[len(items)][maxweight], reconstruction


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: knapsack.py [file]')
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename) as f:
        lines = f.readlines()

    maxweight = int(lines[0])
    items = [map(int, line.split(',')[0:2]) for line in lines[1:]]
    # ilist = [map(int, line.split()) for line in lines[1:]]
    ilist = [line.split(',') for line in lines[1:]]

    bestvalue, reconstruction = knapsack(items, maxweight, ilist)

    print('Best possible value: {0}'.format(bestvalue))
    print('Cost:', sum(int(row[1]) for row in reconstruction))
    print('Items:')
    for value, weight, itype, cat, desc in reconstruction:
        print('V: {0}, W: {1}, T: {2}, C: {3}, D: {4}'.format(value, weight, itype, cat, desc))





