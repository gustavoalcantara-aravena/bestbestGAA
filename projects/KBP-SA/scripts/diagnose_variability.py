#!/usr/bin/env python3
"""
Diagnóstico de variabilidad de tiempos entre ejecuciones
Investiga por qué el tiempo aumenta en ejecuciones posteriores
"""

import sys
import os
from pathlib import Path
import time
import gc
import psutil
import shutil

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)


def get_system_stats():
    """Obtiene estadísticas del sistema"""
    process = psutil.Process(os.getpid())
    return {
        'memory_mb': process.memory_info().rss / 1024 / 1024,
        'cpu_percent': process.cpu_percent(interval=0.1),
        'num_threads': process.num_threads(),
        'open_files': len(process.open_files())
    }


def get_disk_usage(path):
    """Obtiene uso de disco de un directorio"""
    if not Path(path).exists():
        return 0
    total_size = 0
    for entry in Path(path).rglob('*'):
        if entry.is_file():
            total_size += entry.stat().st_size
    return total_size / 1024 / 1024  # MB


def count_files(path):
    """Cuenta archivos en un directorio"""
    if not Path(path).exists():
        return 0
    return len(list(Path(path).rglob('*')))


def run_iteration(iteration_num, clean_output=True):
    """Ejecuta una iteración del test y mide estadísticas"""

    print(f"\n{'='*80}")
    print(f"  ITERACIÓN {iteration_num}")
    print(f"{'='*80}\n")

    # Estadísticas pre-ejecución
    print("📊 Estado ANTES de la ejecución:")
    stats_before = get_system_stats()
    output_size_before = get_disk_usage("output")
    output_files_before = count_files("output")

    print(f"   • Memoria: {stats_before['memory_mb']:.1f} MB")
    print(f"   • Archivos abiertos: {stats_before['open_files']}")
    print(f"   • Threads: {stats_before['num_threads']}")
    print(f"   • Tamaño output/: {output_size_before:.1f} MB")
    print(f"   • Archivos en output/: {output_files_before}")

    # Forzar garbage collection antes de ejecutar
    print(f"\n🗑️  Ejecutando garbage collection...")
    gc_before = gc.get_count()
    collected = gc.collect()
    print(f"   • Objetos antes: {gc_before}")
    print(f"   • Objetos recolectados: {collected}")

    # Ejecutar test
    print(f"\n⏱️  Ejecutando test...")
    start_time = time.time()

    # Importar aquí para medir tiempo de import
    import_start = time.time()
    from quick_test_both import (
        do_imports, generate_algorithms, load_instances,
        configure_experiment, run_experiments, run_statistics,
        run_comparison, generate_base_visualizations,
        generate_sa_visualizations
    )
    import_time = time.time() - import_start

    do_imports()
    algorithms = generate_algorithms()
    instances, loader = load_instances()
    config = configure_experiment(instances, algorithms)
    runner, results = run_experiments(config)
    analyzer, algorithm_results = run_statistics(results, algorithms)
    comparison = run_comparison(analyzer, algorithm_results)

    if comparison:
        best_alg = next(alg for alg in algorithms if alg['name'] == comparison['best_algorithm'])
        plots_dir = generate_base_visualizations(algorithm_results, results, analyzer)
        generate_sa_visualizations(instances, best_alg, plots_dir)

    elapsed = time.time() - start_time

    # Estadísticas post-ejecución
    print(f"\n📊 Estado DESPUÉS de la ejecución:")
    stats_after = get_system_stats()
    output_size_after = get_disk_usage("output")
    output_files_after = count_files("output")

    print(f"   • Memoria: {stats_after['memory_mb']:.1f} MB (+{stats_after['memory_mb']-stats_before['memory_mb']:.1f} MB)")
    print(f"   • Archivos abiertos: {stats_after['open_files']}")
    print(f"   • Threads: {stats_after['num_threads']}")
    print(f"   • Tamaño output/: {output_size_after:.1f} MB (+{output_size_after-output_size_before:.1f} MB)")
    print(f"   • Archivos en output/: {output_files_after} (+{output_files_after-output_files_before})")

    # Limpiar output si se solicita
    if clean_output:
        print(f"\n🗑️  Limpiando directorio output/...")
        if Path("output").exists():
            shutil.rmtree("output")
        print(f"   • Directorio output/ eliminado")

    gc_after = gc.get_count()
    print(f"\n🗑️  Estado garbage collector:")
    print(f"   • Objetos después: {gc_after}")

    return {
        'iteration': iteration_num,
        'time': elapsed,
        'import_time': import_time,
        'memory_before': stats_before['memory_mb'],
        'memory_after': stats_after['memory_mb'],
        'memory_delta': stats_after['memory_mb'] - stats_before['memory_mb'],
        'disk_before': output_size_before,
        'disk_after': output_size_after,
        'disk_delta': output_size_after - output_size_before,
        'files_before': output_files_before,
        'files_after': output_files_after,
        'files_delta': output_files_after - output_files_before,
        'open_files_before': stats_before['open_files'],
        'open_files_after': stats_after['open_files']
    }


def main():
    print("="*80)
    print("  DIAGNÓSTICO DE VARIABILIDAD DE TIEMPOS")
    print("="*80)

    results = []

    # Test 1: Sin limpiar output entre ejecuciones (simula ejecuciones repetidas)
    print("\n\n🔍 TEST 1: SIN LIMPIAR output/ entre ejecuciones")
    print("="*80)
    print("Esto simula ejecutar el script múltiples veces sin limpiar")

    for i in range(3):
        result = run_iteration(i+1, clean_output=False)
        results.append(result)
        time.sleep(1)  # Pausa entre ejecuciones

    # Limpiar antes del segundo test
    print(f"\n\n🗑️  Limpiando TODO antes del Test 2...")
    if Path("output").exists():
        shutil.rmtree("output")

    # Test 2: Limpiando output entre ejecuciones
    print("\n\n🔍 TEST 2: LIMPIANDO output/ entre ejecuciones")
    print("="*80)
    print("Esto simula ejecutar el script con limpieza entre corridas")

    for i in range(3):
        result = run_iteration(i+4, clean_output=True)
        results.append(result)
        time.sleep(1)

    # Resumen
    print("\n\n" + "="*80)
    print("  RESUMEN DE RESULTADOS")
    print("="*80)

    print(f"\n{'Iter':<6} {'Tiempo (s)':<12} {'Import (s)':<12} {'Mem Δ (MB)':<12} {'Disk Δ (MB)':<12} {'Files Δ':<10}")
    print("-"*80)

    for r in results:
        print(f"{r['iteration']:<6} {r['time']:<12.2f} {r['import_time']:<12.2f} "
              f"{r['memory_delta']:<12.1f} {r['disk_delta']:<12.1f} {r['files_delta']:<10}")

    # Análisis de variabilidad
    print("\n\n📊 ANÁLISIS DE VARIABILIDAD:")
    print("-"*80)

    test1_times = [r['time'] for r in results[:3]]
    test2_times = [r['time'] for r in results[3:6]]

    test1_avg = sum(test1_times) / len(test1_times)
    test2_avg = sum(test2_times) / len(test2_times)

    test1_std = (sum((t - test1_avg)**2 for t in test1_times) / len(test1_times))**0.5
    test2_std = (sum((t - test2_avg)**2 for t in test2_times) / len(test2_times))**0.5

    print(f"\nTEST 1 (SIN limpiar output/):")
    print(f"   • Tiempos: {[f'{t:.2f}s' for t in test1_times]}")
    print(f"   • Media: {test1_avg:.2f}s")
    print(f"   • Desv. Est.: {test1_std:.2f}s ({test1_std/test1_avg*100:.1f}%)")
    print(f"   • Tendencia: {'ASCENDENTE' if test1_times[2] > test1_times[0] else 'ESTABLE'} "
          f"({test1_times[2] - test1_times[0]:+.2f}s)")

    print(f"\nTEST 2 (LIMPIANDO output/):")
    print(f"   • Tiempos: {[f'{t:.2f}s' for t in test2_times]}")
    print(f"   • Media: {test2_avg:.2f}s")
    print(f"   • Desv. Est.: {test2_std:.2f}s ({test2_std/test2_avg*100:.1f}%)")
    print(f"   • Tendencia: {'ASCENDENTE' if test2_times[2] > test2_times[0] else 'ESTABLE'} "
          f"({test2_times[2] - test2_times[0]:+.2f}s)")

    # Diagnóstico
    print("\n\n🔍 DIAGNÓSTICO:")
    print("-"*80)

    disk_growth_test1 = sum(r['disk_delta'] for r in results[:3])
    disk_growth_test2 = sum(r['disk_delta'] for r in results[3:6])

    print(f"\n1. Acumulación de archivos:")
    print(f"   • Test 1 (sin limpiar): {disk_growth_test1:.1f} MB acumulados")
    print(f"   • Test 2 (limpiando): {disk_growth_test2:.1f} MB acumulados")

    if disk_growth_test1 > 100:  # > 100 MB
        print(f"   ⚠️  PROBLEMA IDENTIFICADO: Acumulación significativa de archivos")
        print(f"      → Cada ejecución genera ~{disk_growth_test1/3:.1f} MB")
        print(f"      → Sobrescribir archivos puede ser más lento con el tiempo")

    mem_growth_test1 = sum(r['memory_delta'] for r in results[:3])
    mem_growth_test2 = sum(r['memory_delta'] for r in results[3:6])

    print(f"\n2. Uso de memoria:")
    print(f"   • Test 1: {mem_growth_test1:.1f} MB acumulados")
    print(f"   • Test 2: {mem_growth_test2:.1f} MB acumulados")

    if abs(mem_growth_test1 - mem_growth_test2) > 50:
        print(f"   ⚠️  POSIBLE PROBLEMA: Diferencia significativa en uso de memoria")

    time_diff = abs(test1_avg - test2_avg)
    if time_diff > 2.0:  # > 2 segundos de diferencia
        print(f"\n3. Impacto de limpieza:")
        print(f"   • Diferencia promedio: {time_diff:.2f}s")
        print(f"   ⚠️  PROBLEMA IDENTIFICADO: Limpieza de archivos afecta rendimiento")
        print(f"      → {'Limpiar' if test2_avg < test1_avg else 'No limpiar'} mejora el tiempo")

    # Conclusión
    print("\n\n✅ CONCLUSIÓN:")
    print("-"*80)

    if test1_times[2] - test1_times[0] > 2.0:
        print("\n⚠️  CAUSA RAÍZ IDENTIFICADA: SOBRESCRITURA DE ARCHIVOS")
        print("   • El tiempo aumenta cuando se sobrescriben archivos existentes")
        print("   • La fragmentación del disco o cache afecta la escritura")
        print("\n   SOLUCIÓN: Limpiar el directorio output/ antes de cada ejecución")
    elif test1_std / test1_avg > 0.10:  # > 10% de variabilidad
        print("\n⚠️  ALTA VARIABILIDAD DETECTADA (>10%)")
        print("   • Posibles causas: procesos del sistema, cache, scheduling")
        print("\n   SOLUCIÓN: Ejecutar en condiciones controladas (menos carga del sistema)")
    else:
        print("\n✓ Variabilidad normal (<10%)")
        print("   • El sistema se comporta de manera predecible")

    print()


if __name__ == '__main__':
    main()
