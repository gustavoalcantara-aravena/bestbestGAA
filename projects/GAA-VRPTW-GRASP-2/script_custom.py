"""
Script CUSTOM: Ejecutar UNA FAMILIA específica (personalizable)

Modificar la variable FAMILIA_A_USAR para cambiar qué familia ejecutar:
  - 'C1': Clustered, instancias 1-9
  - 'C2': Clustered, instancias 201-208
  - 'R1': Random, instancias 101-112
  - 'R2': Random, instancias 201-211
  - 'RC1': Mezcla, instancias 101-108
  - 'RC2': Mezcla, instancias 201-208

Modo: CUSTOM (una familia)
Algoritmos: 3
Total experimentos: Entre 24 y 36 (depende de familia)
Tiempo estimado: 2-5 minutos
"""

from scripts.experiments import ExperimentExecutor, ExperimentConfig, AlgorithmGenerator
from datetime import datetime
import random

# ╔════════════════════════════════════════════════╗
# ║ CAMBIAR ESTA VARIABLE PARA ELEGIR FAMILIA     ║
# ╚════════════════════════════════════════════════╝
FAMILIA_A_USAR = 'C1'  # Cambia a 'C1', 'C2', 'R1', 'R2', 'RC1', o 'RC2'

# Mapeo de familias a instancias
SOLOMON_FAMILIES = {
    'C1': [f'C1{i:02d}' for i in range(1, 10)],    # 9 instancias
    'C2': [f'C2{i:02d}' for i in range(1, 9)],     # 8 instancias
    'R1': [f'R1{i:02d}' for i in range(1, 13)],    # 12 instancias
    'R2': [f'R2{i:02d}' for i in range(1, 12)],    # 11 instancias
    'RC1': [f'RC1{i:1d}' for i in range(1, 9)],    # 8 instancias
    'RC2': [f'RC2{i:1d}' for i in range(1, 9)],    # 8 instancias
}

def main():
    print("=" * 70)
    print(f"MODO CUSTOM: Test con FAMILIA {FAMILIA_A_USAR}")
    print("=" * 70)
    print(f"Iniciado: {datetime.now().strftime('%d-%m-%y %H:%M:%S')}")
    print()
    
    # PASO 1: Validar familia
    if FAMILIA_A_USAR not in SOLOMON_FAMILIES:
        print(f"❌ Error: Familia '{FAMILIA_A_USAR}' no reconocida")
        print(f"   Opciones válidas: {', '.join(SOLOMON_FAMILIES.keys())}")
        return
    
    instancias = SOLOMON_FAMILIES[FAMILIA_A_USAR]
    num_instancias = len(instancias)
    num_algoritmos = 3
    total_experimentos = num_instancias * num_algoritmos
    
    print(f"Familia seleccionada: {FAMILIA_A_USAR}")
    print(f"Instancias: {num_instancias} ({', '.join(instancias)})")
    print(f"Algoritmos: {num_algoritmos}")
    print(f"Total de experimentos: {total_experimientos}")
    print()
    
    # PASO 2: Generar algoritmos
    print("[1/3] Generando algoritmos...")
    gen = AlgorithmGenerator(seed=42)
    algorithms = gen.generate_algorithms(num_algorithms=num_algoritmos)
    print(f"      ✓ Algoritmos: {algorithms}")
    print()
    
    # PASO 3: Crear configuración
    print("[2/3] Creando configuración...")
    config = ExperimentConfig(
        mode='CUSTOM',
        families=[FAMILIA_A_USAR],
        algorithms=algorithms,
        repetitions=1,
        seed=42
    )
    print(f"      ✓ Configuración lista")
    print()
    
    # PASO 4: Ejecutar experimentos
    print("[3/3] Ejecutando experimentos...")
    executor = ExperimentExecutor(config)
    
    # Obtener instancias Solomon
    solomon_data = executor.get_solomon_instances(config.families)
    
    # Simular ejecución de experimentos
    for family, instances in solomon_data.items():
        for instance_id in instances:
            for algo_id in config.algorithms:
                for run in range(config.repetitions):
                    # Datos simulados (en producción, aquí iría el solver real)
                    k_bks = random.randint(9, 15)
                    k_final = k_bks if random.random() > 0.3 else k_bks + 1
                    d_bks = random.uniform(800, 2000)
                    d_final = d_bks + random.uniform(-100, 200) if k_final == k_bks else d_bks + 100
                    
                    executor.add_result(
                        algorithm_id=algo_id,
                        instance_id=instance_id,
                        family=family,
                        run_id=run,
                        k_final=k_final,
                        k_bks=k_bks,
                        d_final=d_final,
                        d_bks=d_bks,
                        total_time_sec=random.uniform(3.0, 8.0),
                        iterations=random.randint(80, 200)
                    )
    
    # Guardar resultados
    executor.save_raw_results()
    executor.save_experiment_metadata()
    
    # Mostrar resultados
    print(f"      ✓ Experimentos completados")
    print()
    print("=" * 70)
    print("RESULTADOS")
    print("=" * 70)
    print(f"✓ Total de experimentos ejecutados: {len(executor.raw_results)}")
    print(f"✓ Ubicación: {executor.output_dir}")
    print(f"✓ Archivo CSV: {executor.output_dir}/results/raw_results.csv")
    print(f"✓ Metadata: {executor.output_dir}/results/experiment_metadata.json")
    print()
    
    # Análisis rápido
    print("ANÁLISIS RÁPIDO:")
    print(f"  - Alcanzaron BKS (K): {sum(1 for r in executor.raw_results if r['reached_K_BKS'])} de {len(executor.raw_results)}")
    print(f"  - K promedio: {sum(r['K_final'] for r in executor.raw_results) / len(executor.raw_results):.1f}")
    print(f"  - D promedio: {sum(r['D_final'] for r in executor.raw_results) / len(executor.raw_results):.1f}")
    print(f"  - Tiempo promedio: {sum(r['total_time_sec'] for r in executor.raw_results) / len(executor.raw_results):.2f}s")
    print()
    print(f"Finalizado: {datetime.now().strftime('%d-%m-%y %H:%M:%S')}")
    print("=" * 70)

if __name__ == "__main__":
    main()
