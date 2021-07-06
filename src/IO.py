# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # #                                                                                             # # # #
# # # #                    1/2/3-shift scheduling algorithm - phase 1:                              # # # #
# # # #                                                                                             # # # #
# # # #                         - - - - - - - - - - - - - - - - - -                                 # # # #
# # # #                                                                                             # # # #
# # # #                             Automatic shift generator                                       # # # #
# # # #                                                                                             # # # #
# # # #                         - - - - - - - - - - - - - - - - - -                                 # # # #
# # # #                                                                                             # # # #
# # # #   Author: Benjamin Bolling                                                                  # # # #
# # # #   Affiliation: European Spallation Source ERIC                                              # # # #
# # # #   Lund, Sweden                                                                              # # # #
# # # #   Initialization date: 2020-06-08                                                           # # # #
# # # #   Milestone 1 (phase 1, 0:s and 1:s generated):                               2020-06-29    # # # #
# # # #   Milestone 2 (phase 1 all working, proceeding to phase 2):                   2020-07-01    # # # #
# # # #   Milestone 3 (phase 2 all working, initial version ready):                   2020-07-03    # # # #
# # # #   Milestone 4 (phase 2 finished, solution finder implemented):                2020-07-03    # # # #
# # # #   Milestone 5 (abstracting functions, added check for solutions in phase1):   2021-01-09    # # # #
# # # #                                                                                             # # # #
# # # #                                                                                             # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# IO functions for RSW algorithm (phase 1)
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

def returnActiveSeries(shiftseries,workingdays,tempActiveSeries):
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

# IO functions for RSW algorithm (phase 2)
def createSolutionMatrices(days,shifts,zeroOneS,dailyresting,shiftlengths,shifttype,weeklyresting):
    results = cartesianProduct(days,shifts).tolist()
    for indR, result in enumerate(results):
        for indV, value in enumerate(result):
            results[indR][indV] = int(value)
    for result in results:
        matrixOut = insertFreeDaysInSolutionMatrix(result,zeroOneS)
        shiftsOk = checkifshiftsOK(matrixOut,dailyresting,shiftlengths,shifttype,weeklyresting)
        if shiftsOk == True:
            yield matrixOut

def insertFreeDaysInSolutionMatrix(input,zeroOneS):
    ind = -1
    matrixOut = []
    for m in range(len(zeroOneS)):
        if zeroOneS[m] == 1:
            ind += 1
            matrixOut.append(input[ind])
        else:
            matrixOut.append(0)
    return matrixOut

def cartesianProduct(days,shifts):
    import numpy
    arrays = []
    for n in range(days):
        arrays.append(shifts)
    arr = numpy.empty([len(a) for a in arrays] + [days])
    for i, a in enumerate(numpy.ix_(*arrays)):
        arr[...,i] = a
    return arr.reshape(-1, days)

def recursiveCartesianProduct(days,shifts,arrays,array,level,manySolutions,zeroOneS,dailyresting,shiftlengths,shifttype,weeklyresting):
    if len(arrays) > 1 and manySolutions == 0:
        return arrays
    else:
        for m in range(1,len(shifts)):
            for n in range(level-1,days):
                if array[n] != shifts[m]:
                    array2 = array.copy()
                    array2[n] = shifts[m]
                    matrixOut = insertFreeDaysInSolutionMatrix(array2,zeroOneS)
                    if matrixOut not in arrays:
                        if checkifshiftsOK(matrixOut,dailyresting,shiftlengths,shifttype,weeklyresting) == True:
                            arrays.append(matrixOut)
                        if level < days:
                            arrays = recursiveCartesianProduct(days,shifts,arrays,array2,level+1,manySolutions,zeroOneS)
        return arrays

def checkifshiftsOK(solutionMatrix,dailyresting,shiftlengths,shifttype,weeklyresting):
    shiftsOk = True
    prevval = 0
    # Check so time between each shift is obliged
    for shift in solutionMatrix:
        if int(shift) >= prevval or dailyresting < (16 - (prevval-int(shift))*shiftlengths):
            prevval = int(shift)
        elif int(shift) == 0:
            prevval = int(shift)
        else:
            prevval = int(shift)
            shiftsOk = False
    # Check so time between each last and first shift is obliged since shift 0 follows shift -1
    if solutionMatrix[0] < solutionMatrix[-1] and solutionMatrix[0] != 0:
        shiftsOk = False
    # Check if all shifts are filled
    if shiftsOk == True:
        shiftsOk = freedaysweeklycheck_phase2(solutionMatrix,weeklyresting,shiftlengths)
    if shiftsOk == True:
        day = -1
        dayShifts = []
        for m in range(7):
            dayShifts.append([])
        for n in range(int(len(solutionMatrix))):
            day += 1
            dayShifts[day].append(int(solutionMatrix[n]))
            if day == 6:
                day = -1
        for k in range(len(dayShifts)):
            if sum(dayShifts[k]) > 0:
                for l in range(1,shifttype+1):
                    if l not in dayShifts[k]:
                        shiftsOk = False
    return shiftsOk

def freedaysweeklycheck_phase2(item1,weeklyresting,shiftlengths): # Just another constraint that must be fulfilled
    # noOnes = 0 # check so that number of free days over 7 day periods rule is followed.
    # item2 = [] # have to check a week back so when last week goes over to next week, rule is also obeyed.
    # appendflag = True
    # for m in range(len(item1)-7,len(item1)):
    #     item2.append(item1[m])
    # for m in range(len(item1)):
    #     item2.append(item1[m])
    # for item in item2:
    #     if item == "1":
    #         noOnes += 1
    #     elif item == "0":
    #         noOnes = 0
    #     if noOnes > 7-weeklyresting:
    #         appendflag = False
    # return appendflag



    shiftstarts = 24/3
    noOnes = 0 # check so that number of free days over 7 day periods rule is followed.
    item2 = [] # have to check a week back so when last week goes over to next week, rule is also obeyed.
    appendflag = True
    for m in range(len(item1)-7,len(item1)):
        item2.append(item1[m])
    for m in range(len(item1)):
        item2.append(item1[m])
    restingTime = 0
    daysGoneBy = 0
    hoursSinceShiftEnd = 0
    for ind,item in enumerate(item2):
        if item > 0:
            timetoShift = (item-1)*shiftstarts
            if timetoShift + hoursSinceShiftEnd >= weeklyresting:
                daysGoneBy = 0
            else:
                daysGoneBy += 1
            hoursSinceShiftEnd = 24 - ((item-1)*shiftstarts + shiftlengths)
        elif item == 0:
            hoursSinceShiftEnd = hoursSinceShiftEnd + 24
        if daysGoneBy > 6:
            appendflag = False
    return appendflag

def idCombos(matrix,shifttype,shifts,shiftlengths,weeklyresting,dailyresting):
    zeroOneS = []
    dailyresting = 11
    noofcombinations = int(float(shifttype)**float(sum(matrix)))
    proceed = 1
    mode = "mem"
    if proceed == 1:
        if mode == "proc":
            arrays = [[shifts[0]] * sum(matrix)]
            solutionMatrices = recursiveCartesianProduct(sum(matrix),shifts,arrays,arrays[0],1,1,matrix)
            if checkifshiftsOK(solutionMatrices[0],dailyresting,shiftlengths,shifttype,weeklyresting) == False:
                del solutionMatrices[0]
        elif mode == "mem":
            solutionMatrices = list(createSolutionMatrices(sum(matrix),shifts,matrix,dailyresting,shiftlengths,shifttype,weeklyresting))
    return solutionMatrices

def testMatrices(raw_matrix,shifttype,shifts,shiftlengths,weeklyresting,dailyresting):
    matrix = []
    raw_values = raw_matrix.split(" ")
    for raw_value in raw_values:
        if len(raw_value) > 0:
            matrix.append(int(raw_value))
    if len(matrix) == 0:
        return 0
    else:
        return idCombos(matrix,shifttype,shifts,shiftlengths,weeklyresting,dailyresting)

def createODS(matrix,weeks,fn,shifts):
    from pyexcel import save_as
    weekdays = "Mon;Tue;Wed;Thu;Fri;Sat;Sun"
    for week in range(weeks):
        if week == 0:
            headlabel = "Worker:;"+weekdays
        else:
            headlabel = headlabel + ";" + weekdays
    rows = [headlabel.split(";")]

    results = {}
    for shift in shifts:
         results[shift] = [0] * len(matrix[0])

    for ind, person in enumerate(matrix):
        for ind2, shift in enumerate(person):
            for shifttype in shifts:
                if shift == shifttype:
                    results[shifttype][ind2] += 1
        person.insert(0,"Person "+str(ind))
        rows.append(person)

    rows.append([' '] * len(matrix[0]))
    for shift in shifts:
        results[shift].insert(0,"{}-shifts: ".format(shift))
        rows.append(results[shift])

    save_as(bookdict={'RSW': rows}, dest_file_name="{}.ods".format(fn))
