import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# 1. Model
model = gp.Model("optimasi bahan baku daur ulang PET")

# 2. Sets
 # 2.1. Periode (hari)
t = 8
periode = range(0, t)

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
kuantitas = model.addVars(t, name="kuantitas", vtype=GRB.INTEGER)

 # 4.2. Inventory (jumlah per hari)
inventory = model.addVars(t + 1, name="inventory", vtype=GRB.INTEGER)

 # 4.3. Keputusan order (pesan = 1 / tidak pesan = 0)
order = model.addVars(t, name="order", vtype=GRB.BINARY)

 # 4.4. Kapasitas gudang (True - tidak ada stock di luar gudang, False - stock di luar)
capacitated = False
if capacitated:
	M = [7000, 7000, 7000, 7000, 7000, 7000, 7000, 7000]
else:
	M = model.addVars(t, name="M", vtype=GRB.INTEGER)

# 5. Fungsi tujuan    
model.setObjective(gp.quicksum(harga[i] * kuantitas[i] + orderingcost[i] * order[i] + holdingcost[i] * inventory[i] for i in periode), GRB.MINIMIZE)

# 6. Constraints (c)
 # 6.1. Inventory memenuhi demand
for i in range(1, t+1):
    model.addConstr((inventory[i] == inventory[i-1] + kuantitas[i-1] - demand[i-1]), "c1")

 # 6.2. Inventory awal
model.addConstr(inventory[0] == 200, "c2")

 # 6.3. Inventory bahan baku lebih dari safety stock 
model.addConstr(inventory[t] == 0, "c3")

 # 6.4. Hubungan kuantitas pesan dan waktu pesan memenuhi persamaan dengan Big M-value
for i in periode:
    model.addConstr((kuantitas[i] <= M[i]*order[i]), "c4")

 # 6.5. Non-negatif
for i in periode: 
    model.addConstr((order[i] >= 0), "c5")
    model.addConstr((kuantitas[i] >= 0), "c6")
    model.addConstr((inventory[i] >= 0), "c7")
    model.addConstr((M[i] >= 0), "c8");

# 7. Optimasi 
model.optimize()

# 8. Visualisasi hasil
 # 8.1. Text
for v in model.getVars():

	if v.varName.startswith("k"):
		print("Order {} kg bahan baku pada periode {}".format(v.x, v.varName[9:]))
	
print("--------------------------------")
print("Total biaya persediaan: Rp. {}".format(model.objVal))
print("--------------------------------")

 # 8.2. Tabel
kolom_order = pd.DataFrame(columns=["Order"])
for o in order.values():
  kolom_order = kolom_order.append({"Order": o.X}, ignore_index=True)  

kolom_quantity = pd.DataFrame(columns=["Quantity"])
for q in kuantitas.values():
  kolom_quantity = kolom_quantity.append({"Quantity": q.X}, ignore_index=True)  

kolom_inventory = pd.DataFrame(columns=["Inventory"])
for i in inventory.values():
  kolom_inventory = kolom_inventory.append({"Inventory": i.X}, ignore_index=True)  
kolom_inventory = kolom_inventory.drop(labels=t, axis=0)

kolom_demand = pd.DataFrame(demand, columns = ["Demand"])

table = pd.concat([kolom_order, kolom_quantity, kolom_inventory, kolom_demand], axis='columns')
print(table)
print("Inventory akhir: {} kg")
print("--------------------------------")

 # 8.3. Grafik
ind = np.arange(t) 
width = 0.25

xvals = table.Quantity
bar1 = plt.bar(ind, xvals, width, color = 'b')
  
yvals = table.Demand
bar2 = plt.bar(ind+width, yvals, width, color='r')
  
zvals = table.Inventory
bar3 = plt.bar(ind+width*2, zvals, width, color = 'g')
  
plt.xlabel("Periode")
plt.ylabel('Kuantitas')
plt.title("Perencanaan Optimal (Biaya Minimum)")
  
plt.xticks(ind+width,ind)
plt.legend((bar1, bar2, bar3), ('Pesan', 'Demand', 'Inventory'))
plt.show()

# 9. Analisis
status = model.status
if status == GRB.Status.OPTIMAL:
    print('[model sudah optimal]')
if status == GRB.Status.INF_OR_UNBD or status == GRB.Status.INFEASIBLE  or status == GRB.Status.UNBOUNDED:
    print('[model infeasible atau unbounded]')
if status != GRB.Status.OPTIMAL:
    print('Optimasi belum optimal')

# 10. Download model
model.write("perencanaan-bahan-baku-optimal.sol")