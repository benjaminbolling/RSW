# RSW test procedure
A manual testing procedure for the RSW package.

## Test preparation: Create and activate the testing environment
1. Execute `conda env create --file environments.yml` to create the environment.
2. Execute `conda activate rsw` to activate the environment.

## Test 1: Phase 1
1. Execute `python RSW.py` in the same terminal as from *Test preparation*.
2. Select *New* to launch Phase 1.
3. Fill in the Phase 1 window with the following values:
| Parameter     | Value |
| :----------: | :----------: |
| Shift type:            | 2-shift |
| Shift labels:            | D, E |
| Working days per week:   | 7 |
| Number of weeks to cycle over:      | 4 |
| Shift occupancy:                      | 1 |
| Shift lengths:                      | 8.33 |
| Weekly working hours per person:    | 36.00 |
| Weekly minimum single continuous resting time: | 36 |
| Minimum continuous daily resting time:  | 11 |
| Cluster free days?      | Ticked, value: 2 |
4. Press *Generate Combinations*.
5. When completed, a prompt window will ask user to save all combinations. Press yes.
6. Name the file *test01* and click save, it will automatically save the file in a *.combos*-format.
7. Close the window.
8. Execute `python RSW.py` in the same terminal as in *Test preparation*.
9. Select *Load Combos* to launch Phase 1 with a saved combinations file.
10. Select *test01.combos* and press load.
The test is a success if the file could load without any issues.

## Test 2: Phase 2 from Phase 1
1. Execute `python RSW.py` in the same terminal as from *Test preparation*.
2. Select *New* to launch Phase 1.
3. Fill in the Phase 1 window with the following values:

| Parameter     | Value |
| :----------: | :----------: |
| Shift type:            | 2-shift |
| Shift labels:            | D, E |
| Working days per week:   | 7 |
| Number of weeks to cycle over:      | 3 |
| Shift occupancy:                      | 1 |
| Shift lengths:                      | 8.00 |
| Weekly working hours per person:    | 36.00 |
| Weekly minimum single continuous resting time: | 36 |
| Minimum continuous daily resting time:  | 11 |
| Cluster free days?      | Unticked |

4. Press *Generate Combinations*.
5. When completed, a prompt window will ask user to save all combinations. Press no.
6. Using the slider and/or the spinner in the *Post table generation schedule work* section, browse to combination with index 392.
7. Press *Proceed with this combo to next phase*.
8. In the Phase 2 window, press the bottom button *Save*.
9. Name the file *test02*, and it will save the solution in the file format *.sol*.
10. Press the button *Export*, name the file *test02* and press *Save*.
11. Select the file format *ODS*.
The test is a success if the ODS file can be loaded with all values from a Spreadsheet application that supports the *.ODS* file format.

## Test 3: Phase 2 - loading a solution and finding solutions
1. Execute `python RSW.py` in the same terminal as from *Test preparation*.
2. Select *Solve Combo* and select *test02.sol*, and click *Open*.
3. Click on the *Check Weekly Rest* button. It should become green.
4. Select one of the green *D*-s that have another *D* directly afterwards and change it to *E*. The *D* directly afterwards should become red.
5. Click on the button *Find Solutions*. For this combination, only 1 solution will exist.
6. Click on the Export button, name the file *test03* and press *Save*.
7. Select the file format *CSV*.
The test is a success if the CSV-file can be opened with any editor and its values matching the values in the Phase 2 application.
