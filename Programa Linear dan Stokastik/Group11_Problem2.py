# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 20:22:43 2022

@author: Julio Febrian, Muhammad Fadil, Musyaffa M N E
"""

#Problem E-2
"""
A company in the south-west of France needs to transport 180 tonnes of chemical products stored in
depots D1 to D4 to the three recycling centers C1, C2, and C3. The depots D1 to D4 contain respectively
50, 40, 35, and 65 tonnes, that is 190 tonnes in total. Two modes of transport are available: road and rail.
Depot D1 only delivers to centers C1 and C2 and that by road at a cost of BC 12k/t and BC 11k/t. Depot D2
only delivers to C2, by rail or road at BC 12k/t and BC 14k/t respectively. Depot D3 delivers to center C2 by
road (BC 9k/t) and to C3 by rail or road for BC 4k/t and BC 5k/t respectively. The depot D4 delivers to center C2
by rail or road at a cost of BC 11k/t and BC 14k/t, and to C3 by rail or road at BC 10k/t and BC 14k/t respectively.
Its contract with the railway company for the transport of chemical products requires the company to
transport at least 10 tonnes and at most 50 tonnes for any single delivery. Besides the standard security
regulations, there are no specific limitations that apply to road transport. How should the company
transport the 180 tonnes of chemicals to minimize the total cost of transport?
"""
import pandas as pd

import gurobipy as gp
from gurobipy import GRB

# sets
# create depot supply, rail/road limits, and central demand.
supply = dict({'D1': 50,
               'D2': 40,
               'D3': 35,
               'D4': 65})

path = dict({'C1rail': 50,
             'C1road': 50,
             'C2rail': 50,
             'C2road': 50,
             'C3rail': 50,
             'C3road': 50})

demand = dict({'X': 180})

# data explanation
# create shipping costs.
arcs, cost = gp.multidict({
    ('D1','C1road'):12,
    ('D1','C2road'):11,
    ('D2','C1rail'):12,
    ('D2','C1road'):14,
    ('D3','C2road'):9,
    ('D3','C3road'):5,
    ('D3','C3rail'):4,
    ('D4','C2rail'):11,
    ('D4','C2road'):14,
    ('D4','C3rail'):10,
    ('D4','C3road'):14,
    ('C1rail','X'):0,
    ('C2rail','X'):0,
    ('C3rail','X'):0,
    ('C1road','X'):0,
    ('C2road','X'):0,
    ('C2road','X'):0})

# Objective function
# We create a model and the variables. The variables simply capture the amount of product that flows along each allowed path 
# between a source and destination. Objective coefficients are provided here (in  cost ) , so we don't need to provide an optimization 
# objective later.
model = gp.Model('SupplyNetworkDesign')
flow = model.addVars(arcs, obj=cost, name="flow")


# Constraints
# Constrain 1: total Depot product
factories = supply.keys()
factory_flow = model.addConstrs((gp.quicksum(flow.select(factory, '*')) <= supply[factory]
                                 for factory in factories), name="factory")

# Constrain 2: total flow along arcs entering a Transportation to be equal to the demand from that central.
customers = demand.keys()
customer_flow = model.addConstrs((gp.quicksum(flow.select('*', customer)) == demand[customer]
                                  for customer in customers), name="customer")

# Constrain 3: transportation, the total amount of product entering the transportation must equal the total amount leaving.
depots = path.keys()
depot_flow = model.addConstrs((gp.quicksum(flow.select(depot, '*')) == gp.quicksum(flow.select('*', depot))
                               for depot in depots), name="depot")
depot_capacity = model.addConstrs((gp.quicksum(flow.select('*', depot)) <= path[depot]
                                   for depot in depots), name="depot_capacity")

#Run optimization
model.optimize()

#Result & Conclusion
product_flow = pd.DataFrame(columns=["From", "To", "Flow"])
for arc in arcs:
    if flow[arc].x > 1e-6:
        product_flow = product_flow.append({"From": arc[0], "To": arc[1], "Flow": flow[arc].x}, ignore_index=True)  
product_flow
print("the entire stock of 50 tonnes at depot D1 is transported by road to the recycling center C2 with the cost of 30k/t")
print("the entire stock of 30 tonnes at depot D2 is transported by rail to the recycling center C1 with the cost of 50k/t")
print("the entire stock of 35 tonnes at depot D3 is transported by rail to the recycling center C3 with the cost of 50k/t")
print("the stock of 50 tonnes at depot D4 is transported by rail to the recycling center C2 with the cost of 50k/t")
print("and the entire stock of 15 tonnes at depot D4 is transported by road to the recycling center C3 with the cost of 50k/t")
print("So, the minimum cost is 30+50+50+50+50 = 230k/t")
product_flow.index
arc[0]
arc
flow
flow[arc]
flow[arc].x
model.getVars()
model.write("group11 problem 2.sol")

table = pd.DataFrame(columns=["Order", "Quantity", "Inventory"])
for arc in arcs:
    if flow[arc].x > 1e-6:
        table = table.append({"Order": arc[0], "Quantity": arc[1], "Inventory": flow[arc].x}, ignore_index=True)  
table.index=[''] * len(table)
table
