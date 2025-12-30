"""
run.py - CLI para ejecutar ILS sobre instancias DIMACS

Uso:
    python run.py <instance_name> [options]
    python run.py CUL10 --verbose --max-iterations 1000
    python run.py DSJ10 --constructive dsatur --local-search tabu
"""

import argparse
import sys
from pathlib import Path

# Agregar path para imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from data.loader import DataLoader
from core.evaluation import ColoringEvaluator
from metaheuristic.ils_core import IteratedLocalSearch


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='ILS for Graph Coloring Problem',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py CUL10
  python run.py DSJ10 --verbose --max-iterations 1000
  python run.py MYC02 --constructive lf --local-search tabu
  python run.py REG12 --seed 42
        """
    )
    
    parser.add_argument('instance',
                       help='Instance name (e.g., CUL10, DSJ10)')
    
    parser.add_argument('-c', '--constructive',
                       default='dsatur',
                       choices=['dsatur', 'lf', 'sl', 'rs', 'rlf'],
                       help='Constructive operator (default: dsatur)')
    
    parser.add_argument('-ls', '--local-search',
                       default='kempe',
                       choices=['kempe', 'tabu', 'ovm', 'swap'],
                       help='Local search operator (default: kempe)')
    
    parser.add_argument('-p', '--perturbation',
                       default='random_recolor',
                       choices=['random_recolor', 'partial_destroy'],
                       help='Perturbation operator (default: random_recolor)')
    
    parser.add_argument('-i', '--max-iterations',
                       type=int,
                       default=500,
                       help='Maximum iterations (default: 500)')
    
    parser.add_argument('-ps', '--perturbation-strength',
                       type=float,
                       default=0.2,
                       help='Perturbation strength (default: 0.2)')
    
    parser.add_argument('-rt', '--restart-threshold',
                       type=int,
                       default=50,
                       help='Restart threshold (default: 50)')
    
    parser.add_argument('-s', '--seed',
                       type=int,
                       default=None,
                       help='Random seed')
    
    parser.add_argument('-v', '--verbose',
                       action='store_true',
                       help='Verbose output')
    
    parser.add_argument('--dataset-root',
                       type=str,
                       default=None,
                       help='Path to dataset root directory')
    
    args = parser.parse_args()
    
    try:
        # Cargar instancia
        if args.verbose:
            print(f"Loading instance: {args.instance}")
        
        loader = DataLoader(args.dataset_root)
        
        # Intentar cargar, si no existe mostrar disponibles
        try:
            problem = loader.load(args.instance)
        except FileNotFoundError as fnf_err:
            print(f"Error: {fnf_err}")
            print("\nAvailable instances:")
            available = loader.list_available_instances()
            for inst in available[:10]:
                print(f"  - {inst}")
            if len(available) > 10:
                print(f"  ... and {len(available) - 10} more")
            return 1
        
        if args.verbose:
            print(f"Instance loaded: n={problem.n}, m={problem.m}")
            print(f"Lower bound: {problem.lower_bound}")
            if problem.optimal_value:
                print(f"Optimal: {problem.optimal_value}")
            print()
        
        # Crear y ejecutar ILS
        ils = IteratedLocalSearch(
            problem=problem,
            constructive=args.constructive,
            local_search=args.local_search,
            perturbation=args.perturbation,
            max_iterations=args.max_iterations,
            perturbation_strength=args.perturbation_strength,
            restart_threshold=args.restart_threshold,
            seed=args.seed,
            verbose=args.verbose
        )
        
        best_solution, stats = ils.run()
        
        # Mostrar resultados
        print("\n" + "="*60)
        print(f"Result: k = {stats['best_k']}")
        print(f"Time: {stats['total_time']:.2f}s")
        print(f"Iterations: {stats['iterations_completed']}")
        
        if problem.optimal_value:
            gap = best_solution.num_colors - problem.optimal_value
            gap_pct = gap / problem.optimal_value * 100
            print(f"Gap to optimal: {gap} ({gap_pct:.2f}%)")
        
        print("="*60)
        
        # Validar solución
        conflicts = best_solution.count_conflicts(problem)
        if conflicts == 0:
            print("[OK] Solution is feasible")
        else:
            print(f"[ERROR] Solution has {conflicts} conflicts")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
