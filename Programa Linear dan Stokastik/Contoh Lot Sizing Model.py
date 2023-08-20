# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 19:38:56 2023

@author: Yulius
"""

import gurobipy as gp
from gurobipy import GRB

m = gp.Model("ls")

capacitated = False

# Time (e.g. months)
n = 8
t = range(0, n)
  
# Costs for production of one product for each month
p = [100 for i in t]

# Costs for storing a product for each month
h = [5 for i in t]  

# Costs for armoring the machines for each month (has to be done at most once for each month)
q = [5000 for i in t]

# Demand for products for each month
d = [400, 400, 800, 800, 1200, 1200, 1200, 1200]

# Production Amount for each month
x = m.addVars(n, name="x", vtype=GRB.INTEGER)

# Storage Amount for each month
s = m.addVars(n + 1, name="s", vtype=GRB.INTEGER)

# Production Preparation necessary for each month (0 or 1)
y = m.addVars(n, name="y", vtype=GRB.BINARY)

# Production Capacity for each month (in this case unbounded -> LS-U)
if capacitated:
	M = [7000, 0, 0, 0, 0, 0, 0, 0]
else:
	M = m.addVars(n, name="M", vtype=GRB.INTEGER)
    
m.setObjective(gp.quicksum(p[i] * x[i] + q[i] * y[i] + h[i] * s[i+1] for i in t), GRB.MINIMIZE)

# Stored products from the previous month plus the number of products produced in the current
# month must fulfill the demand while the rest of the products must be stored for the next month
m.addConstrs((s[i-1] + x[i-1] == d[i-1] + s[i] for i in range(1, n+1)), "c1")
m.addConstr((s[0] + x[0] == d[0] + s[1]), "c2")

# The number of products stored in the first month must be equal to 200 (Initial stock)
m.addConstr(s[0] == 200, "c3")

# The number of products stored in the last month must be equal to 0 (Final stock)
m.addConstr(s[n] == 0, "c4")

# If products are being produced in the current month the machines must be prepared
m.addConstrs((x[i] <= M[i]*y[i] for i in t), "c5")

# There cant be a negative number of products stored in the warehouse or produced
m.addConstrs((x[i] >= 0 for i in t), "c6")
m.addConstrs((s[i] >= 0 for i in t), "c7")
m.addConstrs((M[i] >= 0 for i in t), "c8");

m.optimize()

for v in m.getVars():

	if v.varName.startswith("x"):
		print("Order {} kg bahan baku pada periode {}".format(v.x, v.varName[1:]))
	
print("--------------------------------")
print("Total cost: {}".format(m.objVal))

m.write("tes2.lp")

