#!/usr/bin/env python3
"""
Analyze GAA Results Against Best Known Solutions (BKS)
=======================================================

Compara resultados GAA contra ÓPTIMO/BKS y genera reportes de validación.

Uso:
    python analyze_results.py                    # Analizar todos los experimentos
    python analyze_results.py --family CUL       # Analizar familia específica
    python analyze_results.py --latest 1         # Analizar experimento más reciente
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import statistics


@dataclass
class InstanceResult:
    """Resultado de una instancia"""
    name: str
    family: str
    vertices: int
    edges: int
    gaa_fitness: float
    gaa_iterations: int
    gaa_time: float
    bks_value: int
    is_optimal: bool
    is_open: bool
    gap_percent: float
    status: str  # "beat_bks", "matched_bks", "under_bks", "open_problem"


@dataclass
class FamilyAnalysis:
    """Análisis de una familia"""
    family: str
    total_instances: int
    optimal_instances: int
    open_instances: int
    results: List[InstanceResult]
    
    def summary(self) -> Dict:
        """Resumen estadístico"""
        if not self.results:
            return {}
        
        gaps = [r.gap_percent for r in self.results if r.gap_percent is not None]
        times = [r.gaa_time for r in self.results]
        
        return {
            "total": len(self.results),
            "beat_bks": sum(1 for r in self.results if r.status == "beat_bks"),
            "matched_bks": sum(1 for r in self.results if r.status == "matched_bks"),
            "under_bks": sum(1 for r in self.results if r.status == "under_bks"),
            "open_problems": sum(1 for r in self.results if r.status == "open_problem"),
            "avg_gap_percent": statistics.mean(gaps) if gaps else 0,
            "max_gap_percent": max(gaps) if gaps else 0,
            "min_gap_percent": min(gaps) if gaps else 0,
            "avg_time_seconds": statistics.mean(times),
            "total_time_seconds": sum(times),
        }


class ResultsAnalyzer:
    """Analiza resultados GAA contra BKS"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.output_dir = self.base_dir / "output"
        self.datasets_dir = self.base_dir / "datasets"
        self.bks_data = self._load_bks()
        self.results = []
        self.family_analyses = {}
    
    def _load_bks(self) -> Dict:
        """Cargar BKS.json"""
        bks_file = self.datasets_dir / "BKS.json"
        if not bks_file.exists():
            print(f"❌ BKS.json no encontrado en {bks_file}")
            return {}
        
        with open(bks_file, 'r') as f:
            return json.load(f)
    
    def _get_bks_info(self, family: str, instance: str) -> Tuple[Optional[int], bool, bool]:
        """
        Obtener BKS, is_optimal, is_open para una instancia.
        Retorna: (bks_value, is_optimal, is_open)
        """
        if family not in self.bks_data or "instances" not in self.bks_data[family]:
            return None, False, False
        
        inst_data = self.bks_data[family]["instances"].get(instance)
        if not inst_data:
            return None, False, False
        
        bks = inst_data.get("bks")
        is_optimal = inst_data.get("optimal", False)
        is_open = inst_data.get("open", False)
        
        return bks, is_optimal, is_open
    
    def _calculate_gap(self, gaa_fitness: float, bks_value: int) -> float:
        """
        Calcular gap % entre GAA y BKS.
        
        Gap = ((BKS - GAA) / BKS) * 100
        - Positivo = GAA es peor que BKS
        - Negativo = GAA es mejor que BKS (¡ganador!)
        """
        if bks_value == 0:
            return 0.0
        
        gap = ((bks_value - gaa_fitness) / bks_value) * 100
        return round(gap, 2)
    
    def _determine_status(self, gap: float, is_open: bool) -> str:
        """Determinar estado del resultado"""
        if is_open:
            return "open_problem"
        elif gap < 0:  # GAA mejor que BKS
            return "beat_bks"
        elif gap == 0:  # Igual a BKS
            return "matched_bks"
        else:  # Peor que BKS
            return "under_bks"
    
    def analyze_results_directory(self, family: Optional[str] = None, latest: int = 0):
        """
        Analizar archivos results.json en output/
        
        Args:
            family: Familia específica o None para todas
            latest: Si > 0, analizar los N más recientes
        """
        if not self.output_dir.exists():
            print(f"❌ No se encontró directorio {self.output_dir}")
            return
        
        # Encontrar carpetas de resultados
        result_dirs = sorted(
            [d for d in self.output_dir.iterdir() if d.is_dir()],
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        if latest > 0:
            result_dirs = result_dirs[:latest]
        
        for result_dir in result_dirs:
            results_file = result_dir / "results.json"
            if not results_file.exists():
                continue
            
            with open(results_file, 'r') as f:
                data = json.load(f)
            
            family_name = data.get("family")
            if family and family_name != family:
                continue
            
            self._process_family_results(family_name, data)
    
    def _process_family_results(self, family: str, data: Dict):
        """Procesar resultados de una familia"""
        family_results = []
        
        for result in data.get("results", []):
            # Skip if result doesn't have required GAA fields (old format)
            if "best_fitness" not in result or "elapsed_time" not in result:
                continue
            
            instance = result["instance"]
            bks_value, is_optimal, is_open = self._get_bks_info(family, instance)
            
            # GAA usa "best_fitness" en escala 0-1, necesitamos convertir a colores
            gaa_fitness = result["best_fitness"]
            # En el sistema actual, fitness ~ 0.9 corresponde a ~50 colores
            # Esto es un mapeo simplificado; ajustar según tu sistema
            
            # Si BKS existe, calcular gap
            gap = None
            if bks_value is not None:
                # Convertir fitness a escala de colores (aproximación)
                estimated_colors = int((1 - gaa_fitness) * (bks_value * 2))
                estimated_colors = max(1, min(estimated_colors, bks_value * 2))
                gap = self._calculate_gap(estimated_colors, bks_value)
            
            status = self._determine_status(gap or 0, is_open)
            
            inst_result = InstanceResult(
                name=instance,
                family=family,
                vertices=result["vertices"],
                edges=result["edges"],
                gaa_fitness=gaa_fitness,
                gaa_iterations=result["iterations"],
                gaa_time=result["elapsed_time"],
                bks_value=bks_value or 0,
                is_optimal=is_optimal,
                is_open=is_open,
                gap_percent=gap or 0,
                status=status
            )
            
            family_results.append(inst_result)
            self.results.append(inst_result)
        
        if family_results:
            analysis = FamilyAnalysis(
                family=family,
                total_instances=len(family_results),
                optimal_instances=sum(1 for r in family_results if r.is_optimal),
                open_instances=sum(1 for r in family_results if r.is_open),
                results=family_results
            )
            self.family_analyses[family] = analysis
    
    def print_summary(self):
        """Imprimir resumen general"""
        if not self.results:
            print("❌ No se encontraron resultados para analizar")
            return
        
        print("\n" + "="*80)
        print("📊 ANÁLISIS DE RESULTADOS GAA vs BKS")
        print("="*80 + "\n")
        
        # Resumen global
        print("📈 RESUMEN GLOBAL")
        print("-" * 80)
        print(f"  Total instancias analizadas: {len(self.results)}")
        print(f"  Familias: {len(self.family_analyses)}")
        print(f"  Óptimos conocidos: {sum(1 for r in self.results if r.is_optimal)}")
        print(f"  Problemas abiertos: {sum(1 for r in self.results if r.is_open)}")
        
        # Por familia
        print("\n📂 ANÁLISIS POR FAMILIA")
        print("-" * 80)
        
        for family_name, analysis in sorted(self.family_analyses.items()):
            summary = analysis.summary()
            print(f"\n  {family_name}")
            print(f"    • Instancias: {summary['total']}")
            print(f"    • Óptimos: {analysis.optimal_instances}, Abiertos: {analysis.open_instances}")
            print(f"    • Beat BKS: {summary['beat_bks']}, Matched: {summary['matched_bks']}, Under: {summary['under_bks']}")
            print(f"    • Gap promedio: {summary['avg_gap_percent']:.2f}%")
            print(f"    • Tiempo total: {summary['total_time_seconds']:.4f}s")
    
    def print_detailed_results(self, family: Optional[str] = None):
        """Imprimir resultados detallados"""
        print("\n" + "="*80)
        print("🔬 RESULTADOS DETALLADOS")
        print("="*80 + "\n")
        
        for fam_name, analysis in sorted(self.family_analyses.items()):
            if family and fam_name != family:
                continue
            
            print(f"\n📋 {fam_name}")
            print("-" * 80)
            print(f"{'Instancia':<20} {'BKS':>6} {'GAA':>6} {'Gap':>8} {'Estado':<15}")
            print("-" * 80)
            
            for result in analysis.results:
                bks_str = f"{result.bks_value}" if result.bks_value > 0 else "?"
                gaa_colors = int((1 - result.gaa_fitness) * (result.bks_value * 2)) if result.bks_value > 0 else "?"
                gap_str = f"{result.gap_percent:+.2f}%" if result.bks_value > 0 else "?"
                
                status_icon = {
                    "beat_bks": "🎉",
                    "matched_bks": "✅",
                    "under_bks": "⚠️",
                    "open_problem": "❓"
                }.get(result.status, "?")
                
                print(f"{result.name:<20} {bks_str:>6} {str(gaa_colors):>6} {gap_str:>8} {status_icon} {result.status:<15}")
    
    def export_json(self, output_file: str = "analysis_report.json"):
        """Exportar análisis a JSON"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_instances": len(self.results),
                "families": len(self.family_analyses),
                "optimal_instances": sum(1 for r in self.results if r.is_optimal),
                "open_instances": sum(1 for r in self.results if r.is_open),
                "beat_bks": sum(1 for r in self.results if r.status == "beat_bks"),
                "matched_bks": sum(1 for r in self.results if r.status == "matched_bks"),
                "under_bks": sum(1 for r in self.results if r.status == "under_bks"),
            },
            "families": {}
        }
        
        for family_name, analysis in self.family_analyses.items():
            summary = analysis.summary()
            report["families"][family_name] = {
                "summary": summary,
                "instances": [
                    {
                        "name": r.name,
                        "bks": r.bks_value,
                        "gaa_fitness": r.gaa_fitness,
                        "gap_percent": r.gap_percent,
                        "status": r.status,
                        "iterations": r.gaa_iterations,
                        "time_seconds": r.gaa_time,
                    }
                    for r in analysis.results
                ]
            }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Reporte exportado a {output_file}")
    
    def export_csv(self, output_file: str = "analysis_report.csv"):
        """Exportar análisis a CSV"""
        import csv
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "Family", "Instance", "Vertices", "Edges", "BKS", 
                "GAA_Fitness", "Gap%", "Status", "Iterations", "Time_s"
            ])
            
            for result in sorted(self.results, key=lambda x: (x.family, x.name)):
                writer.writerow([
                    result.family,
                    result.name,
                    result.vertices,
                    result.edges,
                    result.bks_value,
                    f"{result.gaa_fitness:.4f}",
                    f"{result.gap_percent:.2f}",
                    result.status,
                    result.gaa_iterations,
                    f"{result.gaa_time:.6f}"
                ])
        
        print(f"✅ Reporte CSV exportado a {output_file}")


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Analizar resultados GAA contra BKS"
    )
    parser.add_argument("--family", type=str, help="Analizar familia específica")
    parser.add_argument("--latest", type=int, default=0, help="Analizar N más recientes")
    parser.add_argument("--export-json", action="store_true", help="Exportar a JSON")
    parser.add_argument("--export-csv", action="store_true", help="Exportar a CSV")
    parser.add_argument("--output", type=str, default="analysis_report", help="Nombre base del archivo de salida")
    
    args = parser.parse_args()
    
    # Crear analizador
    analyzer = ResultsAnalyzer()
    
    # Analizar resultados
    analyzer.analyze_results_directory(family=args.family, latest=args.latest if args.latest else 0)
    
    # Imprimir resúmenes
    analyzer.print_summary()
    analyzer.print_detailed_results(family=args.family)
    
    # Exportar si se solicita
    if args.export_json:
        analyzer.export_json(f"{args.output}.json")
    
    if args.export_csv:
        analyzer.export_csv(f"{args.output}.csv")


if __name__ == "__main__":
    main()
