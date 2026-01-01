#!/usr/bin/env python3
"""
run_full_experiment_myciel.py - Experimento completo con familia MYCIEL

Ejecuta el experimento completo usando la familia MYCIEL (myciel3-myciel7)
que tiene BKS conocido para todas las instancias.

Uso:
    python scripts/run_full_experiment_myciel.py
"""

import sys
from pathlib import Path

# Agregar proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.run_full_experiment import FullExperiment


def main():
    """Ejecuta experimento completo con familia MYCIEL"""
    print("="*80)
    print("EXPERIMENTO COMPLETO - FAMILIA MYCIEL (myciel3-myciel7)")
    print("="*80)
    print("Instancias: myciel3, myciel4, myciel5, myciel6, myciel7")
    print("Todas con BKS conocido: 4, 5, 6, 7, 8")
    print("Tiempo total estimado: ~3-5 minutos\n")
    
    # Crear y ejecutar experimento con familia MYCIEL
    experiment = FullExperiment(
        mode='family',
        family='MYC',
        max_time=300,  # 5 minutos por instancia
        num_replicas=3,  # 3 réplicas por instancia
        seed=42
    )
    
    experiment.run_experiment()


if __name__ == "__main__":
    main()
