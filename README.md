# RSW Algo README
A Computational Approach to Generate Multi-Shift Rotational Workforce Schedules.

##Installation procedure

## Example Usage Procedure
We again use the parameters defined in Table~\ref{tab:table1} and then select to cluster the free days in pairs. The boolean combinations selected in phase 1 for phase 2 are \#212 and \#43. In phase 2, the solutions selected are \#0 and \#43 for the boolean combinations \#212 and \#43, respectively. These solutions were then exported as .CSV files, imported into a new spreadsheet in Microsoft~Excel~(2018) followed by adding colours to highlight and differentiate each week as well as lines for all rows and columns. The sum of each shift specie per day has also been calculated in the spreadsheet (using the COUNTIF(cells;shift) formula of Microsoft~Excel~(2018)), see Figure~\ref{fig:figure3}.

Thus it can be concluded that in this example procedure two different 4-week (or 4-people) rotational workforce schedules were generated and then combined together. In the first schedule (persons 0-3, Figure~\ref{fig:figure3}), each staff has two "normal office-hours" weeks with the weekends off, followed by two weeks with weekends working. The second schedule (persons 4-7, Figure~\ref{fig:figure3}) has more evening and weekend shifts, which can be considered as more suited for e.g. students or people working some extra hours. These two schedules have then been combined in order to obtain an a rotational workforce schedule filled as evenly as possible with the exception of Fridays. Fridays have been selected such that all shift workers are scheduled to work, suitable for e.g. activities when \textit{all hands on deck} is required. This schedule has also ensured that each shift is occupied by a minimum of two shift workers.

\begin{figure}[h]
  \centering\includegraphics[width=\columnwidth]{fig3.png}
\caption{Example procedure results. Phase 1 was performed using the parameters defined in Table~\ref{tab:table1} and with free days clustered in pairs. Two boolean combinations were selected, followed by finding and selecting a solution for both, and then exported as CSV and imported in Microsoft~Excel~(2018).}
\label{fig:figure3}
\end{figure}
