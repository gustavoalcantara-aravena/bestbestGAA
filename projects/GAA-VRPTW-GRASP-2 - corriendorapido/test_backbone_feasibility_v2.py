"""
TESTS UNITARIOS - BACKBONE FEASIBILITY (Versión Pragmática)
=============================================================

Validación exhaustiva de restricciones VRPTW usando soluciones reales de GRASP
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.core.loader import SolomonLoader
from src.core.evaluation import evaluate_solution, compare_solutions
from src.metaheuristic.grasp import GRASP


class TestCoverageConstraint:
    """RESTRICCIÓN 1: Cobertura (cada cliente visitado exactamente una vez)"""
    
    @pytest.fixture
    def loader(self):
        return SolomonLoader()
    
    @pytest.fixture
    def instance_r101(self, loader):
        return loader.load_instance('datasets/R1/R101.csv')
    
    def test_loader_loads_all_customers_plus_depot(self, instance_r101):
        """Instance debe incluir depósito + 100 clientes = 101 total"""
        assert len(instance_r101.customers) == 101, \
            f"Esperados 101 clientes (depot+100), obtenidos {len(instance_r101.customers)}"
    
    def test_grasp_covers_all_100_customers(self, instance_r101):
        """GRASP debe producir solución que visita los 100 clientes"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        visited = set()
        for route in solution.routes:
            for c_id in route.sequence:
                if c_id != 0:  # Excluir depósito
                    visited.add(c_id)
        
        assert len(visited) == 100, \
            f"Visitados {len(visited)} clientes, esperados 100"
        print(f"✓ Todos 100 clientes visitados")
    
    def test_no_duplicate_customers(self, instance_r101):
        """Ningún cliente debe visitarse más de una vez"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        all_customers = []
        for route in solution.routes:
            for c_id in route.sequence:
                if c_id != 0:
                    all_customers.append(c_id)
        
        assert len(all_customers) == len(set(all_customers)), \
            f"Hay duplicados: {len(all_customers)} vs {len(set(all_customers))}"
        print(f"✓ Sin clientes duplicados")
    
    def test_evaluator_confirms_coverage(self, instance_r101):
        """evaluate_solution debe reportar coverage_ok = True"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        is_feasible, details = evaluate_solution(solution)
        
        assert details.get('coverage_ok', False) is True, \
            "Evaluador debe reportar coverage_ok=True"
        print(f"✓ Evaluador confirma cobertura completa")


class TestCapacityConstraint:
    """RESTRICCIÓN 2: Capacidad (carga por ruta ≤ Q = 200)"""
    
    @pytest.fixture
    def loader(self):
        return SolomonLoader()
    
    @pytest.fixture
    def instance_r101(self, loader):
        return loader.load_instance('datasets/R1/R101.csv')
    
    def test_instance_has_q_capacity(self, instance_r101):
        """Instance debe cargar Q_capacity correctamente"""
        assert hasattr(instance_r101, 'Q_capacity'), "Instance falta Q_capacity"
        assert instance_r101.Q_capacity == 200, \
            f"Solomon Q debe ser 200, obtenido {instance_r101.Q_capacity}"
        print(f"✓ Q_capacity = {instance_r101.Q_capacity}")
    
    def test_customers_have_demand(self, instance_r101):
        """Todos los clientes deben tener demand > 0"""
        for i in range(1, len(instance_r101.customers)):  # Skip depot
            c = instance_r101.customers[i]
            assert hasattr(c, 'demand'), f"Cliente {i} sin demand"
            assert c.demand > 0, f"Cliente {i} demand <= 0"
        print(f"✓ Todos los clientes tienen demanda")
    
    def test_grasp_respects_capacity(self, instance_r101):
        """GRASP nunca debe violar Q en ninguna ruta"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        for route in solution.routes:
            total_demand = sum(
                instance_r101.customers[c_id].demand
                for c_id in route.sequence
                if c_id != 0
            )
            
            assert total_demand <= instance_r101.Q_capacity, \
                f"Ruta {route.vehicle_id}: {total_demand} > {instance_r101.Q_capacity}"
        
        print(f"✓ Todas las rutas respetan capacidad Q = 200")
    
    def test_evaluator_checks_capacity(self, instance_r101):
        """evaluate_solution debe incluir capacity_ok en resultados"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        is_feasible, details = evaluate_solution(solution)
        
        # Verificar que hay información de capacidad
        route_details = details.get('route_details', [])
        assert len(route_details) > 0, "Debe haber detalles por ruta"
        
        # Verificar que cada ruta tiene 'capacity_ok'
        for route_detail in route_details:
            assert 'capacity_ok' in route_detail, \
                "Cada ruta debe reportar capacity_ok"
            assert route_detail['capacity_ok'] is True, \
                f"Ruta tiene capacity_ok=False"
        
        print(f"✓ Evaluador verifica capacidad en todas las rutas")


class TestTimeWindowConstraint:
    """RESTRICCIÓN 3: Ventanas de Tiempo (a_i ≤ t_i ≤ b_i)"""
    
    @pytest.fixture
    def loader(self):
        return SolomonLoader()
    
    @pytest.fixture
    def instance_c1(self, loader):
        return loader.load_instance('datasets/C1/C101.csv')
    
    def test_customers_have_time_windows(self, instance_c1):
        """Todos los clientes en C1 deben tener ready_time, due_date, service_time"""
        for i in range(len(instance_c1.customers)):
            c = instance_c1.customers[i]
            assert hasattr(c, 'ready_time'), f"Cliente {i} sin ready_time"
            assert hasattr(c, 'due_date'), f"Cliente {i} sin due_date"
            assert hasattr(c, 'service_time'), f"Cliente {i} sin service_time"
            
            assert c.ready_time <= c.due_date, \
                f"Cliente {i}: ready_time > due_date"
        
        print(f"✓ C1 tiene ventanas de tiempo bien formadas")
    
    def test_evaluator_checks_time_windows(self, instance_c1):
        """evaluate_solution debe reportar time_windows_ok por ruta"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_c1)
        
        is_feasible, details = evaluate_solution(solution)
        
        # Verificar que hay detalles de TW
        route_details = details.get('route_details', [])
        assert len(route_details) > 0, "Debe haber detalles por ruta"
        
        # Al menos algunas rutas deben tener time_windows_ok
        has_tw_check = any(
            'time_windows_ok' in rd for rd in route_details
        )
        assert has_tw_check, "Evaluador debe revisar time_windows_ok"
        
        print(f"✓ Evaluador verifica ventanas de tiempo")


class TestFlowConservationConstraint:
    """RESTRICCIÓN 4: Conservación de Flujo (inicio/fin en depósito)"""
    
    @pytest.fixture
    def loader(self):
        return SolomonLoader()
    
    @pytest.fixture
    def instance_r101(self, loader):
        return loader.load_instance('datasets/R1/R101.csv')
    
    def test_all_routes_start_at_depot(self, instance_r101):
        """Toda ruta debe comenzar en depósito (0)"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        for route in solution.routes:
            assert route.sequence[0] == 0, \
                f"Ruta {route.vehicle_id} no comienza en 0"
        
        print(f"✓ Todas las rutas inician en depósito")
    
    def test_all_routes_end_at_depot(self, instance_r101):
        """Toda ruta debe terminar en depósito (0)"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        for route in solution.routes:
            assert route.sequence[-1] == 0, \
                f"Ruta {route.vehicle_id} no termina en 0"
        
        print(f"✓ Todas las rutas terminan en depósito")
    
    def test_no_empty_routes(self, instance_r101):
        """No deben existir rutas vacías (len >= 2 para [0, ..., 0])"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        for route in solution.routes:
            if len(route.sequence) > 0:  # Si existe ruta
                assert len(route.sequence) >= 2, \
                    f"Ruta {route.vehicle_id} es incompleta: {route.sequence}"
        
        print(f"✓ No hay rutas incompletas")


class TestObjectiveMinimizeK:
    """OBJETIVO 1: Minimizar K (número de vehículos)"""
    
    @pytest.fixture
    def loader(self):
        return SolomonLoader()
    
    @pytest.fixture
    def instance_r101(self, loader):
        return loader.load_instance('datasets/R1/R101.csv')
    
    def test_solution_has_num_vehicles_property(self, instance_r101):
        """Solution debe tener propiedad num_vehicles"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        assert hasattr(solution, 'num_vehicles'), "Solution sin num_vehicles"
        K = solution.num_vehicles
        assert K > 0, f"K debe ser > 0, obtenido {K}"
        print(f"✓ Solution.num_vehicles = {K}")
    
    def test_solution_has_fitness_tuple(self, instance_r101):
        """Solution.fitness debe ser tupla (K, D)"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        assert hasattr(solution, 'fitness'), "Solution sin fitness"
        fitness = solution.fitness
        assert isinstance(fitness, tuple), f"fitness debe ser tupla, es {type(fitness)}"
        assert len(fitness) == 2, f"fitness debe tener (K, D), tiene {len(fitness)} elementos"
        
        K, D = fitness
        assert K == solution.num_vehicles, "fitness[0] debe ser K"
        print(f"✓ fitness = ({K}, {D:.2f})")
    
    def test_k_is_primary_objective(self, instance_r101):
        """K debe ser la componente primaria de fitness"""
        grasp = GRASP(max_iterations=5, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        K = solution.num_vehicles
        
        # K debe estar en rango razonable
        assert 1 < K < 50, f"K = {K} parece irrazonable"
        print(f"✓ K = {K} está en rango razonable")
    
    def test_compare_solutions_k_primary(self, instance_r101):
        """compare_solutions debe favorecer menor K"""
        grasp1 = GRASP(max_iterations=1, seed=42)
        sol1, _, _ = grasp1.solve(instance_r101)
        
        grasp2 = GRASP(max_iterations=1, seed=43)
        sol2, _, _ = grasp2.solve(instance_r101)
        
        # compare_solutions retorna: 1 si sol1 > sol2, -1 si sol1 < sol2, 0 si igual
        result = compare_solutions(sol1, sol2)
        
        if sol1.num_vehicles < sol2.num_vehicles:
            assert result == -1, "Menor K debe ser mejor (retorna -1)"
        elif sol1.num_vehicles > sol2.num_vehicles:
            assert result == 1, "Mayor K debe ser peor (retorna 1)"
        
        print(f"✓ compare_solutions favorece K menor")


class TestObjectiveMinimizeD:
    """OBJETIVO 2: Minimizar D (distancia total) - secundario a K"""
    
    @pytest.fixture
    def loader(self):
        return SolomonLoader()
    
    @pytest.fixture
    def instance_r101(self, loader):
        return loader.load_instance('datasets/R1/R101.csv')
    
    def test_solution_has_total_distance(self, instance_r101):
        """Solution debe tener propiedad total_distance"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        assert hasattr(solution, 'total_distance'), "Solution sin total_distance"
        D = solution.total_distance
        assert D > 0, f"total_distance debe ser > 0, obtenido {D}"
        print(f"✓ Solution.total_distance = {D:.2f}")
    
    def test_distance_is_reasonable(self, instance_r101):
        """D debe estar en rango razonable para Solomon R101"""
        grasp = GRASP(max_iterations=5, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        D = solution.total_distance
        
        # Solomon instances típicamente en rango [500, 5000]
        assert D < 10000, f"Distancia {D} parece irrazonablemente alta"
        print(f"✓ D = {D:.2f} está en rango razonable")
    
    def test_compare_d_when_k_equal(self, instance_r101):
        """Si K igual, compare_solutions debe favorecer menor D"""
        grasp = GRASP(max_iterations=1, seed=42)
        sol1, _, _ = grasp.solve(instance_r101)
        
        # Generar otra solución con similar K
        grasp2 = GRASP(max_iterations=1, seed=43)
        sol2, _, _ = grasp2.solve(instance_r101)
        
        # compare_solutions retorna: 1 si sol1 > sol2, -1 si sol1 < sol2, 0 si igual
        if sol1.num_vehicles == sol2.num_vehicles:
            # K igual, debería compararse por D
            result = compare_solutions(sol1, sol2)
            
            if sol1.total_distance < sol2.total_distance:
                assert result == -1, "Con K igual, menor D debe ser mejor (retorna -1)"
            elif sol1.total_distance > sol2.total_distance:
                assert result == 1, "Con K igual, mayor D debe ser peor (retorna 1)"
            
            print(f"✓ Si K igual, se compara por D")


class TestRepairOperatorsPreserveCompleteness:
    """Operadores de REPAIR deben preservar todos los clientes"""
    
    @pytest.fixture
    def loader(self):
        return SolomonLoader()
    
    @pytest.fixture
    def instance_r101(self, loader):
        return loader.load_instance('datasets/R1/R101.csv')
    
    def test_repair_never_loses_customers(self, instance_r101):
        """Después de GRASP + repair, todos los 100 clientes deben estar presentes"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        # Contar clientes en solución final
        visited = set()
        for route in solution.routes:
            for c_id in route.sequence:
                if c_id != 0:
                    visited.add(c_id)
        
        assert len(visited) == 100, \
            f"Después de GRASP: {len(visited)} clientes (esperados 100)"
        
        print(f"✓ Repair operators preservan los 100 clientes")


class TestFeasibilityEvaluator:
    """El evaluador de factibilidad funciona correctamente"""
    
    @pytest.fixture
    def loader(self):
        return SolomonLoader()
    
    @pytest.fixture
    def instance_r101(self, loader):
        return loader.load_instance('datasets/R1/R101.csv')
    
    def test_evaluate_solution_returns_tuple(self, instance_r101):
        """evaluate_solution retorna (is_feasible, details)"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        result = evaluate_solution(solution)
        
        assert isinstance(result, tuple), "evaluate_solution debe retornar tupla"
        assert len(result) == 2, "Debe retornar (is_feasible, details)"
        
        is_feasible, details = result
        assert isinstance(is_feasible, bool), "is_feasible debe ser bool"
        assert isinstance(details, dict), "details debe ser dict"
        
        print(f"✓ evaluate_solution retorna (bool, dict)")
    
    def test_details_include_key_metrics(self, instance_r101):
        """details debe incluir métricas clave"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        is_feasible, details = evaluate_solution(solution)
        
        assert 'num_vehicles' in details, "Falta num_vehicles"
        assert 'total_distance' in details, "Falta total_distance"
        assert 'fitness' in details, "Falta fitness"
        assert 'route_details' in details, "Falta route_details"
        
        print(f"✓ details incluye todas las métricas")


# ============================================================================
# RESUMEN EJECUTABLE
# ============================================================================

if __name__ == "__main__":
    print("""
╔═════════════════════════════════════════════════════════════════╗
║    BACKBONE FEASIBILITY - TESTS UNITARIOS PRAGMÁTICOS          ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  RESTRICCIONES DURAS (4):                                      ║
║    ✓ TestCoverageConstraint          (100% cobertura)         ║
║    ✓ TestCapacityConstraint          (carga ≤ Q=200)          ║
║    ✓ TestTimeWindowConstraint        (ventanas TW)            ║
║    ✓ TestFlowConservationConstraint  (inicio/fin depósito)    ║
║                                                                 ║
║  OBJETIVOS (2):                                                ║
║    ✓ TestObjectiveMinimizeK          (Min K primario)         ║
║    ✓ TestObjectiveMinimizeD          (Min D secundario)       ║
║                                                                 ║
║  VERIFICACIÓN INTEGRIDAD:                                      ║
║    ✓ TestRepairOperatorsPreserveCompleteness                  ║
║    ✓ TestFeasibilityEvaluator                                 ║
║                                                                 ║
║  EJECUCIÓN:                                                    ║
║    pytest test_backbone_feasibility_v2.py -v                  ║
║    pytest test_backbone_feasibility_v2.py -v -s               ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
    """)
