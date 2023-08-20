a = """Academic license - for non-commercial use only - expires 2023-11-23
Gurobi Optimizer version 10.0.0 build v10.0.0rc2 (win64)
CPU model: Intel(R) Core(TM) i5-10300H CPU @ 2.50GHz, instruction set [SSE2|AVX|AVX2]
Thread count: 4 physical cores, 8 logical processors, using up to 8 threads

Optimize a model with 1098 rows, 471 columns and 1566 nonzeros
Model fingerprint: 0x081b8dc7, 0x84384ad4, 0x7d9b9034
Variable types: 315 continuous, 156 integer (156 binary)
Found heuristic solution: objective 1.643115e+08, 1.129931e+08, 3.281822e+07
Presolve removed 810 rows and 33 columns
Presolve time: 0.00s
Presolved:288 rows, 438 columns, 723 nonzeros
Variable types: 288 continuous, 150 integer (150 binary)

Root relaxation model bahan baku 1: objective 1.172338e+08, 46 iterations, 0.02 seconds (0.00 work units)

    Nodes    |    Current Node    |     Objective Bounds      |     Work
 Expl Unexpl |  Obj  Depth IntInf | Incumbent    BestBd   Gap | It/Node Time

     0     0 1.1723e+08    0   44 1.6431e+08 1.1723e+08  28.7%     -    0s
H    0     0                    1.220711e+08 1.1723e+08  3.96%     -    0s

Root relaxation model bahan baku 2: objective 8.185356e+07, 46 iterations, 0.00 seconds (0.00 work units)
    Nodes    |    Current Node    |     Objective Bounds      |     Work
 Expl Unexpl |  Obj  Depth IntInf | Incumbent    BestBd   Gap | It/Node Time

     0     0 8.1854e+07    0   44 1.1299e+08 8.1854e+07  27.6%     -    0s
H    0     0                    8.677946e+07 8.1854e+07  5.68%     -    0s
     0     0     cutoff    0      8.6779e+07 8.6779e+07  0.00%     -    0s

Root relaxation model bahan baku 3: objective 1.044187e+08, 46 iterations, 0.00 seconds (0.00 work units)

    Nodes    |    Current Node    |     Objective Bounds      |     Work
 Expl Unexpl |  Obj  Depth IntInf | Incumbent    BestBd   Gap | It/Node Time

     0     0 1.0442e+08    0   44 1.4376e+08 1.0442e+08  27.4%     -    0s
H    0     0                    1.092970e+08 1.0442e+08  4.46%     -    0s
     0     0     cutoff    0      1.0930e+08 1.0930e+08  0.00%     -    0s
     
Cutting planes: (model 1, 2, 3)
  Cover: 0, 2, 2
  Implied bound: 30, 84, 82
  MIR: 1, 2, 2
  Flow cover: 2, 2, 2
  Flow path: 0, 5, 2

Explored 1 nodes (226 simplex iterations) in 0.08 seconds (0.00 work units)
Thread count was 8 (of 8 available processors)

Solution count 2: 1.22071e+08 1.64312e+08
Solution count 2: 8.67795e+07 1.12993e+08 
Solution count 2: 1.09297e+08 1.43763e+08  

Optimal solution found (tolerance 1.00e-04)
Best objective 1.220711040000e+08, best bound 1.220711040000e+08, gap 0.0000%
Optimal solution found (tolerance 1.00e-04)
Best objective 8.677945600000e+07, best bound 8.677945600000e+07, gap 0.0000%   
Optimal solution found (tolerance 1.00e-04)
Best objective 1.092970453000e+08, best bound 1.092970453000e+08, gap 0.0000%
"""

print(a)