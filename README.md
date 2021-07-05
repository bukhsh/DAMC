# Day-ahead Market Clearing
This tool simulates market clearing based on the following two policies of modelling transmission constraints:

* Available Transfer Capacity (ATC)
* Flow Based Market Clearing (FBMC) 

Please refer to the following publications to learn more about the aforementioned policies:

[1] Kenneth Van den Bergh, Jonas Boury, Erik Delarue, The Flow-Based Market Coupling in Central Western Europe: Concepts and definitions, The Electricity Journal, Volume 29, Issue 1, 2016. (<a href="https://www.sciencedirect.com/science/article/abs/pii/S104061901530004X">Link</a>)


[2] Felten, Björn; Felling, Tim; Osinski, Paul; Weber, Christoph (2019) : FlowBased Market Coupling Revised - Part I: Analyses of Small- and Large-Scale Systems, HEMF
Working Paper, No. 06/2019, University of Duisburg-Essen, House of Energy Markets & Finance, Essen (<a href="https://www.econstor.eu/bitstream/10419/201589/1/wp1906.pdf">Link</a>)

[3] Felten, Björn; Felling, Tim; Osinski, Paul; Weber, Christoph (2019) : FlowBased Market Coupling Revised - Part II: Assessing Improved Price Zones in Central Western
Europe, HEMF Working Paper, No. 07/2019, University of Duisburg-Essen, House of Energy
Markets & Finance, Essen (<a href="https://www.econstor.eu/bitstream/10419/201590/1/wp1907.pdf">Link</a>)

## Dependencies

* Python 3.8
* Solver of choice (this is required by Pyomo; see https://ampl.com/products/solvers/open-source/); this is used in `runtest.py`, so specify solver's name accordingly.
* `pip install requirements.txt`


## Run as a script

Issue the following command to run the Day-Ahead market clearing method.

```
python runtest.py
```

Within the above script, specify the case-study (see an example of data format within the folder 'case studies'), and one of the method of day-ahead market clearing: atc or fmbc.

## Output

Output of market clearing is saved in 'results.xlsx' file
