#==================================================================
# printdata.py
# A Python script to write data file for PYOMO
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# OATS
# Copyright (c) 2015 by W Bukhsh, Glasgow, Scotland
# OATS is distributed under the GNU GENERAL PUBLIC LICENSE v3 (see LICENSE file for details).
#==================================================================
import datetime
import math
import sys
import pandas as pd

deltaT = 1.0
class printdata(object):
    def __init__(self,datfile,data,model):
        self.datfile = datfile
        self.data    = data
        self.model   = model
    def printheader(self):
        with open(self.datfile, 'w') as f:
        #f = open(self.datfile, 'w')
            #####PRINT HEADER--START
            f.write('#This is Python generated data file for a Pyomo model.py\n')
            f.write('#_author_:W. Bukhsh\n')
            f.write('#Time stamp: '+ str(datetime.datetime.now())+'\n')
        #f.close()
    def printdata(self):
        with open(self.datfile, 'a') as f:
            ##===sets===
            #---set of zones---
            f.write('set Z:=\n')
            for i in self.data['zones']['name']:
                f.write(str(i)+"\n")
            f.write(';\n')
            #---set of brps---
            f.write('set BRPG:=\n')
            for i in self.data['brps'].index:
                if self.data['brps']['type'][i]=='G':
                    f.write(str(self.data['brps']['name'][i]) + "\n")
            f.write(';\n')
            f.write('set BRPD:=\n')
            for i in self.data['brps'].index:
                if self.data['brps']['type'][i]=='D':
                    f.write(str(self.data['brps']['name'][i]) + "\n")
            f.write(';\n')

            #---set of links---
            f.write('set LE:=\n 1 \n 2;\n')
            f.write('set L:=\n')
            for i in self.data['network']['Name']:
                f.write(str(i)+"\n")
            f.write(';\n')
            #---set of time period---
            f.write('set T:=\n')
            for i in set(self.data['market']['Time']):
                f.write(str(int(i))+"\n")
            f.write(';\n')

            # ---set of brps and zone mapping---
            f.write('set BRPGZone:=\n')
            for i in self.data['brps'].index:
                if self.data['brps']['type'][i] == 'G':
                    f.write(str(self.data['brps']['name'][i]) + ' ' + str(self.data['brps']['zone'][i]) + "\n")
            f.write(';\n')
            f.write('set BRPDZone:=\n')
            for i in self.data['brps'].index:
                if self.data['brps']['type'][i] == 'D':
                    f.write(str(self.data['brps']['name'][i]) + ' ' + str(self.data['brps']['zone'][i]) + "\n")
            f.write(';\n')

            # ---Volume demanded by BRPs---
            f.write('param VolG:=\n')
            for i in self.data['market'].index:
                if (self.data['market']['Volume(MWh)'][i])>=0:
                    f.write(str(self.data['market']['BRP'][i]) + ' ' + str(int(self.data['market']['Time'][i]))+ ' ' + str(self.data['market']['Volume(MWh)'][i]) + "\n")
            f.write(';\n')
            f.write('param VolD:=\n')
            for i in self.data['market'].index:
                if (self.data['market']['Volume(MWh)'][i]) <= 0:
                    f.write(str(self.data['market']['BRP'][i]) + ' ' + str(int(self.data['market']['Time'][i]))+ ' ' + str(self.data['market']['Volume(MWh)'][i]) + "\n")
            f.write(';\n')
            # ---Cost demanded by BRPs---
            f.write('param cG:=\n')
            for i in self.data['market'].index:
                if (self.data['market']['Volume(MWh)'][i]) >= 0:
                    f.write(str(self.data['market']['BRP'][i]) + ' ' + str(int(self.data['market']['Time'][i]))+ ' ' + str(self.data['market']['Cost(Euros/Mwh)'][i]) + "\n")
            f.write(';\n')
            f.write('param cD:=\n')
            for i in self.data['market'].index:
                if (self.data['market']['Volume(MWh)'][i]) <= 0:
                    f.write(str(self.data['market']['BRP'][i]) + ' ' + str(int(self.data['market']['Time'][i]))+ ' ' + str(self.data['market']['Cost(Euros/Mwh)'][i]) + "\n")
            f.write(';\n')
            # ------
            # ---Transfer Limits---

            f.write('param A:=\n')
            for i in self.data['network'].index:
                f.write(str(self.data['network']['Name'][i]) + ' ' + str(1) + ' ' + str((self.data['network']['FromZone'][i])) + "\n")
                f.write(str(self.data['network']['Name'][i]) + ' ' + str(2) + ' ' + str((self.data['network']['ToZone'][i])) + "\n")
            f.write(';\n')
            f.write('param Cap:=\n')
            for i in self.data['network'].index:
                f.write(str(self.data['network']['Name'][i]) + ' '+str(int(self.data['network']['Time'][i])) + ' ' + str((self.data['network']['ATC(MW)'][i]))+ "\n")
            f.write(';\n')
            # import/export capacities of zones
            f.write('param Import:=\n')
            for i in self.data['fbmc'].index:
                f.write(str(self.data['fbmc']['zone'][i]) + ' '+str(int(self.data['fbmc']['time'][i])) + ' ' + str((self.data['fbmc']['import (MW)'][i]))+ "\n")
            f.write(';\n')
            f.write('param Export:=\n')
            for i in self.data['fbmc'].index:
                f.write(str(self.data['fbmc']['zone'][i]) + ' '+str(int(self.data['fbmc']['time'][i])) + ' ' + str((self.data['fbmc']['export (MW)'][i]))+ "\n")
            f.write(';\n')


        # f.write('set G0:=\n')
            # for i in self.data[tab_names.unit_stat].index.tolist():
            #     if self.data[tab_names.unit_stat][unit_stat.all_or_nothing][i]!=0:
            #         f.write(str(self.data[tab_names.unit_stat][unit_stat.name][i]) + "\n")
            # f.write(';\n')
            # #---set of time-periods---
            # f.write('set T:= \n')
            # for i in self.data[tab_names.requirement][requirement.time_point]:
            #     f.write(str(i) + "\n")
            # f.write(';\n')
            # f.write('set TRed:= \n')
            # for i in self.data[tab_names.requirement][requirement.time_point][:-1]:
            #     f.write(str(i) + "\n")
            # f.write(';\n')
            #
            # # length of the optimisation time horizon
            # f.write('param nT:= \n')
            # f.write(str(self.data[tab_names.requirement][requirement.time_point].iloc[-1]) + "\n")
            # f.write(';\n')
            # # ---FPN---
            # f.write('param PICL:=\n')
            # for i in self.data[tab_names.unit_dyn].index.tolist():
            #     f.write(str(self.data[tab_names.unit_dyn][unit_dyn.name][i]) + " "+str(self.data[tab_names.unit_dyn][unit_dyn.time_point][i]) + " " + str(float(self.data[tab_names.unit_dyn][unit_dyn.pre_instruction_gen_level][i])) + "\n")
            # f.write(';\n')
            #
            # # ---Energy Requirement---
            # f.write('param ReqUB:=\n')
            # for i in self.data[tab_names.requirement].index.tolist():
            #     UB = max(self.data[tab_names.requirement][requirement.requirement_LB_MW][i],self.data[tab_names.requirement][requirement.requirement_UB_MW][i])
            #     f.write(str(self.data[tab_names.requirement][requirement.time_point][i]) + " "+str(UB) + "\n")
            # f.write(';\n')
            # f.write('param ReqLB:=\n')
            # for i in self.data[tab_names.requirement].index.tolist():
            #     LB = min(self.data[tab_names.requirement][requirement.requirement_LB_MW][i],
            #              self.data[tab_names.requirement][requirement.requirement_UB_MW][i])
            #     f.write(str(self.data[tab_names.requirement][requirement.time_point][i]) + " "+str(LB) + "\n")
            # f.write(';\n')
            #
            # # ---Notice to deliver bid and offer---
            # f.write('param NTO:=\n')
            # for i in self.data[tab_names.unit_stat].index.tolist():
            #     f.write(str(self.data[tab_names.unit_stat][unit_stat.name][i]) + " " + str(
            #         int(self.data[tab_names.unit_stat][unit_stat.notice_to_offer][i])) + "\n")
            # f.write(';\n')
            # f.write('param NTB:=\n')
            # for i in self.data[tab_names.unit_stat].index.tolist():
            #     f.write(str(self.data[tab_names.unit_stat][unit_stat.name][i]) + " " + str(
            #         int(self.data[tab_names.unit_stat][unit_stat.notice_to_bid][i])) + "\n")
            # f.write(';\n')
            # # ---Min zero time---
            # f.write('param MZT:=\n')
            # for i in self.data[tab_names.unit_stat].index.tolist():
            #     f.write(str(self.data[tab_names.unit_stat][unit_stat.name][i]) + " " + str(
            #         int(self.data[tab_names.unit_stat][unit_stat.min_zero_time][i])) + "\n")
            # f.write(';\n')
            # # ---Min non-zero time---
            # f.write('param MNZT:=\n')
            # for i in self.data[tab_names.unit_stat].index.tolist():
            #     f.write(str(self.data[tab_names.unit_stat][unit_stat.name][i]) + " " + str(
            #         int(self.data[tab_names.unit_stat][unit_stat.min_nonzero_time][i])) + "\n")
            # f.write(';\n')
            # # time for flat top
            # f.write('param FT:=\n')
            # for i in self.data[tab_names.unit_stat].index.tolist():
            #     f.write(str(self.data[tab_names.unit_stat][unit_stat.name][i]) + " " + str(
            #         int(self.data[tab_names.unit_stat][unit_stat.flat_top_time][i])) + "\n")
            # f.write(';\n')
            #
            # #---Power generation bounds---
            # f.write('param FR:=\n')
            # for i in self.data[tab_names.unit_dyn].index.tolist():
            #     f.write(str(self.data[tab_names.unit_dyn][unit_dyn.name][i])+" "+str(int(self.data[tab_names.unit_dyn][unit_dyn.time_point][i]))+" "+str(float(self.data[tab_names.unit_dyn][unit_dyn.pre_instruction_gen_lb][i]))+"\n")
            # f.write(';\n')
            # f.write('param HR:=\n')
            # for i in self.data[tab_names.unit_dyn].index.tolist():
            #     f.write(str(self.data[tab_names.unit_dyn][unit_dyn.name][i])+" "+str(int(self.data[tab_names.unit_dyn][unit_dyn.time_point][i]))+" "+str(float(self.data[tab_names.unit_dyn][unit_dyn.pre_instruction_gen_ub][i]))+"\n")
            # f.write(';\n')
            #
            # # ---Price Curve---
            # df_price = pd.DataFrame(columns={'Unit','Section','x','y'}) #price data
            # df_price_sections = pd.DataFrame(columns={'Unit', 'Sections'}) #number of price sections
            # # f.write('param xprice:=\n')
            # ind_o=0
            # ind = 0
            # for i in self.data[tab_names.unit_stat].index.tolist():
            #     lst_x = ((self.data[tab_names.unit_stat][unit_stat.x_price_curve][i]).split(','))
            #     lst_y = ((self.data[tab_names.unit_stat][unit_stat.y_price_curve][i]).split(','))
            #
            #     df_price_sections.loc[ind_o] = pd.Series({'Unit':self.data[tab_names.unit_stat][unit_stat.name][i], 'Sections':int(len(lst_x))})
            #     if len(lst_x)==len(lst_y):
            #         ind_PriceSection = 0
            #         for j in range(len(lst_x)):
            #             df_price.loc[ind] = pd.Series(
            #                 {'Unit': self.data[tab_names.unit_stat][unit_stat.name][i],'Section':int(ind_PriceSection+1), 'x': lst_x[j], 'y': lst_y[j]})
            #             ind += 1
            #             ind_PriceSection+=1
            #     else:
            #         raise ValueError('x and y points of the price curve are not equal')
            #     ind_o+=1
            #
            # f.write('param GPriceSections:=\n')
            # for i in df_price_sections.index:
            #     f.write(str(df_price_sections['Unit'][i])+" "+str(int(df_price_sections['Sections'][i]))+ "\n")
            # f.write(';\n')
            #
            # f.write('param GPriceDataX:=\n')
            # for i in df_price.index:
            #     f.write(str(df_price['Unit'][i])+" "+str(int(df_price['Section'][i]))+ " "+str(df_price['x'][i])+ "\n")
            # f.write(';\n')
            #
            # f.write('param GPriceDataY:=\n')
            # for i in df_price.index:
            #     f.write(str(df_price['Unit'][i])+" "+str(int(df_price['Section'][i]))+ " "+str(df_price['y'][i])+ "\n")
            # f.write(';\n')
            #
            # #---ramp rates---
            # f.write('param RU:=\n')
            # for i in self.data[tab_names.unit_stat].index.tolist():
            #     f.write(str(self.data[tab_names.unit_stat][unit_stat.name][i])+" "+str(float(deltaT*self.data[tab_names.unit_stat][unit_stat.ramp_up_rate][i]))+"\n")
            # f.write(';\n')
            # f.write('param RD:=\n')
            # for i in self.data[tab_names.unit_stat].index.tolist():
            #     f.write(str(self.data[tab_names.unit_stat][unit_stat.name][i])+" "+str(float(deltaT*self.data[tab_names.unit_stat][unit_stat.ramp_down_rate][i]))+"\n")
            # f.write(';\n')
            #
            # #--- Max delivery period, volume-offer and volume-bid---
            # f.write('param MDV_Offer:=\n')
            # for i in self.data[tab_names.unit_stat].index.tolist():
            #     f.write(str(self.data[tab_names.unit_stat][unit_stat.name][i])+" "+str(int(self.data[tab_names.unit_stat][unit_stat.max_delivery_vol_offer][i]))+"\n")
            # f.write(';\n')
            # f.write('param MDV_Bid:=\n')
            # for i in self.data[tab_names.unit_stat].index.tolist():
            #     f.write(str(self.data[tab_names.unit_stat][unit_stat.name][i])+" "+str(int(self.data[tab_names.unit_stat][unit_stat.max_delivery_vol_bid][i]))+"\n")
            # f.write(';\n')
            # f.write('param MDP:=\n')
            # for i in self.data[tab_names.unit_stat].index.tolist():
            #     f.write(str(self.data[tab_names.unit_stat][unit_stat.name][i])+" "+str(int(self.data[tab_names.unit_stat][unit_stat.max_delivery_period][i]))+"\n")
            # f.write(';\n')
            #
