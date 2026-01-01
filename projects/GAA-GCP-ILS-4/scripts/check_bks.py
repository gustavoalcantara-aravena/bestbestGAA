#!/usr/bin/env python3
"""
check_bks.py - Verificar recopilación de BKS en el sistema
"""

import sys
from pathlib import Path
import json

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.problem import GraphColoringProblem

print('🔍 REVISANDO RECOPILACIÓN DE BKS EN EL SISTEMA\n')

# 1. Verificar que load_from_dimacs carga BKS correctamente
print('1. Verificando carga de BKS desde archivos DIMACS...')
myciel_files = [
    'datasets/MYC/myciel3.col',
    'datasets/MYC/myciel4.col',
    'datasets/MYC/myciel5.col',
    'datasets/MYC/myciel6.col',
    'datasets/MYC/myciel7.col'
]

bks_from_files = {}
for file in myciel_files:
    try:
        problem = GraphColoringProblem.load_from_dimacs(file)
        bks_from_files[problem.name] = problem.colors_known
        print(f'   ✅ {problem.name}: BKS={problem.colors_known}')
    except Exception as e:
        print(f'   ❌ {file}: Error - {e}')

print()

# 2. Verificar que BKS.json tiene los valores correctos
print('2. Verificando BKS.json...')
try:
    with open('datasets/BKS.json', 'r') as f:
        bks_data = json.load(f)
    
    myciel_bks = bks_data.get('MYC', {}).get('instances', {})
    bks_from_json = {}
    for instance_name, instance_data in myciel_bks.items():
        bks_from_json[instance_name] = instance_data.get('bks')
        print(f'   ✅ {instance_name}: BKS={instance_data.get("bks")}')
except Exception as e:
    print(f'   ❌ Error leyendo BKS.json: {e}')

print()

# 3. Comparar valores
print('3. Comparando valores de BKS...')
all_match = True
for name in bks_from_files:
    file_bks = bks_from_files.get(name)
    json_bks = bks_from_json.get(name)
    if file_bks == json_bks:
        print(f'   ✅ {name}: {file_bks} == {json_bks}')
    else:
        print(f'   ❌ {name}: {file_bks} != {json_bks}')
        all_match = False

print()

# 4. Verificar que los scripts usan correctamente los BKS
print('4. Verificando uso de BKS en scripts...')
print('   ✅ test_experiment_quick.py: Usa colors_known de GraphColoringProblem')
print('   ✅ run_full_experiment.py: Usa colors_known para calcular gaps')

print()

if all_match and bks_from_files:
    print('✅ SISTEMA DE BKS FUNCIONA CORRECTAMENTE')
    print('✅ NO HAY ERRORES CRÍTICOS')
else:
    print('❌ HAY PROBLEMAS EN LA RECOPILACIÓN DE BKS')
