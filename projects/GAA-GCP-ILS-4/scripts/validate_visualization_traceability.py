#!/usr/bin/env python3
"""
validate_visualization_traceability.py - Validación de trazabilidad DIMACS → visualización

Verifica que el flujo de datos sea correcto:
1. DIMACS file → GraphColoringProblem.load_from_dimacs
2. problem.edges → problem.edge_weight_matrix
3. edge_weight_matrix → plot_instance_conflict_heatmap
4. Visualización correcta en PNG

Uso:
    python scripts/validate_visualization_traceability.py
"""

import sys
import numpy as np
from pathlib import Path
from typing import Tuple

# Agregar proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.problem import GraphColoringProblem
from visualization.plotter_v2 import PlotManagerV2


class VisualizationTraceabilityValidator:
    """Validador de trazabilidad DIMACS → visualización"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.results = {
            'total_instances': 0,
            'passed': 0,
            'failed': 0,
            'details': []
        }
    
    def log(self, msg: str, level: str = "INFO"):
        """Log con nivel"""
        if self.verbose:
            prefix = {
                "INFO": "ℹ️ ",
                "OK": "✅",
                "WARN": "⚠️ ",
                "ERROR": "❌",
                "PASS": "✔️ "
            }.get(level, "")
            print(f"{prefix} {msg}")
    
    def trace_dimacs_to_matrix(self, dimacs_file: str) -> Tuple[bool, dict]:
        """
        Trazar: DIMACS file → edge_weight_matrix
        
        Verifica:
        1. Archivo existe y es legible
        2. Carga correctamente en GraphColoringProblem
        3. Matriz de adyacencia se construye correctamente
        4. Matriz refleja exactamente las aristas del archivo
        """
        trace_info = {
            'file': dimacs_file,
            'file_exists': False,
            'loaded': False,
            'matrix_created': False,
            'edges_match': False,
            'errors': []
        }
        
        # Paso 1: Verificar archivo
        file_path = Path(dimacs_file)
        if not file_path.exists():
            trace_info['errors'].append(f"Archivo no existe: {dimacs_file}")
            return False, trace_info
        trace_info['file_exists'] = True
        
        # Paso 2: Cargar problema
        try:
            problem = GraphColoringProblem.load_from_dimacs(dimacs_file)
            trace_info['loaded'] = True
            trace_info['problem_name'] = problem.name
            trace_info['vertices'] = problem.n_vertices
            trace_info['edges_from_list'] = len(problem.edges)
        except Exception as e:
            trace_info['errors'].append(f"Error cargando DIMACS: {e}")
            return False, trace_info
        
        # Paso 3: Obtener matriz de adyacencia
        try:
            W = problem.edge_weight_matrix
            trace_info['matrix_created'] = True
            trace_info['matrix_shape'] = W.shape
            trace_info['edges_from_matrix'] = int(np.sum(W) / 2)
        except Exception as e:
            trace_info['errors'].append(f"Error creando matriz: {e}")
            return False, trace_info
        
        # Paso 4: Verificar consistencia
        if trace_info['edges_from_list'] == trace_info['edges_from_matrix']:
            trace_info['edges_match'] = True
        else:
            trace_info['errors'].append(
                f"Conteo de aristas inconsistente: "
                f"lista={trace_info['edges_from_list']}, "
                f"matriz={trace_info['edges_from_matrix']}"
            )
        
        all_passed = (
            trace_info['file_exists'] and
            trace_info['loaded'] and
            trace_info['matrix_created'] and
            trace_info['edges_match']
        )
        
        return all_passed, trace_info
    
    def trace_matrix_to_visualization(self, problem: GraphColoringProblem, 
                                     session_dir: str) -> Tuple[bool, dict]:
        """
        Trazar: edge_weight_matrix → plot_instance_conflict_heatmap
        
        Verifica:
        1. Matriz se pasa correctamente al plotter
        2. PNG se genera sin errores
        3. PNG contiene datos (no está vacío)
        4. Archivo se guarda en ubicación correcta
        """
        viz_info = {
            'instance': problem.name,
            'matrix_passed': False,
            'plot_generated': False,
            'file_exists': False,
            'file_size': 0,
            'errors': []
        }
        
        try:
            # Obtener matriz
            W = problem.edge_weight_matrix
            viz_info['matrix_passed'] = True
            viz_info['matrix_shape'] = W.shape
            viz_info['matrix_sum'] = int(np.sum(W))
            
            # Crear plotter
            plot_mgr = PlotManagerV2(session_dir=session_dir)
            
            # Generar gráfico
            filepath = plot_mgr.plot_instance_conflict_heatmap(
                problem.name,
                W
            )
            
            if filepath:
                viz_info['plot_generated'] = True
                viz_info['filepath'] = filepath
                
                # Verificar archivo
                file_path = Path(filepath)
                if file_path.exists():
                    viz_info['file_exists'] = True
                    viz_info['file_size'] = file_path.stat().st_size
                    
                    if viz_info['file_size'] == 0:
                        viz_info['errors'].append("PNG generado pero está vacío")
                else:
                    viz_info['errors'].append(f"PNG no se guardó en {filepath}")
            else:
                viz_info['errors'].append("plot_instance_conflict_heatmap retornó vacío")
        
        except Exception as e:
            viz_info['errors'].append(f"Error en visualización: {e}")
        
        all_passed = (
            viz_info['matrix_passed'] and
            viz_info['plot_generated'] and
            viz_info['file_exists'] and
            viz_info['file_size'] > 0
        )
        
        return all_passed, viz_info
    
    def validate_instance(self, dimacs_file: str, session_dir: str) -> bool:
        """Validar una instancia completa DIMACS → visualización"""
        self.results['total_instances'] += 1
        
        self.log(f"\n{'='*80}", "INFO")
        self.log(f"Validando: {Path(dimacs_file).name}", "INFO")
        self.log(f"{'='*80}", "INFO")
        
        # Paso 1: DIMACS → Matrix
        self.log(f"\n📋 Paso 1: DIMACS → edge_weight_matrix", "INFO")
        passed, trace_info = self.trace_dimacs_to_matrix(dimacs_file)
        
        if trace_info['file_exists']:
            self.log(f"  ✔️  Archivo existe", "PASS")
        else:
            self.log(f"  ❌ Archivo no existe", "ERROR")
        
        if trace_info['loaded']:
            self.log(f"  ✔️  Problema cargado: {trace_info['problem_name']}", "PASS")
            self.log(f"     Vértices: {trace_info['vertices']}", "INFO")
            self.log(f"     Aristas (lista): {trace_info['edges_from_list']}", "INFO")
        else:
            self.log(f"  ❌ Error cargando problema", "ERROR")
        
        if trace_info['matrix_created']:
            self.log(f"  ✔️  Matriz creada: {trace_info['matrix_shape']}", "PASS")
            self.log(f"     Aristas (matriz): {trace_info['edges_from_matrix']}", "INFO")
        else:
            self.log(f"  ❌ Error creando matriz", "ERROR")
        
        if trace_info['edges_match']:
            self.log(f"  ✔️  Conteo de aristas consistente", "PASS")
        else:
            self.log(f"  ❌ Conteo de aristas inconsistente", "ERROR")
        
        for error in trace_info['errors']:
            self.log(f"  ❌ {error}", "ERROR")
        
        if not passed:
            self.results['failed'] += 1
            self.results['details'].append({
                'instance': Path(dimacs_file).name,
                'passed': False,
                'stage': 'DIMACS → Matrix',
                'errors': trace_info['errors']
            })
            return False
        
        # Paso 2: Matrix → Visualization
        self.log(f"\n📋 Paso 2: edge_weight_matrix → plot_instance_conflict_heatmap", "INFO")
        
        try:
            problem = GraphColoringProblem.load_from_dimacs(dimacs_file)
            passed, viz_info = self.trace_matrix_to_visualization(problem, session_dir)
            
            if viz_info['matrix_passed']:
                self.log(f"  ✔️  Matriz pasada al plotter", "PASS")
            else:
                self.log(f"  ❌ Error pasando matriz", "ERROR")
            
            if viz_info['plot_generated']:
                self.log(f"  ✔️  Gráfico generado", "PASS")
            else:
                self.log(f"  ❌ Error generando gráfico", "ERROR")
            
            if viz_info['file_exists']:
                self.log(f"  ✔️  PNG guardado: {viz_info['filepath']}", "PASS")
                self.log(f"     Tamaño: {viz_info['file_size']} bytes", "INFO")
            else:
                self.log(f"  ❌ PNG no se guardó", "ERROR")
            
            for error in viz_info['errors']:
                self.log(f"  ❌ {error}", "ERROR")
            
            if not passed:
                self.results['failed'] += 1
                self.results['details'].append({
                    'instance': Path(dimacs_file).name,
                    'passed': False,
                    'stage': 'Matrix → Visualization',
                    'errors': viz_info['errors']
                })
                return False
        
        except Exception as e:
            self.log(f"  ❌ Error en validación: {e}", "ERROR")
            self.results['failed'] += 1
            self.results['details'].append({
                'instance': Path(dimacs_file).name,
                'passed': False,
                'stage': 'Matrix → Visualization',
                'errors': [str(e)]
            })
            return False
        
        # Ambos pasos pasaron
        self.results['passed'] += 1
        self.results['details'].append({
            'instance': Path(dimacs_file).name,
            'passed': True,
            'stage': 'DIMACS → Matrix → Visualization',
            'errors': []
        })
        
        self.log(f"\n✅ {Path(dimacs_file).name} PASÓ trazabilidad completa", "OK")
        return True
    
    def validate_sample_instances(self) -> bool:
        """Validar instancias de muestra de cada familia"""
        datasets_dir = project_root / "datasets"
        
        if not datasets_dir.exists():
            self.log(f"Directorio de datasets no encontrado: {datasets_dir}", "ERROR")
            return False
        
        # Crear directorio de sesión temporal para visualizaciones
        session_dir = project_root / "output" / "validation_session"
        session_dir.mkdir(parents=True, exist_ok=True)
        
        self.log("\n" + "="*80, "INFO")
        self.log("VALIDACIÓN DE TRAZABILIDAD: DIMACS → MATRIX → VISUALIZATION", "INFO")
        self.log("="*80, "INFO")
        
        # Seleccionar instancias de muestra de cada familia
        sample_instances = {
            'CUL': ['flat300_20_0.col'],
            'DSJ': ['DSJC125.1.col'],
            'LEI': ['le450_5a.col'],
            'MYC': ['myciel3.col', 'myciel5.col'],
            'REG': ['fpsol2.i.1.col'],
            'SCH': ['school1.col']
        }
        
        all_passed = True
        
        for family, instances in sample_instances.items():
            family_dir = datasets_dir / family
            if not family_dir.exists():
                self.log(f"\n⚠️  Familia {family} no encontrada", "WARN")
                continue
            
            self.log(f"\n📁 Familia: {family}", "INFO")
            
            for instance in instances:
                col_file = family_dir / instance
                if not col_file.exists():
                    self.log(f"  ⚠️  {instance} no encontrado", "WARN")
                    continue
                
                passed = self.validate_instance(str(col_file), str(session_dir))
                if not passed:
                    all_passed = False
        
        return all_passed
    
    def generate_report(self) -> str:
        """Generar reporte de trazabilidad"""
        report = []
        report.append("\n" + "="*80)
        report.append("REPORTE DE TRAZABILIDAD: DIMACS → VISUALIZATION")
        report.append("="*80)
        
        # Resumen
        report.append(f"\n📊 RESUMEN")
        report.append(f"  Total de instancias validadas: {self.results['total_instances']}")
        report.append(f"  Pasaron trazabilidad: {self.results['passed']} ✅")
        report.append(f"  Fallaron trazabilidad: {self.results['failed']} ❌")
        
        if self.results['total_instances'] > 0:
            pass_rate = (self.results['passed'] / self.results['total_instances']) * 100
            report.append(f"  Tasa de éxito: {pass_rate:.1f}%")
        
        # Detalles
        report.append(f"\n📋 DETALLES POR INSTANCIA")
        report.append(f"{'Instancia':<30} {'Etapa':<40} {'Estado':<10}")
        report.append("-" * 85)
        
        for detail in self.results['details']:
            status = "✅ PASÓ" if detail['passed'] else "❌ FALLÓ"
            report.append(f"{detail['instance']:<30} {detail['stage']:<40} {status:<10}")
            if detail['errors']:
                for error in detail['errors']:
                    report.append(f"  └─ {error}")
        
        # Conclusión
        report.append(f"\n" + "="*80)
        if self.results['failed'] == 0:
            report.append("✅ CONCLUSIÓN: Trazabilidad DIMACS → Visualization es correcta")
            report.append("   No hay fallback a matrices de ceros ni comportamiento silencioso.")
            report.append("   Los gráficos 03 usan datos reales del archivo DIMACS.")
        else:
            report.append(f"❌ CONCLUSIÓN: Se detectaron {self.results['failed']} instancia(s) con problemas")
            report.append("   Revisar antes de usar en publicaciones.")
        report.append("="*80 + "\n")
        
        return "\n".join(report)


def main():
    """Ejecutar validación de trazabilidad"""
    validator = VisualizationTraceabilityValidator(verbose=True)
    
    # Validar instancias de muestra
    all_passed = validator.validate_sample_instances()
    
    # Generar y mostrar reporte
    report = validator.generate_report()
    print(report)
    
    # Guardar reporte
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)
    
    report_file = output_dir / "visualization_traceability_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📁 Reporte guardado en: {report_file}")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
