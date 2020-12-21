# item1 = [1,1,1,1,0,2,2,2,0,0,1,1,1,1,0,2,2,2,2,0,0,1,1,1,1,1,0,0,1,1,1,1,1,0,0]
#
# shiftlengths = 8 # hours
# weeklyresting = 36 # hours
# shiftstarts = 24/3

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
print(appendflag)
