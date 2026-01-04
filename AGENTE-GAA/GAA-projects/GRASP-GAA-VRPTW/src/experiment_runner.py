"""
============================================================
Experiment Runner
GRASP + GAA for VRPTW (Solomon)
============================================================

Orquestador del experimento completo:
- Carga configuración
- Itera sobre instancias y algoritmos
- Ejecuta GRASP solver
- Evalúa contra BKS
- Genera logs JSONL

Uso:
    runner = ExperimentRunner(config_path="config/config.yaml")
    runner.run_experiment()
"""

import json
import yaml
import time
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import uuid

from evaluation.bks_loader import BKSLoader
from evaluation.bks_validation import validate_solution_vs_bks
from evaluation.solution_evaluator import evaluate_solution_full


class ExperimentRunner:
    """
    Orquestador de experimentos.
    
    Responsabilidades:
    - Cargar configuración (YAML)
    - Iterar sobre instancias y algoritmos
    - Ejecutar GRASP solver
    - Evaluar soluciones
    - Loguear resultados en JSONL
    - Generar reportes
    """
    
    def __init__(self, config_path: str):
        """
        Inicializa el runner.
        
        Args:
            config_path: Ruta a config.yaml
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
        # Inicializar BKS loader
        bks_file = Path(self.config["bks"]["file"])
        self.bks_loader = BKSLoader(str(bks_file))
        
        # Output
        self.output_dir = Path(self.config["logging"]["output_dir"])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Logs
        self.log_file = self.output_dir / f"experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Experiment metadata
        self.experiment_id = str(uuid.uuid4())[:8]
        self.start_time = None
    
    def _load_config(self) -> Dict[str, Any]:
        """Carga configuración desde YAML."""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def run_experiment(self) -> Dict[str, Any]:
        """
        Ejecuta el experimento completo.
        
        Returns:
            Dict con resultados agregados
        """
        self.start_time = datetime.now()
        print(f"🚀 Iniciando experimento {self.experiment_id}")
        print(f"📝 Logs: {self.log_file}")
        
        results = {
            "experiment_id": self.experiment_id,
            "timestamp": self.start_time.isoformat(),
            "total_runs": 0,
            "successful_runs": 0,
            "failed_runs": 0,
            "results_by_instance": {},
            "aggregate_stats": {}
        }
        
        # Iterar sobre instancias
        instances = self._get_instances_to_run()
        print(f"📊 Instancias a procesar: {len(instances)}")
        
        for instance_id in instances:
            try:
                run_result = self._run_single_instance(instance_id)
                results["total_runs"] += 1
                results["successful_runs"] += 1
                results["results_by_instance"][instance_id] = run_result
                
                # Log JSONL
                self._log_result(run_result)
                
            except Exception as e:
                results["total_runs"] += 1
                results["failed_runs"] += 1
                print(f"❌ Error en {instance_id}: {e}")
        
        # Estadísticas finales
        results["aggregate_stats"] = self._compute_aggregate_stats(results)
        results["duration_seconds"] = (datetime.now() - self.start_time).total_seconds()
        
        # Guardar resumen
        self._save_summary(results)
        
        print(f"\n✅ Experimento completado en {results['duration_seconds']:.1f}s")
        print(f"   Éxitos: {results['successful_runs']}/{results['total_runs']}")
        
        return results
    
    def _get_instances_to_run(self) -> List[str]:
        """Obtiene lista de instancias a procesar."""
        eval_config = self.config.get("evaluation", {})
        
        instances = []
        for family in ["design_set", "selection_set", "evaluation_set"]:
            if family in eval_config:
                instances.extend(eval_config[family])
        
        # Remover duplicados
        return sorted(list(set(instances)))
    
    def _run_single_instance(self, instance_id: str) -> Dict[str, Any]:
        """
        Ejecuta GRASP para una instancia.
        
        TODO: Integrar con GRASPSolver real
        """
        bks_entry = self.bks_loader.get_or_raise(instance_id)
        
        print(f"  ▶ Procesando {instance_id}...")
        
        # Placeholder: simulación de solución (reemplazar con solver real)
        solution_metrics = {
            "instance_id": instance_id,
            "n_vehicles": bks_entry.n_vehicles - 1,  # Simulación: mejorar BKS
            "total_distance": bks_entry.total_distance * 0.95,
            "feasible": True
        }
        
        # Validar contra BKS
        comparison = validate_solution_vs_bks(solution_metrics, bks_entry)
        
        # Preparar registro para JSONL
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "experiment_id": self.experiment_id,
            "instance_id": instance_id,
            "algorithm_id": "GRASP-v1",  # Reemplazar con ID real del AST
            "run_id": 1,  # Reemplazar con número de run real
            "seed": self.config["random"]["global_seed"],
            
            # Métricas
            **comparison.to_dict(),
            
            # Timing (simulado)
            "cpu_time_sec": 1.234,
            "status": "OK" if comparison.feasible else "INFEASIBLE"
        }
        
        return log_entry
    
    def _log_result(self, log_entry: Dict[str, Any]) -> None:
        """Escribe resultado en JSONL."""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def _compute_aggregate_stats(self, results: Dict) -> Dict[str, Any]:
        """Calcula estadísticas agregadas."""
        instance_results = list(results["results_by_instance"].values())
        
        if not instance_results:
            return {}
        
        feasible_count = sum(1 for r in instance_results if r.get("feasible", False))
        dominates_count = sum(1 for r in instance_results if r.get("dominates_bks", False))
        gaps = [r.get("distance_gap_percent", 0) for r in instance_results]
        
        return {
            "total_instances": len(instance_results),
            "feasible_count": feasible_count,
            "feasible_percent": feasible_count / len(instance_results) * 100,
            "dominates_count": dominates_count,
            "avg_gap_percent": sum(gaps) / len(gaps) if gaps else 0,
            "min_gap_percent": min(gaps) if gaps else 0,
            "max_gap_percent": max(gaps) if gaps else 0,
        }
    
    def _save_summary(self, results: Dict) -> None:
        """Guarda resumen en JSON."""
        summary_file = self.output_dir / f"experiment_{self.experiment_id}_summary.json"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"📄 Resumen: {summary_file}")


# ============================================================
# Script de ejecución
# ============================================================

if __name__ == "__main__":
    runner = ExperimentRunner(config_path="config/config.yaml")
    results = runner.run_experiment()
    
    print("\n" + "="*60)
    print("RESULTADOS AGREGADOS")
    print("="*60)
    for key, value in results["aggregate_stats"].items():
        if isinstance(value, float):
            print(f"{key:30} {value:10.2f}")
        else:
            print(f"{key:30} {value:10}")
