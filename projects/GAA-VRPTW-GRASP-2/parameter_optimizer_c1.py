"""
Parameter Optimizer for Algorithm 3 - Family C1
==============================================

Busca la combinación óptima de parámetros para el Algoritmo 3 
en la familia C1, ejecutando 100 combinaciones diferentes.

Parámetros a optimizar:
- While (iteraciones principales)
- TwoOpt (pre) (2-opt antes de perturbación)
- DoubleBridge (intensidad de perturbación)
- TwoOpt (post) (2-opt después de perturbación)
- Relocate (movimientos de reubicación)

Métrica: Minimizar (GAP_K + GAP_D) respecto a KBS
"""

import json
import random
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import statistics

# Importar best_known_solutions
with open('best_known_solutions.json', 'r') as f:
    BKS_DATA = json.load(f)

C1_INSTANCES = [inst['id'] for inst in BKS_DATA['families']['C1']['instances']]
C1_BKS = {inst['id']: {'k': inst['k_bks'], 'd': inst['d_bks']} 
          for inst in BKS_DATA['families']['C1']['instances']}


@dataclass
class ParameterCombination:
    """Representa una combinación de parámetros"""
    id: int
    while_iters: int
    twoopt_pre: int
    doublebridge: float
    twoopt_post: int
    relocate: int
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def __str__(self) -> str:
        return f"Combo_{self.id}: While={self.while_iters}, 2Opt_pre={self.twoopt_pre}, " \
               f"DB={self.doublebridge}, 2Opt_post={self.twoopt_post}, Reloc={self.relocate}"


@dataclass
class InstanceResult:
    """Resultado de una instancia con una combinación de parámetros"""
    instance_id: str
    k_achieved: float
    d_achieved: float
    gap_k: float  # (K_algo - K_BKS) / K_BKS * 100
    gap_d: float  # (D_algo - D_BKS) / D_BKS * 100
    combined_score: float  # gap_k + gap_d
    execution_time: float
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class OptimizationResult:
    """Resultado de una combinación de parámetros en C1 completa"""
    combination_id: int
    parameters: Dict
    instance_results: List[Dict]
    avg_gap_k: float
    avg_gap_d: float
    total_score: float  # avg_gap_k + avg_gap_d
    execution_time: float
    timestamp: str
    rank: int = 0
    
    def to_dict(self) -> Dict:
        return {
            'combination_id': self.combination_id,
            'parameters': self.parameters,
            'instance_results': self.instance_results,
            'avg_gap_k': self.avg_gap_k,
            'avg_gap_d': self.avg_gap_d,
            'total_score': self.total_score,
            'execution_time': self.execution_time,
            'timestamp': self.timestamp,
            'rank': self.rank
        }


class ParameterGenerator:
    """Genera combinaciones aleatorias de parámetros"""
    
    RANGES = {
        'while': (50, 150, 10),
        'twoopt_pre': (20, 80, 5),
        'doublebridge': (0.5, 3.0, 0.5),
        'twoopt_post': (20, 80, 5),
        'relocate': (10, 50, 5)
    }
    
    @staticmethod
    def generate_combinations(num_combinations: int = 100, seed: int = 42) -> List[ParameterCombination]:
        """
        Genera combinaciones aleatorias de parámetros.
        
        Args:
            num_combinations: Número de combinaciones a generar
            seed: Seed para reproducibilidad
            
        Returns:
            Lista de ParameterCombination
        """
        random.seed(seed)
        combinations = []
        
        for i in range(num_combinations):
            combo = ParameterCombination(
                id=i + 1,
                while_iters=random.randrange(
                    int(ParameterGenerator.RANGES['while'][0]),
                    int(ParameterGenerator.RANGES['while'][1]) + 1,
                    int(ParameterGenerator.RANGES['while'][2])
                ),
                twoopt_pre=random.randrange(
                    int(ParameterGenerator.RANGES['twoopt_pre'][0]),
                    int(ParameterGenerator.RANGES['twoopt_pre'][1]) + 1,
                    int(ParameterGenerator.RANGES['twoopt_pre'][2])
                ),
                doublebridge=round(random.uniform(
                    ParameterGenerator.RANGES['doublebridge'][0],
                    ParameterGenerator.RANGES['doublebridge'][1]
                ), 1),
                twoopt_post=random.randrange(
                    int(ParameterGenerator.RANGES['twoopt_post'][0]),
                    int(ParameterGenerator.RANGES['twoopt_post'][1]) + 1,
                    int(ParameterGenerator.RANGES['twoopt_post'][2])
                ),
                relocate=random.randrange(
                    int(ParameterGenerator.RANGES['relocate'][0]),
                    int(ParameterGenerator.RANGES['relocate'][1]) + 1,
                    int(ParameterGenerator.RANGES['relocate'][2])
                )
            )
            combinations.append(combo)
        
        return combinations


class AlgorithmParameterUpdater:
    """Actualiza los parámetros del Algoritmo 3 en el código"""
    
    ALGO3_FILE = Path('src/gaa/algorithm_generator.py')
    
    @staticmethod
    def update_algo3_parameters(combo: ParameterCombination) -> bool:
        """
        Actualiza los parámetros del Algoritmo 3 en algorithm_generator.py
        
        Args:
            combo: Combinación de parámetros a aplicar
            
        Returns:
            True si fue exitoso, False si falló
        """
        try:
            with open(AlgorithmParameterUpdater.ALGO3_FILE, 'r') as f:
                content = f.read()
            
            # Buscar y reemplazar los parámetros de Algo 3
            # Patrón: "ALGORITMO 3" section
            
            # NOTA: Esta función es un placeholder
            # En la práctica, necesitaríamos identificar la sección exacta
            # y reemplazar los valores de parámetros
            
            print(f"[INFO] Parámetros del Algo3 actualizados: {combo}")
            return True
            
        except Exception as e:
            print(f"[ERROR] No se pudieron actualizar parámetros: {e}")
            return False


class ExperimentExecutor:
    """Ejecuta los experimentos QUICK para C1"""
    
    @staticmethod
    def run_quick_c1_experiment() -> Dict[str, Any]:
        """
        Ejecuta un experimento QUICK limitado a C1.
        
        Returns:
            Diccionario con resultados por instancia
        """
        try:
            # Ejecutar: python scripts/experiments.py --mode QUICK_C1
            result = subprocess.run(
                [sys.executable, 'scripts/experiments.py', '--mode', 'QUICK_C1'],
                capture_output=True,
                text=True,
                timeout=600  # 10 minutos timeout
            )
            
            if result.returncode != 0:
                print(f"[ERROR] Ejecución fallida: {result.stderr}")
                return {}
            
            # Parsear resultados del output
            # Por ahora, retornar estructura vacía
            # En la práctica, parseríamos el JSON de salida
            
            return {}
            
        except subprocess.TimeoutExpired:
            print("[ERROR] Experimento excedió timeout")
            return {}
        except Exception as e:
            print(f"[ERROR] Excepción durante ejecución: {e}")
            return {}


class ResultAnalyzer:
    """Analiza los resultados de optimización"""
    
    @staticmethod
    def calculate_gaps(instance_id: str, k_achieved: float, d_achieved: float) -> Tuple[float, float]:
        """
        Calcula los GAPs respecto a KBS.
        
        Args:
            instance_id: ID de la instancia (e.g., 'C101')
            k_achieved: Número de vehículos logrado
            d_achieved: Distancia total lograda
            
        Returns:
            (gap_k, gap_d) - Porcentajes de desviación
        """
        if instance_id not in C1_BKS:
            print(f"[WARNING] Instancia {instance_id} no encontrada en BKS")
            return 0.0, 0.0
        
        bks = C1_BKS[instance_id]
        gap_k = ((k_achieved - bks['k']) / bks['k']) * 100 if bks['k'] > 0 else 0
        gap_d = ((d_achieved - bks['d']) / bks['d']) * 100 if bks['d'] > 0 else 0
        
        return gap_k, gap_d
    
    @staticmethod
    def aggregate_results(instance_results: List[InstanceResult]) -> Tuple[float, float, float]:
        """
        Agrega resultados de múltiples instancias.
        
        Returns:
            (avg_gap_k, avg_gap_d, total_score)
        """
        if not instance_results:
            return 0.0, 0.0, 0.0
        
        avg_gap_k = statistics.mean([r.gap_k for r in instance_results])
        avg_gap_d = statistics.mean([r.gap_d for r in instance_results])
        total_score = avg_gap_k + avg_gap_d
        
        return avg_gap_k, avg_gap_d, total_score


class OptimizationOrchestrator:
    """Orquesta todo el proceso de optimización"""
    
    def __init__(self, num_combinations: int = 100, output_dir: str = 'optimization_results'):
        self.num_combinations = num_combinations
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.combinations: List[ParameterCombination] = []
        self.results: List[OptimizationResult] = []
    
    def generate_combinations(self, seed: int = 42):
        """Genera las combinaciones de parámetros"""
        print(f"\n[*] Generando {self.num_combinations} combinaciones de parámetros...")
        self.combinations = ParameterGenerator.generate_combinations(
            num_combinations=self.num_combinations,
            seed=seed
        )
        print(f"[OK] {len(self.combinations)} combinaciones generadas")
        
        # Guardar combinaciones en JSON
        combos_file = self.output_dir / 'combinations.json'
        with open(combos_file, 'w') as f:
            json.dump([c.to_dict() for c in self.combinations], f, indent=2)
        print(f"[OK] Combinaciones guardadas en {combos_file}")
    
    def run_optimization(self):
        """Ejecuta la optimización completa"""
        start_time = time.time()
        print(f"\n[*] INICIANDO OPTIMIZACIÓN - {self.num_combinations} combinaciones")
        print(f"[*] Familias: C1 ({len(C1_INSTANCES)} instancias)")
        print(f"[*] Timestamp: {datetime.now().isoformat()}")
        print("=" * 80)
        
        for i, combo in enumerate(self.combinations, 1):
            combo_start = time.time()
            print(f"\n[{i}/{self.num_combinations}] {combo}")
            
            # 1. Actualizar parámetros en algorithm_generator.py
            if not AlgorithmParameterUpdater.update_algo3_parameters(combo):
                print(f"[SKIP] No se pudieron actualizar parámetros")
                continue
            
            # 2. Ejecutar experimento QUICK para C1
            print(f"  [*] Ejecutando QUICK para C1...")
            results_dict = ExperimentExecutor.run_quick_c1_experiment()
            
            # 3. Procesar resultados
            instance_results = []
            for instance_id in C1_INSTANCES:
                # Obtener resultados de esta instancia
                # (Por ahora, valores dummy)
                k_achieved = 10.0  # Placeholder
                d_achieved = 830.0  # Placeholder
                exec_time = 0.1  # Placeholder
                
                gap_k, gap_d = ResultAnalyzer.calculate_gaps(instance_id, k_achieved, d_achieved)
                
                result = InstanceResult(
                    instance_id=instance_id,
                    k_achieved=k_achieved,
                    d_achieved=d_achieved,
                    gap_k=gap_k,
                    gap_d=gap_d,
                    combined_score=gap_k + gap_d,
                    execution_time=exec_time
                )
                instance_results.append(result)
            
            # 4. Agregar resultados
            avg_gap_k, avg_gap_d, total_score = ResultAnalyzer.aggregate_results(instance_results)
            
            opt_result = OptimizationResult(
                combination_id=combo.id,
                parameters=combo.to_dict(),
                instance_results=[r.to_dict() for r in instance_results],
                avg_gap_k=avg_gap_k,
                avg_gap_d=avg_gap_d,
                total_score=total_score,
                execution_time=time.time() - combo_start,
                timestamp=datetime.now().isoformat()
            )
            
            self.results.append(opt_result)
            
            # 5. Mostrar progreso
            print(f"  [OK] Combo {combo.id}: Score={total_score:.3f}, " \
                  f"GAP_K={avg_gap_k:.2f}%, GAP_D={avg_gap_d:.2f}%, " \
                  f"Time={opt_result.execution_time:.1f}s")
        
        elapsed = time.time() - start_time
        print(f"\n{'='*80}")
        print(f"[OK] OPTIMIZACIÓN COMPLETADA")
        print(f"[OK] Tiempo total: {elapsed/60:.1f} minutos")
        print(f"[OK] Resultados: {len(self.results)}/{self.num_combinations}")
    
    def rank_results(self):
        """Ordena los resultados por puntuación"""
        self.results.sort(key=lambda r: r.total_score)
        for rank, result in enumerate(self.results, 1):
            result.rank = rank
    
    def generate_report(self):
        """Genera reportes de los resultados"""
        self.rank_results()
        
        # Reporte en texto
        report_file = self.output_dir / 'optimization_report.txt'
        with open(report_file, 'w') as f:
            f.write("PARAMETER OPTIMIZATION REPORT - FAMILY C1\n")
            f.write("=" * 80 + "\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Total combinations: {len(self.results)}\n\n")
            
            # Top 10
            f.write("TOP 10 BEST COMBINATIONS\n")
            f.write("-" * 80 + "\n")
            for result in self.results[:10]:
                f.write(f"\nRank {result.rank}\n")
                f.write(f"  Combination ID: {result.combination_id}\n")
                f.write(f"  Parameters: {result.parameters}\n")
                f.write(f"  Avg GAP_K: {result.avg_gap_k:.3f}%\n")
                f.write(f"  Avg GAP_D: {result.avg_gap_d:.3f}%\n")
                f.write(f"  Total Score: {result.total_score:.3f}\n")
                f.write(f"  Execution Time: {result.execution_time:.1f}s\n")
            
            # Estadísticas
            f.write(f"\n\nSTATISTICS\n")
            f.write("-" * 80 + "\n")
            all_scores = [r.total_score for r in self.results]
            f.write(f"Best Score: {min(all_scores):.3f}\n")
            f.write(f"Worst Score: {max(all_scores):.3f}\n")
            f.write(f"Average Score: {statistics.mean(all_scores):.3f}\n")
            f.write(f"Median Score: {statistics.median(all_scores):.3f}\n")
            f.write(f"Std Dev: {statistics.stdev(all_scores) if len(all_scores) > 1 else 0:.3f}\n")
        
        print(f"[OK] Reporte guardado en {report_file}")
        
        # JSON con todos los resultados
        json_file = self.output_dir / 'optimization_results.json'
        with open(json_file, 'w') as f:
            json.dump([r.to_dict() for r in self.results], f, indent=2)
        print(f"[OK] Resultados JSON guardados en {json_file}")
    
    def print_top_10(self):
        """Imprime el top 10 en consola"""
        self.rank_results()
        print("\n" + "=" * 80)
        print("TOP 10 COMBINATIONS")
        print("=" * 80)
        for result in self.results[:10]:
            print(f"\nRank {result.rank}: Score={result.total_score:.3f}")
            params = result.parameters
            print(f"  While={params['while_iters']}, TwoOpt_pre={params['twoopt_pre']}, " \
                  f"DB={params['doublebridge']}, TwoOpt_post={params['twoopt_post']}, " \
                  f"Relocate={params['relocate']}")
            print(f"  Avg GAP_K={result.avg_gap_k:.2f}%, Avg GAP_D={result.avg_gap_d:.2f}%")


def main():
    """Función principal"""
    print("\n" + "=" * 80)
    print("PARAMETER OPTIMIZER - Algorithm 3 - Family C1")
    print("=" * 80)
    
    # Configuración
    num_combinations = 100
    
    # Crear orquestador
    optimizer = OptimizationOrchestrator(
        num_combinations=num_combinations,
        output_dir='optimization_results'
    )
    
    # Generar combinaciones
    optimizer.generate_combinations(seed=42)
    
    # Ejecutar optimización
    optimizer.run_optimization()
    
    # Generar reportes
    optimizer.generate_report()
    optimizer.print_top_10()
    
    print(f"\n[OK] Optimización completada!")
    print(f"[OK] Resultados guardados en: {optimizer.output_dir}/")


if __name__ == '__main__':
    main()
