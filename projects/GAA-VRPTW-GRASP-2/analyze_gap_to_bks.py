#!/usr/bin/env python3
"""
Analyze GAP to Best Known Solutions (BKS) for Solomon VRPTW instances
BKS values from: http://web.cba.neu.edu/~msolomon/vrptw.htm
"""

import pandas as pd
import numpy as np

# Best Known Solutions (Distance) for Solomon VRPTW
# Source: Gehring & Homberger (2001) and subsequent literature
BKS = {
    # C1 family (100 customers, short horizon)
    'C101': 828.94,
    'C102': 828.94,
    'C103': 828.94,
    'C104': 828.94,
    'C105': 828.94,
    'C106': 828.94,
    'C107': 828.94,
    'C108': 828.94,
    'C109': 828.94,
    
    # C2 family (100 customers, long horizon)
    'C201': 589.86,
    'C202': 589.86,
    'C203': 589.86,
    'C204': 589.86,
    'C205': 589.86,
    'C206': 589.86,
    'C207': 589.86,
    'C208': 589.86,
    
    # R1 family (100 customers, short horizon)
    'R101': 1650.80,
    'R102': 1486.12,
    'R103': 1292.65,
    'R104': 1084.39,
    'R105': 1377.11,
    'R106': 1252.89,
    'R107': 1104.86,
    'R108': 960.88,
    'R109': 1194.73,
    'R110': 1118.60,
    'R111': 1096.72,
    'R112': 948.14,
    
    # R2 family (1000 customers, long horizon)
    'R201': 1252.37,
    'R202': 1191.70,
    'R203': 939.54,
    'R204': 825.52,
    'R205': 994.42,
    'R206': 906.14,
    'R207': 890.84,
    'R208': 726.82,
    'R209': 909.13,
    'R210': 939.49,
    'R211': 885.84,
    
    # RC1 family (100 customers, short horizon, mix)
    'RC101': 1696.94,
    'RC102': 1554.75,
    'RC103': 1258.00,
    'RC104': 1132.33,
    'RC105': 1629.44,
    'RC106': 1446.43,
    'RC107': 1298.76,
    'RC108': 1117.75,
    
    # RC2 family (100 customers, long horizon, mix)
    'RC201': 1406.91,
    'RC202': 1365.64,
    'RC203': 1057.46,
    'RC204': 798.46,
    'RC205': 1297.65,
    'RC206': 1143.32,
}

# Read the FULL experiment results
df = pd.read_csv(
    'output/vrptw_experiments_FULL_03-01-26_02-18-27/results/raw_results_detailed.csv'
)

# Filter for Algorithm 2 only
algo2 = df[df['algorithm'] == 'GAA_Algorithm_2'].copy()

# Add BKS values
algo2['bks'] = algo2['instance_id'].map(BKS)

# Calculate GAP
algo2['gap_abs'] = algo2['d_final'] - algo2['bks']
algo2['gap_pct'] = ((algo2['d_final'] - algo2['bks']) / algo2['bks'] * 100).round(2)

# Analysis
print("=" * 90)
print("ALGORITHM 2: GAP ANALYSIS vs BEST KNOWN SOLUTIONS (BKS)")
print("=" * 90)
print()

# Overall statistics
print("GLOBAL STATISTICS")
print("-" * 90)
print(f"Total Instances: {len(algo2)}")
print(f"Avg GAP: {algo2['gap_pct'].mean():.2f}%")
print(f"Median GAP: {algo2['gap_pct'].median():.2f}%")
print(f"Min GAP: {algo2['gap_pct'].min():.2f}% (instance: {algo2.loc[algo2['gap_pct'].idxmin(), 'instance_id']})")
print(f"Max GAP: {algo2['gap_pct'].max():.2f}% (instance: {algo2.loc[algo2['gap_pct'].idxmax(), 'instance_id']})")
print(f"Std Dev: {algo2['gap_pct'].std():.2f}%")
print()

# Hit statistics
hit_count = len(algo2[algo2['gap_pct'] <= 5])
print(f"Solutions within 5% of BKS: {hit_count}/{len(algo2)} ({100*hit_count/len(algo2):.1f}%)")
print(f"Solutions within 10% of BKS: {len(algo2[algo2['gap_pct'] <= 10])}/{len(algo2)}")
print(f"Solutions within 15% of BKS: {len(algo2[algo2['gap_pct'] <= 15])}/{len(algo2)}")
print(f"Solutions at BKS (GAP=0%): {len(algo2[algo2['gap_pct'] == 0])}/{len(algo2)}")
print()

# Per-family analysis
print("PERFORMANCE BY FAMILY")
print("-" * 90)
for family in ['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2']:
    family_data = algo2[algo2['family'] == family]
    if len(family_data) > 0:
        print(f"{family:3} (n={len(family_data):2}): Avg GAP = {family_data['gap_pct'].mean():6.2f}%, "
              f"Min = {family_data['gap_pct'].min():6.2f}%, Max = {family_data['gap_pct'].max():6.2f}%")
print()

# Detailed results - best performers
print("TOP 10 BEST SOLUTIONS (Lowest GAP)")
print("-" * 90)
best10 = algo2.nsmallest(10, 'gap_pct')[['instance_id', 'd_final', 'bks', 'gap_abs', 'gap_pct']]
for idx, row in best10.iterrows():
    print(f"{row['instance_id']:6} | Distance: {row['d_final']:8.2f} | BKS: {row['bks']:8.2f} | "
          f"GAP: {row['gap_abs']:7.2f} units ({row['gap_pct']:6.2f}%)")
print()

# Detailed results - worst performers
print("TOP 10 WORST SOLUTIONS (Highest GAP)")
print("-" * 90)
worst10 = algo2.nlargest(10, 'gap_pct')[['instance_id', 'd_final', 'bks', 'gap_abs', 'gap_pct']]
for idx, row in worst10.iterrows():
    print(f"{row['instance_id']:6} | Distance: {row['d_final']:8.2f} | BKS: {row['bks']:8.2f} | "
          f"GAP: {row['gap_abs']:7.2f} units ({row['gap_pct']:6.2f}%)")
print()

# Export detailed results
algo2_sorted = algo2.sort_values('gap_pct')
algo2_sorted[['instance_id', 'family', 'k_final', 'd_final', 'bks', 'gap_abs', 'gap_pct', 'time_sec']].to_csv(
    'algo2_gap_analysis.csv', index=False
)
print(f"Detailed results saved to: algo2_gap_analysis.csv")
print("=" * 90)
