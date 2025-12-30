"""
Demo Script - Demostración de GRASP en instancia C101

Muestra cómo usar el sistema completo de VRPTW-GRASP.
"""

import sys
from pathlib import Path

# Agregar ruta
sys.path.insert(0, str(Path(__file__).parent))

from data.loader import VRPTWDataLoader
from metaheuristic.grasp_core import solve_vrptw


def main():
    """Ejecuta demostración"""
    
    print("=" * 70)
    print("VRPTW-GRASP Demo - Solving C101 Instance")
    print("=" * 70)
    
    # Cargar instancia
    print("\n[1] Loading dataset...")
    loader = VRPTWDataLoader(str(Path(__file__).parent / 'datasets'))
    
    problem = loader.load_instance('C1', 'C101', vehicle_capacity=200)
    
    if problem is None:
        print("ERROR: Could not load C101")
        return
    
    print(problem.summary())
    
    # Resolver con GRASP
    print("\n[2] Solving with GRASP...")
    print("  Parameters:")
    print("    - max_iterations: 50")
    print("    - alpha_rcl: 0.15 (Restricted Candidate List)")
    print("    - construction_method: randomized")
    print("    - local_search: Variable Neighborhood Descent (VND)")
    print()
    
    best_solution = solve_vrptw(
        problem,
        max_iterations=50,
        alpha_rcl=0.15,
        seed=42,
        log_level=1
    )
    
    # Mostrar resultado
    print("\n[3] Solution Details:")
    print(best_solution.info())
    
    # Estadísticas
    print("\n[4] Solution Quality:")
    print(f"  Total Distance:    {best_solution.distance:,.2f}")
    print(f"  Num Vehicles:      {best_solution.num_routes()}")
    print(f"  Min Vehicles (LB): {problem.min_vehicles_needed()}")
    print(f"  Excess Vehicles:   {best_solution.num_routes() - problem.min_vehicles_needed()}")
    print(f"  Is Feasible:       {'Yes ✓' if best_solution.is_feasible else 'No ✗'}")
    print(f"  Cost (hierarchical): {best_solution.cost:,.2f}")


if __name__ == '__main__':
    main()
