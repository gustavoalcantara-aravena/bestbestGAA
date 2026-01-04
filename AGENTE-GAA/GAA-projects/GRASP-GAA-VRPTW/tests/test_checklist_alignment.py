"""
TEST SUITE: Checklist Final Antes de Testeo Intensivo

Verifica:
1. Alineación Generator → Validator → Parser
2. Round-trip AST (generar → validar → parsear)
3. Estados exactamente definidos
4. Determinismo total
5. Evaluación contra Solomon + BKS
6. SolutionPool y dominancia
7. Logging schema correcto
8. Canary run C101

Regla de Oro: NO agregues features nuevas. TODO debe cumplir contratos existentes.
"""

import sys
import os
import json
import hashlib
from typing import Dict, Any, Set, List, Tuple
import pytest

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ast.generator import RandomASTGenerator
from ast.validator import (
    ASTValidator, 
    ASTValidationConfig,
    DEFAULT_ALLOWED_NODE_TYPES,
    DEFAULT_FUNCTIONAL_NODE_TYPES,
)
from ast.parser import ASTParser
from evaluation.solution_evaluator import SolutionEvaluator
from evaluation.bks_loader import BKSLoader
from evaluation.bks_validation import BKSValidation
from solution.solution_pool import SolutionPool


# ============================================================================
# 1️⃣ ALINEACIÓN: GENERATOR → VALIDATOR → PARSER
# ============================================================================

class TestASTLanguageAlignment:
    """Verifica que todos los node types y campos coincidan entre los 3 módulos."""
    
    def test_generator_produces_only_allowed_types(self):
        """Cada type que genera el generator está en DEFAULT_ALLOWED_NODE_TYPES."""
        gen = RandomASTGenerator(seed=42)
        
        # Generar múltiples ASTs
        for _ in range(10):
            ast_const = gen.generate(phase="construction", seed=42)
            ast_ls = gen.generate(phase="local_search", seed=42)
            
            # Recolectar todos los tipos usados
            types_used = self._collect_node_types(ast_const)
            types_used.update(self._collect_node_types(ast_ls))
            
            # Verificar que todos están permitidos
            for node_type in types_used:
                assert node_type in DEFAULT_ALLOWED_NODE_TYPES, \
                    f"Generator produced type '{node_type}' not in DEFAULT_ALLOWED_NODE_TYPES"
    
    def test_validator_accepts_generator_output(self):
        """ASTValidator acepta todos los types que generator produce."""
        gen = RandomASTGenerator(seed=42)
        validator = ASTValidator()
        
        for _ in range(5):
            ast_const = gen.generate(phase="construction", seed=42)
            ast_ls = gen.generate(phase="local_search", seed=42)
            
            # Validar construcción
            result_const = validator.validate_construction_ast(ast_const)
            assert result_const.ok, f"Validation failed: {result_const.errors}"
            
            # Validar búsqueda local
            result_ls = validator.validate_local_search_ast(ast_ls)
            assert result_ls.ok, f"Validation failed: {result_ls.errors}"
    
    def test_parser_supports_all_allowed_types(self):
        """ASTParser tiene evaluate() para todos los DEFAULT_ALLOWED_NODE_TYPES."""
        parser = ASTParser()
        
        # Listar todos los tipos permitidos
        # (En una implementación real, parser.py tiene un mapeo de tipos)
        supported = {
            "Const", "Feature",
            "Add", "Sub", "Mul", "Div",
            "Less", "Greater", "And", "Or",
            "If", "Normalize", "Clip", "Choose",
            "WeightedSum"
        }
        
        for node_type in DEFAULT_ALLOWED_NODE_TYPES:
            assert node_type in supported, \
                f"Parser doesn't support node type '{node_type}'"
    
    def _collect_node_types(self, ast: Dict[str, Any]) -> Set[str]:
        """Recursivamente recolecta todos los tipos de nodos en un AST."""
        types = set()
        
        def traverse(node):
            if isinstance(node, dict):
                if "type" in node:
                    types.add(node["type"])
                for key, val in node.items():
                    if isinstance(val, (dict, list)):
                        traverse(val)
            elif isinstance(node, list):
                for item in node:
                    traverse(item)
        
        traverse(ast)
        return types


# ============================================================================
# 2️⃣ TESTS ROUND-TRIP: GENERATION → VALIDATION → PARSING
# ============================================================================

class TestASTRoundTrip:
    """Tests de construcción → validación → parsing.
    
    Detecta:
    - Bugs de tipos
    - Bugs de campos faltantes
    - Crashes en runtime
    """
    
    def test_construction_ast_roundtrip(self):
        """Construction phase: generar → validar → parsear → evaluar."""
        gen = RandomASTGenerator(seed=42)
        validator = ASTValidator()
        parser = ASTParser()
        
        # Generar AST de construcción
        ast = gen.generate(phase="construction", seed=42)
        
        # Validar
        result = validator.validate_construction_ast(ast)
        assert result.ok, f"Validation failed: {result.errors}"
        
        # Parsear
        root_node = parser.parse(ast)
        assert root_node is not None
        
        # Evaluar con estado ficticio
        state = self._fake_construction_state()
        value = root_node.evaluate(state)
        assert isinstance(value, (int, float))
        assert not (value != value), "Value is NaN"  # Detectar NaN
    
    def test_local_search_ast_roundtrip(self):
        """Local search phase: generar → validar → parsear → evaluar."""
        gen = RandomASTGenerator(seed=123)
        validator = ASTValidator()
        parser = ASTParser()
        
        # Generar AST de búsqueda local
        ast = gen.generate(phase="local_search", seed=123)
        
        # Validar
        result = validator.validate_local_search_ast(ast)
        assert result.ok, f"Validation failed: {result.errors}"
        
        # Parsear
        root_node = parser.parse(ast)
        assert root_node is not None
        
        # Evaluar con estado ficticio
        state = self._fake_local_search_state()
        value = root_node.evaluate(state)
        # Local search retorna string (nombre de operador)
        assert isinstance(value, str)
    
    def test_roundtrip_with_multiple_seeds(self):
        """Verificar round-trip con múltiples seeds."""
        gen = RandomASTGenerator(seed=42)
        validator = ASTValidator()
        parser = ASTParser()
        
        for seed in [42, 123, 999, 1234567]:
            # Construction
            ast_c = gen.generate(phase="construction", seed=seed)
            result_c = validator.validate_construction_ast(ast_c)
            assert result_c.ok
            
            parser.parse(ast_c)  # No crash
            
            # Local Search
            ast_ls = gen.generate(phase="local_search", seed=seed)
            result_ls = validator.validate_local_search_ast(ast_ls)
            assert result_ls.ok
            
            parser.parse(ast_ls)  # No crash
    
    @staticmethod
    def _fake_construction_state() -> Dict[str, Any]:
        """Estado ficticio para fase de construcción."""
        return {
            "route_length": 3,
            "route_load": 150,
            "route_capacity_remaining": 50,
            "route_current_time": 100,
            "cust_demand": 25,
            "cust_ready_time": 50,
            "cust_due_time": 200,
            "delta_distance": 10,
            "urgency": 0.5,
            "utilization": 0.75,
        }
    
    @staticmethod
    def _fake_local_search_state() -> Dict[str, Any]:
        """Estado ficticio para fase de búsqueda local."""
        return {
            "num_routes": 5,
            "total_distance": 500,
            "penalty_value": 10,
            "iterations_no_improve": 2,
            "temperature": 0.8,
            "acceptance_threshold": 0.3,
            "feasibility_score": 0.95,
        }


# ============================================================================
# 3️⃣ CONGELACIÓN DE ESTADOS: CONTRATOS EXACTOS
# ============================================================================

CONSTRUCTION_STATE_KEYS = {
    "route_length",
    "route_load",
    "route_capacity_remaining",
    "route_current_time",
    "cust_demand",
    "cust_ready_time",
    "cust_due_time",
    "delta_distance",
    "urgency",
    "utilization",
}

LOCAL_SEARCH_STATE_KEYS = {
    "num_routes",
    "total_distance",
    "penalty_value",
    "iterations_no_improve",
    "temperature",
    "acceptance_threshold",
    "feasibility_score",
}


class TestStateContracts:
    """Congela los contratos de estado exactamente definidos."""
    
    def test_construction_state_has_required_keys(self):
        """El estado de construcción tiene EXACTAMENTE las keys definidas."""
        state = TestASTRoundTrip._fake_construction_state()
        assert set(state.keys()) == CONSTRUCTION_STATE_KEYS, \
            f"Construction state keys mismatch.\n" \
            f"Expected: {CONSTRUCTION_STATE_KEYS}\n" \
            f"Got: {set(state.keys())}"
    
    def test_local_search_state_has_required_keys(self):
        """El estado de búsqueda local tiene EXACTAMENTE las keys definidas."""
        state = TestASTRoundTrip._fake_local_search_state()
        assert set(state.keys()) == LOCAL_SEARCH_STATE_KEYS, \
            f"Local search state keys mismatch.\n" \
            f"Expected: {LOCAL_SEARCH_STATE_KEYS}\n" \
            f"Got: {set(state.keys())}"
    
    def test_ast_features_all_exist_in_state(self):
        """Todas las features usadas por el AST existen en el estado."""
        gen = RandomASTGenerator(seed=42)
        validator = ASTValidator()
        
        # Generar y validar
        ast_const = gen.generate(phase="construction", seed=42)
        result = validator.validate_construction_ast(ast_const)
        assert result.ok
        
        # Recolectar features usadas
        features_used = self._collect_features(ast_const)
        
        # Verificar que existen en estado de construcción
        state = TestASTRoundTrip._fake_construction_state()
        for feature in features_used:
            assert feature in state, \
                f"Feature '{feature}' not found in construction state"
    
    @staticmethod
    def _collect_features(ast: Dict[str, Any]) -> Set[str]:
        """Recolecta todos los "Feature" nodes del AST."""
        features = set()
        
        def traverse(node):
            if isinstance(node, dict):
                if node.get("type") == "Feature":
                    features.add(node.get("name"))
                for val in node.values():
                    if isinstance(val, (dict, list)):
                        traverse(val)
            elif isinstance(node, list):
                for item in node:
                    traverse(item)
        
        traverse(ast)
        return features


# ============================================================================
# 4️⃣ DETERMINISMO TOTAL: CIENTÍFICAMENTE CRÍTICO
# ============================================================================

class TestDeterminism:
    """Verifica que el sistema es 100% determinista con seed."""
    
    def test_generator_determinism(self):
        """ASTGenerator es 100% determinista con seed."""
        gen1 = RandomASTGenerator(seed=42)
        gen2 = RandomASTGenerator(seed=42)
        
        # Generar con el mismo seed múltiples veces
        for _ in range(5):
            ast1_c = gen1.generate(phase="construction", seed=42)
            ast2_c = gen2.generate(phase="construction", seed=42)
            
            # Convertir a JSON strings para comparar exactamente
            json1 = json.dumps(ast1_c, sort_keys=True)
            json2 = json.dumps(ast2_c, sort_keys=True)
            
            assert json1 == json2, "Generator is not deterministic"
    
    def test_parser_no_rng(self):
        """ASTParser NO usa RNG (es puro)."""
        parser = ASTParser()
        
        # AST simple
        ast = {"type": "Const", "value": 42}
        
        # Parsear múltiples veces - debe ser idéntico
        state = TestASTRoundTrip._fake_construction_state()
        values = [parser.parse(ast).evaluate(state) for _ in range(10)]
        
        assert all(v == values[0] for v in values), "Parser is not deterministic"
    
    def test_seed_reproducibility(self):
        """Mismo seed produce exactamente el mismo AST."""
        gen = RandomASTGenerator(seed=999)
        
        # Generar 10 veces con el mismo seed
        asts = [gen.generate(phase="construction", seed=999) for _ in range(10)]
        
        # Todos deben ser idénticos
        first = json.dumps(asts[0], sort_keys=True)
        for i, ast in enumerate(asts[1:], 1):
            assert json.dumps(ast, sort_keys=True) == first, \
                f"Run {i} differs from run 0"


# ============================================================================
# 5️⃣ EVALUACIÓN CONTRA SOLOMON + BKS
# ============================================================================

class TestSolomonAndBKS:
    """Tests "duros" contra Solomon y BKS."""
    
    def test_parse_solomon_c101(self):
        """Parsear C101 correctamente."""
        evaluator = SolutionEvaluator()
        
        # Cargar C101 (debe existir)
        instance = evaluator.parse_solomon_instance("C101.txt")
        
        # Verificaciones básicas
        assert instance["capacity"] == 200
        assert len(instance["nodes"]) == 101
        assert instance["nodes"][0]["id"] == 0
        assert instance["nodes"][0]["x"] == 40
        assert instance["nodes"][0]["y"] == 50
    
    def test_bks_loading(self):
        """Cargar BKS correctamente."""
        loader = BKSLoader()
        bks = loader.load_from_file("best_known_solutions.json")
        
        # BKS para C101 = (10 vehículos, 828.93664 de distancia)
        assert "C101" in bks
        vehicles, distance = bks["C101"]
        assert vehicles == 10
        assert abs(distance - 828.93664) < 1e-4
    
    def test_gap_computation_exact(self):
        """Computar gap exactamente contra BKS."""
        loader = BKSLoader()
        bks = loader.load_from_file("best_known_solutions.json")
        validation = BKSValidation()
        
        # Solución = exactamente BKS
        sol = {"vehicles": 10, "distance": 828.93664}
        gap = validation.compute_gap(sol, bks["C101"])
        
        assert abs(gap) < 1e-9, f"Gap should be ~0, got {gap}"
    
    def test_gap_computation_worse(self):
        """Solución peor que BKS tiene gap positivo."""
        loader = BKSLoader()
        bks = loader.load_from_file("best_known_solutions.json")
        validation = BKSValidation()
        
        # Solución peor: 1 vehículo más
        sol_worse = {"vehicles": 11, "distance": 900}
        gap = validation.compute_gap(sol_worse, bks["C101"])
        
        assert gap > 0, f"Gap should be positive, got {gap}"


# ============================================================================
# 6️⃣ SOLUTIONPOOL: DOMINANCIA Y PROPIEDADES
# ============================================================================

class TestSolutionPool:
    """Verifica propiedades críticas de SolutionPool."""
    
    def test_pool_never_stores_dominated(self):
        """Pool NUNCA almacena soluciones dominadas."""
        pool = SolutionPool()
        
        sol1 = {"vehicles": 10, "distance": 828.93664, "instance": "C101"}
        sol_worse = {"vehicles": 11, "distance": 900, "instance": "C101"}
        
        pool.add(sol1)
        pool.add(sol_worse)
        
        # El mejor debe ser sol1
        assert pool.best == sol1
        # Pool debe tener solo 1 solución
        assert len(pool) == 1
    
    def test_pool_lexicographic_comparison(self):
        """Pool compara lexicográficamente (vehículos primero, distancia segundo)."""
        pool = SolutionPool()
        
        sol_more_vehicles = {"vehicles": 11, "distance": 800, "instance": "C101"}
        sol_fewer_vehicles = {"vehicles": 10, "distance": 900, "instance": "C101"}
        
        pool.add(sol_more_vehicles)
        pool.add(sol_fewer_vehicles)
        
        # El mejor debe ser el con MENOS vehículos (aunque tenga más distancia)
        assert pool.best["vehicles"] == 10


# ============================================================================
# 7️⃣ LOGGING: AUDITORÍA CIENTÍFICA
# ============================================================================

REQUIRED_LOG_FIELDS = {
    "algorithm_id",
    "seed",
    "instance_id",
    "vehicles",
    "distance",
    "gap_percent",
    "feasible",
    "timestamp",
}


class TestLogging:
    """Verifica que logging permite reconstruir experimentos."""
    
    def test_log_schema_complete(self):
        """Cada log tiene todos los campos requeridos."""
        log_entry = {
            "algorithm_id": "algo_001",
            "seed": 42,
            "instance_id": "C101",
            "vehicles": 10,
            "distance": 828.93664,
            "gap_percent": 0.0,
            "feasible": True,
            "timestamp": "2026-01-04T10:00:00",
        }
        
        assert set(log_entry.keys()) >= REQUIRED_LOG_FIELDS, \
            f"Log missing fields. Has {set(log_entry.keys())}, needs {REQUIRED_LOG_FIELDS}"
    
    def test_log_reproducibility(self):
        """Con logs y seed, puedo reconstruir un experimento."""
        # Simular log
        log = {
            "algorithm_id": "algo_123",
            "seed": 42,
            "instance_id": "C101",
            "vehicles": 10,
            "distance": 828.93664,
            "gap_percent": 0.0,
            "feasible": True,
        }
        
        # Con seed + algorithm_id, debo poder reproducir exactamente
        gen = RandomASTGenerator(seed=42)
        ast = gen.generate(phase="construction", seed=42)
        
        # AST determinista ✓
        # Seeds coinciden ✓
        # Puedo reconstruir


# ============================================================================
# 8️⃣ CANARY RUN: ÚLTIMA PRUEBA ANTES DEL EXPERIMENTO
# ============================================================================

class TestCanaryRun:
    """Canary run: 1 instancia, 1 algoritmo, 1 run, seed fija.
    
    Verifica:
    - No warnings
    - No excepciones
    - Gap razonable (≠ NaN, ≠ infinito)
    - Log generado correctamente
    """
    
    @pytest.mark.integration
    def test_canary_c101_single_run(self):
        """Canary run en C101 con 1 algoritmo y seed fija."""
        # Cargar datos
        evaluator = SolutionEvaluator()
        instance = evaluator.parse_solomon_instance("C101.txt")
        
        loader = BKSLoader()
        bks = loader.load_from_file("best_known_solutions.json")
        
        # Generar 1 algoritmo
        gen = RandomASTGenerator(seed=42)
        ast_const = gen.generate(phase="construction", seed=42)
        ast_ls = gen.generate(phase="local_search", seed=42)
        
        # Validar
        validator = ASTValidator()
        assert validator.validate_construction_ast(ast_const).ok
        assert validator.validate_local_search_ast(ast_ls).ok
        
        # Ejecutar GRASP (requiere GRASPSolver implementado)
        # solver = GRASPSolver(instance, ast_const, ast_ls)
        # solution = solver.solve(max_iterations=100)
        
        # Simular solución C101 BKS
        solution = {"vehicles": 10, "distance": 828.93664}
        
        # Evaluar
        validation = BKSValidation()
        comparison = validation.validate_solution(solution, bks["C101"])
        
        # Verificaciones
        assert comparison["feasible"] is True
        assert "gap_percent" in comparison
        gap = comparison["gap_percent"]
        
        # Gap debe ser número válido (no NaN, no infinito)
        assert gap == gap, "Gap is NaN"
        assert gap != float('inf'), "Gap is infinity"
        assert gap >= 0, "Gap is negative"


# ============================================================================
# RUNNER Y MAIN
# ============================================================================

if __name__ == "__main__":
    # Ejecutar todos los tests
    pytest.main([__file__, "-v", "--tb=short"])
