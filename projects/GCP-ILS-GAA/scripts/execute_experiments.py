#!/usr/bin/env python3
"""
execute_experiments.py - Script maestro para ejecutar experimentos GAA

Este es el punto de entrada principal que articula:
- Ejecución de experimentos (single, family, all)
- Generación de reportes (Markdown, JSON, CSV)
- Regeneración de reportes faltantes
"""

import argparse
import sys
from pathlib import Path
from run_experiments import ExperimentRunner
from regenerate_reports import regenerate_missing_reports
from document_orchestrator import DocumentationOrchestrator

def execute_single(runner, family=None, instance=None, runs=1):
    """Ejecutar una instancia específica"""
    if not family:
        family = runner.select_family()
        if not family:
            return False
    
    if not instance:
        runner.print_family_details(family)
        instance = runner.select_instance(family)
        if not instance:
            return False
    
    print(f"\n{'='*80}")
    print(f"🔬 Ejecutando: {family} / {instance}")
    print(f"📊 Número de ejecuciones: {runs}")
    print(f"{'='*80}\n")
    
    runner.run_single_instance(family, instance, num_runs=runs)
    return True

def execute_family(runner, family=None, runs=1):
    """Ejecutar una familia completa"""
    if not family:
        family = runner.select_family()
        if not family:
            return False
    
    runner.print_family_details(family)
    
    confirm = input(f"\n¿Ejecutar {family} completo? (s/n): ").lower()
    if confirm != 's':
        return False
    
    print(f"\n{'='*80}")
    print(f"🔬 Ejecutando familia: {family}")
    print(f"📊 Número de ejecuciones por instancia: {runs}")
    print(f"{'='*80}\n")
    
    runner.run_family(family, num_runs=runs)
    return True

def execute_all(runner, runs=1):
    """Ejecutar todas las familias"""
    confirm = input(f"\n¿Ejecutar TODAS las familias? (s/n): ").lower()
    if confirm != 's':
        return False
    
    print(f"📊 Ejecuciones por instancia: {runs}")
    runner.run_all_families(num_runs=runs)
    return True

def show_menu():
    """Mostrar menú principal"""
    print("\n" + "="*80)
    print("GAA EXPERIMENT EXECUTOR - SISTEMA INTEGRADO DE EJECUCIÓN")
    print("="*80)
    print("\n📋 OPCIONES DISPONIBLES:\n")
    print("  1. Ejecutar INSTANCIA ESPECÍFICA")
    print("  2. Ejecutar FAMILIA COMPLETA")
    print("  3. Ejecutar TODAS LAS FAMILIAS")
    print("  4. Regenerar reportes faltantes")
    print("  0. Salir\n")

def main():
    parser = argparse.ArgumentParser(
        description='GAA Experiment Executor - Sistema integrado de ejecución',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Modo interactivo
  python execute_experiments.py
  
  # Ejecutar familia específica
  python execute_experiments.py --family CUL
  
  # Ejecutar instancia específica
  python execute_experiments.py --family CUL --instance flat300_20_0
  
  # Ejecutar todas las familias
  python execute_experiments.py --all
  
  # Regenerar reportes faltantes
  python execute_experiments.py --regenerate
        """
    )
    
    parser.add_argument('--family', help='Familia a ejecutar')
    parser.add_argument('--instance', help='Instancia específica a ejecutar')
    parser.add_argument('--all', action='store_true', help='Ejecutar todas las familias')
    parser.add_argument('--runs', type=int, default=1, help='Número de ejecuciones para robustez (default: 1)')
    parser.add_argument('--regenerate', action='store_true', help='Regenerar reportes faltantes')
    parser.add_argument('--bks-file', default='datasets/BKS.json', help='Archivo BKS')
    
    args = parser.parse_args()
    
    # Inicializar runner
    runner = ExperimentRunner(bks_file=args.bks_file)
    
    # Modo no-interactivo (flags)
    if args.regenerate:
        print(f"\n{'='*80}")
        print("🔄 Regenerando reportes faltantes...")
        print(f"{'='*80}\n")
        regenerate_missing_reports()
        return 0
    
    if args.family and args.instance:
        # Ejecutar instancia específica
        if execute_single(runner, args.family, args.instance, args.runs):
            regenerate_missing_reports()
        return 0
    
    if args.family:
        # Ejecutar familia
        if execute_family(runner, args.family, args.runs):
            regenerate_missing_reports()
        return 0
    
    if args.all:
        # Ejecutar todas
        if execute_all(runner, args.runs):
            regenerate_missing_reports()
        return 0
    
    # Modo interactivo
    print("\n" + "="*80)
    print("✅ Sistema listo. Iniciando modo interactivo...")
    print("="*80)
    
    while True:
        show_menu()
        
        try:
            choice = int(input("👉 Selecciona opción (0-4): ").strip())
        except ValueError:
            print("❌ Opción inválida. Intenta de nuevo.")
            continue
        
        # Pedir número de runs en modo interactivo (excepto regenerar)
        runs = 1
        if choice in [1, 2, 3]:
            try:
                runs_input = input("\n📊 ¿Cuántas ejecuciones? (default 1): ").strip()
                if runs_input:
                    runs = int(runs_input)
                    if runs < 1:
                        runs = 1
            except ValueError:
                runs = 1
            
            if runs > 1:
                print(f"   ℹ️  Se ejecutará {runs} veces para análisis de robustez\n")
        
        if choice == 0:
            print("\n👋 ¡Hasta luego!")
            break
        
        elif choice == 1:
            # Instancia específica
            if execute_single(runner, runs=runs):
                regenerate_missing_reports()
                
                print("\n" + "="*80)
                resp = input("¿Deseas ejecutar otro experimento? (s/n): ").lower()
                if resp != 's':
                    print("👋 ¡Hasta luego!")
                    break
        
        elif choice == 2:
            # Familia completa
            if execute_family(runner, runs=runs):
                regenerate_missing_reports()
                
                print("\n" + "="*80)
                resp = input("¿Deseas ejecutar otro experimento? (s/n): ").lower()
                if resp != 's':
                    print("👋 ¡Hasta luego!")
                    break
        
        elif choice == 3:
            # Todas las familias
            if execute_all(runner, runs=runs):
                regenerate_missing_reports()
                
                print("\n" + "="*80)
                resp = input("¿Deseas ejecutar otro experimento? (s/n): ").lower()
                if resp != 's':
                    print("👋 ¡Hasta luego!")
                    break
        
        elif choice == 4:
            # Regenerar reportes
            print(f"\n{'='*80}")
            print("🔄 Regenerando reportes faltantes...")
            print(f"{'='*80}\n")
            regenerate_missing_reports()
            
            print("\n" + "="*80)
            resp = input("¿Deseas hacer algo más? (s/n): ").lower()
            if resp != 's':
                print("👋 ¡Hasta luego!")
                break
        
        else:
            print("❌ Opción inválida. Intenta de nuevo.")
    
    return 0

if __name__ == '__main__':
    exit(main())
