
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		Description for the algorithm

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Author: Benjamin Bolling
2020-06-08 - 2020-07-02

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Phase 1.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

First we set up the empty tables by defining shift cycle length (number of weeks) and the number of working days each week.

Next we define the number of people to populate the shifts with and shift types (1-, 2-, 3-shifts). These definitions are used to construct all possible shift table combinations.

Then the constraints are set up:
- number of people per shift
- shift lengths
- number of working hours per person per week (on average)
- minimum daily resting hours between each shift
- minimum single continuous resting hours per week

Then the algorithm first constructs an empty shift series, followed by a container for all shift combinations.

The issue now is that for e.g. a 2-shift with 7 days to populate/choose from and 5 weeks, a single person would have a 5.003E16 possible combinations and hence consume enormous amount of computer power to setup each one as shift series. As it is not feasible to construct all possible combinations and remove all that do not fulfil the constraints, a different approach is needed. We will begin by creating a sample array which is populated with all shifts, followed by the free days. 

Example: 
Number of weeks to cycle over = 2, Shifts per person per cycle = 9, Shift type = 1-shift.

[ 1 1 1 1 1 1 1 1 1 0 0 0 0 0 ]

This series is then manipulated such that the total number of shifts per person per cycle is constant. The combination generating algorithm will be focusing on the free days and working days by swapping them in all possible combinations for the series with only 1:s and 0:s resembling shift or no shift, respectively.

We do not want all combinations, however. We want to first ensure that for each week, for the number of working days, we want all shifts to be occupied. This is accomplished by summing the number of shifts for each day over all the weeks and days in the combination and ensuring that this sum is larger than or equal to the number of shifts that day. This will then pass the combination further for more constraints testing, otherwise discard of it and look at next combination (until no combinations remain).

The next check is the constraint for continuous weekly resting time. E.g. the series above is not accepted since it has 9 shifts in a row. It would accept e.g. 

[ 0 0 1 1 0 1 1 1 1 0 0 1 1 1 ]

as a 2-week-cycle single-shift 7-workday-weeks combination.

More shifts per week requires more weeks and workers, as each week in this method corresponds to each worker with identical schedules each shifted by one week.

The user is then presented with all the possible combinations with a slider and a spin-box to select a combination and the option to proceed to phase 2. Note that multiple phase 2:s can be launched and worked on at the same time.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Phase 2.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

In this phase, the combination is imported from phase 1 into a table and the 1:s (the shift-days) are converted to the first shift-type defined in phase 1 (for 3-shift, the pre-defined is D-, E- and N-shifts, short notations for Day, Evening and Night, respectively, but these can be edited by the user). Each shift-day gets their own dropdown menu where the user can change the shift into other shift(s) defined in phase 1 (for 2- or 3-shifts). The results table on the bottom aids the user in keeping track on how each shift type is populated.







