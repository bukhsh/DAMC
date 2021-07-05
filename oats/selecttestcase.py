#==================================================================
# select_testcase.py
# This Python script loads the test case file from the library
# ---Author---
# W. Bukhsh,
#==================================================================

import pandas as pd

def selecttestcase(test):
    xl = pd.ExcelFile(test,engine='openpyxl')

    df_zones   = xl.parse('Zones')
    df_brps    = xl.parse('BRPs')
    df_market  = xl.parse('MarketData')
    df_network = xl.parse('NetworkData')
    df_fbmc    = xl.parse('FBMC')


    data = {
    'zones'  : df_zones.dropna(how='all'),
    'brps'   : df_brps.dropna(how='all'),
    'market' : df_market.dropna(how='all'),
    'network': df_network.dropna(how='all'),
        'fbmc': df_fbmc.dropna(how='all'),
    }

    return data
