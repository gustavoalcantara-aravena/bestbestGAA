"""
Test unitarios para debuggear VND e ILS

Objetivo: Identificar y arreglar los problemas de integración
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
from copy import deepcopy
from src.core.loader import SolomonLoader
from src.metaheuristic.grasp import GRASP
from src.metaheuristic.vnd import VariableNeighborhoodDescent
from src.metaheuristic.ils import IteratedLocalSearch
from src.operators import RandomizedInsertion


class TestVNDDebug(unittest.TestCase):
    """Debuggear VND"""
    
    def setUp(self):
        """Load real instance"""
        loader = SolomonLoader()
        instances = loader.load_all_instances('datasets')
        self.instance = instances['R1']['R101']
        print(f"\n[INSTANCE] R101: {self.instance.n_customers} clientes")
    
    def test_01_vnd_search_signature(self):
        """Test: ¿Cuál es la firma correcta de VND.search()?"""
        vnd = VariableNeighborhoodDescent(verbose=True)
        print(f"\n[VND.search] Firma: {vnd.search.__doc__}")
        
        # Crear solución inicial con GRASP
        grasp = GRASP(alpha=0.15, max_iterations=5, seed=42, verbose=False)
        initial_solution, fitness, stats = grasp.solve(self.instance)
        print(f"[GRASP] K={fitness[0]}, D={fitness[1]:.2f}")
        
        # Llamar VND.search()
        print(f"\n[VND] Iniciando search...")
        result = vnd.search(initial_solution)
        
        print(f"[VND] Resultado type: {type(result)}")
        print(f"[VND] K={result.num_vehicles}, D={result.total_distance:.2f}")
        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, 'num_vehicles'))
        self.assertTrue(hasattr(result, 'total_distance'))
    
    def test_02_vnd_return_value(self):
        """Test: ¿Qué retorna VND.search() exactamente?"""
        vnd = VariableNeighborhoodDescent(verbose=True)
        
        grasp = GRASP(alpha=0.15, max_iterations=5, seed=42, verbose=False)
        initial_solution, fitness, stats = grasp.solve(self.instance)
        
        print(f"\n[INPUT] Initial solution type: {type(initial_solution)}")
        print(f"[INPUT] Initial K={initial_solution.num_vehicles}, D={initial_solution.total_distance:.2f}")
        
        result = vnd.search(deepcopy(initial_solution))
        
        print(f"[OUTPUT] Result type: {type(result)}")
        print(f"[OUTPUT] Result K={result.num_vehicles}, D={result.total_distance:.2f}")
        
        # Verificar que retorna un Solution
        self.assertEqual(type(result).__name__, 'Solution')
        self.assertGreater(result.num_vehicles, 0)
        self.assertGreater(result.total_distance, 0)


class TestILSDebug(unittest.TestCase):
    """Debuggear ILS"""
    
    def setUp(self):
        """Load real instance"""
        loader = SolomonLoader()
        instances = loader.load_all_instances('datasets')
        self.instance = instances['R1']['R101']
        print(f"\n[INSTANCE] R101: {self.instance.n_customers} clientes")
    
    def test_01_ils_solve_signature(self):
        """Test: ¿Cuál es la firma correcta de ILS.solve()?"""
        ils = IteratedLocalSearch(
            perturbation_strength=3,
            max_iterations=5,
            seed=42,
            verbose=True
        )
        print(f"\n[ILS.solve] Firma: {ils.solve.__doc__}")
        
        # Llamar ILS.solve()
        print(f"\n[ILS] Iniciando solve...")
        result = ils.solve(self.instance)
        
        print(f"[ILS] Resultado: {type(result)}")
        print(f"[ILS] Es tupla: {isinstance(result, tuple)}")
        if isinstance(result, tuple):
            print(f"[ILS] Tupla size: {len(result)}")
            solution, fitness, stats = result
            print(f"[ILS] Solution type: {type(solution)}")
            print(f"[ILS] Fitness type: {type(fitness)}")
            print(f"[ILS] Stats type: {type(stats)}")
            print(f"[ILS] K={fitness[0]}, D={fitness[1]:.2f}")
    
    def test_02_ils_search_method(self):
        """Test: ¿Existe ILS.search()?"""
        ils = IteratedLocalSearch(
            perturbation_strength=3,
            max_iterations=5,
            seed=42,
            verbose=False
        )
        
        # Verificar métodos disponibles
        methods = [m for m in dir(ils) if not m.startswith('_')]
        print(f"\n[ILS] Métodos disponibles: {methods}")
        
        # Buscar search
        has_search = hasattr(ils, 'search')
        has_solve = hasattr(ils, 'solve')
        print(f"[ILS] Tiene .search(): {has_search}")
        print(f"[ILS] Tiene .solve(): {has_solve}")
        
        self.assertTrue(has_solve, "ILS debería tener método .solve()")


class TestIntegrationExperiment(unittest.TestCase):
    """Test cómo se debe llamar VND e ILS en el script de experimentos"""
    
    def setUp(self):
        """Load real instance"""
        loader = SolomonLoader()
        instances = loader.load_all_instances('datasets')
        self.instance = instances['R1']['R101']
    
    def test_vnd_in_experiment(self):
        """Test: Forma correcta de usar VND en experimentos"""
        print(f"\n[EXPERIMENT] Probando VND...")
        
        # 1. Crear solución inicial
        constructor = RandomizedInsertion(alpha=0.15, seed=42)
        initial_solution = constructor.construct(self.instance)
        print(f"[INITIAL] K={initial_solution.num_vehicles}, D={initial_solution.total_distance:.2f}")
        
        # 2. Crear VND
        vnd = VariableNeighborhoodDescent(verbose=False)
        
        # 3. Aplicar VND
        solution = vnd.search(initial_solution)  # ← Retorna Solution
        
        print(f"[VND RESULT] K={solution.num_vehicles}, D={solution.total_distance:.2f}")
        
        # 4. Extraer métricas (como en el script)
        k_final = solution.num_vehicles
        d_final = solution.total_distance
        
        print(f"[METRICS] k_final={k_final}, d_final={d_final}")
        
        self.assertEqual(type(k_final).__name__, 'int')
        self.assertIsInstance(d_final, float)
    
    def test_ils_in_experiment(self):
        """Test: Forma correcta de usar ILS en experimentos"""
        print(f"\n[EXPERIMENT] Probando ILS...")
        
        # 1. Crear ILS
        ils = IteratedLocalSearch(
            perturbation_strength=3,
            max_iterations=5,
            seed=42,
            verbose=False
        )
        
        # 2. Aplicar ILS
        result = ils.solve(self.instance)  # ← Retorna Tuple[Solution, Tuple[int, float], dict]
        
        print(f"[ILS RESULT] Tipo: {type(result)}")
        
        if isinstance(result, tuple) and len(result) == 3:
            solution, fitness, stats = result
            k_final = fitness[0]
            d_final = fitness[1]
            print(f"[METRICS] k_final={k_final}, d_final={d_final}")
            
            self.assertEqual(type(k_final).__name__, 'int')
            self.assertIsInstance(d_final, float)
        else:
            print(f"[ERROR] ILS.solve() no retornó tupla esperada")
            print(f"[ERROR] Retornó: {result}")
            self.fail("ILS.solve() debe retornar (solution, fitness, stats)")


if __name__ == '__main__':
    unittest.main(verbosity=2)
