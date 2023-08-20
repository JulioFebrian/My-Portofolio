a = """Gurobi Optimizer version 10.0.0 build v10.0.0rc2 (win64)
CPU model: Intel(R) Core(TM) i5-10300H CPU @ 2.50GHz, instruction set [SSE2|AVX|AVX2]
Thread count: 4 physical cores, 8 logical processors, using up to 8 threads

Optimize a model with 1098 rows, 471 columns and 1566 nonzeros
Model fingerprint: 0xaf0951af
Variable types: 315 continuous, 156 integer (156 binary)
Coefficient statistics:
  Matrix range     [1e+00, 1e+06]
  Objective range  [1e+01, 1e+05]
  Bounds range     [1e+00, 1e+00]
  RHS range        [1e+04, 1e+06]
Found heuristic solution: objective 4.002105e+07, 2.492695e+07, 3.281822e+07
Presolve removed 810 rows and 33 columns
Presolve time: 0.00s
Presolved:288 rows, 438 columns, 723 nonzeros
Variable types: 288 continuous, 150 integer (150 binary)

Root relaxation 1: objective 2.006112e+08, 46 iterations, 0.00 seconds (0.00 work units)

    Nodes    |    Current Node    |     Objective Bounds      |     Work
 Expl Unexpl |  Obj  Depth IntInf | Incumbent    BestBd   Gap | It/Node Time

     0     0 2.0061e+08    0   44 2.4518e+08 2.0061e+08  18.2%     -    0s
H    0     0                    2.054484e+08 2.0061e+08  2.35%     -    0s

Root relaxation 2: objective 1.127925e+08, 46 iterations, 0.00 seconds (0.00 work units)

    Nodes    |    Current Node    |     Objective Bounds      |     Work
 Expl Unexpl |  Obj  Depth IntInf | Incumbent    BestBd   Gap | It/Node Time

     0     0 1.1279e+08    0   44 1.3952e+08 1.1279e+08  19.2%     -    0s
H    0     0                    1.177184e+08 1.1279e+08  4.18%     -    0s
     0     0     cutoff    0      1.1772e+08 1.1772e+08  0.00%     -    0s
     
Root relaxation: objective 1.585538e+08, 46 iterations, 0.00 seconds (0.00 work units)

    Nodes    |    Current Node    |     Objective Bounds      |     Work
 Expl Unexpl |  Obj  Depth IntInf | Incumbent    BestBd   Gap | It/Node Time

     0     0 1.5855e+08    0   44 1.9476e+08 1.5855e+08  18.6%     -    0s
H    0     0                    1.634321e+08 1.5855e+08  2.98%     -    0s

Cutting planes: (model 1, 2, 3)
  Gomory: 0, 0, 1
  Cover: 0, 2, 0
  Implied bound: 8, 84, 20
  MIR: 0, 2, 0
  Flow cover: 0, 2, 2
  Flow path: 0, 3, 0

Explored 1 nodes (182 simplex iterations) in 0.09 seconds (0.00 work units)
Thread count was 8 (of 8 available processors)

Solution count 2: 2.05448e+08 2.45179e+08
Solution count 2: 1.17718e+08 1.39521e+08 
Solution count 2: 1.63432e+08 1.9476e+08 

Optimal solution found (tolerance 1.00e-04)
Best objective 2.054484400000e+08, best bound 2.054484400000e+08, gap 0.0000%
Optimal solution found (tolerance 1.00e-04)
Best objective 1.177183500000e+08, best bound 1.177183500000e+08, gap 0.0000%
Optimal solution found (tolerance 1.00e-04)
Best objective 1.634321090000e+08, best bound 1.634321090000e+08, gap 0.0000%
"""

print(a)

b = """
Optimize a model with 1098 rows, 471 columns and 1566 nonzeros
Model fingerprint: 0x081b8dc7, 0x84384ad4, 0x7d9b9034
Variable types: 315 continuous, 156 integer (156 binary)
Explored 1 nodes (182 simplex iterations) in 0.09 seconds (0.00 work units)
Bahan Baku 1 (Clear):
Optimal solution found (tolerance 1.00e-04)
Best objective 1.220711040000e+08, best bound 1.220711040000e+08, gap 0.0000%
Bahan Baku 2 (Light Blue):
Optimal solution found (tolerance 1.00e-04)
Best objective 8.677945600000e+07, best bound 8.677945600000e+07, gap 0.0000%   
Bahan Baku 3 (Mix):
Optimal solution found (tolerance 1.00e-04)
Best objective 1.092970453000e+08, best bound 1.092970453000e+08, gap 0.0000%
--------------------------------
Total biaya persediaan minimum bahan baku 1 (Clear): Rp. 122071104.0
--------------------------------
Total biaya persediaan minimum bahan baku 2 (Light Blue): Rp. 86779456.0
--------------------------------
Total biaya persediaan minimum bahan baku 3 (Mix): Rp. 109297045.0
--------------------------------
Total biaya persediaan minimum ketiga bahan baku: Rp. 318147605.0
"""

print(b)