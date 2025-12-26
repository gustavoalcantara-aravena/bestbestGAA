#!/usr/bin/env python3
"""
Test rápido de variabilidad - Ejecuta el script 5 veces y mide diferencias
"""

import subprocess
import time
import json
from pathlib import Path
import shutil

def run_test(iteration, clean_before=False):
    """Ejecuta el test y mide tiempo"""

    if clean_before and Path("output").exists():
        print(f"   🗑️  Limpiando output/...")
        shutil.rmtree("output")

    print(f"\n{'='*60}")
    print(f"  ITERACIÓN {iteration}")
    print(f"{'='*60}")

    # Contar archivos antes
    output_files_before = 0
    output_size_before = 0
    if Path("output").exists():
        output_files_before = len(list(Path("output").rglob("*")))
        output_size_before = sum(f.stat().st_size for f in Path("output").rglob("*") if f.is_file())

    print(f"   Estado ANTES:")
    print(f"   • Archivos en output/: {output_files_before}")
    print(f"   • Tamaño: {output_size_before/1024/1024:.1f} MB")

    # Ejecutar
    start = time.time()
    result = subprocess.run(
        ["python3", "scripts/quick_test_both.py"],
        capture_output=True,
        text=True,
        timeout=180
    )
    elapsed = time.time() - start

    # Extraer tiempo del output
    for line in result.stdout.split('\n'):
        if 'Tiempo total:' in line:
            try:
                script_time = float(line.split(':')[-1].strip().replace('segundos', '').strip())
            except:
                script_time = elapsed

    # Contar archivos después
    output_files_after = 0
    output_size_after = 0
    if Path("output").exists():
        output_files_after = len(list(Path("output").rglob("*")))
        output_size_after = sum(f.stat().st_size for f in Path("output").rglob("*") if f.is_file())

    print(f"\n   Estado DESPUÉS:")
    print(f"   • Archivos en output/: {output_files_after} (+{output_files_after - output_files_before})")
    print(f"   • Tamaño: {output_size_after/1024/1024:.1f} MB (+{(output_size_after-output_size_before)/1024/1024:.1f} MB)")
    print(f"   ⏱️  Tiempo: {elapsed:.2f}s")

    return {
        'iteration': iteration,
        'time': elapsed,
        'files_before': output_files_before,
        'files_after': output_files_after,
        'size_before_mb': output_size_before/1024/1024,
        'size_after_mb': output_size_after/1024/1024,
        'clean_before': clean_before
    }


def main():
    print("="*60)
    print("  TEST DE VARIABILIDAD - 5 EJECUCIONES")
    print("="*60)

    results = []

    # Ejecución 1: Limpiando antes (baseline)
    print("\n\n🧪 TEST 1: PRIMERA EJECUCIÓN (output/ limpio)")
    r = run_test(1, clean_before=True)
    results.append(r)
    time.sleep(2)

    # Ejecuciones 2-4: Sin limpiar (acumulando archivos)
    print("\n\n🧪 TEST 2-4: SIN LIMPIAR (acumulando archivos)")
    for i in range(2, 5):
        r = run_test(i, clean_before=False)
        results.append(r)
        time.sleep(2)

    # Ejecución 5: Limpiando antes de nuevo
    print("\n\n🧪 TEST 5: LIMPIANDO DE NUEVO")
    r = run_test(5, clean_before=True)
    results.append(r)

    # Resumen
    print("\n\n" + "="*60)
    print("  RESUMEN")
    print("="*60)

    print(f"\n{'#':<4} {'Limpio':<8} {'Tiempo (s)':<12} {'Archivos':<12} {'Tamaño (MB)':<12}")
    print("-"*60)

    for r in results:
        clean = "SÍ" if r['clean_before'] else "NO"
        print(f"{r['iteration']:<4} {clean:<8} {r['time']:<12.2f} "
              f"{r['files_after']:<12} {r['size_after_mb']:<12.1f}")

    # Análisis
    times = [r['time'] for r in results]
    clean_times = [r['time'] for r in results if r['clean_before']]
    dirty_times = [r['time'] for r in results if not r['clean_before']]

    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    std_time = (sum((t - avg_time)**2 for t in times) / len(times))**0.5

    print(f"\n📊 ESTADÍSTICAS:")
    print(f"   • Media: {avg_time:.2f}s")
    print(f"   • Mínimo: {min_time:.2f}s")
    print(f"   • Máximo: {max_time:.2f}s")
    print(f"   • Desv. Est.: {std_time:.2f}s ({std_time/avg_time*100:.1f}%)")
    print(f"   • Rango: {max_time - min_time:.2f}s ({(max_time-min_time)/avg_time*100:.1f}%)")

    if clean_times and dirty_times:
        avg_clean = sum(clean_times) / len(clean_times)
        avg_dirty = sum(dirty_times) / len(dirty_times)

        print(f"\n🔍 COMPARACIÓN:")
        print(f"   • Con output/ limpio: {avg_clean:.2f}s")
        print(f"   • Sin limpiar: {avg_dirty:.2f}s")
        print(f"   • Diferencia: {avg_dirty - avg_clean:+.2f}s ({(avg_dirty-avg_clean)/avg_clean*100:+.1f}%)")

    # Tendencia
    print(f"\n📈 TENDENCIA:")
    print(f"   • Primera ejecución: {times[0]:.2f}s")
    print(f"   • Última (sin limpiar): {times[3]:.2f}s")
    print(f"   • Cambio: {times[3] - times[0]:+.2f}s ({(times[3]-times[0])/times[0]*100:+.1f}%)")

    if times[3] > times[0] + 2.0:  # > 2s más lento
        print(f"\n⚠️  PROBLEMA IDENTIFICADO: Degradación en ejecuciones sucesivas")
        print(f"      → El tiempo aumenta {times[3] - times[0]:.2f}s sin limpiar output/")
    elif std_time / avg_time > 0.10:  # > 10% variabilidad
        print(f"\n⚠️  ALTA VARIABILIDAD: {std_time/avg_time*100:.1f}%")
        print(f"      → Posibles causas: cache del sistema, procesos background")
    else:
        print(f"\n✓ Variabilidad normal: {std_time/avg_time*100:.1f}%")

    # Guardar resultados
    with open("variability_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n📄 Resultados guardados en: variability_results.json")
    print()


if __name__ == '__main__':
    main()
