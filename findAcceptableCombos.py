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

# A simple method to check if a list of combinations in a .combo file has real
# solutions based on the parameters defined below
filename = "x"
shifttype = 2 # 1-shift, 2-shift, 3-shift  = 1,2,3 (resp.)
shiftlengths = 8 # hours
shifts = [1,2]
dailyresting = 11
weeklyresting = 36 # continous weeklys resting time in hours

import IO
contents = open(filename+".combo", "r").read()
raw_matrices = contents.split("\n")
matrices = []
for raw_matrix in raw_matrices:
    matrix = []
    raw_values = raw_matrix.split(" ")
    for raw_value in raw_values:
        if len(raw_value) > 0:
            matrix.append(int(raw_value))
    if len(matrix) > 0:
        matrices.append(matrix)
for n in range(10):
    solutionMatrices = IO.idCombos(matrices[n],shifttype,shifts,shiftlengths,weeklyresting,dailyresting)
    print(len(solutionMatrices))
