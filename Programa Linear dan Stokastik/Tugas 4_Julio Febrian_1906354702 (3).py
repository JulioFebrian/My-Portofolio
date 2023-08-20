# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 15:25:37 2022

@author: Julio Febrian
"""

# Nama : Julio Febrian
# NPM  : 1906354702

# B-2 Flow-Shop Scheduling
# narasi Problem
"""A workshop that produces metal pipes on demand for the automobile industry has three machines for
bending the pipes, soldering the fastenings, and assembling the links. The workshop has to produce
six pieces, for which the durations of the processing steps (in minutes) are given in the following table.
Every workpiece first goes to bending, then to soldering, and finally to assembly of the links. Once
started, any operations must be carried out without interruption, but the workpieces may wait between
the machines.
Table 7.2: Processing durations in minutes
Workpiece 1 2 3 4 5 6
Bending 3 6 3 5 5 7
Soldering 5 4 2 4 4 5
Assembly 5 2 4 6 3 6
Every machine only processes one piece at a time. A workpiece may not overtake any other by passing
onto the following machine. This means that if at the beginning a sequence of the workpieces is established, they will be processed on every machine in exactly this order. Which is the sequence of workpieces
that minimizes the total time for completing all pieces?"""

# definisikan model gurobi
import gurobipy
from gurobipy import *

modelgurobi = Model()

# sets dan penjelasannya

NM = 3              # set of machines atau number of machines (NM), 
MACH = range(NM)    # index m
NJ = 6              # set of jobs atau number of jobs (NJ)
JOBS = range(NJ)    # index j
RANK = range(NJ)    # index k

""" dengan MACH = {1,...,NM} sebagai himpunan mesin 
# dan JOBS = {1,2,3,..., NJ} sebagai himpunan pieces untuk diproduksi
# Durasi pemrosesan bagian j pada mesin m diberikan oleh DURm,j
# Setiap pieces harus melewati mesin 1, . . . , NM secara berurutan, 
# tanpa bisa mendahului pieces lainnya. 
# Oleh karena itu, dapat ditentukan jadwal berdasarkan urutan awal pieces
 """

# parameters / data  dan penjelasannya
DUR_mj = [[3, 6, 3, 5, 5, 7],
        [5, 4, 2, 4, 4, 5],
        [5, 2, 4, 6, 3, 6]]

" sesuai pada tabel soal durasi tiap proses dalam menit "
" DUR_mj = durasi proses piece j pada machine m "

# decision variables dan penjelasannya
R_jk = modelgurobi.addVars(JOBS, RANK,
                vtype=GRB.BINARY,
                name="rank")

" Urutan pekerjaan dapat ditentukan dengan bantuan variabel biner rankjk "
" R_jk = Urutan dari tiap proses / jobs j pada posisi rank k "


"Dalam masalah ini relatif sulit untuk menghitung waktu mulai atau selesainya" 
"operasi dari jajaran. Untuk mendapatkan nilai-nilai ini, maka dibentuklah" 
"dua set variabel tambahan emptymk (E_mk) dan waitmk (w_mk)"

E_mk = modelgurobi.addVars(MACH, range(NJ-1),
                vtype=GRB.CONTINUOUS,
                name="empty")
" E_mk = waktu idle posisi proses k pada machine m "

w_mk = modelgurobi.addVars(range(NM-1), RANK,
                vtype=GRB.CONTINUOUS,
                name="wait")
" Durasi jadwal sebagai waktu tepat ketika mesin NM menyelesaikan proses terakhir"
" yaitu 1 jika dan hanya jika piece j mesin m memiliki rank (posisi) k pada urutan awal"
" w_mk = waktu tunggu pada m dengan rank k "

# objective function dan penjelasannya
modelgurobi.setObjective(quicksum(DUR_mj[i][j] * R_jk[j, 0]
                   for i in range(NM-1) for j in JOBS) +
               quicksum(E_mk[NM-1, k] for k in range(NJ-1)),
               GRB.MINIMIZE)
"objective function untuk meminimalkan durasi proses produksi yang dibutuhkan"

# constraints dan penjelasannya
""" Setiap job perlu diassigned sebuah rank
 Himpunan posisi awal RANKS adalah sama dengan JOBS 
 karena setiap pekerjaan harus diberi peringkat"""
for k in RANK:
    modelgurobi.addConstr(sum(R_jk[j, k] for j in JOBS) == 1,
                "Rank[%d]" % k)

"dan setiap peringkat harus ditempati oleh satu proses (job) saja"
for j in JOBS:
    modelgurobi.addConstr(sum(R_jk[j, k] for k in RANK) == 1,
                "Job[%d]" % j)

"Keenam workpieces dapat diproses tanpa berhenti pada machine pertama"
for k in range(NJ-1):
    modelgurobi.addConstr((E_mk[0, k]) == 0)

"Workpiece pertama dalam urutan dapat melalui semua mesin tanpa waktu tunggu"
for i in range(NM-1):
    modelgurobi.addConstr((w_mk[i, 0]) == 0)

"Menghubungkan variabel E_mk dan w_mk kepada variabel R_jk"
for i in range(NM-1):
    for k in range(NJ-1):
        modelgurobi.addConstr(E_mk[i, k] +
                    quicksum(DUR_mj[i][j] * R_jk[j, k+1] for j in JOBS)
                    == w_mk[i, k] + quicksum(DUR_mj[i+1][j] * R_jk[j, k] for j in JOBS) + 
                                             E_mk[i+1, k])

# Run optimasi dan penjelasannya
modelgurobi.optimize()

"""Running optimasi model gurobi untuk menemukan durasi minimun 
berdasarkan assignment rank k pada job j"""

# print hasil dan penjelasanny
for k in RANK:
    for j in JOBS:
        if R_jk[j, k].x > 0.99:
            print('Rank %d is assigned to Job %d' % (k+1, j+1))

"""
Solusi Optimal:
Rank 1 is assigned to Job 3
Rank 2 is assigned to Job 1
Rank 3 is assigned to Job 2
Rank 4 is assigned to Job 5
Rank 5 is assigned to Job 4
Rank 6 is assigned to Job 6
"""

