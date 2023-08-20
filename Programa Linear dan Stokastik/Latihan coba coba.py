# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 12:22:38 2023

@author: Yulius
"""

import gurobipy as gp
from gurobipy import *
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# Model
m = gp.Model('Optimasi Bahan Baku Daur Ulang PET')

# Indeks / Sets
materials = ["CL", "LB", "MX"] #jenis bahan baku i ["Clear", "LightBlue", "Mixed"]
days = ["one","two","three","four","five"] #periode waktu

# Parameters
leadtime = {"CL":2,"LB":2,"MX":2} # lead time per bahan baku i, yaitu 2 hari
price = {"CL":10,"LB":20,"MX":30} #harga bahan baku i per satuan kg
holdingcost = {"CL":100,"LB":200,"MX":300} # holding cost bahan baku i
demand = { # demand bahan baku i pada periode t
    ("one", "CL"):10, ("one", "LB"):20,("one","MX"):30,
    ("two", "CL"):15, ("two", "LB"):25,("two", "MX"):30,
    ("three","CL"):20,("three","LB"):20,("three","MX"):30,
    ("four","CL"):25, ("four","LB"):25, ("four","MX"):30,
    ("five","CL"):30, ("five","LB"):20, ("five","MX"):30,
    }

orderingcost = 100 # ordering cost semua bahan baku
safetystock = 20 # safety stock bahan baku i pada periode t
warehousecapacity = 1000 # kapasitas gudang bahan baku, yaitu 110 ton
mvalue = 110000 # Big-M Value

# Variabel 
order = m.addVars(days, materials,  name="order", vtype=GRB.BINARY) # keputusan pesan atau tidak pesan
kuantitas = m.addVars(days, materials,  name="kuantitas", vtype=GRB.CONTINUOUS) # jumlah kuantitas pesan
inventory = m.addVars(days, materials, name="inventory", vtype=GRB.CONTINUOUS, ub=warehousecapacity) # Inventory

# Fungsi Tujuan
obj = quicksum(orderingcost*order[day, material] + holdingcost[material]*inventory[day, material] for day in days for material in materials)
m.setObjective(obj, GRB.MINIMIZE)

# Constraints
m.addConstrs((inventory[day, material] == kuantitas[day, material] - demand[day, material] for day in days for material in materials), "c1") ## Memastikan total pemesanan bahan baku pada periode sebelumnya 
                                                                          ## memenuhi demand dengan mendefinisikan nilai level persediaan awal (𝑋_(𝑖𝑡))
m.addConstrs((inventory[day, material] >= safetystock for day in days for material in materials), "c2") ## Memastikan persediaan awal tidak kurang dari jumlah safety stock yang telah ditentukan
m.addConstrs((kuantitas[day, material] <= mvalue*order[day, material] for day in days for material in materials), "c3") ## Mendefinisikan keputusan 𝑌_(𝑖𝑡𝑡′)  bergantung pada 𝑄_(𝑖𝑡𝑡'). Untuk memenuhi hubungan antara 𝑌_(𝑖𝑡𝑡')  dan 𝑄_(𝑖𝑡𝑡'), 
                                        ## diperlukan angka positif (𝑀) yang sangat besar

m.addConstrs((kuantitas[day, material] >= 0 for day in days for material in materials), "c4") ## non negatif
m.addConstrs((order[day, material] >= 0 for day in days for material in materials), "c5") ## non negatif
m.addConstrs((inventory[day, material] >= 0 for day in days for material in materials), "c6"); ## non negatif

# Optimize GRB
m.optimize()

# Analysis
for v in m.getVars():

	if v.varName.startswith("x"):
		print("Order {} kg bahan baku pada periode {}".format(v.x, v.varName[1:]))
	
print("--------------------------------")
print("Total cost: {}".format(m.objVal))

# Download Output
m.write("perencanaan-bahan-baku-output.sol")
