#!/usr/bin/env python3
"""
Test suite para verificación de GCP-ILS scripts
Ejecuta 10 tests para validar la funcionalidad completa
"""

import subprocess
import sys
from pathlib import Path

def run_test(name, cmd, description=""):
    """Ejecuta un test y reporta resultado"""
    print(f"\n{'='*70}")
    print(f"TEST: {name}")
    if description:
        print(f"DESC: {description}")
    print(f"{'='*70}")
    
    result = subprocess.run(cmd, shell=True, cwd=Path(__file__).parent, 
                          capture_output=False)
    
    if result.returncode == 0:
        print(f"[PASS] {name}")
        return True
    else:
        print(f"[FAIL] {name} (exit code: {result.returncode})")
        return False

def main():
    """Ejecuta todos los tests"""
    tests = [
        ("Test 1: run.py básico", 
         "python scripts/run.py flat300_20_0 --verbose --max-iterations 5",
         "Verificar que run.py carga instancia y ejecuta ILS"),
        
        ("Test 2: run.py con constructor DSATUR",
         "python scripts/run.py flat300_20_0 --constructive dsatur --max-iterations 5",
         "Verificar operator constructivo DSATUR"),
        
        ("Test 3: run.py con constructor LF",
         "python scripts/run.py flat300_20_0 --constructive lf --max-iterations 5",
         "Verificar operator constructivo LargestFirst"),
        
        ("Test 4: run.py con local search Kempe",
         "python scripts/run.py flat300_20_0 --local-search kempe --max-iterations 5",
         "Verificar local search KempeChain"),
        
        ("Test 5: run.py con local search OneVertexMove",
         "python scripts/run.py flat300_20_0 --local-search ovm --max-iterations 5",
         "Verificar local search OneVertexMove"),
        
        ("Test 6: run.py con instancia le450",
         "python scripts/run.py le450_5b --max-iterations 5",
         "Verificar con instancia de familia LEI"),
        
        ("Test 7: run.py con instancia Myciel",
         "python scripts/run.py myciel4 --max-iterations 5",
         "Verificar con instancia Myciel pequeña"),
        
        ("Test 8: demo_complete.py",
         "python scripts/demo_complete.py",
         "Ejecutar demo con múltiples instancias"),
        
        ("Test 9: QUICKSTART paso 1",
         "python scripts/run.py le450_5a --verbose --max-iterations 3",
         "Verificar ejemplo del QUICKSTART"),
        
        ("Test 10: Instancias disponibles",
         "python -c \"from data.loader import DataLoader; loader = DataLoader(); instances = loader.list_available_instances(); print(f'Total instances: {len(instances)}')\"",
         "Verificar que todas las instancias se encuentran"),
    ]
    
    results = []
    for name, cmd, desc in tests:
        result = run_test(name, cmd, desc)
        results.append((name, result))
    
    # Resumen
    print(f"\n{'='*70}")
    print("RESUMEN DE TESTS")
    print(f"{'='*70}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status}: {name}")
    
    print(f"\n{passed}/{total} tests pasaron")
    
    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(main())
