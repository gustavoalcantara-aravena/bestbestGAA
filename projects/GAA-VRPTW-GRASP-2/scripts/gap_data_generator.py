"""
Generador de datos JSON con GAP para gráficos comparativos
Separa la generación de datos de la visualización
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any

# BKS - Best Known Solutions (Solomon VRPTW)
BKS = {
    'C101': 828.94, 'C102': 828.94, 'C103': 828.94, 'C104': 828.94, 'C105': 828.94,
    'C106': 828.94, 'C107': 828.94, 'C108': 828.94, 'C109': 828.94,
    'C201': 589.86, 'C202': 589.86, 'C203': 589.86, 'C204': 589.86, 'C205': 589.86,
    'C206': 589.86, 'C207': 589.86, 'C208': 589.86,
    'R101': 1650.80, 'R102': 1486.12, 'R103': 1292.65, 'R104': 1109.80, 'R105': 1377.11,
    'R106': 1251.43, 'R107': 1104.28, 'R108': 960.88, 'R109': 1194.73, 'R110': 1118.60,
    'R111': 1096.72, 'R112': 948.14,
    'R201': 1252.37, 'R202': 1191.70, 'R203': 939.54, 'R204': 825.52, 'R205': 994.42,
    'R206': 906.14, 'R207': 890.60, 'R208': 726.82, 'R209': 909.23, 'R210': 939.40,
    'R211': 885.84,
    'RC101': 1696.94, 'RC102': 1554.75, 'RC103': 1460.99, 'RC104': 1357.04, 
    'RC105': 1629.44, 'RC106': 1446.43, 'RC107': 1371.16, 'RC108': 1117.75,
    'RC201': 1406.91, 'RC202': 1365.64, 'RC203': 1057.46, 'RC204': 798.46, 
    'RC205': 1297.65, 'RC206': 1143.32, 'RC207': 1061.14, 'RC208': 880.59,
}


def generate_gap_data_json(csv_path: str, output_path: str) -> Dict[str, Any]:
    """
    Lee CSV de resultados y genera JSON con datos de GAP
    
    Args:
        csv_path: Ruta al CSV de raw_results
        output_path: Ruta donde guardar el JSON
    
    Returns:
        Dict con datos de GAP organizados por instancia y algoritmo
    """
    csv_path = Path(csv_path)
    output_path = Path(output_path)
    
    if not csv_path.exists():
        print(f"[ERROR] CSV no encontrado: {csv_path}")
        return {}
    
    # Leer CSV
    df = pd.read_csv(csv_path)
    
    # Estructura para almacenar datos de GAP
    gap_data = {
        'metadata': {
            'csv_source': str(csv_path),
            'total_instances': len(df['instance_id'].unique()),
            'algorithms': sorted(df['algorithm'].unique().tolist()),
            'timestamp': pd.Timestamp.now().isoformat(),
        },
        'instances': {}
    }
    
    # Procesar cada instancia
    for instance_id in sorted(df['instance_id'].unique()):
        instance_data = df[df['instance_id'] == instance_id]
        
        # Extraer familia
        family = instance_id[0] if instance_id[0] in ['C', 'R'] else instance_id[:2]
        if family == 'C' and len(instance_id) > 1 and instance_id[1].isdigit():
            family = family + instance_id[1]
        elif family == 'R' and len(instance_id) > 1 and instance_id[1].isdigit():
            family = family + instance_id[1]
        elif family in ['RC']:
            family = family + instance_id[2]
        
        bks = BKS.get(instance_id, None)
        
        algorithms_data = {}
        
        # Procesar cada algoritmo para esta instancia
        for algo in sorted(instance_data['algorithm'].unique()):
            algo_row = instance_data[instance_data['algorithm'] == algo].iloc[0]
            
            d_final = float(algo_row['d_final'])
            d_bks = float(algo_row['d_bks'])
            
            # Calcular GAP
            if bks and bks > 0:
                gap_percent = ((d_final - bks) / bks) * 100
            else:
                gap_percent = None
            
            algo_num = algo.split('_')[-1]
            
            algorithms_data[f'algo{algo_num}'] = {
                'name': algo,
                'distance': round(d_final, 2),
                'd_bks': round(d_bks, 2),
                'bks': round(bks, 2) if bks else None,
                'gap_percent': round(gap_percent, 2) if gap_percent else None,
                'time_sec': round(float(algo_row['time_sec']), 4),
                'feasible': bool(algo_row['feasible']),
                'k_bks': int(algo_row['k_bks']) if pd.notna(algo_row['k_bks']) else None,
                'k_final': int(algo_row['k_final']) if pd.notna(algo_row['k_final']) else None,
            }
        
        gap_data['instances'][instance_id] = {
            'family': family,
            'bks': round(bks, 2) if bks else None,
            'algorithms': algorithms_data
        }
    
    # Agregar estadísticas por algoritmo
    gap_data['summary_by_algorithm'] = {}
    
    for algo in gap_data['metadata']['algorithms']:
        algo_num = algo.split('_')[-1]
        algo_gaps = []
        algo_distances = []
        
        for instance_data in gap_data['instances'].values():
            algo_key = f'algo{algo_num}'
            if algo_key in instance_data['algorithms']:
                gap = instance_data['algorithms'][algo_key]['gap_percent']
                distance = instance_data['algorithms'][algo_key]['distance']
                if gap is not None:
                    algo_gaps.append(gap)
                algo_distances.append(distance)
        
        if algo_gaps:
            gap_data['summary_by_algorithm'][algo_num] = {
                'name': algo,
                'avg_distance': round(sum(algo_distances) / len(algo_distances), 2),
                'std_distance': round(
                    (sum((x - sum(algo_distances)/len(algo_distances))**2 
                    for x in algo_distances) / len(algo_distances))**0.5, 2),
                'avg_gap': round(sum(algo_gaps) / len(algo_gaps), 2),
                'std_gap': round(
                    (sum((x - sum(algo_gaps)/len(algo_gaps))**2 
                    for x in algo_gaps) / len(algo_gaps))**0.5, 2),
                'min_gap': round(min(algo_gaps), 2),
                'max_gap': round(max(algo_gaps), 2),
                'count_instances': len(algo_distances),
            }
    
    # Guardar JSON
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(gap_data, f, indent=2)
    
    print(f"[OK] Datos de GAP guardados en: {output_path}")
    
    return gap_data


def load_gap_data_json(json_path: str) -> Dict[str, Any]:
    """Carga datos de GAP desde JSON"""
    json_path = Path(json_path)
    if not json_path.exists():
        print(f"[ERROR] JSON no encontrado: {json_path}")
        return {}
    
    with open(json_path, 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python gap_data_generator.py <ruta_csv> [ruta_output]")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else csv_path.replace('.csv', '_gap_data.json')
    
    generate_gap_data_json(csv_path, output_path)
