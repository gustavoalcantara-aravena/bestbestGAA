#!/usr/bin/env python3
"""
Script de profiling para demo_experimentation_both.py
Mide tiempos detallados de cada fase
"""

import cProfile
import pstats
import io
import time
from pathlib import Path

def profile_script():
    """Ejecuta profiling del script both"""

    # Crear profiler
    profiler = cProfile.Profile()

    print("=" * 80)
    print("  PROFILING: demo_experimentation_both.py")
    print("=" * 80)
    print()

    # Medir tiempo total
    start_time = time.time()

    # Ejecutar con profiling
    profiler.enable()

    # Importar y ejecutar el script
    import sys
    sys.path.insert(0, str(Path(__file__).parent))

    from demo_experimentation_both import main
    main()

    profiler.disable()

    end_time = time.time()
    total_time = end_time - start_time

    # Guardar resultados
    print("\n" + "=" * 80)
    print("  RESULTADOS DEL PROFILING")
    print("=" * 80)
    print(f"\n⏱️  Tiempo total: {total_time:.2f} segundos")
    print()

    # Crear reporte
    s = io.StringIO()
    sortby = pstats.SortKey.CUMULATIVE
    ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)

    # Top 30 funciones más costosas
    ps.print_stats(30)

    profile_output = s.getvalue()

    # Guardar a archivo
    output_dir = Path("output/profiling")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "profile_both_results.txt"
    with open(output_file, 'w') as f:
        f.write(f"Tiempo total de ejecución: {total_time:.2f} segundos\n")
        f.write("=" * 80 + "\n\n")
        f.write(profile_output)

    print(f"📊 Reporte completo guardado en: {output_file}")
    print()

    # Mostrar top 15 funciones
    print("🔝 Top 15 funciones más costosas (tiempo acumulado):")
    print()
    lines = profile_output.split('\n')
    for i, line in enumerate(lines):
        if i < 20:  # Headers
            print(line)
        elif i < 35:  # Top 15
            print(line)
        else:
            break

if __name__ == '__main__':
    profile_script()
