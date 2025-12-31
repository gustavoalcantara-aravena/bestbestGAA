#!/usr/bin/env python3
"""
test_doc_generation.py - Test rápido de generación de documentación

Ejecuta una familia pequeña y verifica que se generen todos los archivos
"""

import sys
from pathlib import Path

# Agregar scripts al path
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from run_experiments import ExperimentRunner

def test_family_documentation():
    """Test generación de documentación para una familia"""
    
    print("\n" + "="*80)
    print("🧪 TEST: Generación de Documentación")
    print("="*80 + "\n")
    
    runner = ExperimentRunner()
    
    # Ejecutar familia pequeña (MYC tiene 6 instancias)
    print("📂 Ejecutando familia MYC (6 instancias)...\n")
    runner.run_family('MYC')
    
    # Verificar archivos generados
    output_dir = Path("output")
    latest_folder = max(output_dir.glob("MYC_*"), key=lambda p: p.stat().st_mtime)
    
    print("\n" + "="*80)
    print(f"✅ Carpeta generada: {latest_folder.name}")
    print("="*80 + "\n")
    
    expected_files = [
        "config.json",
        "results.json",
        "RESULTS.md",
        "analysis_report.json",
        "analysis_report.csv",
        "COMPARISON_GAP_ANALYSIS.json",
        "COMPARISON_GAP_ANALYSIS.csv",
        "validation_report.json",
        "EXECUTIVE_SUMMARY.md"
    ]
    
    print("📋 Archivos esperados vs generados:\n")
    
    for filename in expected_files:
        filepath = latest_folder / filename
        status = "✅" if filepath.exists() else "❌"
        size = f"({filepath.stat().st_size} bytes)" if filepath.exists() else "(NO ENCONTRADO)"
        print(f"  {status} {filename:40s} {size}")
    
    # Verificar contenido de COMPARISON_GAP_ANALYSIS.json
    print("\n" + "="*80)
    print("📊 Contenido de COMPARISON_GAP_ANALYSIS.json:")
    print("="*80 + "\n")
    
    import json
    comp_file = latest_folder / "COMPARISON_GAP_ANALYSIS.json"
    if comp_file.exists():
        with open(comp_file, 'r') as f:
            comp_data = json.load(f)
        
        print(f"Familia: {comp_data.get('family')}")
        print(f"Total de instancias: {comp_data['summary'].get('total_instances')}")
        print(f"Con referencia: {comp_data['summary'].get('with_reference')}")
        print(f"Óptimos encontrados: {comp_data['summary'].get('optimal_found')}")
        print(f"GAP promedio: {comp_data['summary'].get('avg_gap_percent', 0):.2f}%")
        
        print("\nPrimeras 3 comparaciones:\n")
        for i, comp in enumerate(comp_data.get('comparisons', [])[:3], 1):
            print(f"  {i}. {comp.get('instance')}")
            ref_val = comp.get('reference_value') if comp.get('reference_value') is not None else 'N/A'
            print(f"     Ref: {ref_val} ({comp.get('reference_type')})")
            gaa_val = comp.get('gaa_value', 'N/A')
            gaa_str = f"{gaa_val:.4f}" if isinstance(gaa_val, (int, float)) else str(gaa_val)
            print(f"     GAA: {gaa_str}")
            gap = comp.get('gap_percent')
            gap_str = f"{gap:.2f}%" if gap is not None else "N/A"
            print(f"     GAP: {gap_str}")
            print()
    else:
        print("❌ COMPARISON_GAP_ANALYSIS.json NO ENCONTRADO")
    
    print("="*80)
    print("✅ TEST COMPLETADO")
    print("="*80 + "\n")

if __name__ == '__main__':
    try:
        test_family_documentation()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
