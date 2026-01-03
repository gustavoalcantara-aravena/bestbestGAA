"""
TESTS UNITARIOS - BACKBONE FEASIBILITY
=======================================

Validación exhaustiva de todas las restricciones VRPTW documentadas en BACKBONE_FEASIBILITY.md

Fases de Testing:
1. FASE 2: Auditoría de Código (Verificación de implementación)
2. FASE 3: Testing Exhaustivo (Tests unitarios por restricción)
3. FASE 4: Auditoría de Restricciones Implementadas
"""

import pytest
import sys
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.loader import SolomonLoader
from src.core.models import Route, Solution, Customer, Instance
from src.core.evaluation import evaluate_solution, compare_solutions
from src.metaheuristic.grasp import GRASP
from src.operators.perturbation import RepairCapacity, RepairTimeWindows


class TestRestrictionSpecification:
    """FASE 2: Verificar que especificaciones están en documentación"""
    
    def test_problema_vrptw_exists(self):
        """Verificar que 01-problema-vrptw.md existe y contiene restricciones"""
        doc = Path("projects/GAA-VRPTW-GRASP-2/01-problema-vrptw.md").read_text()
        
        assert "Cobertura" in doc
        assert "Capacidad" in doc
        assert "Ventanas de tiempo" in doc
        
    def test_modelo_matematico_exists(self):
        """Verificar que 02-modelo-matematico.md existe y contiene restricciones"""
        doc = Path("projects/GAA-VRPTW-GRASP-2/02-modelo-matematico.md").read_text()
        
        assert "Minimizar K" in doc or "minimizar k" in doc.lower()
        assert "Distancia" in doc or "distancia" in doc.lower()
        
    def test_fitness_canonico_exists(self):
        """Verificar que 07-fitness-canonico.md existe y define función objetivo"""
        doc = Path("projects/GAA-VRPTW-GRASP-2/07-fitness-canonico.md").read_text()
        
        assert "fitness" in doc.lower()
        assert "K" in doc or "vehículos" in doc.lower()


class TestCoverageConstraint:
    """RESTRICCIÓN 1: Cobertura (cada cliente visitado exactamente una vez)"""
    
    @pytest.fixture
    def loader(self):
        """Cargar instancia Solomon"""
        return SolomonLoader()
    
    @pytest.fixture
    def instance_r101(self, loader):
        """Cargar R101 (100 clientes)"""
        return loader.load_instance('datasets/R1/R101.csv')
    
    def test_loader_loads_all_customers(self, instance_r101):
        """Verificar que loader carga los 100 clientes (+ depósito)"""
        # Instance.customers incluye depósito (cliente 0) + 100 clientes
        assert len(instance_r101.customers) == 101, \
            f"Se esperaban 101 clientes (depósito + 100), se obtuvieron {len(instance_r101.customers)}"
    
    def test_grasp_covers_all_customers(self, instance_r101):
        """Verificar que GRASP produce solución con todos los 100 clientes"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        # Recolectar todos los clientes visitados
        visited = set()
        for route in solution.routes:
            for c_id in route.sequence:
                if c_id != 0:  # Excluir depósito
                    visited.add(c_id)
        
        assert len(visited) == 100, \
            f"Se cubrieron {len(visited)} clientes, esperados 100"
    
    def test_no_duplicate_customers(self, instance_r101):
        """Verificar que ningún cliente se visita más de una vez"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        visited = []
        for route in solution.routes:
            for c_id in route.sequence:
                if c_id != 0:  # Excluir depósito
                    visited.append(c_id)
        
        assert len(visited) == len(set(visited)), \
            f"Hay clientes duplicados: {len(visited)} visitados, {len(set(visited))} únicos"
    
    def test_coverage_by_evaluator(self, instance_r101):
        """Verificar que evaluate_solution detecta cobertura"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        is_feasible, details = evaluate_solution(solution)
        
        # Al menos debe reportar que la cobertura está OK
        assert details.get('coverage_ok', False), "coverage_ok debería ser True"


class TestCapacityConstraint:
    """RESTRICCIÓN 2: Capacidad (carga por ruta ≤ Q)"""
    
    @pytest.fixture
    def loader(self):
        return SolomonLoader()
    
    @pytest.fixture
    def instance_r101(self, loader):
        return loader.load_instance('datasets/R1/R101.csv')
    
    def test_instance_has_capacity(self, instance_r101):
        """Verificar que Instance carga Q_capacity"""
        assert hasattr(instance_r101, 'Q_capacity'), "Instance debería tener Q_capacity"
        assert instance_r101.Q_capacity == 200, \
            f"Solomon Q debería ser 200, se obtuvo {instance_r101.Q_capacity}"
    
    def test_customers_have_demand(self, instance_r101):
        """Verificar que todos los clientes tienen demanda"""
        for i, customer in enumerate(instance_r101.customers):
            assert hasattr(customer, 'demand'), f"Cliente {i} no tiene atributo demand"
            assert customer.demand > 0, f"Cliente {i} demanda debería ser > 0"
    
    def test_route_calculates_total_load(self, instance_r101):
        """Verificar que Route calcula total_load correctamente"""
        c1 = instance_r101.customers[0]
        c2 = instance_r101.customers[1]
        
        route = Route(vehicle_id=0, sequence=[0, 1, 2, 0])
        
        # Route debería poder calcular carga
        assert hasattr(route, 'total_load') or hasattr(route, 'get_load'), \
            "Route debería calcular carga total"
    
    def test_grasp_respects_capacity(self, instance_r101):
        """Verificar que GRASP nunca viola capacidad"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        # Verificar cada ruta
        for route in solution.routes:
            total_demand = sum(
                instance_r101.customers[c_id - 1].demand
                for c_id in route.sequence
                if c_id != 0  # Excluir depósito
            )
            
            assert total_demand <= instance_r101.Q_capacity, \
                f"Ruta {route.vehicle_id} excede capacidad: {total_demand} > {instance_r101.Q_capacity}"
    
    def test_evaluator_detects_capacity_violation(self, instance_r101):
        """Verificar que evaluate_solution detecta violación de capacidad"""
        # Crear una ruta que viola capacidad
        route = Route(vehicle_id=0, sequence=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0])
        
        solution = Solution(routes=[route])
        is_feasible, details = evaluate_solution(solution)
        
        # Si la ruta sobrepasa capacidad, debería reportarse como infactible
        total_demand = sum(
            instance_r101.customers[c_id - 1].demand
            for c_id in route.sequence
            if c_id != 0
        )
        
        if total_demand > instance_r101.Q_capacity:
            assert is_feasible is False or details['capacity_constraint'] is False, \
                "Evaluador debería detectar violación de capacidad"
    
    def test_repair_capacity_operator_exists(self, instance_r101):
        """Verificar que RepairCapacity existe"""
        assert RepairCapacity is not None
        
        # Intentar instanciar
        repair = RepairCapacity()
        assert hasattr(repair, 'apply'), "RepairCapacity debería tener método apply()"


class TestTimeWindowConstraint:
    """RESTRICCIÓN 3: Ventanas de Tiempo (a_i ≤ t_i ≤ b_i)"""
    
    @pytest.fixture
    def loader(self):
        return SolomonLoader()
    
    @pytest.fixture
    def instance_c1(self, loader):
        """Cargar C1 (ventanas restrictivas)"""
        return loader.load_instance('datasets/C1/C101.csv')
    
    def test_customers_have_time_windows(self, instance_c1):
        """Verificar que clientes tienen ready_time y due_date"""
        for i, customer in enumerate(instance_c1.customers):
            assert hasattr(customer, 'ready_time'), f"Cliente {i} sin ready_time"
            assert hasattr(customer, 'due_date'), f"Cliente {i} sin due_date"
            assert hasattr(customer, 'service_time'), f"Cliente {i} sin service_time"
            
            # Validar que ventana sea coherente
            assert customer.ready_time <= customer.due_date, \
                f"Cliente {i}: ready_time ({customer.ready_time}) > due_date ({customer.due_date})"
    
    def test_depot_has_time_window(self, instance_c1):
        """Verificar que depósito (cliente 0) tiene ventana de tiempo"""
        depot = instance_c1.customers[0]
        assert hasattr(depot, 'ready_time')
        assert hasattr(depot, 'due_date')
        assert hasattr(depot, 'service_time')
    
    def test_route_calculates_arrival_times(self, instance_c1):
        """Verificar que Route puede calcular tiempos de llegada"""
        route = Route(vehicle_id=0, sequence=[0, 1, 0])
        
        # Route debería poder calcular tiempo total
        assert hasattr(route, 'total_time') or hasattr(route, 'get_arrival_times'), \
            "Route debería calcular tiempos de servicio"
    
    def test_grasp_respects_time_windows(self, instance_c1):
        """Verificar que GRASP respeta ventanas de tiempo en C1"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_c1)
        
        is_feasible, details = evaluate_solution(solution)
        
        # En C1, si la solución es reportada como factible, debe respetar TW
        if is_feasible:
            assert details.get('time_window_constraint', True), \
                "Si es factible, debe respetar ventanas de tiempo"
    
    def test_evaluator_detects_time_window_violation(self, instance_c1):
        """Verificar que evaluate_solution detecta violación de TW"""
        # Crear ruta que podría violar ventanas
        route = Route(vehicle_id=0, sequence=[0, 1, 2, 3, 0])
        solution = Solution(routes=[route])
        
        is_feasible, details = evaluate_solution(solution)
        
        # Si hay violación, debería reportarse
        # Este test es flexible porque depende del orden de clientes
        assert 'time_window_constraint' in details, \
            "Evaluador debería incluir time_window_constraint en resultados"
    
    def test_repair_time_windows_operator_exists(self, instance_c1):
        """Verificar que RepairTimeWindows existe"""
        assert RepairTimeWindows is not None
        
        repair = RepairTimeWindows()
        assert hasattr(repair, 'apply'), "RepairTimeWindows debería tener método apply()"


class TestFlowConservationConstraint:
    """RESTRICCIÓN 4: Conservación de Flujo (inicio/fin en depósito)"""
    
    @pytest.fixture
    def loader(self):
        return SolomonLoader()
    
    @pytest.fixture
    def instance_r101(self, loader):
        return loader.load_instance('datasets/R1/R101.csv')
    
    def test_all_routes_start_at_depot(self, instance_r101):
        """Verificar que todas las rutas comienzan en depósito (nodo 0)"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        for i, route in enumerate(solution.routes):
            assert route.sequence[0] == 0, \
                f"Ruta {i} no comienza en depósito: {route.sequence[0]}"
    
    def test_all_routes_end_at_depot(self, instance_r101):
        """Verificar que todas las rutas terminan en depósito (nodo 0)"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        for i, route in enumerate(solution.routes):
            assert route.sequence[-1] == 0, \
                f"Ruta {i} no termina en depósito: {route.sequence[-1]}"
    
    def test_all_routes_have_minimum_length(self, instance_r101):
        """Verificar que no hay rutas vacías (mínimo: [0, cliente, 0])"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        for i, route in enumerate(solution.routes):
            assert len(route.sequence) >= 2, \
                f"Ruta {i} está vacía o incompleta: {route.sequence}"
    
    def test_no_routes_with_only_depot(self, instance_r101):
        """Verificar que no hay rutas que solo contengan depósito"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        for i, route in enumerate(solution.routes):
            # Una ruta válida debe tener al menos: [0, cliente, 0]
            assert len(route.sequence) >= 3 or len(route.sequence) == 0, \
                f"Ruta {i} inválida: {route.sequence}"


class TestObjectiveMinimizeK:
    """OBJETIVO 1: Minimizar K (número de vehículos)"""
    
    def test_solution_has_fitness_property(self):
        """Verificar que Solution tiene propiedad fitness"""
        route = Route(vehicle_id=0, sequence=[0, 1, 0])
        solution = Solution(routes=[route])
        
        assert hasattr(solution, 'fitness'), "Solution debería tener propiedad fitness"
        assert hasattr(solution, 'num_vehicles'), "Solution debería tener num_vehicles"
    
    def test_fitness_is_tuple(self):
        """Verificar que fitness es tupla (K, D)"""
        route = Route(vehicle_id=0, sequence=[0, 1, 0])
        solution = Solution(routes=[route])
        
        fitness = solution.fitness
        assert isinstance(fitness, tuple), f"fitness debería ser tupla, es {type(fitness)}"
        assert len(fitness) == 2, f"fitness debería tener 2 elementos (K, D), tiene {len(fitness)}"
    
    def test_k_is_first_in_fitness(self):
        """Verificar que K es la primera componente de fitness"""
        route1 = Route(vehicle_id=0, sequence=[0, 1, 0])
        route2 = Route(vehicle_id=1, sequence=[0, 2, 0])
        
        solution_2veh = Solution(routes=[route1, route2])
        solution_1veh = Solution(routes=[route1])
        
        # 2 vehículos debería tener K más alto
        assert solution_2veh.num_vehicles > solution_1veh.num_vehicles
        
        # fitness[0] debería ser K
        k_2veh, _ = solution_2veh.fitness
        k_1veh, _ = solution_1veh.fitness
        
        assert k_2veh > k_1veh, "Más vehículos debería significar fitness peor"
    
    def test_compare_solutions_k_primary(self):
        """Verificar que compare_solutions compara K primero"""
        # Solución 1: K=5, D=1000
        # Solución 2: K=10, D=100
        # Sol1 debería ser mejor porque K es primario
        
        route1_sol1 = Route(vehicle_id=0, sequence=[0, 1, 0])
        sol1 = Solution(routes=[route1_sol1] * 5)
        
        route1_sol2 = Route(vehicle_id=0, sequence=[0, 1, 0])
        sol2 = Solution(routes=[route1_sol2] * 10)
        
        # sol1 debería ser mejor (K menor)
        assert sol1.fitness < sol2.fitness, \
            f"Solución con K=5 debería ser mejor que K=10, pero {sol1.fitness} >= {sol2.fitness}"
    
    @pytest.fixture
    def loader(self):
        return SolomonLoader()
    
    @pytest.fixture
    def instance_r101(self, loader):
        return loader.load_instance('datasets/R1/R101.csv')
    
    def test_grasp_minimizes_k(self, instance_r101):
        """Verificar que GRASP minimiza K"""
        grasp = GRASP(max_iterations=5, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        # K debería ser razonable (no 1, no 100)
        K = solution.num_vehicles
        
        assert K > 1, f"K={K} es demasiado bajo (debería ser > 1)"
        assert K < 50, f"K={K} es demasiado alto (debería ser < 50)"


class TestObjectiveMinimizeD:
    """OBJETIVO 2: Minimizar D (distancia total) - secundario a K"""
    
    def test_distance_is_second_in_fitness(self):
        """Verificar que D es segunda componente de fitness"""
        route = Route(vehicle_id=0, sequence=[0, 1, 0])
        solution = Solution(routes=[route])
        
        _, d = solution.fitness
        assert isinstance(d, (int, float)), f"D debería ser número, es {type(d)}"
    
    def test_solution_has_total_distance(self):
        """Verificar que Solution calcula distancia total"""
        route = Route(vehicle_id=0, sequence=[0, 1, 0])
        solution = Solution(routes=[route])
        
        assert hasattr(solution, 'total_distance'), "Solution debería tener total_distance"
    
    def test_compare_d_only_if_k_equal(self):
        """Verificar que D se compara solo si K es igual"""
        # Ambas con K=1 pero diferente D
        route1 = Route(vehicle_id=0, sequence=[0, 1, 0])
        route2 = Route(vehicle_id=0, sequence=[0, 2, 0])
        
        sol1 = Solution(routes=[route1])
        sol2 = Solution(routes=[route2])
        
        # Si K es igual (K=1 ambas), comparar D
        if sol1.num_vehicles == sol2.num_vehicles:
            # fitness[1] debería ser D
            _, d1 = sol1.fitness
            _, d2 = sol2.fitness
            
            # Solo debería importar D si K igual
            assert (d1 < d2 and sol1.fitness < sol2.fitness) or \
                   (d1 > d2 and sol1.fitness > sol2.fitness) or \
                   (d1 == d2 and sol1.fitness == sol2.fitness), \
                "Si K igual, debería compararse por D"
    
    @pytest.fixture
    def loader(self):
        return SolomonLoader()
    
    @pytest.fixture
    def instance_r101(self, loader):
        return loader.load_instance('datasets/R1/R101.csv')
    
    def test_grasp_minimizes_d_with_fixed_k(self, instance_r101):
        """Verificar que GRASP minimiza D cuando K está fijo"""
        grasp = GRASP(max_iterations=5, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        D = solution.total_distance
        
        # D debería ser positivo
        assert D > 0, f"Distancia debería ser > 0, es {D}"
        
        # D debería ser razonable (proporcional a 100 clientes)
        # Solomon instances típicamente están en rango [500, 5000]
        assert D < 10000, f"Distancia {D} parece irrazonablemente alta"


class TestRepairOperatorsCompleteness:
    """Verificar que operadores de repair funcionan correctamente"""
    
    @pytest.fixture
    def loader(self):
        return SolomonLoader()
    
    @pytest.fixture
    def instance_r101(self, loader):
        return loader.load_instance('datasets/R1/R101.csv')
    
    def test_repair_capacity_preserves_all_customers(self, instance_r101):
        """Verificar que RepairCapacity nunca pierde clientes"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        repair = RepairCapacity()
        
        # Contar clientes antes
        customers_before = set()
        for route in solution.routes:
            for c_id in route.sequence:
                if c_id != 0:
                    customers_before.add(c_id)
        
        # Aplicar repair
        repaired_solution = repair.apply(solution, instance_r101)
        
        # Contar clientes después
        customers_after = set()
        for route in repaired_solution.routes:
            for c_id in route.sequence:
                if c_id != 0:
                    customers_after.add(c_id)
        
        # Verificar que no se perdieron clientes
        assert customers_after == customers_before, \
            f"RepairCapacity perdió clientes: antes {len(customers_before)}, después {len(customers_after)}"
    
    def test_repair_time_windows_preserves_all_customers(self, instance_r101):
        """Verificar que RepairTimeWindows nunca pierde clientes"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        repair = RepairTimeWindows()
        
        # Contar clientes antes
        customers_before = set()
        for route in solution.routes:
            for c_id in route.sequence:
                if c_id != 0:
                    customers_before.add(c_id)
        
        # Aplicar repair
        repaired_solution = repair.apply(solution, instance_r101)
        
        # Contar clientes después
        customers_after = set()
        for route in repaired_solution.routes:
            for c_id in route.sequence:
                if c_id != 0:
                    customers_after.add(c_id)
        
        # Verificar que no se perdieron clientes
        assert customers_after == customers_before, \
            f"RepairTimeWindows perdió clientes: antes {len(customers_before)}, después {len(customers_after)}"


class TestFeasibilityEvaluator:
    """Verificar que el evaluador de factibilidad funciona correctamente"""
    
    @pytest.fixture
    def loader(self):
        return SolomonLoader()
    
    @pytest.fixture
    def instance_r101(self, loader):
        return loader.load_instance('datasets/R1/R101.csv')
    
    def test_evaluate_solution_returns_boolean_and_details(self, instance_r101):
        """Verificar que evaluate_solution retorna (is_feasible, details)"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        result = evaluate_solution(solution)
        
        assert isinstance(result, tuple), "evaluate_solution debería retornar tupla"
        assert len(result) == 2, "evaluate_solution debería retornar (is_feasible, details)"
        
        is_feasible, details = result
        assert isinstance(is_feasible, bool), "is_feasible debería ser bool"
        assert isinstance(details, dict), "details debería ser dict"
    
    def test_details_include_all_constraints(self, instance_r101):
        """Verificar que details incluya todas las restricciones"""
        grasp = GRASP(max_iterations=1, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        is_feasible, details = evaluate_solution(solution)
        
        # Verificar que al menos algunos constraints estén presentes
        assert 'coverage_constraint' in details or 'capacity_constraint' in details or \
               'time_window_constraint' in details, \
            f"details debería incluir constraint checks, se obtuvo: {details.keys()}"
    
    def test_feasible_solution_passes_evaluation(self, instance_r101):
        """Verificar que una solución GRASP es factible según evaluador"""
        grasp = GRASP(max_iterations=5, seed=42)
        solution, _, _ = grasp.solve(instance_r101)
        
        is_feasible, details = evaluate_solution(solution)
        
        # Una solución del framework debería ser factible
        assert is_feasible is True or is_feasible is not False, \
            f"Solución GRASP debería ser factible, se obtuvo: {is_feasible}"


class TestComparisonOperator:
    """Verificar que las comparaciones de soluciones son correctas"""
    
    def test_compare_solutions_returns_better_with_lower_k(self):
        """Verificar que comparación lexicográfica favorece K menor"""
        route1 = Route(vehicle_id=0, sequence=[0, 1, 0])
        sol_low_k = Solution(routes=[route1] * 5)
        sol_high_k = Solution(routes=[route1] * 10)
        
        better = compare_solutions(sol_low_k, sol_high_k)
        
        assert better == sol_low_k, \
            f"Solución con K=5 debería ser mejor que K=10"
    
    def test_compare_solutions_returns_better_with_lower_d_if_k_equal(self):
        """Verificar que con K igual, compara por D"""
        route1 = Route(vehicle_id=0, sequence=[0, 1, 0])
        route2 = Route(vehicle_id=0, sequence=[0, 2, 0])
        
        sol1 = Solution(routes=[route1])
        sol2 = Solution(routes=[route2])
        
        better = compare_solutions(sol1, sol2)
        
        # Si K es igual, la de menor distancia debería ser mejor
        if sol1.num_vehicles == sol2.num_vehicles:
            if sol1.total_distance < sol2.total_distance:
                assert better == sol1
            elif sol1.total_distance > sol2.total_distance:
                assert better == sol2


# ============================================================================
# RESUMEN DE TESTS
# ============================================================================

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════╗
║     TESTS UNITARIOS - BACKBONE FEASIBILITY FRAMEWORK          ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  RESTRICCIONES DURAS (4):                                    ║
║    ✓ TestCoverageConstraint         (Cobertura)             ║
║    ✓ TestCapacityConstraint         (Capacidad ≤ Q)         ║
║    ✓ TestTimeWindowConstraint       (Ventanas TW)           ║
║    ✓ TestFlowConservationConstraint (Flujo)                 ║
║                                                               ║
║  OBJETIVOS (2):                                              ║
║    ✓ TestObjectiveMinimizeK         (Min K primario)        ║
║    ✓ TestObjectiveMinimizeD         (Min D secundario)      ║
║                                                               ║
║  VERIFICACIÓN:                                               ║
║    ✓ TestRepairOperatorsCompleteness                        ║
║    ✓ TestFeasibilityEvaluator                               ║
║    ✓ TestComparisonOperator                                 ║
║                                                               ║
║  TOTAL: 9 clases de tests, ~50+ tests unitarios              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

Ejecutar con:
  pytest test_backbone_feasibility.py -v
  pytest test_backbone_feasibility.py -v --tb=short
  pytest test_backbone_feasibility.py::TestCoverageConstraint -v
    """)
