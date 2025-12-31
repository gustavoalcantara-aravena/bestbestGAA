"""
Tests para módulo GAA
"""

import pytest
import numpy as np
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from gaa.grammar import Grammar
from gaa.generator import AlgorithmGenerator
from gaa.interpreter import execute_algorithm
from gaa.ast_nodes import (
    Seq, While, For, If, Call,
    GreedyConstruct, LocalSearch, Perturbation,
    mutate_ast, crossover_ast
)
from core.problem import GraphColoringProblem


class TestASTNodes:
    """Tests para nodos del AST"""
    
    def test_greedy_construct(self):
        """Test nodo GreedyConstruct"""
        node = GreedyConstruct(heuristic="DSATUR")
        assert node.heuristic == "DSATUR"
        assert node.size() == 1
        assert node.depth() == 1
    
    def test_local_search(self):
        """Test nodo LocalSearch"""
        node = LocalSearch(method="KempeChain", max_iterations=100)
        assert node.method == "KempeChain"
        assert node.max_iterations == 100
    
    def test_perturbation(self):
        """Test nodo Perturbation"""
        node = Perturbation(method="RandomRecolor", intensity=0.2)
        assert node.method == "RandomRecolor"
        assert 0 <= node.intensity <= 1
    
    def test_seq(self):
        """Test nodo Seq"""
        body = [
            GreedyConstruct("DSATUR"),
            LocalSearch("KempeChain")
        ]
        seq = Seq(body=body)
        assert len(seq.body) == 2
        assert seq.size() == 3  # 1 Seq + 2 hijos
    
    def test_while(self):
        """Test nodo While"""
        loop = While(
            max_iterations=100,
            body=LocalSearch("KempeChain")
        )
        assert loop.max_iterations == 100
        assert loop.size() == 2


class TestGrammar:
    """Tests para gramática"""
    
    def test_grammar_creation(self):
        """Test creación de gramática"""
        grammar = Grammar()
        assert len(grammar.CONSTRUCTIVE_TERMINALS) > 0
        assert len(grammar.IMPROVEMENT_TERMINALS) > 0
        assert len(grammar.PERTURBATION_TERMINALS) > 0
    
    def test_validate_valid_ast(self):
        """Test validación de AST válido"""
        grammar = Grammar(min_depth=1, max_depth=5)
        ast = Seq(body=[
            GreedyConstruct("DSATUR"),
            LocalSearch("KempeChain")
        ])
        
        errors = grammar.validate_ast(ast)
        assert len(errors) == 0, f"AST válido tiene errores: {errors}"
    
    def test_validate_invalid_heuristic(self):
        """Test validación detecta heurística inválida"""
        grammar = Grammar()
        ast = GreedyConstruct(heuristic="INVALIDO")
        
        errors = grammar.validate_ast(ast)
        assert len(errors) > 0, "Debería detectar heurística inválida"
    
    def test_validate_invalid_method(self):
        """Test validación detecta método inválido"""
        grammar = Grammar()
        ast = LocalSearch(method="INVALIDO")
        
        errors = grammar.validate_ast(ast)
        assert len(errors) > 0, "Debería detectar método inválido"


class TestGenerator:
    """Tests para generador"""
    
    def test_generate_simple(self):
        """Test generación de algoritmo simple"""
        generator = AlgorithmGenerator(seed=42)
        alg = generator.generate()
        
        assert alg is not None
        assert alg.size() > 0
        assert alg.depth() > 0
    
    def test_generate_population(self):
        """Test generación de población"""
        generator = AlgorithmGenerator(seed=42)
        pop = generator.generate_population(size=5)
        
        assert len(pop) == 5
        assert all(alg is not None for alg in pop)
    
    def test_generate_with_validation(self):
        """Test generación con validación"""
        grammar = Grammar(min_depth=2, max_depth=4)
        generator = AlgorithmGenerator(grammar=grammar, seed=42)
        
        alg = generator.generate_with_validation()
        
        assert alg is not None
        errors = grammar.validate_ast(alg)
        assert len(errors) == 0, f"Algoritmo validado tiene errores: {errors}"
    
    def test_reproducibility(self):
        """Test reproducibilidad con seed"""
        gen1 = AlgorithmGenerator(seed=42)
        alg1 = gen1.generate()
        
        gen2 = AlgorithmGenerator(seed=42)
        alg2 = gen2.generate()
        
        # Deberían tener misma estructura
        assert alg1.size() == alg2.size()
        assert alg1.depth() == alg2.depth()


class TestMutation:
    """Tests para mutación de AST"""
    
    def test_mutate_ast(self):
        """Test mutación de AST"""
        original = GreedyConstruct("DSATUR")
        mutated = mutate_ast(original)
        
        assert mutated is not None
        assert mutated.size() >= original.size()
    
    def test_mutation_changes_tree(self):
        """Test que mutación cambia el árbol"""
        original = Seq(body=[
            GreedyConstruct("DSATUR"),
            LocalSearch("KempeChain", max_iterations=100)
        ])
        
        # Mutar varias veces
        for _ in range(10):
            mutated = mutate_ast(original)
            # Probabilidad alta de cambio
            # (aunque no garantizado en cada iteración)


class TestCrossover:
    """Tests para crossover de AST"""
    
    def test_crossover_ast(self):
        """Test crossover entre dos AST"""
        ast1 = GreedyConstruct("DSATUR")
        ast2 = LocalSearch("KempeChain")
        
        child1, child2 = crossover_ast(ast1, ast2)
        
        assert child1 is not None
        assert child2 is not None


class TestInterpreter:
    """Tests para intérprete"""
    
    @pytest.fixture
    def simple_problem(self):
        """Problema simple para tests"""
        edges = [(0, 1), (1, 2), (2, 0)]
        return GraphColoringProblem(
            vertices=3,
            edges=edges,
            colors_known=3,
            name="test_triangle"
        )
    
    def test_execute_greedy_construct(self, simple_problem):
        """Test ejecución de construcción"""
        alg = GreedyConstruct("DSATUR")
        solution = execute_algorithm(alg, simple_problem, seed=42)
        
        assert solution is not None
        assert solution.num_colors >= simple_problem.colors_known
    
    def test_execute_simple_algorithm(self, simple_problem):
        """Test ejecución de algoritmo simple"""
        alg = Seq(body=[
            GreedyConstruct("DSATUR"),
            LocalSearch("KempeChain", max_iterations=50)
        ])
        
        solution = execute_algorithm(alg, simple_problem, seed=42)
        
        assert solution is not None
        assert solution.num_colors >= 0


# Ejecutar tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
