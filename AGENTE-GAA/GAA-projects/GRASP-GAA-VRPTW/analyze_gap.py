import json
import csv

# Cargar BKS
bks_data = {}
try:
    with open('03-data/best_known_solutions-Solomon-VRPTW-Dataset.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            instance = row['instance_id'].strip()
            bks_data[instance] = {
                'vehicles': int(row['k_bks']),
                'distance': float(row['d_bks'])
            }
except FileNotFoundError:
    print('Archivo BKS no encontrado')

# Cargar resultados
with open('output/Canary_RUN_2026-01-04_02-21-05/canary_results.json', 'r') as f:
    results = json.load(f)

# Agrupar por instancia
by_instance = {}
for r in results:
    inst = r['instance_id']
    if inst not in by_instance:
        by_instance[inst] = []
    by_instance[inst].append(r)

# Análisis GAP
print('=== ANÁLISIS GAP % ===')
print()

gaps_vehicles = []
gaps_distance = []

for inst_id in sorted(by_instance.keys()):
    results_inst = by_instance[inst_id]
    
    if inst_id in bks_data:
        bks = bks_data[inst_id]
        print(f'Instancia: {inst_id}')
        print(f'  BKS: {bks["vehicles"]} vehículos, {bks["distance"]:.1f} km')
        print(f'  Algoritmo | Vehículos | Distancia | GAP% Vehículos | GAP% Distancia')
        print(f'  ' + '-'*70)
        
        for r in sorted(results_inst, key=lambda x: x['algorithm_id']):
            algo = r['algorithm_id']
            vehicles = r['vehicles']
            distance = r['distance']
            
            # GAP de vehículos
            gap_vehicles = ((vehicles - bks['vehicles']) / bks['vehicles']) * 100
            gaps_vehicles.append(gap_vehicles)
            
            # GAP de distancia (solo si mismo número de vehículos)
            if vehicles == bks['vehicles']:
                gap_distance = ((distance - bks['distance']) / bks['distance']) * 100
                gap_str = f'{gap_distance:+.2f}%'
                gaps_distance.append(gap_distance)
            else:
                gap_distance = None
                gap_str = 'N/A (V diferente)'
            
            print(f'  {algo}         | {vehicles:9} | {distance:9.1f} | {gap_vehicles:+.2f}%         | {gap_str}')
        print()

# Resumen
print('=== RESUMEN DE GAPS ===')
if gaps_vehicles:
    print(f'Gap Vehículos:')
    print(f'  Promedio: {sum(gaps_vehicles)/len(gaps_vehicles):+.2f}%')
    print(f'  Min: {min(gaps_vehicles):+.2f}%')
    print(f'  Max: {max(gaps_vehicles):+.2f}%')
    print()

if gaps_distance:
    print(f'Gap Distancia (solo cuando V=V*):')
    print(f'  Promedio: {sum(gaps_distance)/len(gaps_distance):+.2f}%')
    print(f'  Min: {min(gaps_distance):+.2f}%')
    print(f'  Max: {max(gaps_distance):+.2f}%')
