import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Model
model = gp.Model("optimasi bahan baku daur ulang PET")

# 2. Sets & Parameter
 # 2.1. Demand per hari (kg)
# path = r'C:\Users\Yulius\OneDrive\Documents\Dokumen Julio\Skripsi\Sidang\Input Data Model_Historical 1 Tahun.xlsx'
# path = r'C:\Users\Yulius\OneDrive\Documents\Dokumen Julio\Skripsi\Sidang\Input Data Model_Forecasted Demand.xlsx'
path = r'C:\Users\Yulius\OneDrive\Documents\Dokumen Julio\Skripsi\Sidang\Input Data Model_Validasi Dummy.xlsx'
data = pd.read_excel(path, sheet_name='Clear')
demand = data['Demand (kg)'].tolist()
t = len(demand)
periode = range(0, t)

 # 2.2. Inventory_awal (kg)
input_inventory_awal = data.at[0, 'Inventory_Awal (kg)']
inventory_awal = input_inventory_awal

 # 2.3. Holding cost per unit kg per hari (Rp.)
input_holding_cost = data.at[0, 'Holding_Cost (Rp.)/kg']
holding_cost = [input_holding_cost for i in periode]  

 # 2.4. Ordering cost per satu kali pesan (Rp.)
input_ordering_cost = data.at[0, 'Ordering_Cost (Rp.)']
ordering_cost = [input_ordering_cost for i in periode]

 # 2.5 Safety stock (kg)
input_safety_stock = data.at[0, 'Safety_Stock (kg)']
safety_stock = input_safety_stock

 # 2.6. Inventory akhir
inventory_akhir = safety_stock

 # 2.7. Kapasitas Gudang (mencegah stock di luar gudang)
kapasitas_gudang = data.at[0, 'Kapasitas_Gudang (kg)']

# 3. Variabel
 # 3.1. Kuantitas pesan
kuantitas = model.addVars(t, name="kuantitas", vtype=GRB.INTEGER)

 # 3.2. Inventory (jumlah per hari)
inventory = model.addVars(t + 1, name="inventory", vtype=GRB.CONTINUOUS)

 # 3.3. Keputusan order (pesan = 1 / tidak pesan = 0)
 # Fungsi Kendala 4 (c4) -> Variabel keputusan order 
   # Mendefinisikan keputusan order berbentuk bilangan biner 𝑌_it
   # 1 = melakukan pemesanan bahan baku
   # 0 = tidak melakukan pemesanan bahan baku
order = model.addVars(t, name="order", vtype=GRB.BINARY)

 # 3.4. Big-M Value 
max_kedatangan = data.at[0, 'Max_Kedatangan (kg)']
capacitated = True
if capacitated:
	M = [max_kedatangan for t in periode]
else:
	M = model.addVars(t, name="M", vtype=GRB.CONTINUOUS)

# 4. Fungsi tujuan    
 # Meminimalkan total biaya persediaan dari hasil penjumlahan 
 # biaya pesan dan biaya simpan tiap periode
model.setObjective(gp.quicksum(ordering_cost[i] * order[i] + holding_cost[i] * inventory[i] for i in periode), GRB.MINIMIZE)

# 5. Constraints (c)
 # 5.1. Inventory memenuhi demand
 # Memastikan total pemesanan bahan baku periode sebelumnya memenuhi demand 
 # Mendefinisikan nilai level persediaan i pada periode t (𝑋_𝑖𝑡) 
for t in range(1, t+1):
    model.addConstr((inventory[t-1] + kuantitas[t-1] - demand[t-1]) == inventory[t], "c1")

 # 5.2. Kuantitas Pesan tidak melebihi batas kedatangan bahan baku dan sebagai hubungan kuantitas pesan dan waktu pesan memenuhi persamaan dengan Big M-value
# Fungsi Kendala 2 (c2)
 # Mendefinisikan keputusan 𝑌_𝑖𝑡 yang bergantung pada 𝑄_(𝑖𝑡). 
 # Memenuhi hubungan diperlukan sebuah bilangan positif (𝑀) yang sangat besar
for i in periode:
    model.addConstr((kuantitas[i] <= M[i]*order[i]), "c2")

 # 5.3. Inventory setiap periode lebih dari safety stock yang telah ditetapkan
for t in range(1, t+1):
  model.addConstr(inventory[t] >= safety_stock, "c3")
  
 # 5.4. Inventory tidak melebihi kapasitas gudang
for i in periode:
    model.addConstr((inventory[i] <= kapasitas_gudang), "c4")

 # 5.5. Non-negatif
 # Fungsi Kendala 5 (c5)
  # Mendefinisikan variabel keputusan adalah non-negatif
for i in periode: 
    model.addConstr((order[i] >= 0), "c5")
    model.addConstr((kuantitas[i] >= 0), "c6")
    model.addConstr((inventory[i] >= 0), "c7")
    
 # 5.2. Inventory awal
 # Fungsi Kendala 2 (c2)
  # Memastikan persediaan awal tiap periode tidak kurang dari 
  # nilai safety stock yang ditentukan
  # Dalam kasus ini, belum diterapkan safety stock sehingga bernilai 0
  # Digunakan dalam peningkatan skenario penerapan safety stock
model.addConstr(inventory[0] == inventory_awal, "c8")

 # 5.3. Inventory akhir sama dengan safety stock 
model.addConstr(inventory[t] == inventory_akhir, "c9")

# 6. Optimasi 
model.optimize()

# 7. Analisis & Visualisasi hasil
for v in model.getVars():

	if v.varName.startswith("k"):
		print("Order {} kg bahan baku pada periode {}".format(abs(round((v.x),2)), v.varName[9:]))

minimum_cost = round(model.objVal,0)
print("--------------------------------")
print("Total biaya persediaan minimum: Rp. {}".format(minimum_cost))
print("--------------------------------")

kolom_order = pd.DataFrame(columns=["Order"])
for o in order.values():
  kolom_order = kolom_order.append({"Order": abs(o.X)}, ignore_index=True)  

kolom_quantity = pd.DataFrame(columns=["Quantity"])
for q in kuantitas.values():
  kolom_quantity = kolom_quantity.append({"Quantity": round(abs(q.X),0)}, ignore_index=True)  

kolom_inventory = pd.DataFrame(columns=["Inventory"])
for i in inventory.values():
  kolom_inventory = kolom_inventory.append({"Inventory": round(abs(i.X),0)}, ignore_index=True)  
kolom_inventory = kolom_inventory.drop(labels=t, axis=0)

kolom_demand = round(pd.DataFrame(demand, columns = ["Demand"]),0)

table = pd.concat([kolom_order, kolom_quantity, kolom_inventory, kolom_demand], axis='columns')
print(table)
print("--------------------------------")

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
plt.legend((bar1, bar2, bar3), ('Pesan Q&T', 'Demand', 'Inventory'))
plt.show()

# 8. Status
status = model.status
if status == GRB.Status.OPTIMAL:
    print('[model sudah optimal]')
if status == GRB.Status.INF_OR_UNBD or status == GRB.Status.INFEASIBLE  or status == GRB.Status.UNBOUNDED:
    print('[model infeasible atau unbounded]')
if status != GRB.Status.OPTIMAL:
    print('Optimasi belum optimal')
    
#9. Download
#model.write("Perencanaan-Persediaan-CL-Januari.sol")
#model.write("Perencanaan-Persediaan-CL-Januari.lp")
#model.write("perencanaan-bahan-baku-output.mps")

# #10. Export model output to Excel
# output_path = r'C:\Users\Yulius\OneDrive\Documents\Dokumen Julio\Skripsi\Sidang\Output Data Model_1 Bulan.xlsx'
# writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
# table.to_excel(writer, sheet_name = 'Output_CL', index = True)
# writer.save()