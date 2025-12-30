"""
Main Script - Ejecución de experimentos VRPTW-GRASP

Permite resolver instancias individuales o familias completas.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

# Agregar ruta
sys.path.insert(0, str(Path(__file__).parent))

from data.loader import VRPTWDataLoader
from metaheuristic.grasp_core import solve_vrptw, GRASPParameters
from core.evaluation import VRPTWEvaluator


def solve_single_instance(instance_path: str, 
                         max_iterations: int = 100,
                         alpha_rcl: float = 0.15,
                         seed: Optional[int] = None,
                         time_limit: Optional[float] = None) -> None:
    """Resuelve una instancia individual"""
    
    from core.problem import VRPTWProblem
    
    print(f"\nSolving: {instance_path}")
    print("=" * 70)
    
    # Cargar problema
    try:
        problem = VRPTWProblem.from_file(instance_path)
    except Exception as e:
        print(f"ERROR: Could not load instance: {e}")
        return
    
    # Mostrar información del problema
    print(problem.summary())
    
    # Resolver
    print(f"\nGRASP Parameters:")
    print(f"  max_iterations: {max_iterations}")
    print(f"  alpha_rcl:      {alpha_rcl}")
    print(f"  seed:           {seed}")
    print(f"  time_limit:     {time_limit}")
    print()
    
    solution = solve_vrptw(
        problem,
        max_iterations=max_iterations,
        alpha_rcl=alpha_rcl,
        seed=seed,
        time_limit=time_limit,
        log_level=1
    )
    
    # Mostrar solución
    print(solution.info())
    
    # Evaluación detallada
    evaluator = VRPTWEvaluator(problem)
    metrics = evaluator.evaluate(solution)
    
    print("\nDetailed Metrics:")
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"  {key:20s}: {value:10.2f}")
        else:
            print(f"  {key:20s}: {value}")


def solve_family(family: str, 
                max_iterations: int = 100,
                alpha_rcl: float = 0.15,
                seed: Optional[int] = None,
                time_limit: Optional[float] = None) -> None:
    """Resuelve una familia completa de instancias"""
    
    print(f"\nSolving Family: {family}")
    print("=" * 70)
    
    # Cargar instancias
    loader = VRPTWDataLoader(str(Path(__file__).parent / 'datasets'))
    instances = loader.load_family(family, vehicle_capacity=200)
    
    if not instances:
        print(f"ERROR: No instances found for family {family}")
        return
    
    print(f"Found {len(instances)} instances\n")
    
    # Resolver cada instancia
    results = {}
    
    for instance_name, problem in sorted(instances.items()):
        print(f"Instance {instance_name:10s}: ", end="", flush=True)
        
        try:
            solution = solve_vrptw(
                problem,
                max_iterations=max_iterations,
                alpha_rcl=alpha_rcl,
                seed=seed,
                time_limit=time_limit,
                log_level=0  # Silent
            )
            
            results[instance_name] = {
                'cost': solution.cost,
                'distance': solution.distance,
                'vehicles': solution.num_routes(),
                'feasible': solution.is_feasible,
            }
            
            print(f"Cost: {solution.cost:10,.2f} | Vehicles: {solution.num_routes():2d} | "
                  f"Feasible: {'Yes' if solution.is_feasible else 'No'}")
        
        except Exception as e:
            print(f"ERROR: {e}")
            results[instance_name] = None
    
    # Resumen
    print("\nFamily Summary:")
    print("-" * 70)
    
    feasible_count = sum(1 for r in results.values() if r and r['feasible'])
    avg_cost = sum(r['cost'] for r in results.values() if r) / len([r for r in results.values() if r])
    avg_vehicles = sum(r['vehicles'] for r in results.values() if r) / len([r for r in results.values() if r])
    
    print(f"Total Instances:     {len(instances)}")
    print(f"Feasible:            {feasible_count}/{len(instances)}")
    print(f"Average Cost:        {avg_cost:,.2f}")
    print(f"Average Vehicles:    {avg_vehicles:.1f}")


def main():
    """Función principal"""
    
    parser = argparse.ArgumentParser(
        description="VRPTW-GRASP Solver - Solución de Problemas de Ruteo con Ventanas de Tiempo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Resolve single instance
  python run.py --family C1 --instance C101
  
  # Resolve entire family
  python run.py --family C2 --iterations 50
  
  # With time limit
  python run.py --family R1 --instance R101 --time-limit 300
  
  # With reproducible seed
  python run.py --family RC1 --instance RC101 --seed 42
        """
    )
    
    parser.add_argument('--family', type=str, default='C1',
                       choices=['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2'],
                       help='Dataset family')
    parser.add_argument('--instance', type=str, default=None,
                       help='Specific instance (if None, solve entire family)')
    parser.add_argument('--iterations', type=int, default=100,
                       help='Maximum number of iterations')
    parser.add_argument('--alpha', type=float, default=0.15,
                       help='RCL parameter (0=greedy, 1=random)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for reproducibility')
    parser.add_argument('--time-limit', type=float, default=None,
                       help='Time limit in seconds')
    
    args = parser.parse_args()
    
    # Cargar loader
    loader = VRPTWDataLoader(str(Path(__file__).parent / 'datasets'))
    
    # Resolver
    if args.instance:
        # Instancia individual
        path = loader.get_instance_path(args.family, args.instance)
        if path is None:
            print(f"ERROR: Instance not found: {args.family}/{args.instance}")
            return
        
        solve_single_instance(
            str(path),
            max_iterations=args.iterations,
            alpha_rcl=args.alpha,
            seed=args.seed,
            time_limit=args.time_limit
        )
    else:
        # Familia completa
        solve_family(
            args.family,
            max_iterations=args.iterations,
            alpha_rcl=args.alpha,
            seed=args.seed,
            time_limit=args.time_limit
        )


if __name__ == '__main__':
    main()
