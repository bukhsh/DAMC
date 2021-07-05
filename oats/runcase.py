#==================================================================
# runcase.py
# This is a second level script, which is called by the runfile.
# This script receives model,testcase as an input to run simulation
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# July 2021
#==================================================================

#===============Import===============
from __future__ import division
import pyutilib.subprocess.GlobalData
import os
from pyomo.environ import *
from pyomo.opt import SolverFactory
from pyomo.opt import SolverStatus, TerminationCondition

import logging
from oats.selecttestcase import selecttestcase
from oats.printdata import printdata
from oats.printoutput import printoutput
import imp
#====================================

def runcase(testcase,mod,neos,solver):
    oats_dir = os.path.dirname(os.path.realpath(__file__))
    try:
        modelf = imp.load_source(mod, oats_dir+'/models/'+mod+'.py')
        model = modelf.model
        logging.info("Given model file found and selected from the models library")
    except Exception:
        logging.error("Given model file not found in the 'models' library", exc_info=False)
        raise
    try:
        ptc = selecttestcase(testcase) #read test case
        logging.info("Given testcase file found and selected from the testcase library")
    except Exception:
        logging.error("Given testcase  not found in the 'testcases' library", exc_info=False)
        raise
    datfile = 'datafile.dat'
    r = printdata(datfile,ptc,mod)
    r.printheader()
    r.printdata()


    ###############Solver settings####################
    if (not neos):
        optimise = SolverFactory(solver)
        #################################################

        ############Solve###################
        instance = model.create_instance(datfile)
        instance.dual = Suffix(direction=Suffix.IMPORT)
        results = optimise.solve(instance,tee=True)
        instance.solutions.load_from(results)

        # ##################################
        #
        # ############Output###################
        o = printoutput(results, instance,mod,testcase)
        o.greet()
        o.solutionstatus()
        o.printsummary()
        o.printoutputxls()
    else:
        instance       = model.create_instance(datfile)
        #solveroptions  = SolverFactory(opt['solver'])
        solver_manager = SolverManagerFactory('neos')
        print (dir(solver_manager.solve))
        results        = solver_manager.solve(instance, opt=solveroptions)
        print (results)
