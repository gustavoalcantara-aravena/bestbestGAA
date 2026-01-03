"""
Script FULL: Ejecutar TODAS las familias (168 experimentos)

Modo: FULL
Familias: 6 (C1, C2, R1, R2, RC1, RC2)
Instancias: 56 total
Algoritmos: 3
Total experimentos: 168
Tiempo estimado: 15-25 minutos
"""

from scripts.experiments import FullExperiment, AlgorithmGenerator
from datetime import datetime

def main():
    print("=" * 70)
    print("MODO FULL: Test completo con todas las 6 familias")
    print("=" * 70)
    print(f"Iniciado: {datetime.now().strftime('%d-%m-%y %H:%M:%S')}")
    print()
    
    print("Configuración:")
    print("  • Familias: C1, C2, R1, R2, RC1, RC2")
    print("  • Total instancias: 56")
    print("  • Algoritmos: 3")
    print("  • Total experimentos: 168")
    print("  • Tiempo estimado: 15-25 minutos")
    print()
    print("⚠️  Este es un test más largo. Para un test rápido, usa script_quick.py")
    print()
    
    # PASO 1: Generar algoritmos
    print("[1/2] Generando algoritmos...")
    gen = AlgorithmGenerator(seed=42)
    algorithms = gen.generate_algorithms(num_algorithms=3)
    print(f"      ✓ Algoritmos generados: {algorithms}")
    print()
    
    # PASO 2: Ejecutar FULL
    print("[2/2] Ejecutando experimentos FULL...")
    print("      Esto puede tomar 15-25 minutos...")
    executor = FullExperiment.run()
    
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
    
    # Análisis por familia
    print("ANÁLISIS POR FAMILIA:")
    families = set(r['family'] for r in executor.raw_results)
    for family in sorted(families):
        family_results = [r for r in executor.raw_results if r['family'] == family]
        bks_reached = sum(1 for r in family_results if r['reached_K_BKS'])
        avg_k = sum(r['K_final'] for r in family_results) / len(family_results)
        print(f"  {family}: {len(family_results)} exp, BKS={bks_reached}, K_avg={avg_k:.1f}")
    
    print()
    print("Próximos pasos:")
    print("  1. Abre raw_results.csv para ver todos los datos")
    print("  2. Corre script_analyze.py para análisis estadístico completo")
    print("  3. Corre script_visualize.py para generar gráficos")
    print()
    print(f"Finalizado: {datetime.now().strftime('%d-%m-%y %H:%M:%S')}")
    print("=" * 70)

if __name__ == "__main__":
    main()
