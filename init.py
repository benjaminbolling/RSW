# Initialization of the values
def init_values():
    shifttype = 1              # 1-shift or 2-shift or 3-shift, 1, 2, 3, resp.
    workingdays = 7            # Amount of days per week
    noofweeks = 2              # Amount of weeks to cycle over
    shiftlengths = 8.33        # Length of shifts in hours
    workinghours = 36          # Amount of working hours per person each week
    weeklyresting = 36         # Length of weekly minimum single continuous resting time in hours
    overwrite = 0              # In order to avoid re-running the algorithm unnecessarily
    shiftLabel1 = "D"          # Define how this shift is to be labelled in the next phase
    shiftLabel2 = "E"          # Define how this shift is to be labelled in the next phase
    shiftLabel3 = "N"          # Define how this shift is to be labelled in the next phase
    fastGen = False            # Finish algorithm after the first 100 combos
    clusterFreeDays = False    # Free days have to be clustered
    freeDaysClusterValue = 2   # Free days clustering value
    noOfPeople = 1           # Minimum number of people per shift
    return shifttype,workingdays,noofweeks,shiftlengths,workinghours,weeklyresting,overwrite,shiftLabel1,shiftLabel2,shiftLabel3,fastGen,clusterFreeDays,freeDaysClusterValue,noOfPeople
