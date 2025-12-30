#!/usr/bin/env python3
"""
Test suite para verificacion de GCP-ILS scripts
Ejecuta 10 tests para validar la funcionalidad completa
"""

import subprocess
import sys
from pathlib import Path

def run_test(name, cmd):
    """Ejecuta un test y reporta resultado"""
    print(f"\nTesting: {name}")
    result = subprocess.run(cmd, shell=True, cwd=Path(__file__).parent)
    return result.returncode == 0

def main():
    """Ejecuta todos los tests"""
    tests = [
        ("run.py basic", "python scripts/run.py flat300_20_0 --verbose --max-iterations 5"),
        ("run.py DSATUR", "python scripts/run.py flat300_20_0 --constructive dsatur --max-iterations 5"),
        ("run.py LF", "python scripts/run.py flat300_20_0 --constructive lf --max-iterations 5"),
        ("run.py Kempe", "python scripts/run.py flat300_20_0 --local-search kempe --max-iterations 5"),
        ("run.py OVM", "python scripts/run.py flat300_20_0 --local-search ovm --max-iterations 5"),
        ("run.py le450", "python scripts/run.py le450_5b --max-iterations 5"),
        ("run.py myciel", "python scripts/run.py myciel4 --max-iterations 5"),
        ("demo_complete.py", "python scripts/demo_complete.py"),
        ("QUICKSTART", "python scripts/run.py le450_5a --verbose --max-iterations 3"),
        ("list instances", "python -c \"from data.loader import DataLoader; print(len(DataLoader().list_available_instances()), 'instances')\""
        ),
    ]
    
    results = []
    for name, cmd in tests:
        result = run_test(name, cmd)
        results.append((name, result))
        status = "PASS" if result else "FAIL"
        print(f"  Result: {status}")
    
    # Resumen
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(main())
