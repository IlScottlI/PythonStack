def makeChange(num):
    change = num
    numQ = 0
    numD = 0
    numN = 0
    numP = 0
    if (change / 25) > 1:
        numQ = str(change/25).split('.')[0]
        change = change - (int(numQ)*25)
    if (change / 10) > 1:
        numD = str(change/10).split('.')[0]
        change = change - (int(numD)*10)
    if (change / 5) > 1:
        numN = str(change/5).split('.')[0]
        change = change - (int(numN)*10)
    if change > 1:
        numP = change
    result = {
        'numQ': numQ,
        'numD': numD,
        'numN': numN,
        'numP': numP
    }

    return result


print(makeChange(100))
