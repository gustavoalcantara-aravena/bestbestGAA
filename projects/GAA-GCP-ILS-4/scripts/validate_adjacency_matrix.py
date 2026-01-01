#!/usr/bin/env python3
"""
validate_adjacency_matrix.py - Validación rigurosa de la matriz de adyacencia

Realiza validación end-to-end de:
1. Propiedades matemáticas de la matriz de adyacencia
2. Consistencia en todos los datasets DIMACS
3. Trazabilidad de datos: DIMACS → edge_weight_matrix → visualización
4. Generación de reporte de validación

Uso:
    python scripts/validate_adjacency_matrix.py
"""

import sys
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple

# Agregar proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.problem import GraphColoringProblem


class AdjacencyMatrixValidator:
    """Validador riguroso de matrices de adyacencia"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.results = {
            'total_instances': 0,
            'passed': 0,
            'failed': 0,
            'anomalies': [],
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
    
    def validate_matrix_properties(self, problem: GraphColoringProblem) -> Tuple[bool, List[str]]:
        """
        Validar propiedades matemáticas fundamentales de la matriz de adyacencia
        
        Verifica:
        a) W es cuadrada (n × n)
        b) W es simétrica (W[i][j] == W[j][i])
        c) Diagonal es cero (W[i][i] == 0)
        d) Entradas son binarias (W[i][j] ∈ {0,1})
        """
        errors = []
        W = problem.edge_weight_matrix
        n = problem.n_vertices
        
        # Propiedad a: Matriz cuadrada
        if W.shape != (n, n):
            errors.append(f"Matriz NO es cuadrada: {W.shape} ≠ ({n}×{n})")
        
        # Propiedad b: Simetría
        if not np.allclose(W, W.T):
            asymmetric_pairs = np.where(W != W.T)
            errors.append(f"Matriz NO es simétrica: {len(asymmetric_pairs[0])} pares asimétricos")
        
        # Propiedad c: Diagonal cero
        diagonal = np.diag(W)
        if not np.all(diagonal == 0):
            self_loops = np.where(diagonal != 0)[0]
            errors.append(f"Diagonal NO es cero: {len(self_loops)} auto-loops detectados en vértices {self_loops.tolist()}")
        
        # Propiedad d: Valores binarios
        unique_values = np.unique(W)
        if not np.all(np.isin(unique_values, [0, 1])):
            errors.append(f"Matriz NO es binaria: valores únicos = {unique_values.tolist()}")
        
        return len(errors) == 0, errors
    
    def validate_edge_count(self, problem: GraphColoringProblem) -> Tuple[bool, List[str]]:
        """
        Validar conteo de aristas
        
        Verifica: |E| = sum(W) / 2
        """
        errors = []
        W = problem.edge_weight_matrix
        
        # Calcular aristas desde matriz
        edge_count_from_matrix = int(np.sum(W) / 2)
        edge_count_from_list = len(problem.edges)
        
        if edge_count_from_matrix != edge_count_from_list:
            errors.append(
                f"Conteo de aristas inconsistente: "
                f"matriz={edge_count_from_matrix}, lista={edge_count_from_list}"
            )
        
        return len(errors) == 0, errors
    
    def validate_edge_list_consistency(self, problem: GraphColoringProblem) -> Tuple[bool, List[str]]:
        """
        Validar consistencia entre lista de aristas y matriz
        
        Verifica que cada arista en la lista esté representada en la matriz
        """
        errors = []
        W = problem.edge_weight_matrix
        
        for u, v in problem.edges:
            # Convertir de 1-indexed a 0-indexed
            i, j = u - 1, v - 1
            
            # Verificar que la arista existe en la matriz
            if W[i, j] != 1 or W[j, i] != 1:
                errors.append(f"Arista ({u},{v}) NO representada correctamente en matriz")
        
        # Verificar que no hay aristas en la matriz que no estén en la lista
        for i in range(W.shape[0]):
            for j in range(i + 1, W.shape[1]):
                if W[i, j] == 1:
                    u, v = i + 1, j + 1  # Convertir a 1-indexed
                    if (u, v) not in problem.edges and (v, u) not in problem.edges:
                        errors.append(f"Arista ({u},{v}) en matriz pero NO en lista")
        
        return len(errors) == 0, errors
    
    def validate_indexing(self, problem: GraphColoringProblem) -> Tuple[bool, List[str]]:
        """
        Validar consistencia de indexación (1-based vs 0-based)
        """
        errors = []
        W = problem.edge_weight_matrix
        n = problem.n_vertices
        
        # Verificar que todas las aristas están dentro de rango
        for u, v in problem.edges:
            if u < 1 or u > n or v < 1 or v > n:
                errors.append(f"Arista ({u},{v}) fuera de rango [1,{n}]")
        
        return len(errors) == 0, errors
    
    def validate_instance(self, problem: GraphColoringProblem) -> bool:
        """Validar una instancia completa"""
        instance_name = problem.name
        self.results['total_instances'] += 1
        
        self.log(f"\nValidando: {instance_name}", "INFO")
        self.log(f"  Vértices: {problem.n_vertices}, Aristas: {problem.n_edges}", "INFO")
        
        all_passed = True
        instance_errors = []
        
        # Validación 1: Propiedades matemáticas
        passed, errors = self.validate_matrix_properties(problem)
        if not passed:
            all_passed = False
            instance_errors.extend(errors)
            for error in errors:
                self.log(f"  ❌ {error}", "ERROR")
        else:
            self.log(f"  ✔️  Propiedades matemáticas correctas", "PASS")
        
        # Validación 2: Conteo de aristas
        passed, errors = self.validate_edge_count(problem)
        if not passed:
            all_passed = False
            instance_errors.extend(errors)
            for error in errors:
                self.log(f"  ❌ {error}", "ERROR")
        else:
            self.log(f"  ✔️  Conteo de aristas consistente", "PASS")
        
        # Validación 3: Consistencia lista-matriz
        passed, errors = self.validate_edge_list_consistency(problem)
        if not passed:
            all_passed = False
            instance_errors.extend(errors)
            for error in errors:
                self.log(f"  ❌ {error}", "ERROR")
        else:
            self.log(f"  ✔️  Consistencia lista-matriz correcta", "PASS")
        
        # Validación 4: Indexación
        passed, errors = self.validate_indexing(problem)
        if not passed:
            all_passed = False
            instance_errors.extend(errors)
            for error in errors:
                self.log(f"  ❌ {error}", "ERROR")
        else:
            self.log(f"  ✔️  Indexación correcta", "PASS")
        
        # Actualizar resultados
        if all_passed:
            self.results['passed'] += 1
            self.log(f"  ✅ {instance_name} PASÓ todas las validaciones", "OK")
        else:
            self.results['failed'] += 1
            self.results['anomalies'].append({
                'instance': instance_name,
                'errors': instance_errors
            })
            self.log(f"  ❌ {instance_name} FALLÓ validación", "ERROR")
        
        self.results['details'].append({
            'instance': instance_name,
            'vertices': problem.n_vertices,
            'edges': problem.n_edges,
            'passed': all_passed,
            'errors': instance_errors
        })
        
        return all_passed
    
    def validate_all_datasets(self) -> bool:
        """Validar todos los datasets DIMACS"""
        datasets_dir = project_root / "datasets"
        
        if not datasets_dir.exists():
            self.log(f"Directorio de datasets no encontrado: {datasets_dir}", "ERROR")
            return False
        
        families = ["CUL", "DSJ", "LEI", "MYC", "REG", "SCH", "SGB"]
        all_passed = True
        
        self.log("\n" + "="*80, "INFO")
        self.log("VALIDACIÓN DE MATRIZ DE ADYACENCIA - TODOS LOS DATASETS", "INFO")
        self.log("="*80, "INFO")
        
        for family in families:
            family_dir = datasets_dir / family
            if not family_dir.exists():
                self.log(f"\nFamilia {family} no encontrada", "WARN")
                continue
            
            self.log(f"\n📁 Familia: {family}", "INFO")
            col_files = sorted(family_dir.glob("*.col"))
            
            if not col_files:
                self.log(f"  No hay archivos .col en {family}", "WARN")
                continue
            
            for col_file in col_files:
                try:
                    problem = GraphColoringProblem.load_from_dimacs(str(col_file))
                    passed = self.validate_instance(problem)
                    if not passed:
                        all_passed = False
                except Exception as e:
                    self.log(f"  ❌ Error cargando {col_file.name}: {e}", "ERROR")
                    all_passed = False
                    self.results['failed'] += 1
                    self.results['total_instances'] += 1
        
        return all_passed
    
    def generate_report(self) -> str:
        """Generar reporte de validación"""
        report = []
        report.append("\n" + "="*80)
        report.append("REPORTE DE VALIDACIÓN DE MATRIZ DE ADYACENCIA")
        report.append("="*80)
        
        # Resumen
        report.append(f"\n📊 RESUMEN")
        report.append(f"  Total de instancias: {self.results['total_instances']}")
        report.append(f"  Pasaron validación: {self.results['passed']} ✅")
        report.append(f"  Fallaron validación: {self.results['failed']} ❌")
        
        if self.results['total_instances'] > 0:
            pass_rate = (self.results['passed'] / self.results['total_instances']) * 100
            report.append(f"  Tasa de éxito: {pass_rate:.1f}%")
        
        # Anomalías detectadas
        if self.results['anomalies']:
            report.append(f"\n⚠️  ANOMALÍAS DETECTADAS ({len(self.results['anomalies'])})")
            for anomaly in self.results['anomalies']:
                report.append(f"\n  Instancia: {anomaly['instance']}")
                for error in anomaly['errors']:
                    report.append(f"    - {error}")
        else:
            report.append(f"\n✅ NO SE DETECTARON ANOMALÍAS")
        
        # Detalles por instancia
        report.append(f"\n📋 DETALLES POR INSTANCIA")
        report.append(f"{'Instancia':<30} {'V':<6} {'E':<8} {'Estado':<10}")
        report.append("-" * 60)
        
        for detail in self.results['details']:
            status = "✅ PASÓ" if detail['passed'] else "❌ FALLÓ"
            report.append(f"{detail['instance']:<30} {detail['vertices']:<6} {detail['edges']:<8} {status:<10}")
        
        # Conclusión
        report.append(f"\n" + "="*80)
        if self.results['failed'] == 0:
            report.append("✅ CONCLUSIÓN: Todas las matrices de adyacencia son matemáticamente correctas")
            report.append("   y pueden ser incluidas en publicaciones científicas con confianza.")
        else:
            report.append(f"❌ CONCLUSIÓN: Se detectaron {self.results['failed']} instancia(s) con problemas")
            report.append("   Revisar anomalías antes de usar en publicaciones.")
        report.append("="*80 + "\n")
        
        return "\n".join(report)


def main():
    """Ejecutar validación completa"""
    validator = AdjacencyMatrixValidator(verbose=True)
    
    # Validar todos los datasets
    all_passed = validator.validate_all_datasets()
    
    # Generar y mostrar reporte
    report = validator.generate_report()
    print(report)
    
    # Guardar reporte
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)
    
    report_file = output_dir / "adjacency_matrix_validation_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📁 Reporte guardado en: {report_file}")
    
    # Retornar código de salida
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
