## Benchmarking results
### Benchmarking Computer Specifications
The algorithm benchmarking was done on an Apple MacBook Pro with the specifications defined in Table 2.

Table 1: Benchmarking computer specifications.

| Definition     | Value        |
| :------------- | :----------: |
| Computer type: | Apple MacBook Pro (13-inch, 2019) |
| OS: | macOS Mojave v. 10.14.6 |
| Processor: |  2.8 GHz Intel Core i7 processor |
| Internal Memory: | 16 GB 2133 MHz LPDDR3 |
| Graphics Card: |  Intel Iris Plus Graphics 655 1536 MB |

### Benchmarking Phase 1
In the GUI, there is a "fast generation" checkbox which stops the algorithm from further calculations once the first 100 approved combinations have been found. This way, computation time can be lowered (in comparison to "full generation" which will go through all possible combinations from the boolean array). For the parameters defined in Table 1, the time it took to complete decreased from 508.7 s to 24.55 s for the full generation (see Table 3), which is a decrease in time by 95\%.

The parameters used are defined in Table 1, with the exception of $N$ and Shift types' labels. Note that for Table 3, the number (\#) of weeks given is the minimum amount of weeks required for a full shift cycle in order to find acceptable combinations for the N-shift problems (with $N = 1,2,3$ for single-, two- and three-shifts, respectively). The free days clustering option is not selected for the benchmarking.

Table 2: Benchmarking for fast and full generation of the Boolean Arrays (as defined in Section 3.1 for Phase 1), and the number of combinations and approved combinations found for full generations of the Boolean Arrays (as defined in Table 1). The types are single-, two- or three-shifts during 5 or 7 days per week, and the internal memory (IM) is given for the different shift array objects.

| Type: | 1-shift, 5d/w | 1-shift, 7d/w | 2-shift, 7d/w | 3-shift, 7d/w   |
| :------------- | :----------: | :----------: | :----------: | :----------: |
| \# of weeks: | 1 | 2 | 4 | 5 |
| Combinations (total): | 1 | 2 002 | 1.312e+07 | 1.476e+09 |
| Combinations (accepted): | 1 | 462 | 1.668e+06 | 1.138e+07 |
| IM: | 88 B | 4.216 kB | 13.53 MB | 100.4 MB |
| Time (fast) [s]: | 7.224e-05 | 1.497e-02 | 24.55 | 3 087 |
| Time (full) [s]: | 7.224e-05 | 5.211e-02 | 508.7 | 6.627e+04 |

Plotting the benchmarking results yields the logarithmic graph in \autoref{fig:benchmarking}. As can be seen, the computation time $T_{C}$ increases exponentially with the number of weeks in a shift cycle on average in accordance with
\begin{equation}
T_C \text{(full)} = \exp{\{5.046 \times n_W\}} \times 9 \times 10^{-7}
\end{equation}
and
\begin{equation}
T_C \text{(fast)} = \exp{\{4.254 \times n_W\}} \times 2  \times 10^{-6}
\end{equation}
for the full and fast generations, respectively, calculated with an exponential regression.

### Benchmarking Phase 2
If the given combination has only a single shift specie, there is one solution for the given combination. If there are more than one shift specie, multiple solutions may be found. The main impact on time consumption is the number of accepted combinations $N_{C}$. Limiting factors are not limited to time only but also on the internal memory due to that a Cartesian Product method is used, meaning all combinations are stored as string objects in an array. Some values have been timed and calculated in Table 4 using the Cartesian Product method.

Table 3: Benchmarking for Phase 2: Time required for obtaining all solutions for different $n_{S}$, $n_{W}$ and $N$ using the Cartesian Product method, and the internal memory (IM).

| Type ($N$): | 2-shift | 2-shift | 2-shift |
| :------------- | :----------: | :----------: | :----------: |
| $n_{W}$: | 3 | 4 | 4 |
| $n_{S}$: |14 | 18 | 20 |
| Solutions (for each combination): | 16 384 | 262 144 | 1 048 576 |
| Time [s]: | 0.2963 |  5.843 | 12.72 |

Note: The number of solutions for each combination in Table 4 is the total number of combinations for the solution matrix (and not the number of viable solutions).

![The benchmarking results in respect of time for fast- and full generation of the boolean arrays (on the left vertical axis), and the number of combinations gone through and the solutions found (on the right vertical axis), for different number of weeks in a shift cycle (see Table 3).\label{fig:benchmarking}](docs/fig4.png){ width=80% }
