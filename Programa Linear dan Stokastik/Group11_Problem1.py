# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 21:12:53 2022

@author: Julio Febrian, Muhammad Fadil, Musyaffa M N E
"""

#Problem A-2
"""
The company CowFood produces food for farm animals that is sold in two forms: powder and granules.
The raw materials used for the production of the food are: oat, maize and molasses. The raw materials
(with the exception of molasses) first need to be ground, and then all raw materials that will form a
product are blended. In the last step of the production process the product mix is either transformed to
granules or sieved to obtain food in the form of powder.
Every food product needs to fulfill certain nutritional requirements. The percentages of proteins, lipids
and fibers contained in the raw materials and the required percentages in the final products are listed in
Table 6.3.
There are limits on the availability of raw materials. Table 6.4 displays the amount of raw material that is
available every day and the respective prices.
The cost of the different production steps are given in the following table.
With a daily demand of nine tonnes of granules and twelve tonnes of powder, which quantities of raw
materials are required and how should they be blended to minimize the total cost?
"""
from gurobipy import *

# Model
model = Model("Animal Food Production")


# Sets
NumberofFood = 2
FOOD = range(NumberofFood) # index f
NumberofRawmaterials = 3
RAW = range(NumberofRawmaterials) # index r
NumberofComposition = 3
COMP = range(NumberofComposition) # index c
NumberofProduction = 4
PROD = range(NumberofProduction) # index p


# Parameters
PERCENTAGE_rc = [[13.6, 4.1, 5.0], 
        [7.1, 2.4, 0.3], 
        [7.0, 3.7, 25.0]]
REQUIRED_c = [9.5, 2.0, 6.0]
AVAILABLE_r = [11900, 
               23500, 
               750]
COST_r = [0.13, 
          0.17, 
          0.12]
PRODUCTIONCOST_p = [0.25, 0.05, 0.42, 0.17]
DEMAND_f = [9000, 12000]


# Decision variable
use_rf = model.addVars(RAW, FOOD, 
                       vtype=GRB.CONTINUOUS, 
                       name="use")
produce_f = model.addVars(FOOD, 
                          vtype=GRB.CONTINUOUS, 
                          name="produce")


# Objective function
model.setObjective( quicksum(COST_r[r] * use_rf[r, f] for r in RAW for f in FOOD) + 
                   quicksum(PRODUCTIONCOST_p[0] * use_rf[r, f] for r in RAW for f in FOOD) +
                   quicksum(PRODUCTIONCOST_p[1] * use_rf[r, f] for r in RAW for f in FOOD) +
                   quicksum(PRODUCTIONCOST_p[2] * use_rf[r, 0] for r in RAW) +
                   quicksum(PRODUCTIONCOST_p[3] * use_rf[r, 1] for r in RAW), GRB.MINIMIZE)

# Constraints
## constraint 1
for f in FOOD:
    model.addConstr(sum(use_rf[r, f] for r in RAW) == 
                    produce_f[f])

## constraint 2
for f in FOOD:
    for c in COMP[0:2]:
        model.addConstr( quicksum(PERCENTAGE_rc[r][c] * use_rf[r, f] for r in RAW) >= 
    (REQUIRED_c[c] * produce_f[f]))
        
## constraint 3
for f in FOOD:
    model.addConstr( quicksum(PERCENTAGE_rc[r][2] * use_rf[r, f] for r in RAW) <= 
    (REQUIRED_c[2] * produce_f[f]))

## constraint 4
for r in RAW:
    model.addConstr(sum(use_rf[r, f] for f in FOOD) <= 
                    AVAILABLE_r[r])

## constraint 5
for f in FOOD:
    model.addConstr(produce_f[f] >= DEMAND_f[f])

## constraint 6
for r in RAW:
    for f in FOOD:
        model.addConstr(use_rf[r, f] >= 0)

for f in FOOD:
    model.addConstr(produce_f[f] >= 0)


# Run optimization
model.optimize()

# Result & Conclusion
print('\nOPTIMAL SOLUTION:')
print("\n1.The minimum cost for producing the demanded products is %d euro" % model.objVal)
                    
print('\n2.The composition of the food products are as follows:')
print('product 1 for granule and product 2 for powder')
for f in FOOD:
    for r in RAW:
        if use_rf[r, f].x != 0:
            print("%d kg of product %d is produced from Raw Material %d" % (use_rf[r, f].x, (f+1), (r+1)))

model.write("group11_problem1.sol")
