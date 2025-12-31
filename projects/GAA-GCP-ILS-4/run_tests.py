#!/usr/bin/env python3
"""
run_tests.py
Script para ejecutar la suite de tests con diferentes opciones

Uso:
    python run_tests.py            # Ejecutar todos los tests
    python run_tests.py --quick    # Solo validación rápida
    python run_tests.py --core     # Solo tests de Core
    python run_tests.py --coverage # Con reporte de cobertura
    python run_tests.py --verbose  # Verbose completo
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n{'='*70}")
    print(f"  {description}")
    print(f"{'='*70}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Ejecutar suite de tests GCP-ILS'
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Ejecutar solo validación rápida (10s)'
    )
    parser.add_argument(
        '--core',
        action='store_true',
        help='Ejecutar solo tests de Core'
    )
    parser.add_argument(
        '--operators',
        action='store_true',
        help='Ejecutar solo tests de Operadores'
    )
    parser.add_argument(
        '--ils',
        action='store_true',
        help='Ejecutar solo tests de ILS'
    )
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Ejecutar con reporte de cobertura'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Modo verbose'
    )
    
    args = parser.parse_args()
    
    # Determinar qué ejecutar
    if args.quick:
        return run_command(
            'python scripts/test_quick.py',
            'VALIDACIÓN RÁPIDA'
        )
    
    if args.core:
        cmd = 'pytest tests/test_core.py -v'
        if args.verbose:
            cmd += ' --tb=long'
        return run_command(cmd, 'TESTS DE CORE')
    
    if args.operators:
        cmd = 'pytest tests/test_operators.py -v'
        if args.verbose:
            cmd += ' --tb=long'
        return run_command(cmd, 'TESTS DE OPERADORES')
    
    if args.ils:
        cmd = 'pytest tests/test_ils.py -v'
        if args.verbose:
            cmd += ' --tb=long'
        return run_command(cmd, 'TESTS DE ILS')
    
    # Por defecto: ejecutar todos
    if args.coverage:
        cmd = (
            'pytest tests/ '
            '--cov=core --cov=operators --cov=metaheuristic '
            '--cov-report=html --cov-report=term-missing -v'
        )
        return run_command(cmd, 'TODOS LOS TESTS CON COBERTURA')
    
    # Todos los tests sin cobertura
    cmd = 'pytest tests/ -v'
    if args.verbose:
        cmd += ' --tb=long'
    
    return run_command(cmd, 'TODOS LOS TESTS')


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
