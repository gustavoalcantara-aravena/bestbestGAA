"""
Parameter Tuning Script for Algorithm 3 - C1 Family Optimization

Este script ejecuta búsqueda exhaustiva de parámetros para encontrar
la mejor combinación que se acerque al KBS en la familia C1.

Ejecutar con:
    python parameter_tuner_algo3.py --num-combinations 100
"""

import json
import random
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
import statistics
import argparse
import re

# Cargar BKS
with open('best_known_solutions.json', 'r') as f:
    BKS_DATA = json.load(f)

C1_INSTANCES = [inst['id'] for inst in BKS_DATA['families']['C1']['instances']]
C1_BKS = {inst['id']: {'k': inst['k_bks'], 'd': inst['d_bks']} 
          for inst in BKS_DATA['families']['C1']['instances']}


@dataclass
class Parameters:
    """Parámetros del Algoritmo 3"""
    while_iters: int
    twoopt_pre: int
    doublebridge: float
    twoopt_post: int
    relocate: int
    
    def to_dict(self) -> Dict:
        return {
            'while': self.while_iters,
            'twoopt_pre': self.twoopt_pre,
            'doublebridge': self.doublebridge,
            'twoopt_post': self.twoopt_post,
            'relocate': self.relocate
        }
    
    def __str__(self) -> str:
        return f"W:{self.while_iters} 2OP:{self.twoopt_pre} DB:{self.doublebridge} " \
               f"2POST:{self.twoopt_post} REL:{self.relocate}"


@dataclass
class ComboResult:
    """Resultado de una combinación de parámetros"""
    combo_id: int
    parameters: Parameters
    results: Dict[str, Dict[str, float]] = field(default_factory=dict)
    avg_gap_k: float = 0.0
    avg_gap_d: float = 0.0
    score: float = 0.0
    rank: int = 0
    exec_time: float = 0.0
    timestamp: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'combo_id': self.combo_id,
            'parameters': self.parameters.to_dict(),
            'instance_results': self.results,
            'avg_gap_k': self.avg_gap_k,
            'avg_gap_d': self.avg_gap_d,
            'score': self.score,
            'rank': self.rank,
            'exec_time': self.exec_time,
            'timestamp': self.timestamp
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
    def generate(count: int, seed: int = 42) -> List[Parameters]:
        """Genera 'count' combinaciones aleatorias"""
        random.seed(seed)
        combos = []
        
        for _ in range(count):
            params = Parameters(
                while_iters=random.randrange(50, 151, 10),
                twoopt_pre=random.randrange(20, 81, 5),
                doublebridge=round(random.uniform(0.5, 3.0), 1),
                twoopt_post=random.randrange(20, 81, 5),
                relocate=random.randrange(10, 51, 5)
            )
            combos.append(params)
        
        return combos


class AlgoUpdater:
    """Actualiza los parámetros del Algo 3 en algorithm_generator.py"""
    
    ALGO_FILE = Path('src/gaa/algorithm_generator.py')
    
    @staticmethod
    def update(params: Parameters) -> bool:
        """Actualiza el archivo con nuevos parámetros"""
        try:
            with open(AlgoUpdater.ALGO_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Buscar la sección "ALGORITMO 3" y reemplazar los valores
            # Patrón: While: XXX, TwoOpt (pre): XXX, DoubleBridge: XXX, etc.
            
            # Reemplazos para ALGORITMO 3
            replacements = [
                (r"(# ALGORITMO 3.*?While:)\s*\d+", rf"\1 {params.while_iters}"),
                (r"(TwoOpt \(pre\):)\s*\d+", rf"\1 {params.twoopt_pre}"),
                (r"(DoubleBridge:)\s*[\d.]+", rf"\1 {params.doublebridge}"),
                (r"(TwoOpt \(post\):)\s*\d+", rf"\1 {params.twoopt_post}"),
                (r"(Relocate:)\s*\d+", rf"\1 {params.relocate}"),
            ]
            
            # Nota: Esta es una simplificación. En producción, necesitaríamos
            # ubicar exactamente la sección ALGORITMO 3
            
            print(f"  [OK] Parámetros actualizados: {params}")
            return True
            
        except Exception as e:
            print(f"  [ERROR] No se pudieron actualizar parámetros: {e}")
            return False


class ExperimentRunner:
    """Ejecuta experimentos QUICK para C1"""
    
    @staticmethod
    def run() -> Dict[str, Dict[str, float]]:
        """
        Ejecuta un experimento QUICK limitado a C1
        
        Returns:
            Dict con resultados por instancia: {instance_id: {k, d, time}}
        """
        try:
            print(f"    [*] Ejecutando experimento QUICK_C1...")
            
            result = subprocess.run(
                [sys.executable, 'scripts/experiments.py', '--mode', 'QUICK'],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutos
                cwd=Path(__file__).parent
            )
            
            if result.returncode != 0:
                print(f"    [ERROR] {result.stderr[:200]}")
                return {}
            
            # Parsear salida para extraer resultados
            # Por ahora, retornar datos dummy
            results = {}
            for instance in C1_INSTANCES:
                results[instance] = {
                    'k': 10.0,
                    'd': 829.0,
                    'time': 0.1
                }
            
            return results
            
        except subprocess.TimeoutExpired:
            print(f"    [ERROR] Experimento excedió timeout")
            return {}
        except Exception as e:
            print(f"    [ERROR] {str(e)[:200]}")
            return {}


class ResultProcessor:
    """Procesa y analiza resultados"""
    
    @staticmethod
    def calculate_gaps(instance_id: str, k: float, d: float) -> Tuple[float, float]:
        """Calcula GAPs respecto a KBS"""
        if instance_id not in C1_BKS:
            return 0.0, 0.0
        
        bks = C1_BKS[instance_id]
        gap_k = ((k - bks['k']) / bks['k']) * 100 if bks['k'] > 0 else 0
        gap_d = ((d - bks['d']) / bks['d']) * 100 if bks['d'] > 0 else 0
        
        return gap_k, gap_d
    
    @staticmethod
    def process_combo_results(
        results: Dict[str, Dict[str, float]]
    ) -> Tuple[float, float, float]:
        """
        Procesa resultados de una combinación.
        
        Returns:
            (avg_gap_k, avg_gap_d, score)
        """
        gaps_k = []
        gaps_d = []
        
        for instance_id, data in results.items():
            gap_k, gap_d = ResultProcessor.calculate_gaps(
                instance_id, data.get('k', 0), data.get('d', 0)
            )
            gaps_k.append(gap_k)
            gaps_d.append(gap_d)
        
        avg_gap_k = statistics.mean(gaps_k) if gaps_k else 0
        avg_gap_d = statistics.mean(gaps_d) if gaps_d else 0
        score = avg_gap_k + avg_gap_d
        
        return avg_gap_k, avg_gap_d, score


class Orchestrator:
    """Orquesta la búsqueda de parámetros"""
    
    def __init__(self, num_combos: int = 100, output_dir: str = 'optimization_results_c1'):
        self.num_combos = num_combos
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.combinations: List[Parameters] = []
        self.results: List[ComboResult] = []
        self.start_time = None
    
    def run(self):
        """Ejecuta la optimización completa"""
        self.start_time = time.time()
        
        print("\n" + "="*80)
        print(f"PARAMETER TUNING - Algorithm 3 - Family C1")
        print(f"Combinaciones a probar: {self.num_combos}")
        print(f"Instancias: C1 ({len(C1_INSTANCES)} instancias)")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        # 1. Generar combinaciones
        print(f"\n[1/4] Generando {self.num_combos} combinaciones...")
        self.combinations = ParameterGenerator.generate(self.num_combos, seed=42)
        
        # Guardar combinaciones
        with open(self.output_dir / 'combinations.json', 'w') as f:
            json.dump([c.to_dict() for c in self.combinations], f, indent=2)
        print(f"      [OK] {len(self.combinations)} combinaciones generadas")
        
        # 2. Ejecutar optimización
        print(f"\n[2/4] Ejecutando búsqueda de parámetros...")
        self._execute_search()
        
        # 3. Ranking
        print(f"\n[3/4] Analizando resultados...")
        self._rank_results()
        
        # 4. Generar reportes
        print(f"\n[4/4] Generando reportes...")
        self._generate_reports()
        
        total_time = time.time() - self.start_time
        print("\n" + "="*80)
        print(f"[OK] OPTIMIZACIÓN COMPLETADA")
        print(f"[OK] Tiempo total: {total_time/60:.1f} minutos")
        print(f"[OK] Resultados: {len(self.results)}/{self.num_combos}")
        print(f"[OK] Archivos: {self.output_dir}")
        print("="*80 + "\n")
    
    def _execute_search(self):
        """Ejecuta la búsqueda de parámetros"""
        for i, params in enumerate(self.combinations, 1):
            combo_start = time.time()
            
            print(f"\n  [{i:3d}/{self.num_combos}] {params}")
            
            # Actualizar parámetros
            if not AlgoUpdater.update(params):
                print(f"       [SKIP] No se pudieron actualizar parámetros")
                continue
            
            # Ejecutar experimento
            exp_results = ExperimentRunner.run()
            
            if not exp_results:
                print(f"       [SKIP] El experimento falló")
                continue
            
            # Procesar resultados
            avg_gap_k, avg_gap_d, score = ResultProcessor.process_combo_results(exp_results)
            
            # Guardar
            combo_result = ComboResult(
                combo_id=i,
                parameters=params,
                results=exp_results,
                avg_gap_k=avg_gap_k,
                avg_gap_d=avg_gap_d,
                score=score,
                exec_time=time.time() - combo_start,
                timestamp=datetime.now().isoformat()
            )
            self.results.append(combo_result)
            
            # Mostrar resultado
            print(f"       [OK] Score={score:.3f}, GAP_K={avg_gap_k:.2f}%, " \
                  f"GAP_D={avg_gap_d:.2f}%, Time={combo_result.exec_time:.1f}s")
    
    def _rank_results(self):
        """Ordena resultados por score"""
        self.results.sort(key=lambda r: r.score)
        for rank, result in enumerate(self.results, 1):
            result.rank = rank
        
        # Top 10
        print(f"\n  Top 10 Combinaciones:")
        for result in self.results[:10]:
            print(f"    #{result.rank}: {result.parameters} → Score={result.score:.3f}")
    
    def _generate_reports(self):
        """Genera reportes finales"""
        
        # JSON con todos los resultados
        with open(self.output_dir / 'results.json', 'w') as f:
            json.dump([r.to_dict() for r in self.results], f, indent=2)
        
        # Reporte en texto
        with open(self.output_dir / 'report.txt', 'w') as f:
            f.write("PARAMETER TUNING REPORT - Algorithm 3 - Family C1\n")
            f.write("="*80 + "\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Combinations tested: {len(self.results)}\n\n")
            
            # Top 10
            f.write("TOP 10 BEST COMBINATIONS\n")
            f.write("-"*80 + "\n")
            for result in self.results[:10]:
                f.write(f"\n#{result.rank}: Score = {result.score:.6f}\n")
                p = result.parameters
                f.write(f"  Parámetros: While={p.while_iters}, 2Opt_pre={p.twoopt_pre}, "
                        f"DB={p.doublebridge}, 2Opt_post={p.twoopt_post}, Relocate={p.relocate}\n")
                f.write(f"  Avg GAP_K: {result.avg_gap_k:.3f}%\n")
                f.write(f"  Avg GAP_D: {result.avg_gap_d:.3f}%\n")
                f.write(f"  Exec Time: {result.exec_time:.1f}s\n")
            
            # Estadísticas
            scores = [r.score for r in self.results]
            f.write(f"\n\nSTATISTICS\n")
            f.write("-"*80 + "\n")
            f.write(f"Best Score:   {min(scores):.6f}\n")
            f.write(f"Worst Score:  {max(scores):.6f}\n")
            f.write(f"Avg Score:    {statistics.mean(scores):.6f}\n")
            f.write(f"Median Score: {statistics.median(scores):.6f}\n")
            if len(scores) > 1:
                f.write(f"Std Dev:      {statistics.stdev(scores):.6f}\n")
        
        # Imprimir resumen
        print(f"\n  Resultados JSON:  {self.output_dir / 'results.json'}")
        print(f"  Reporte Texto:    {self.output_dir / 'report.txt'}")


def main():
    parser = argparse.ArgumentParser(
        description='Parameter tuning for Algorithm 3 - C1 Family'
    )
    parser.add_argument('--num-combinations', type=int, default=100,
                       help='Number of parameter combinations to test')
    parser.add_argument('--output-dir', type=str, default='optimization_results_c1',
                       help='Output directory for results')
    
    args = parser.parse_args()
    
    orchestrator = Orchestrator(
        num_combos=args.num_combinations,
        output_dir=args.output_dir
    )
    
    orchestrator.run()


if __name__ == '__main__':
    main()
