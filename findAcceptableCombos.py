
def createSolutionMatrices(days,shifts,zeroOneS):
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
    if solutionMatrix[0] < int(shift):
        shiftsOk = False
    # Check if all shifts are filled
    if shiftsOk == True:
        shiftsOk = freedaysweeklycheck(solutionMatrix,weeklyresting)
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

def freedaysweeklycheck(item1,weeklyresting): # Just another constraint that must be fulfilled
    noOnes = 0 # check so that number of free days over 7 day periods rule is followed.
    item2 = [] # have to check a week back so when last week goes over to next week, rule is also obeyed.
    appendflag = True
    for m in range(len(item1)-7,len(item1)):
        item2.append(item1[m])
    for m in range(len(item1)):
        item2.append(item1[m])
    for item in item2:
        if item == "1":
            noOnes += 1
        elif item == "0":
            noOnes = 0
        if noOnes > 7-weeklyresting:
            appendflag = False
    return appendflag

def idCombos(matrix,shifttype,shifts,shiftlengths,weeklyresting,dailyresting):
    zeroOneS = []
    for m in range(len(matrix[0])):
        if matrix[0][m] == "-":
            zeroOneS.append(0)
        else:
            zeroOneS.append(1)
    dailyresting = 11
    noofcombinations = int(float(shifttype)**float(sum(zeroOneS)))
    print(noofcombinations)
    # if noofcombinations > 10**9:
    #     msgbox = QMessageBox()
    #     msgbox.setWindowTitle("Select how to proceed")
    #     memoryNeeded = noofcombinations*sum(zeroOneS)
    #     if memoryNeeded < 10**12:
    #         memoryNeeded = str(memoryNeeded/(10**9)) + " Gb"
    #     else:
    #         memoryNeeded = str(memoryCalc/(10**12)) + " Tb"
    #     msgbox.setText("Combinations to go through: "+str(noofcombinations)+".\nThis means up to "+memoryNeeded+" may be required in memory mode.\n\n     : Select which method to proceed with : \n\nInternal Memory mode may require substantial amount of memories.\n\nProcessing Mode requires less far less internal memory but more processing power (and is usually slower).")
    #     memBtn = msgbox.addButton("Memory Mode",QMessageBox.ResetRole)
    #     procBtn = msgbox.addButton("Processor Mode",QMessageBox.ApplyRole)
    #     cancelBtn = msgbox.addButton("Cancel",QMessageBox.NoRole)
    #     msgbox.exec_()
    #     if msgbox.clickedButton() == memBtn:
    #         proceed = 1
    #         mode = "proc"
    #     elif msgbox.clickedButton() == procBtn:
    #         proceed = 1
    #         mode = "mem"
    #     else:
    #         proceed = 0
    #         mode = ""
    # else:
    proceed = 1
    mode = "mem"
    if proceed == 1:
        t0 = time()
        if mode == "proc":
            arrays = [[shifts[0]] * sum(zeroOneS)]
            solutionMatrices = recursiveCartesianProduct(sum(zeroOneS),shifts,arrays,arrays[0],1,1,zeroOneS)
            if checkifshiftsOK(solutionMatrices[0],dailyresting,shiftlengths,shifttype,weeklyresting) == False:
                del solutionMatrices[0]
        elif mode == "mem":
            solutionMatrices = list(createSolutionMatrices(sum(zeroOneS),shifts,zeroOneS))
        t1  = time()
        if mode == "proc" or mode == "mem":
            print("Solutions found: "+str(int(len(solutionMatrices))))
            print("Time for completion: "+str(float("{:.6f}".format(t1-t0)))+" s")

    return solutionMatrices

from time import time
import numpy

filename = "2shifts3w"

contents = open(filename+".combo", "r").read()
matrices = contents.split("\n")
shifttype = 2 # 1-shift, 2-shift, 3-shift  = 1,2,3 (resp.)
shiftlengths = 8 # hours
shifts = [1,2]
dailyresting = 11
weeklyresting = 36 # continous weeklys resting time in hours

solutionMatrices = idCombos(matrices[0],shifttype,shifts,shiftlengths,weeklyresting,dailyresting)
