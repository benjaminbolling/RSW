# IO functions for RSW algorithm
def shiftsperpersonpercycle(workinghours,noofweeks,shiftlengths):
    return int(workinghours*noofweeks/shiftlengths)+(workinghours*noofweeks/shiftlengths > 0) # rounding integer up

def weeksneeded(noOfPeople,workingdays,shifttype,shiftlengths,workinghours):
    return int(noOfPeople*workingdays*shifttype*shiftlengths/workinghours) + (noOfPeople*workingdays*shifttype*shiftlengths/workinghours > 0)

def freedaysover7days(weeklyresting):
    return int(weeklyresting/24)+(weeklyresting/24 > 0)

def checkifallshiftsfilled(workingdays,noOfPeople,shifttype,appendflag,item1): # Just a constraint that must be fulfilled
    day = 0
    cycleseries = []
    weekseries = []
    for m in range(len(item1)):
        weekseries.append(item1[m])
        day += 1
        if day > workingdays-1:
            day = 0
            cycleseries.append(weekseries)
            weekseries = []
    cyclecheck = []
    for a in range(workingdays):
        cyclecheck.append(0)
    for a in cycleseries:
        for b in range(len(a)):
            cyclecheck[b] = cyclecheck[b] + int(a[b])
    for m in cyclecheck:
        if m < shifttype*noOfPeople:
            appendflag = False
    return appendflag

def freedaysweeklycheck(freedaysover7days,appendflag,item1): # Just another constraint that must be fulfilled
    noOnes = 0 # check so that number of free days over 7 day periods rule is followed.
    item2 = [] # have to check a week back so when last week goes over to next week, rule is also obeyed.
    for m in range(len(item1)-7,len(item1)):
        item2.append(item1[m])
    for m in range(len(item1)):
        item2.append(item1[m])
    for item in item2:
        if item == "1":
            noOnes += 1
        elif item == "0":
            noOnes = 0
        if noOnes > 7-freedaysover7days:
            appendflag = False
    return appendflag

def freeDaysClusterCheck(appendflag,item1): # An additional constraint that might need to be fulfilled
    freeDays = 0
    item2 = [] # have to check a week back so when last week goes over to next week, rule is also obeyed.
    for m in range(len(item1)-7,len(item1)):
        item2.append(item1[m])
    for m in range(len(item1)):
        item2.append(item1[m])
    minzero = 0
    for item in item2:
        if item == "0":
            if minzero == 0:
                minzero = 1
            else:
                minzero += 1
        elif item == "1":
            if minzero == 1:
                appendflag = False
            else:
                minzero = 0
    return appendflag

def returnActiveSeries(shiftseries,afterworkIntValue,workingdays)
    try:
        tempActiveSeries = shiftseries[afterworkIntValue].split(" ")
        afterweeksvisible(True)
    except:
        tempActiveSeries = []
        afterweeksvisible(False)
    activeSeries = []
    for s in tempActiveSeries:
        activeSeries.append(int(s))
    activeSeriesSerie = []
    n = 0
    activeSerie = []
    for m in activeSeries:
        n += 1
        activeSerie.append(m)
        if n == workingdays:
            activeSeriesSerie.append(activeSerie)
            activeSerie = []
            n = 0
    return activeSeries
