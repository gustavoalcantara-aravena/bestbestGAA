#!/usr/bin/env python3
"""
main.py - Punto de entrada principal para GCP-ILS-GAA

Ejecuta desde aquí: python main.py

Este script articula toda la ejecución de experimentos GAA
"""

import sys
from pathlib import Path

# Agregar scripts al path
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

# Importar y ejecutar el script maestro
from execute_experiments import main

if __name__ == '__main__':
    exit(main())
