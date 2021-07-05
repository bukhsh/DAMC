#==================================================================
# printout.py
# A Python script to write output to xls and on screen
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# OATS
# Copyright (c) 2015 by W Bukhsh, Glasgow, Scotland
# OATS is distributed under the GNU GENERAL PUBLIC LICENSE v3 (see LICENSE file for details).
#==================================================================
from pyomo.opt import SolverStatus, TerminationCondition
from tabulate import tabulate
import pandas as pd
import math
import sys
class printoutput(object):
    def __init__(self, results, instance,mod,testcase):
        self.results   = results
        self.instance  = instance
        self.mod       = mod
        self.tc        = testcase
    def greet(self):
        print ("========================")
        print ("\n Output from the OATS")
        print ("========================")
    def solutionstatus(self):
        self.instance.solutions.load_from(self.results)
        print ("------Solver Message------")
        print (self.results.solver)
        print ("--------------------------")
        if (self.results.solver.status == SolverStatus.ok) \
        and (self.results.solver.termination_condition == TerminationCondition.optimal):
            print ("Optimization Converged!")
        elif self.results.solver.termination_condition == TerminationCondition.infeasible:
            sys.exit("Problem is infeasible!\nOats terminated. No output is written on the results file.")
        else:
            print (sys.exit("Problem is infeasible!\nOats terminated. No output is written on the results file."))
    def printsummary(self):
        print ("Value of the objective function:", str(float(self.instance.OBJ())))
        print ("***********")
        print ("\n Summary")
        print ("***********")
        tab_summary = []
        tab_summary.append(['TP', 'Generation (MW)','Demand (MW)'])
        for t in self.instance.T:
            tab_summary.append([t,round(sum(self.instance.pG[g,t].value for g in self.instance.BRPG),2),
                                round(sum(self.instance.pD[g,t].value for g in self.instance.BRPD),2)])
        print (tabulate(tab_summary, headers="firstrow", tablefmt="grid"))
        print ("==============================================")
    def printoutputxls(self):
        #===initialise pandas dataframes
        cols_summary    = ['TP', 'Generation (MW)','Demand (MW)']
        cols_generation = ['Zone', 'Time', 'Generation (MW)','Demand (MW)', 'LMP']
        cols_trade      = ['Zone (from)', 'Zone (to)', 'Time', 'Flow (MW)']

        summary         = pd.DataFrame(columns=cols_summary)
        zone            = pd.DataFrame(columns=cols_generation)
        trade           = pd.DataFrame(columns=cols_trade)

        #-----write Data Frames
        ind = 0
        for t in self.instance.T:
            summary.loc[ind] = pd.Series({'TP':t,
                                   'Generation (MW)':round(sum(self.instance.pG[g,t].value for g in self.instance.BRPG),2),
                                   'Demand (MW)':round(sum(self.instance.pD[g,t].value for g in self.instance.BRPD),2)
            })
        ind += 1

        # zonal data
        ind = 0
        for z in self.instance.Z:
            for t in self.instance.T:
                zone.loc[ind] = pd.Series({'Zone':z, 'Time':t,\
                                            'Generation (MW)':round(sum(self.instance.pG[g,t].value for g in self.instance.BRPG if (g,z) in self.instance.BRPGZone),2),\
                                            'Demand (MW)':round(sum(self.instance.pD[g,t].value for g in self.instance.BRPD if (g,z) in self.instance.BRPDZone),2), 'LMP':1})
                ind += 1

        # trades
        ind = 0
        cols_trade = ['Zone (from)', 'Zone (to)', 'Time', 'Flow (MW)']
        for l in self.instance.L:
            for t in self.instance.T:
                trade.loc[ind] = pd.Series({'Zone (from)':self.instance.A[l,1],'Zone (to)':self.instance.A[l,2], 'Time':t,\
                                            'Flow (MW)':self.instance.pL[l,t].value})
                ind += 1

           #----------------------------------------------------------
        #===write output on xlsx file===
        # print (summary)
        # units = units.sort_values(['tp'])
        writer = pd.ExcelWriter('results.xlsx', engine ='xlsxwriter')
        summary.to_excel(writer, sheet_name = 'Summary',index=False)
        zone.to_excel(writer, sheet_name = 'Zonal Data',index=False)
        trade.to_excel(writer, sheet_name = 'Trades',index=False)
        writer.save()
