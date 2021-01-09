---
title: 'Computer-Aided Generation of N-shift RWS'
tags:
  - Python
  - Workforce scheduling
  - Shift
  - Two-shift
  - Three-shift
  - Rotating Shift Work
  - Rotational Workforce
  - Scheduling
  - Schedules
authors:
  - name: Benjamin Edward Bolling
    orcid: 0000-0002-6650-5365
    affiliation: "1, 2"
date: 10 January 2020
affiliations:
 - name: European Spallation Source ERIC
   index: 1
 - name: MAX IV Laboratory
   index: 2
bibliography: paper.bib
---

# Summary
A Computational Approach to Generate Multi-Shift Rotational Workforce Schedules.

# Abstract
Generating schedules for shift workers is essential for many employers, whether the employer is a small or a large industrial complex, research laboratory, or other businesses involving shift works.

Previous methods for creating rotational workforce schedules included interactions between the schedule maker and the algorithm, including defining the length of sequences of consecutive days of working shifts.

In this project, an algorithm takes into account inputs (or constraints) from the schedule maker and then presents the possible solutions (incl. that all shifts must be filled, working hours per week, minimal resting time, etc.) in a first phase. The schedule maker can then select which solutions are most feasible to proceed with in the second phase, where the final schedules are then constructed and exported.

# Introduction
Creating shift work schedules has always been a challenging task, especially such that are equal for all workers and at the same time distributes the shifts evenly and properly to prevent staff burnout. In order to achieve schedules for the workers that treats everyone equally, the focus will be on so-called rotational workforce schedules (RWS:s). Rotational workforce schedules means that the schedule rotates after time, and hence, the other option would be static shift schedules. In this project, the term 'shift arrays' is defined to represent all possible schedules following a list of constraints.

# Computational Approach and Results
In this approach, each worker has the same schedule but shifted by one week resulting in that all workers follow the same schedule. The project has been divided into two phases, *Boolean Shift Arrays* (in which boolean shift arrays are generated) and *From Boolean Shift Arrays to a RWS* (in which a selected boolean shift array is shaped into its final RWS layout).

## Boolean Shift Arrays (phase 1)
A boolean shift array is defined such that 1 means that the worker is working and 0 that the worker is not. Then the constraints imposed are:
| Column 1       | Column 2     |
| :------------- | :----------: |
| n_wd | number of working days per week   |
| n_W | number of weeks to cycle over      |


For simplicity, we begin by using boolean shift arrays with 1 meaning that the person works and 0 meaning that the person does not work. In order to impose some constraints on the shift arrays, we define the  as $n_{wd}$ and  as $n_W$. This results in a shift array of length $7n_W$. For constructing the different combinations of the boolean array, we use Algorithm~\ref{algorithm1}.




Since each week also resembles a worker, the shift array can be set up as a matrix with 7 columns, each representing the days of a week. The columns can then be summed to achieve the shift occupancy (or how many people are working each shift). Thus, the algorithm only allows shift arrays to pass for which all shifts are occupied by at least one worker, with a shift represented by the first $n_{wd}$ days for each week. In order to extend to not only use single shifts but also 2- or 3-shifts, a simple logical reasoning was added into the algorithm. For $N$ shifts per day, each day has to be filled with at least $N$ workers.

The next input that the algorithm needs is the shift lengths and the weekly working hours per worker, defined as $t_s$ and $t_W$, respectively. However, in order to generate "good schedules", an additional constraint will be needed in order to avoid all working days being clustered together.

\begin{figure}[h]
  \centering\includegraphics[width=0.9\columnwidth]{fig1.png}
\caption{The RWS:ing Application's algorithm's "phase 1 GUI" (dark and light themes, left and right, respectively). In the left figure, the combinations have been generated. In the right figure, the combinations have been loaded from a file.}
\label{fig:figure1}
\end{figure}

Hence, the constraint for weekly minimum single continuous resting time is added, defined as $t_r$. The algorithm ensures that all passed shift arrays have at least this many hours of free-time for each week. The number of shifts $n_S$ per shift array is calculated by
\[
n_S = \mathrm{ceil}\left(\frac{t_W}{t_s}\right).
\]
The reason for using ceiling function and not the floor function is simply the argument that it is better with a couple of more hours than fewer. In order to cluster days off ($n_cf$), the algorithm's GUI has an optional additional constraint that serves this purpose and simply does not allow shift arrays with 0:s in clusters less than this through.

By using the input $n_Wn_{wd}$ as an iterable and $n_S$ as the length of subsequences of elements from the iterable, we use the same methodology as \textit{itertools} \cite{Itertools} module in Python to create each shift array. The other inputs are used as constraints on whether the shift array should be appended to the array of shift arrays or trashed. The reasoning for not using the built-in module itertools.combinations \cite{Itertools} is that it returns all array combinations it could find. Without the constraints, the returned arrays become too large for a normal up-to-date computer's internal memory to handle.

With this, the final result is an array of shift arrays in which each shift array is filled with $7n_S$ 1:s and $n_W(7-n_S)$ 0:s whilst obeying the above mentioned constraints. The number of possible combinations $C$ using Algorithm~\ref{algorithm1} can be expressed as:
\begin{equation}
    C = \frac{(n_Wn_{wd})!}{n_S! (n_Wn_{wd}-n_S)!}.
\end{equation}

\begin{table}[h]
\centering
\caption{Parameters selected for the generation of a N-shift RWS.}
\label{tab:table1}
\begin{tabular}{| cccccccc |}
\hline\noalign{\smallskip}
$N$ & $n_{wd}$ & $n_W$ & $t_S$ & $t_W$ & $t_r$ & $n_cf$ & Shift types' labels\\
\noalign{\smallskip}
\hline\noalign{\smallskip}
2 & 7 & 4 & 8.33 & 36.00 & 36 & 2 & D, E\\
\noalign{\smallskip}
\hline
\end{tabular}
\end{table}

The parameters selected for the RWS is defined in Table~\ref{tab:table1}. These values are then reflected in the algorithm's GUI for phase 1 can be seen in Figure~\ref{fig:figure1} to the left. Note that the generated shift arrays can be browsed through using the slider or the numerical input field and that the shift arrays are constructed such that each week or worker (depending on the viewing angle) is represented in separate rows.

## From Boolean Shift Arrays to RWS (phase 2)
\begin{figure}[h]
  \centering\includegraphics[width=0.98\columnwidth]{fig2.png}
\caption{The RWS:ing Application's algorithm's "phase 2 GUI" as launched from the "phase 1 GUI" and with the second Thursday's shift changed to an evening shift (left) and after finding solutions, showing the first solution (right).}
\label{fig:figure2}
\end{figure}
In this phase, we have generated a new list of combinations with free days clustered in pairs, and then we chose to proceed with combination \#212 since it has two out of four weekends off (note the zeroes in the bottom table in Figure~\ref{fig:figure1} to the right). By proceeding, the "phase 2 GUI" is launched with the selected array as input as can be seen in Figure~\ref{fig:figure2} to the left.

The free days are all represented by zeroes whilst all other shifts (ones) are converted to the first defined shift type label. For $N>1$, each shift can be replaced by another shift via dropdown menus. The GUI shows the number of shifts of each type each week or worker has and a table with the results, i.e. number of worker per shift and day. Shifts that are occupied have green background whilst shifts that are unoccupied have a red background.

If the continuous resting time between two assigned shifts is too low, the background colour of the second shift becomes red (e.g. a Friday day-shift after a Thursday evening-shift if the continuous resting time has to be at least 11 hours, as shown in Figure~\ref{fig:figure2} to the left). With enough resting time in between shifts, the background of the second shift is be green.

Pressing the \textit{Find solutions} results in what is shown in Figure~\ref{fig:figure2} (right figure). A schedule can also be constructed completely by hand, but note that the algorithm will find all possible combinations. The algorithm is a simple Cartesian Product calculator, in which each set is a list of shifts (1 = Day, 2 = Evening, etc.) with one set per working day:
\[
\mathrm{combinations} =
\underbrace{
\begin{pmatrix} 1 \\ 2 \\ \vdots\end{pmatrix}
\times
\begin{pmatrix} 1 \\ 2 \\ \vdots\end{pmatrix}
\times ... \times
\begin{pmatrix} 1 \\ 2 \\ \vdots\end{pmatrix}
}
_{n_{wd}} =
\begin{cases}
  [11\cdot\cdot\cdot1]\\
  [11\cdot\cdot\cdot2]\\
  \vdots\\
  [22\cdot\cdot\cdot1]\\
  [22\underbrace{\cdot\cdot\cdot}_{n_{wd}}2]
\end{cases}
\]
where each array in the resulting product is considered as a possible shift schedule matrix. Imposing constraints (resting time between shifts and ensuring all shifts are filled) on each combinations results in solutions from which the user can choose between.

Since all combinations are stored in a matrix form before different combinations are removed from the final solutions matrix, large datasets require severe amount of internal memory for the Cartesian Product method to work. For this, a controlling script has been implemented which calculates a pre-estimate of required internal memory. The required internal memory for different operations can be roughly calculated by
\[
\mathrm{IM} \approx N_{C}n_{wd} = N^{n_{wd}}n_{wd},
\]
returning the memory demand $\mathrm{IM}$ in bytes and where $N_C = N^{n_{wd}}$ is the total number of combinations (without any constraints imposed).

If the estimated expected internal memory requirement for an operation exceeds 1Gb, the user is prompted whether to continue with the default Cartesian Product method or to use a less internal memory demanding recursive method. The recursive method can be simplified as shown in Algorithm~\ref{algorithm2}.

\begin{algorithm}[H]
\SetAlgoLined
def recursiveCaPr(N,shifts,arrays,array,level):
    \For{m in range(1,len(shifts))}{
        \For{n in range(level-1,N)}{
            \If{array[n] != shifts[m]}{
                array2 = array.copy()
                array2[n] = shifts[m]
                matrixOut = insertFreeDaysInSolutionMatrix(array2)
                \If{matrixOut not in arrays}{
                    \If{checkifshiftsOK(matrixOut) is True}{
                        arrays.append(matrixOut)
                    }
                    \If{level < N:}{
                        arrays = recursiveCaPr(N,shifts,arrays,array2,level+1)
                    }
                }
            }
        }
    }
    return arrays
arrays = [[shifts[0]] * N]
solutions = recursiveCaPr(N,shifts,arrays,arrays[0],level)
\caption{Finding solutions to a Cartesian Product of length N using a recursive function.}
\label{algorithm2}
\end{algorithm}



# Benchmarking results
\subsection{Benchmarking Computer Specifications}
The algorithm benchmarking was done on an Apple MacBook Pro with the specifications as defined in Table~\ref{tab:computerSpecs}.
\begin{table}[h]
\centering
\caption{Benchmarking computer specifications.}
\label{tab:computerSpecs}
\begin{tabular}{| r l |}
\hline\noalign{\smallskip}
Computer type: & Apple MacBook Pro (13-inch, 2019)\\
OS: & macOS Mojave v. 10.14.6\\
Processor: &  2.8 GHz Intel Core i7 processor\\
Internal Memory: & 16 GB 2133 MHz LPDDR3\\
Graphics Card: &  Intel Iris Plus Graphics 655 1536 MB\\
\noalign{\smallskip}
\hline
\end{tabular}
\end{table}

## Phase 1 - Construction of  Combinations as Boolean Arrays
In the GUI, there is a "fast generation" checkbox which stops the algorithm from further calculations once the first 100 solutions have been found. This way, computation time can be lowered (in comparison to "full generation" which will go through all possible solutions from the boolean array). For our example, the time it took to complete decreased from 508.7 s (for a full generation) to 24.55 s (for the full generation) (see Table~\ref{tab:fullBenchmarking}), which is a decrease in time by 95\%.

We use the parameters defined in Table~\ref{tab:table1}, with the exception of $N$ and Shift types' labels. Note that for Table~\ref{tab:fullBenchmarking} and Table~\ref{tab:fullCombos}, the number (\#) of weeks given is the minimum amount of weeks required for a full shift cycle in order to find solutions for the N-shift problems (with $N = 1,2,3$ for single-, two- and three-shifts, respectively). The free days clustering option is not selected for the benchmarking.

\begin{table}[h]
\centering
\caption{Benchmarking for fast and full generation of the Boolean Arrays (as defined in Section 3.1 for Phase 1).}
\label{tab:fullBenchmarking}
\begin{tabular}{| r | c | r r |}
\hline\noalign{\smallskip}
Type: & \# of weeks: & Time (fast) [s]: & Time (full) [s]:\\
\noalign{\smallskip}
\hline\noalign{\smallskip}
Single-shift, 5 days/week   & 1 & 7.224e-05 & 7.224e-05\\
Single-shift, 7 days/week   & 2 & 1.497e-02 & 5.211e-02\\
Two-shift, 7 days/week      & 4 & 24.55 & 508.7\\
Three-shift, 7 days/week    & 5 & 3 087 & 6.627e+04\\
\noalign{\smallskip}
\hline
\end{tabular}
\end{table}

\begin{table}[h]
\centering
\caption{Number of combinations and solutions found for full generations of the Boolean Arrays (as defined in Section 3.1 for Phase 1).}
\label{tab:fullCombos}
\begin{tabular}{| r | c | r r |}
\hline\noalign{\smallskip}
Type: & \# of weeks: & Combinations: & Solutions:\\
\noalign{\smallskip}
\hline\noalign{\smallskip}
Single-shift, 5 days/week   & 1 & 1 & 1\\
Single-shift, 7 days/week   & 2 & 2 002 & 462\\
Two-shift, 7 days/week      & 4 & 13 123 110 & 1 668 226\\
Three-shift, 7 days/week    & 5 & 1 476 337 800 & 11 383 225\\
\noalign{\smallskip}
\hline
\end{tabular}
\end{table}

Plotting the benchmarking results, we find the logarithmic graph given in Figure~\ref{fig:figure4}. As can be seen, the computation time $T_C$ increases exponentially with the number of weeks in a shift cycle on average in accordance with
\[
T_C(full) = \exp(5.046\times n_W)\times9\times10^{-7}
\]
and
\[
T_C(fast) = \exp(4.254\times n_W)\times2\times10^{-6}
\]
for the full and fast generations on, respectively.

\begin{figure}[h]
  \centering\includegraphics[width=0.94\columnwidth]{fig4.png}
\caption{The benchmarking results in respect of time for fast- and full generation of the boolean arrays (on the left vertical axis), and the number of combinations gone through and the solutions found (on the right vertical axis).}
\label{fig:figure4}
\end{figure}

## Phase 2 - Finding Solutions for a given Combination
If the given combination has only a single shift specie, there is one solution for the given combination. If there are more than one shift specie, multiple solutions may be found. The main impact on time consumption is the number of combinations $N_C$. Limiting factors are not limited to time only but also on the internal memory due to that a Cartesian Product method is used, meaning all combinations are stored as list objects. Some values have been timed and calculated in Table~\ref{tab:phase2} using the Cartesian Product method.

\begin{table}[h]
\centering
\caption{Benchmarking for Phase 2: Time and estimated internal memory (IM) required for obtaining all combinations and solutions for different $n_{wd}$ and $N$ using the Cartesian Product method.}
\label{tab:phase2}
\begin{tabular}{| r | c c | r r | r r |}
\hline\noalign{\smallskip}
Type ($N$): & $n_{wd}$: & $n_{W}$: & Combinations: & Solutions: & IM: & Time [s]:\\
\noalign{\smallskip}
\hline\noalign{\smallskip}
2-shift & 14    & 3 & 16 384 & 7 & 229.38 kB & 0.2963\\
2-shift & 18    & 4 & 262 144 & 64 & 4.7186 MB & 5.843\\
3-shift & 14    & 3 & 4 782 969 & 0 & 66.96 MB & 92.54\\
3-shift & 18    & 4 & 387 420 489 & - & 6.9736 GB & -\\
\noalign{\smallskip}
\hline
\end{tabular}
\end{table}

# Conclusions
In this article, we have demonstrated that the constructed algorithm can generate schedules for different number of weeks to cycle over. The current issue is that the computational complexity (and hence the computation time) increases with the number of weeks, as can be seen in Table~\ref{tab:fullCombos} and Figure~\ref{fig:figure4}. This means that for a higher amount of weeks in a shift cycle, this application will need development in order to have more efficient ways of finding the solutions and/or deployment of the application onto super-computers for generating the Boolean Arrays.

For up to 5 weeks in a shift cycle it is possible to use a general-purpose computer such as the benchmarking Apple MacBook Pro with specifications defined in Table~\ref{tab:computerSpecs}.
It has thus been demonstrated that the application can be used to generate 1, 2 and 3-shift schedules. Future development plans include adding an automated assignment function of shift types in phase 2, which would further strengthen the usability of this application.
