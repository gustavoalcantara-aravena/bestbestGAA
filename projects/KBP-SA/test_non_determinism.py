#!/usr/bin/env python3
"""
Test para verificar no-determinismo en AlgorithmGenerator
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gaa.generator import AlgorithmGenerator
from gaa.grammar import Grammar

def test_determinism():
    """Prueba si el mismo seed genera los mismos algoritmos"""

    print("=" * 80)
    print("TEST DE DETERMINISMO: AlgorithmGenerator")
    print("=" * 80)
    print()

    # Generar 3 algoritmos con seed=42
    print("🧪 Generación 1 (seed=42):")
    grammar1 = Grammar(min_depth=2, max_depth=3)
    generator1 = AlgorithmGenerator(grammar=grammar1, seed=42)

    algos1 = []
    for i in range(3):
        ast = generator1.generate_with_validation()
        algos1.append(ast)
        print(f"  Algoritmo {i+1}: {ast.to_pseudocode()[:80]}...")

    print()

    # Generar 3 algoritmos con seed=42 (segunda vez)
    print("🧪 Generación 2 (seed=42, debería ser idéntica):")
    grammar2 = Grammar(min_depth=2, max_depth=3)
    generator2 = AlgorithmGenerator(grammar=grammar2, seed=42)

    algos2 = []
    for i in range(3):
        ast = generator2.generate_with_validation()
        algos2.append(ast)
        print(f"  Algoritmo {i+1}: {ast.to_pseudocode()[:80]}...")

    print()
    print("=" * 80)
    print("COMPARACIÓN:")
    print("=" * 80)
    print()

    all_match = True
    for i in range(3):
        match = algos1[i].to_pseudocode() == algos2[i].to_pseudocode()
        status = "✅ MATCH" if match else "❌ DIFFERENT"
        print(f"Algoritmo {i+1}: {status}")
        if not match:
            all_match = False
            print(f"  Gen1: {algos1[i].to_pseudocode()[:100]}")
            print(f"  Gen2: {algos2[i].to_pseudocode()[:100]}")

    print()
    print("=" * 80)
    if all_match:
        print("✅ DETERMINISTA: Todas las generaciones coinciden")
    else:
        print("❌ NO-DETERMINISTA: Las generaciones difieren")
    print("=" * 80)

    return all_match

if __name__ == "__main__":
    is_deterministic = test_determinism()
    sys.exit(0 if is_deterministic else 1)
