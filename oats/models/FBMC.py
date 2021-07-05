#==================================================================
# FBMC.mod
# PYOMO model file of "Flow based market clearing"
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
#==================================================================

#==========Import==========
from __future__ import division
from pyomo.environ import *
#==========================

model = AbstractModel()

# --- SETS ---
model.Z          = Set()  # set of zones
model.BRPG       = Set()  # set of Generation balancing responsible parties
model.BRPD       = Set()  # set of Demand balancing responsible parties
model.T          = Set()  # set of time period
model.L          = Set()  # set of connections
model.LE         = Set()  # set of connections {1,2} matrix 'to' and 'from' link
model.BRPGZone   = Set(within=model.BRPG*model.Z)  # set of mapping BRP (generation) and zone
model.BRPDZone   = Set(within=model.BRPD*model.Z)  # set of mapping BRP (demand) and zone

# --- parameters ---
model.VolG   = Param(model.BRPG*model.T,within=NonNegativeReals)    # Volume provided( +ve) by a generation BRP in timeperiod [t,t+1]
model.VolD   = Param(model.BRPD*model.T,within=NegativeReals)       # Volume provided (-ve) demanded by a BRP in timeperiod [t,t+1]
model.cG     = Param(model.BRPG*model.T,within=Reals)               # Cost of generation volume a BRP in timeperiod [t,t+1]
model.cD     = Param(model.BRPD*model.T,within=Reals)               # Cost of demand volume by a BRP in timeperiod [t,t+1]
model.Cap    = Param(model.L*model.T,within=Reals)                  # interconnection capacity allocated on link l in [t,t+1]
model.Import = Param(model.Z,model.T,within=NonNegativeReals)
model.Export = Param(model.Z,model.T,within=NonNegativeReals)
# # Connections
model.A     = Param(model.L*model.LE,within=Any)       # bus-line matrix

#
# --- variables ---
model.pG    = Var(model.BRPG,model.T, domain= NonNegativeReals)
model.pD    = Var(model.BRPD,model.T, domain= NegativeReals)
model.pL    = Var(model.L,model.T, domain= Reals)
# --- cost function ---
def objective(model):
    obj = sum(model.cG[brp,t]*(model.pG[brp,t]) for (brp,t) in model.BRPG*model.T)\
          # +sum(model.cD[brp,t]*(model.pD[brp,t]) for (brp,t) in model.BRPD*model.T)
    return obj
model.OBJ = Objective(rule=objective, sense=minimize)
#
# --- balance constraint ---
def balance_def(model, z, t):
    return sum(model.pG[brpg,t] for brpg in model.BRPG if (brpg,z) in model.BRPGZone)+\
    sum(model.pD[brpd,t] for brpd in model.BRPD if (brpd,z) in model.BRPDZone) - \
    sum(model.pL[l, t] for l in model.L if model.A[l,1]==z) +\
    sum(model.pL[l, t] for l in model.L if model.A[l,2]==z)   == 0


model.balance_const = Constraint(model.Z,model.T, rule=balance_def)
#
# --- Constraint on volume---
def vol_def(model,brp,t):
    return model.pD[brp,t] == model.VolD[brp,t]
model.vol_def_const     = Constraint(model.BRPD,model.T, rule=vol_def)

# --- Constraint on volume---
def vol_def_G(model,brp,t):
    return model.pG[brp,t] <= model.VolG[brp,t]
model.volG_def_const     = Constraint(model.BRPG,model.T, rule=vol_def_G)

# --- Network constraints---
def capacity_def(model,l,t):
    return model.pL[l,t] <= model.Cap[l,t]
model.capacity_def_const     = Constraint(model.L,model.T, rule=capacity_def)

# --- Group constraints---
def group_export_def(model,z,t):
    return -sum(model.pL[l, t] for l in model.L if model.A[l,1]==z)+\
           sum(model.pL[l, t] for l in model.L if model.A[l,2]==z)   <= model.Export[z,t]
def group_import_def(model,z,t):
    return sum(model.pL[l, t] for l in model.L if model.A[l,1]==z)-\
           sum(model.pL[l, t] for l in model.L if model.A[l,2]==z)   <= model.Import[z,t]

model.group_export_const     = Constraint(model.Z,model.T, rule=group_export_def)
model.group_import_const     = Constraint(model.Z,model.T, rule=group_import_def)
