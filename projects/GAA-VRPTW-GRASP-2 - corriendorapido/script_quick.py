"""
Script QUICK: Ejecutar 1 familia (R1) - 5 minutos de test

Modo: QUICK
Familias: 1 (R1)
Instancias: 12 (R101-R112)
Algoritmos: 3
Total experimentos: 36
Tiempo estimado: 2-5 minutos
"""

from scripts.experiments import QuickExperiment, AlgorithmGenerator
from datetime import datetime

def main():
    print("=" * 70)
    print("MODO QUICK: Test rápido con 1 familia (R1)")
    print("=" * 70)
    print(f"Iniciado: {datetime.now().strftime('%d-%m-%y %H:%M:%S')}")
    print()
    
    # PASO 1: Generar algoritmos (una sola vez)
    print("[1/2] Generando algoritmos...")
    gen = AlgorithmGenerator(seed=42)
    algorithms = gen.generate_algorithms(num_algorithms=3)
    print(f"      ✓ Algoritmos generados: {algorithms}")
    print()
    
    # PASO 2: Ejecutar QUICK
    print("[2/2] Ejecutando experimentos QUICK...")
    executor = QuickExperiment.run()
    
    # Resultados
    print()
    print("=" * 70)
    print("RESULTADOS")
    print("=" * 70)
    print(f"✓ Total de experimentos: {len(executor.raw_results)}")
    print(f"✓ Ubicación de resultados: {executor.output_dir}")
    print(f"✓ Archivo CSV: {executor.output_dir}/results/raw_results.csv")
    print(f"✓ Metadata: {executor.output_dir}/results/experiment_metadata.json")
    print()
    print("Próximos pasos:")
    print("  1. Abre raw_results.csv para ver los datos")
    print("  2. Corre script_analyze.py para análisis estadístico")
    print("  3. Corre script_visualize.py para gráficos")
    print()
    print(f"Finalizado: {datetime.now().strftime('%d-%m-%y %H:%M:%S')}")
    print("=" * 70)

if __name__ == "__main__":
    main()
