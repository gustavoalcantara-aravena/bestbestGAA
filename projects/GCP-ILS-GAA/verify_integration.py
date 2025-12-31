#!/usr/bin/env python3
"""
verify_integration.py - Verificar que el sistema está completamente integrado
"""

import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Verificar si un archivo existe"""
    exists = filepath.exists()
    status = "✅" if exists else "❌"
    print(f"  {status} {description:50s} {filepath.name}")
    return exists

def verify_integration():
    """Verificar integración completa"""
    
    print("\n" + "="*80)
    print("🔍 VERIFICACIÓN DE INTEGRACIÓN DEL SISTEMA")
    print("="*80 + "\n")
    
    project_root = Path.cwd()
    scripts_dir = project_root / "scripts"
    
    print("1️⃣  SCRIPTS PRINCIPALES\n")
    
    files_to_check = [
        (project_root / "main.py", "Punto de entrada principal"),
        (scripts_dir / "execute_experiments.py", "Script maestro"),
        (scripts_dir / "run_experiments.py", "Ejecutor de experimentos"),
        (scripts_dir / "document_orchestrator.py", "Orquestador de documentación"),
        (scripts_dir / "regenerate_reports.py", "Regeneración de reportes"),
        (scripts_dir / "gaa_executor.py", "Ejecutor GAA"),
    ]
    
    all_exist = True
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_exist = False
    
    print(f"\n   Status: {'✅ OK' if all_exist else '❌ FALTAN ARCHIVOS'}\n")
    
    # Verificar integración en run_experiments.py
    print("2️⃣  INTEGRACIÓN EN run_experiments.py\n")
    
    run_exp = scripts_dir / "run_experiments.py"
    try:
        content = run_exp.read_text(encoding='utf-8')
    except:
        content = run_exp.read_text(encoding='latin-1')
    
    checks = [
        ("DocumentationOrchestrator", "Importación del orquestador"),
        ("DOC_ORCHESTRATOR.generate_all_reports", "Uso en run_single_instance()"),
    ]
    
    integration_ok = True
    for text, description in checks:
        found = text in content
        status = "✅" if found else "❌"
        print(f"  {status} {description:50s} ({text})")
        if not found:
            integration_ok = False
    
    print(f"\n   Status: {'✅ OK' if integration_ok else '❌ FALTA INTEGRACIÓN'}\n")
    
    # Verificar carpetas de salida
    print("3️⃣  ESTRUCTURA DE OUTPUT\n")
    
    output_dir = project_root / "output"
    
    if output_dir.exists():
        folders = list(output_dir.glob("MYC_*"))
        if folders:
            latest = max(folders, key=lambda p: p.stat().st_mtime)
            print(f"   Carpeta más reciente: {latest.name}\n")
            
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
            
            generated_count = 0
            for filename in expected_files:
                filepath = latest / filename
                exists = filepath.exists()
                status = "✅" if exists else "❌"
                print(f"   {status} {filename}")
                if exists:
                    generated_count += 1
            
            print(f"\n   Archivos: {generated_count}/{len(expected_files)}")
            print(f"   Status: {'✅ COMPLETO' if generated_count == len(expected_files) else '⚠️  INCOMPLETO'}\n")
        else:
            print("   ⚠️  No hay carpetas de ejecución (ejecuta un experimento primero)\n")
    else:
        print("   ❌ Carpeta output no existe\n")
    
    # Documentación
    print("4️⃣  DOCUMENTACIÓN\n")
    
    doc_dir = project_root / "documentacion"
    doc_files = [
        "DOCUMENTATION_GENERATION_FLOW.md",
        "SISTEMA_INTEGRADO_CONFIRMACION.md",
    ]
    
    doc_ok = True
    for filename in doc_files:
        filepath = doc_dir / filename
        exists = filepath.exists()
        status = "✅" if exists else "❌"
        print(f"   {status} {filename}")
        if not exists:
            doc_ok = False
    
    print(f"\n   Status: {'✅ OK' if doc_ok else '⚠️  FALTA DOCUMENTACIÓN'}\n")
    
    # Resumen final
    print("="*80)
    print("📋 RESUMEN FINAL")
    print("="*80 + "\n")
    
    if all_exist and integration_ok and generated_count == len(expected_files) and doc_ok:
        print("✅ SISTEMA COMPLETAMENTE INTEGRADO Y FUNCIONAL\n")
        print("El usuario puede ejecutar:\n")
        print("   python main.py --family CUL")
        print("\nY encontrará TODO en: output/CUL_DD_MM_YY_HH_MM/\n")
        return 0
    else:
        print("⚠️  REVISAR LOS PUNTOS MARCADOS CON ❌\n")
        return 1

if __name__ == '__main__':
    sys.exit(verify_integration())
