#==================================================================
# runfile.py
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
#==================================================================
import os

import logging

from oats.runcase import runcase

logging.info("FBMC log file")
logging.info("Program started")
dir = os.path.dirname(os.path.realpath(__file__))
default_testcase = dir+'/case studies/example.xlsx'

#----------------------------------------------------------------------
# FBMC tool
def fbmc(tc='default',solver='ipopt',neos=True):
    """
    Solves Flow Based Market Clearing problem

    ARGUMENTS:
        **tc** (*.xlsx file)  - case study

        **solver** (str)  - name of a solver. Default is 'ipopt'

        **neos** (bool) - If True, the problem is solved using NEOS otherwise using a locally install solver.

        **out** (bool) - If True, the output is displayed on screen.
    """

    if tc == 'default':
        tc = default_testcase
    #add solver into options

    testcase = tc
    model ='FBMC'
    # ==log==
    logging.info("Solver selected: "+solver)
    logging.info("Testcase selected: "+testcase)
    logging.info("Model selected: "+model)
    runcase(testcase,model,neos,solver)
    logging.info("Done!")

def atc(tc='default',solver='ipopt',neos=True):
    """
    Solves 'Available Transfer Capacity' Clearing problem

    ARGUMENTS:
        **tc** (*.xlsx file)  - case study

        **solver** (str)  - name of a solver. Default is 'ipopt'

        **neos** (bool) - If True, the problem is solved using NEOS otherwise using a locally install solver.

        **out** (bool) - If True, the output is displayed on screen.
    """

    if tc == 'default':
        tc = default_testcase
    #add solver into options

    testcase = tc
    model ='ATC'
    # ==log==
    logging.info("Solver selected: "+solver)
    logging.info("Testcase selected: "+testcase)
    logging.info("Model selected: "+model)
    runcase(testcase,model,neos,solver)
    logging.info("Done!")
