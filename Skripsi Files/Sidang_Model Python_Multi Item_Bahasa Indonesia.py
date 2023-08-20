import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Model
model_1 = gp.Model("optimasi bahan baku Clear daur ulang PET")
model_2 = gp.Model("optimasi bahan baku Light Blue daur ulang PET")
model_3 = gp.Model("optimasi bahan baku Mix daur ulang PET")

# 2. Sets & Parameter
 # Bahan Baku 1 = 'CL', 2 = 'LB', 3 = 'MX'
 # 2.1. Demand per hari (kg)
# path = r'C:\Users\Yulius\OneDrive\Documents\Dokumen Julio\Skripsi\Sidang\Input Data Model_Historical 1 Tahun.xlsx'
path = r'C:\Users\Yulius\OneDrive\Documents\Dokumen Julio\Skripsi\Sidang\Input Data Model_Forecasted Demand.xlsx'
data_1 = pd.read_excel(path, sheet_name='Clear')
data_2 = pd.read_excel(path, sheet_name='Light Blue')
data_3 = pd.read_excel(path, sheet_name='Mix')
demand_1 = data_1['Demand (kg)'].tolist()
t_1 = len(demand_1)
periode_1 = range(0, t_1)
demand_2 = data_2['Demand (kg)'].tolist()
t_2 = len(demand_2)
periode_2 = range(0, t_2)
demand_3 = data_3['Demand (kg)'].tolist()
t_3 = len(demand_3)
periode_3 = range(0, t_3)

 # 2.2. Inventory_awal (kg)
input_inventory_awal_1 = data_1.at[0, 'Inventory_Awal (kg)']
inventory_awal_1 = input_inventory_awal_1
input_inventory_awal_2 = data_2.at[0, 'Inventory_Awal (kg)']
inventory_awal_2 = input_inventory_awal_2
input_inventory_awal_3 = data_3.at[0, 'Inventory_Awal (kg)']
inventory_awal_3 = input_inventory_awal_3

 # 2.3. Holding cost per unit kg per hari (Rp.)
input_holding_cost_1 = data_1.at[0, 'Holding_Cost (Rp.)/kg']
holding_cost_1 = [input_holding_cost_1 for i in periode_1]  
input_holding_cost_2 = data_2.at[0, 'Holding_Cost (Rp.)/kg']
holding_cost_2 = [input_holding_cost_2 for i in periode_2]  
input_holding_cost_3 = data_3.at[0, 'Holding_Cost (Rp.)/kg']
holding_cost_3 = [input_holding_cost_3 for i in periode_3]  

 # 2.4. Ordering cost per satu kali pesan (Rp.)
input_ordering_cost_1 = data_1.at[0, 'Ordering_Cost (Rp.)']
ordering_cost_1 = [input_ordering_cost_1 for i in periode_1]
input_ordering_cost_2 = data_2.at[0, 'Ordering_Cost (Rp.)']
ordering_cost_2 = [input_ordering_cost_2 for i in periode_2]
input_ordering_cost_3 = data_3.at[0, 'Ordering_Cost (Rp.)']
ordering_cost_3 = [input_ordering_cost_3 for i in periode_3]

 # 2.5 Safety stock (kg)
input_safety_stock_1 = data_1.at[0, 'Safety_Stock (kg)']
safety_stock_1 = input_safety_stock_1
input_safety_stock_2 = data_2.at[0, 'Safety_Stock (kg)']
safety_stock_2 = input_safety_stock_2
input_safety_stock_3 = data_3.at[0, 'Safety_Stock (kg)']
safety_stock_3 = input_safety_stock_3

 # 2.6. Inventory akhir
inventory_akhir_1 = safety_stock_1
inventory_akhir_2 = safety_stock_2
inventory_akhir_3 = safety_stock_3

 # 2.7. Kapasitas Gudang (mencegah stock di luar gudang)
kapasitas_gudang_1 = data_1.at[0, 'Kapasitas_Gudang (kg)']
kapasitas_gudang_2 = data_2.at[0, 'Kapasitas_Gudang (kg)']
kapasitas_gudang_3 = data_3.at[0, 'Kapasitas_Gudang (kg)']

# 3. Variabel
 # 3.1. Kuantitas pesan
kuantitas_1 = model_1.addVars(t_1, name="kuantitas_1", vtype=GRB.CONTINUOUS)
kuantitas_2 = model_2.addVars(t_2, name="kuantitas_2", vtype=GRB.CONTINUOUS)
kuantitas_3 = model_3.addVars(t_3, name="kuantitas_3", vtype=GRB.CONTINUOUS)

 # 3.2. Inventory (jumlah per hari)
inventory_1 = model_1.addVars(t_1 + 1, name="inventory_1", vtype=GRB.CONTINUOUS)
inventory_2 = model_2.addVars(t_2 + 1, name="inventory_2", vtype=GRB.CONTINUOUS)
inventory_3 = model_3.addVars(t_3 + 1, name="inventory_3", vtype=GRB.CONTINUOUS)

 # 5.5. Keputusan order binary (pesan = 1 / tidak pesan = 0)
is_order_1 = model_1.addVars(t_1, name="is_order_1", vtype=GRB.BINARY)
is_order_2 = model_2.addVars(t_2, name="is_order_2", vtype=GRB.BINARY)
is_order_3 = model_3.addVars(t_3, name="is_order_3", vtype=GRB.BINARY)

 # 3.4. Big-M Value / Maksimal Kedatangan (True - dibatasi, False - tidak dibatasi)
max_kedatangan_1 = data_1.at[0, 'Max_Kedatangan (kg)']
max_kedatangan_2 = data_2.at[0, 'Max_Kedatangan (kg)']
max_kedatangan_3 = data_3.at[0, 'Max_Kedatangan (kg)']
capacitated = True
if capacitated:
	M_1 = [max_kedatangan_1 for t in periode_1]
	M_2 = [max_kedatangan_2 for t in periode_2]
	M_3 = [max_kedatangan_3 for t in periode_3]
else:
	M_1 = model_1.addVars(t_1, name="M", vtype=GRB.CONTINUOUS)
	M_2 = model_2.addVars(t_2, name="M", vtype=GRB.CONTINUOUS)
	M_3 = model_3.addVars(t_3, name="M", vtype=GRB.CONTINUOUS)

# 4. Fungsi tujuan    
# Fungsi Tujuan: Meminimalkan Total Biaya Persediaan
model_1.setObjective(gp.quicksum(ordering_cost_1[t] * is_order_1[t] + holding_cost_1[t] * inventory_1[t] 
                                 for t in periode_1), GRB.MINIMIZE)
model_2.setObjective(gp.quicksum(ordering_cost_2[t] * is_order_2[t] + holding_cost_2[t] * inventory_2[t] 
                                 for t in periode_2), GRB.MINIMIZE)
model_3.setObjective(gp.quicksum(ordering_cost_3[t] * is_order_3[t] + holding_cost_3[t] * inventory_3[t] 
                                 for t in periode_3), GRB.MINIMIZE)

# 5. Constraints (c)
 # 5.1. Inventory memenuhi demand (ci1)
for t in range(1, t_1+1):
    model_1.addConstr((inventory_1[t-1] + kuantitas_1[t-1] - demand_1[t-1]) == inventory_1[t], "c11")
for t in range(1, t_2+1):
    model_2.addConstr((inventory_2[t-1] + kuantitas_2[t-1] - demand_2[t-1]) == inventory_2[t], "c21")
for t in range(1, t_3+1):
    model_3.addConstr((inventory_3[t-1] + kuantitas_3[t-1] - demand_3[t-1]) == inventory_3[t], "c31")

 # 5.2. Hubungan kuantitas dan keputusan pesan memenuhi persamaan dengan Big M-value (ci2)
for t in periode_1:
    model_1.addConstr((kuantitas_1[t] <= M_1[t]*is_order_1[t]), "c12")
for t in periode_2:
    model_2.addConstr((kuantitas_2[t] <= M_2[t]*is_order_2[t]), "c22")
for t in periode_3:
    model_3.addConstr((kuantitas_3[t] <= M_3[t]*is_order_3[t]), "c32")
    
 # 5.3. Inventory tidak melebihi kapasitas gudang (ci3)
for t in periode_1:
    model_1.addConstr((inventory_1[t] <= kapasitas_gudang_1), "c13")
for t in periode_2:
    model_2.addConstr((inventory_2[t] <= kapasitas_gudang_2), "c23")
for t in periode_3:
    model_3.addConstr((inventory_3[t] <= kapasitas_gudang_3), "c33")

 # 5.4. Inventory setiap periode lebih dari safety stock yang telah ditetapkan (ci4)
for t in range(1, t_1+1):
  model_1.addConstr(inventory_1[t-1] >= safety_stock_1, "c14")
for t in range(1, t_2+1):
  model_2.addConstr(inventory_2[t-1] >= safety_stock_2, "c24")
for t in range(1, t_3+1):
  model_3.addConstr(inventory_3[t-1] >= safety_stock_3, "c34")

 # 5.6. Non-negativity constraint (ci6)
for t in periode_1: 
    model_1.addConstr((is_order_1[t] >= 0), "c16")
    model_1.addConstr((kuantitas_1[t] >= 0), "c16")
    model_1.addConstr((inventory_1[t] >= 0), "c16")
for t in periode_2: 
    model_2.addConstr((is_order_2[t] >= 0), "c26")
    model_2.addConstr((kuantitas_2[t] >= 0), "c26")
    model_2.addConstr((inventory_2[t] >= 0), "c26")
for t in periode_3: 
    model_3.addConstr((is_order_3[t] >= 0), "c36")
    model_3.addConstr((kuantitas_3[t] >= 0), "c36")
    model_3.addConstr((inventory_3[t] >= 0), "c36")

 # 5.5. Inventory awal (ci5)
model_1.addConstr(inventory_1[0] == inventory_awal_1, "c15")
model_2.addConstr(inventory_2[0] == inventory_awal_2, "c25")
model_3.addConstr(inventory_3[0] == inventory_awal_3, "c35")

 # 5.6. Inventory akhir sama dengan safety stock (ci6)
model_1.addConstr(inventory_1[t_1] == inventory_akhir_1, "c16")
model_2.addConstr(inventory_2[t_2] == inventory_akhir_2, "c26")
model_3.addConstr(inventory_3[t_3] == inventory_akhir_3, "c36")

# 6. Optimasi 
model_1.optimize()
model_2.optimize()
model_3.optimize()

# 7. Analisis & Visualisasi hasil
# for v in model_1.getVars():
#     if v.varName.startswith("k"):
#         print("Order {} kg bahan baku{} pada periode {}".format(abs(round((v.x),0)), v.varName[9:11], v.varName[11:]))

# minimum_cost_1 = round(model_1.objVal,0)
# print("--------------------------------")
# print("Total biaya persediaan minimum: Rp. {}".format(minimum_cost_1))
# print("--------------------------------")

# for v in model_2.getVars():
#     if v.varName.startswith("k"):
#         print("Order {} kg bahan baku{} pada periode {}".format(abs(round((v.x),0)), v.varName[9:11], v.varName[11:]))

# minimum_cost_2 = round(model_2.objVal,0)
# print("--------------------------------")
# print("Total biaya persediaan minimum: Rp. {}".format(minimum_cost_2))
# print("--------------------------------")

# for v in model_3.getVars():
#     if v.varName.startswith("k"):
#         print("Order {} kg bahan baku{} pada periode {}".format(abs(round((v.x),0)), v.varName[9:11], v.varName[11:]))

# minimum_cost_3 = round(model_3.objVal,0)
# print("--------------------------------")
# print("Total biaya persediaan minimum: Rp. {}".format(minimum_cost_3))
# print("--------------------------------")

kolom_is_order_1 = pd.DataFrame(columns=["is_Order_1"])
for o in is_order_1.values():
  kolom_is_order_1 = kolom_is_order_1.append({"is_Order_1": int(abs(o.X))}, ignore_index=True)  

kolom_quantity_1 = pd.DataFrame(columns=["Quantity_1"])
for q in kuantitas_1.values():
  kolom_quantity_1 = kolom_quantity_1.append({"Quantity_1": round(int(abs(q.X)),0)}, ignore_index=True)  

kolom_inventory_1 = pd.DataFrame(columns=["Inventory_1"])
for i in inventory_1.values():
  kolom_inventory_1 = kolom_inventory_1.append({"Inventory_1": round(abs(i.X),0)}, ignore_index=True)  
kolom_inventory_1 = kolom_inventory_1.drop(labels=t_1, axis=0)

kolom_demand_1 = round(pd.DataFrame(demand_1, columns = ["Demand_1"]),0)

table_1 = pd.concat([kolom_demand_1, kolom_inventory_1, kolom_is_order_1, kolom_quantity_1], axis='columns')
print(table_1)
print("--------------------------------")

kolom_is_order_2 = pd.DataFrame(columns=["is_Order_2"])
for o in is_order_2.values():
  kolom_is_order_2 = kolom_is_order_2.append({"is_Order_2": int(abs(o.X))}, ignore_index=True)  

kolom_quantity_2 = pd.DataFrame(columns=["Quantity_2"])
for q in kuantitas_2.values():
  kolom_quantity_2 = kolom_quantity_2.append({"Quantity_2": round(int(abs(q.X)),0)}, ignore_index=True)  

kolom_inventory_2 = pd.DataFrame(columns=["Inventory_2"])
for i in inventory_2.values():
  kolom_inventory_2 = kolom_inventory_2.append({"Inventory_2": round(abs(i.X),0)}, ignore_index=True)  
kolom_inventory_2 = kolom_inventory_2.drop(labels=t_2, axis=0)

kolom_demand_2 = round(pd.DataFrame(demand_2, columns = ["Demand_2"]),0)

table_2 = pd.concat([kolom_demand_2, kolom_inventory_2, kolom_is_order_2, kolom_quantity_2], axis='columns')
print(table_2)
print("--------------------------------")

kolom_is_order_3 = pd.DataFrame(columns=["is_Order_3"])
for o in is_order_3.values():
  kolom_is_order_3 = kolom_is_order_3.append({"is_Order_3": int(abs(o.X))}, ignore_index=True)  

kolom_quantity_3 = pd.DataFrame(columns=["Quantity_3"])
for q in kuantitas_3.values():
  kolom_quantity_3 = kolom_quantity_3.append({"Quantity_3": round(int(abs(q.X)),0)}, ignore_index=True)  

kolom_inventory_3 = pd.DataFrame(columns=["Inventory_3"])
for i in inventory_3.values():
  kolom_inventory_3 = kolom_inventory_3.append({"Inventory_3": round(abs(i.X),0)}, ignore_index=True)  
kolom_inventory_3 = kolom_inventory_3.drop(labels=t_3, axis=0)

kolom_demand_3 = round(pd.DataFrame(demand_3, columns = ["Demand_3"]),0)

table_3 = pd.concat([kolom_demand_3, kolom_inventory_3, kolom_is_order_3, kolom_quantity_3], axis='columns')
print(table_3)
print("--------------------------------")

table_4 = pd.concat([kolom_demand_1, kolom_demand_2, kolom_demand_3, kolom_inventory_1, kolom_inventory_2, kolom_inventory_3, kolom_is_order_1, kolom_quantity_1, kolom_is_order_2, kolom_quantity_2, kolom_is_order_3, kolom_quantity_3], axis = 1)
print(table_4)
print("--------------------------------")

# ind = np.arange(t_1) 
# width = 0.25

# xvals = table_1.Quantity_1
# bar1_1 = plt.bar(ind, xvals, width, color = 'b')
  
# yvals = table_1.Demand_1
# bar2_1 = plt.bar(ind+width, yvals, width, color='r')
  
# zvals = table_1.Inventory_1
# bar3_1 = plt.bar(ind+width*2, zvals, width, color = 'g')
  
# plt.xlabel("Periode")
# plt.ylabel('Kuantitas')
# plt.title("Perencanaan Bahan Baku 1 Optimal (Biaya Minimum)")
  
# plt.xticks(ind+width,ind)
# plt.legend((bar1_1, bar2_1, bar3_1), ('Pesan Q&T', 'Demand', 'Inventory'))
# plt.show()

# ind = np.arange(t_2) 
# width = 0.25

# xvals = table_2.Quantity_2
# bar1_2 = plt.bar(ind, xvals, width, color = 'b')
  
# yvals = table_2.Demand_2
# bar2_2 = plt.bar(ind+width, yvals, width, color='r')
  
# zvals = table_2.Inventory_2
# bar3_2 = plt.bar(ind+width*2, zvals, width, color = 'g')
  
# plt.xlabel("Periode")
# plt.ylabel('Kuantitas')
# plt.title("Perencanaan Bahan Baku 2 Optimal (Biaya Minimum)")
  
# plt.xticks(ind+width,ind)
# plt.legend((bar1_2, bar2_2, bar3_2), ('Pesan Q&T', 'Demand', 'Inventory'))
# plt.show()

# ind = np.arange(t_3) 
# width = 0.25

# xvals = table_3.Quantity_3
# bar1_3 = plt.bar(ind, xvals, width, color = 'b')
  
# yvals = table_3.Demand_3
# bar2_3 = plt.bar(ind+width, yvals, width, color='r')
  
# zvals = table_3.Inventory_3
# bar3_3 = plt.bar(ind+width*2, zvals, width, color = 'g')
  
# plt.xlabel("Periode")
# plt.ylabel('Kuantitas')
# plt.title("Perencanaan Bahan Baku 3 Optimal (Biaya Minimum)")
  
# plt.xticks(ind+width,ind)
# plt.legend((bar1_3, bar2_3, bar3_3), ('Pesan Q&T', 'Demand', 'Inventory'))
# plt.show()

# 8. Status
status_1 = model_1.status
if status_1 == GRB.Status.OPTIMAL:
    print('[model bahan baku 1 sudah optimal]')
if status_1 == GRB.Status.INF_OR_UNBD or status_1 == GRB.Status.INFEASIBLE  or status_1 == GRB.Status.UNBOUNDED:
    print('[model 2 infeasible atau unbounded]')
if status_1 != GRB.Status.OPTIMAL:
    print('Optimasi belum optimal')
    
status_2 = model_2.status
if status_2 == GRB.Status.OPTIMAL:
    print('[model bahan baku 2 sudah optimal]')
if status_2 == GRB.Status.INF_OR_UNBD or status_2 == GRB.Status.INFEASIBLE  or status_2 == GRB.Status.UNBOUNDED:
    print('[model infeasible atau unbounded]')
if status_2 != GRB.Status.OPTIMAL:
    print('Optimasi belum optimal')

status_3 = model_3.status
if status_3 == GRB.Status.OPTIMAL:
    print('[model bahan baku 3 sudah optimal]')
if status_3 == GRB.Status.INF_OR_UNBD or status_3 == GRB.Status.INFEASIBLE  or status_3 == GRB.Status.UNBOUNDED:
    print('[model infeasible atau unbounded]')
if status_3 != GRB.Status.OPTIMAL:
    print('Optimasi belum optimal')
    
#9. Download
#model_1.write("Perencanaan-Persediaan-Optimal.sol")
#model_2.write("Perencanaan-Persediaan-Optimal.lp")
#model_3.write("Perencanaan-Persediaan-Optimal.mps")

#10. Export model output to Excel
# output_path = r'C:\Users\Yulius\OneDrive\Documents\Dokumen Julio\Skripsi\Sidang\Output Data Model Final Forecast.xlsx'
# writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
# table_4.to_excel(writer, sheet_name = 'Output_All', index = True)
# writer.save()
