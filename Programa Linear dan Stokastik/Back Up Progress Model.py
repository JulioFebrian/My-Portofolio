# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 19:38:56 2023

@author: Julio Febrian
"""

import gurobipy as gp
from gurobipy import GRB

# 1. Model
model = gp.Model("optimasi bahan baku daur ulang PET")

# 2. Sets
 # 2.1. Periode (hari)
n = 8
periode = range(0, n)
  
# 3. Parameter
 # 3.1. Harga bahan baku
harga = [100 for i in periode]

 # 3.2. Holding cost per unit kg per hari penyimpanan
holdingcost = [5 for i in periode]  

 # 3.3. Ordering cost per satu kali pesan
orderingcost = [5000 for i in periode]

 # 3.4. Demand per hari (dapat berupa target produksi atau forecast permintaan harian)
demand = [400, 400, 800, 800, 1200, 1200, 1200, 1200]
    
# 4. Variabel
 # 4.1. Kuantitas pesan
kuantitas = model.addVars(n, name="kuantitas", vtype=GRB.INTEGER)

 # 4.2. Inventory (jumlah per hari)
inventory = model.addVars(n + 1, name="inventory", vtype=GRB.INTEGER)

 # 4.3. Keputusan order (pesan = 1 / tidak pesan = 0)
order = model.addVars(n, name="order", vtype=GRB.BINARY)

 # 4.4. Kapasitas gudang (True - tidak ada stock di luar gudang, False - stock di luar)
capacitated = True
if capacitated:
	M = [7000, 7000, 7000, 7000, 7000, 7000, 7000, 7000]
else:
	M = model.addVars(n, name="M", vtype=GRB.INTEGER)

# 5. Fungsi tujuan    
model.setObjective(gp.quicksum(harga[i] * kuantitas[i] + orderingcost[i] * order[i] + holdingcost[i] * inventory[i+1] for i in periode), GRB.MINIMIZE)

# 6. Constraints (c)
 # 6.1. c1, c2
 # Bahan baku yang disimpan dari periode sebelumnya ditambah kedatangan order
 # harus memenuhi demand dengan selisihnya menjadi stock untuk periode selanjutnya
model.addConstrs((inventory[i-1] + kuantitas[i-1] == demand[i-1] + inventory[i] for i in range(1, n+1)), "c1")
model.addConstr((inventory[0] + kuantitas[0] == demand[0] + inventory[1]), "c2")

 # 6.2. Inventory awal
model.addConstr(inventory[0] == 200, "c3")

 # 6.3. Inventory bahan baku lebih dari safety stock 
model.addConstr(inventory[n] == 0, "c4")

 # 6.4. Hubungan kuantitas pesan dan waktu pesan memenuhi persamaan dengan Big M-value
model.addConstrs((kuantitas[i] <= M[i]*order[i] for i in periode), "c5")

 # 6.5. Non-negatif
model.addConstrs((order[i] >= 0 for i in periode), "c6")
model.addConstrs((kuantitas[i] >= 0 for i in periode), "c7")
model.addConstrs((inventory[i] >= 0 for i in periode), "c8")
model.addConstrs((M[i] >= 0 for i in periode), "c9");

# 7. Optimasi 
model.optimize()

# 8. Visualisasi hasil
for v in model.getVars():

	if v.varName.startswith("k"):
		print("Order {} kg bahan baku pada periode {}".format(v.x, v.varName[9:]))
	
print("--------------------------------")
print("Total biaya persediaan: Rp. {}".format(model.objVal))

# 9. Analisis
model.getVars()
model.objVal

# 10. Download solusi
model.write("order-bahan-baku-optimal-output.sol")
