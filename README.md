# RSW Algo README
A Computational Approach to Generate Multi-Shift Rotational Workforce Schedules.

##Installation procedure
Step-by-step ...

## Example Usage Procedure
Table 1: Constraints, i.e. the variables and their meanings, and some example values.

| Variable       | Meaning     | Value |
| :------------- | :----------: | :----------: |
| *N* | number of shifts per days            | 2 |
| *n<sub>cf</sub>* | number of days off clustered      | 2 |
| *n<sub>S</sub>* | number of shifts per shift cycle      | 2 |
| *n<sub>W</sub>* | number of weeks to cycle over      | 4 |
| *n<sub>wd</sub>* | number of working days per week   | 7 |
| *t<sub>r</sub>* | weekly minimum single continuous resting time | 36 |
| *t<sub>s</sub>* | shift lengths                      | 8.33 |
| *t<sub>W</sub>* | weekly working hours per worker    | 36.00 |

The parameters selected for the RWS is defined in Table 1. These values are then reflected in the algorithm's GUI for phase 1 can be seen in Figure 1 to the left. Note that the generated shift arrays can be browsed through using the slider or the numerical input field and that the shift arrays are constructed such that each week or worker (depending on the viewing angle) is represented in separate rows.
We again use the parameters defined in Table 1 and then select to cluster the free days in pairs. The boolean combinations selected in phase 1 for phase 2 are \#212 and \#43. In phase 2, the solutions selected are \#0 and \#43 for the boolean combinations \#212 and \#43, respectively. These solutions were then exported as .CSV files, imported into a new spreadsheet in Microsoft Excel (2018) followed by adding colours to highlight and differentiate each week as well as lines for all rows and columns. The sum of each shift specie per day has also been calculated in the spreadsheet (using the COUNTIF(cells;shift) formula of Microsoft Excel (2018)), see Figure 3.

Thus it can be concluded that in this example procedure two different 4-week (or 4-people) rotational workforce schedules were generated and then combined together. In the first schedule (persons 0-3, Figure 3), each staff has two "normal office-hours" weeks with the weekends off, followed by two weeks with weekends working. The second schedule (persons 4-7, Figure 3) has more evening and weekend shifts, which can be considered as more suited for e.g. students or people working some extra hours. These two schedules have then been combined in order to obtain an a rotational workforce schedule filled as evenly as possible with the exception of Fridays. Fridays have been selected such that all shift workers are scheduled to work, suitable for e.g. activities when \textit{all hands on deck} is required. This schedule has also ensured that each shift is occupied by a minimum of two shift workers.

\begin{figure}[h]
  \centering\includegraphics[width=\columnwidth]{fig3.png}
\caption{Example procedure results. Phase 1 was performed using the parameters defined in Table 1 and with free days clustered in pairs. Two boolean combinations were selected, followed by finding and selecting a solution for both, and then exported as CSV and imported in Microsoft Excel (2018).}
\label{fig:figure3}
\end{figure}

# Phase 2
By proceeding with a selected combination, the "phase 2 GUI" is launched with the selected combination as input (which can be seen in Figure 2 to the left).

The free days are all represented by zeroes whilst all other shifts (ones) are converted to the first defined shift type label. For $N>1$, each shift can be replaced by another shift via dropdown menus. The GUI shows the number of shifts of each type per week and a table with the results, i.e. the number of workers per shift and day. Shifts that are occupied have green background whilst shifts that are unoccupied have a red background.

If the continuous resting time between two assigned shifts is too low, the background colour of the second shift becomes red (e.g. a Friday day-shift after a Thursday evening-shift if the continuous resting time has to be at least 11 hours, as shown in Figure 2 to the left). With enough resting time in between shifts, the background of the second shift is be green.

# Figures
![Figure 1](docs/fig1.png)
Figure 1: The RWS:ing Application's algorithm's "phase 1 GUI" (dark and light themes, left and right, respectively). In the left figure, the combinations have been generated. In the right figure, the combinations have been loaded from a file.

![Figure 2](docs/fig2.png)
Figure 2: The RWS:ing Application's algorithm's "phase 2 GUI" as launched from the "phase 1 GUI" and with the second Thursday's shift changed to an evening shift (left) and after finding solutions, showing the first solution (right).

![Figure 3](docs/fig3.png)
Figure 3: Example procedure results. Phase 1 was performed using the parameters defined in Table 1 and with free days clustered in pairs. Two boolean combinations were selected, followed by finding and selecting a solution for both, and then exported as CSV and imported in Microsoft Excel (2018).
