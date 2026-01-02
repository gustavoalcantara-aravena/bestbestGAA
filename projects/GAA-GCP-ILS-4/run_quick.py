#!/usr/bin/env python3
"""
run_quick.py - Script wrapper para ejecutar test_experiment_quick.py desde cualquier directorio

Asegura que:
1. El directorio actual sea el raíz del proyecto
2. Los outputs se creen en output/{timestamp}/
3. Todos los imports funcionen correctamente
"""

import sys
import os
from pathlib import Path

# Obtener el directorio del script actual
script_dir = Path(__file__).parent.absolute()

# Cambiar al directorio del proyecto
os.chdir(script_dir)

# Agregar el proyecto al path
sys.path.insert(0, str(script_dir))

# Importar y ejecutar
from scripts.test_experiment_quick import test_quick_experiment

if __name__ == "__main__":
    test_quick_experiment()
