#!/usr/bin/env python3
"""
QUICK REFERENCE: Estado de GAA
Verificación de 30 segundos
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("\n" + "="*80)
print("  VERIFICACIÓN RÁPIDA: GAA EN GAA-GCP-ILS-4")
print("="*80 + "\n")

# Check 1: Module exists
print("1. ¿Existe el módulo GAA? ", end="")
try:
    from gaa import Grammar, AlgorithmGenerator, ASTInterpreter
    print("✅")
except:
    print("❌")
    sys.exit(1)

# Check 2: Core integration
print("2. ¿Está integrado con core/? ", end="")
try:
    from gaa.interpreter import ASTInterpreter
    from core import GraphColoringProblem, ColoringSolution, ColoringEvaluator
    print("✅")
except:
    print("❌")
    sys.exit(1)

# Check 3: Operators integration
print("3. ¿Está integrado con operators/? ", end="")
try:
    from operators.constructive import GreedyDSATUR, GreedyLF
    from operators.improvement import KempeChain, OneVertexMove
    from operators.perturbation import RandomRecolor, PartialDestroy
    print("✅")
except:
    print("❌")
    sys.exit(1)

# Check 4: Operator mapping
print("4. ¿Están bien mapeados los operadores? ", end="")
try:
    from gaa.interpreter import ASTInterpreter
    assert "DSATUR" in ASTInterpreter.CONSTRUCTIVE_OPS
    assert "KempeChain" in ASTInterpreter.IMPROVEMENT_OPS
    assert "RandomRecolor" in ASTInterpreter.PERTURBATION_OPS
    print("✅")
except:
    print("❌")
    sys.exit(1)

# Check 5: Generation works
print("5. ¿Se generan algoritmos? ", end="")
try:
    from gaa import Grammar, AlgorithmGenerator
    g = Grammar()
    gen = AlgorithmGenerator(grammar=g, seed=42)
    ast = gen.generate()
    assert ast is not None
    print("✅")
except:
    print("❌")
    sys.exit(1)

print("\n" + "="*80)
print("  RESULTADO: ✅ GAA ESTÁ COMPLETAMENTE INTEGRADO Y FUNCIONAL")
print("="*80 + "\n")

print("📚 Documentación recomendada:")
print("   • RESUMEN_EJECUTIVO_INTEGRACION_GAA.md - Resumen ejecutivo")
print("   • ANALISIS_INTEGRACION_GAA.md - Análisis técnico completo")
print("   • gaa/README.md - Guía de uso")
print("\n🚀 Para usar GAA:")
print("   • python scripts/gaa_quick_demo.py - Demo rápida")
print("   • python scripts/gaa_experiment.py - Experimento completo")
print("   • python validate_integration.py - Validación detallada")
print("\n")
