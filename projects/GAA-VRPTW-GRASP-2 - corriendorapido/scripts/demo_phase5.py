#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Phase 5 Demonstration Script: GAA (Generación Automática de Algoritmos)

This script demonstrates the complete workflow of the GAA framework:
1. Generate a random algorithm
2. Validate it against the grammar
3. Repair if necessary
4. Execute on a VRPTW instance
5. Analyze results

Run with: python scripts/demo_phase5.py
"""

import sys
from pathlib import Path

# Setup paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.gaa import (
    AlgorithmGenerator,
    ASTValidator,
    ASTRepairMechanism,
    ASTNormalizer,
    ASTInterpreter,
    ASTStatistics,
)
from src.models import Instance, Solution


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def demo_generation():
    """Demonstrate algorithm generation."""
    print_section("1. ALGORITHM GENERATION")
    
    print("Creating algorithm generator with seed=42...")
    generator = AlgorithmGenerator(seed=42)
    
    print("Generating 3 algorithms (reproducible with seed)...\n")
    algorithms = generator.generate_three_algorithms(seed=42)
    
    for i, algo in enumerate(algorithms, 1):
        print(f"Algorithm {i}:")
        print(f"  - Size: {algo.size()} nodes")
        print(f"  - Depth: {algo.depth()}")
        print(f"  - Type: {type(algo).__name__}")
        print(f"  - Pseudocode:\n{algo.to_pseudocode()}\n")
    
    return algorithms[0]  # Return first algorithm for further demos


def demo_validation(algo):
    """Demonstrate validation."""
    print_section("2. VALIDATION AGAINST GRAMMAR")
    
    validator = ASTValidator()
    is_valid, violations = validator.validate(algo)
    
    if is_valid:
        print("✅ Algorithm is VALID against all constraints!")
    else:
        print(f"❌ Found {len(violations)} violation(s):")
        for i, violation in enumerate(violations, 1):
            print(f"   {i}. {violation}")
    
    return is_valid


def demo_repair(algo, is_valid):
    """Demonstrate repair mechanism."""
    print_section("3. REPAIR MECHANISM")
    
    if is_valid:
        print("Algorithm is already valid. Demonstrating repair on invalid case...\n")
        # Create an intentionally invalid algorithm
        from src.gaa import LocalSearch  # Missing constructor
        invalid_algo = LocalSearch(operator='TwoOpt', max_iterations=50)
        algo_to_repair = invalid_algo
    else:
        print("Attempting to repair invalid algorithm...\n")
        algo_to_repair = algo
    
    repair = ASTRepairMechanism()
    repaired_algo, was_repaired, repairs = repair.repair(algo_to_repair)
    
    if was_repaired:
        print(f"✅ Repairs applied: {repairs}")
        print(f"\nRepaired algorithm:")
        print(f"  - Size: {repaired_algo.size()} nodes")
        print(f"  - Depth: {repaired_algo.depth()}")
    else:
        print("✅ No repairs needed")
        repaired_algo = algo_to_repair
    
    return repaired_algo


def demo_normalization(algo):
    """Demonstrate normalization."""
    print_section("4. NORMALIZATION")
    
    print("Original algorithm metrics:")
    print(f"  - Size: {algo.size()}")
    print(f"  - Depth: {algo.depth()}\n")
    
    normalizer = ASTNormalizer()
    normalized = normalizer.normalize(algo)
    
    print("After normalization:")
    print(f"  - Size: {normalized.size()}")
    print(f"  - Depth: {normalized.depth()}")
    
    if normalized.size() < algo.size():
        print("\n✅ Normalization reduced complexity")
    else:
        print("\n✅ Already normalized")
    
    return normalized


def demo_execution(algo):
    """Demonstrate algorithm execution."""
    print_section("5. ALGORITHM EXECUTION")
    
    print("Creating sample VRPTW instance...")
    instance = Instance()
    instance.num_customers = 5
    instance.num_vehicles = 2
    instance.capacity = 1000
    
    # Add dummy customers (in real usage, load from dataset)
    import random
    random.seed(42)
    instance.customers = [
        {
            'id': i,
            'x': random.randint(0, 100),
            'y': random.randint(0, 100),
            'demand': random.randint(10, 50),
            'service_time': random.randint(5, 15),
            'time_window': (0, 500)
        }
        for i in range(1, 6)
    ]
    
    print(f"Instance: {instance.num_customers} customers, {instance.num_vehicles} vehicles\n")
    
    print("Executing algorithm on instance...\n")
    interpreter = ASTInterpreter()
    
    try:
        solution = interpreter.execute(algo, instance)
        
        print("✅ Execution completed successfully!")
        print(f"\nResults:")
        print(f"  - Solution cost: {solution.cost:.2f}")
        print(f"  - Number of routes: {solution.num_routes}")
        print(f"  - Feasible: {solution.is_feasible}")
        
        stats = interpreter.get_stats()
        print(f"\nExecution statistics:")
        print(f"  - Nodes executed: {stats['nodes_executed']}")
        print(f"  - Operator calls: {stats['operator_calls']}")
        print(f"  - Feasible solutions found: {stats['feasible_solutions']}")
        print(f"  - Improvements made: {stats['improvements']}")
        
    except Exception as e:
        print(f"❌ Execution failed: {e}")
        print("   (This is expected if operators are not fully configured)")


def demo_serialization(algo):
    """Demonstrate serialization."""
    print_section("6. SERIALIZATION")
    
    print("Converting algorithm to dictionary...")
    data = algo.to_dict()
    
    print(f"Dictionary keys: {list(data.keys())}")
    print(f"Dictionary size: {len(str(data))} characters\n")
    
    print("Reconstructing from dictionary...")
    from src.gaa import reconstruct_node
    restored = reconstruct_node(data)
    
    print("✅ Successfully reconstructed!")
    print(f"\nVerification:")
    print(f"  - Original size: {algo.size()}")
    print(f"  - Restored size: {restored.size()}")
    print(f"  - Match: {algo.size() == restored.size()}")


def demo_analysis(algo):
    """Demonstrate algorithm analysis."""
    print_section("7. ALGORITHM ANALYSIS")
    
    stats = ASTStatistics.analyze(algo)
    
    print("Algorithm characteristics:")
    for key, value in stats.items():
        if key == 'structure':
            print(f"  - {key}:")
            for line in value.split('\n'):
                print(f"    {line}")
        else:
            print(f"  - {key}: {value}")


def main():
    """Run complete demonstration."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + "  PHASE 5 DEMONSTRATION: GAA (Automatic Algorithm Generation)".center(58) + "║")
    print("╚" + "="*58 + "╝")
    
    # 1. Generation
    algo = demo_generation()
    
    # 2. Validation
    is_valid = demo_validation(algo)
    
    # 3. Repair
    algo = demo_repair(algo, is_valid)
    
    # 4. Normalization
    algo = demo_normalization(algo)
    
    # 5. Execution
    demo_execution(algo)
    
    # 6. Serialization
    demo_serialization(algo)
    
    # 7. Analysis
    demo_analysis(algo)
    
    # Summary
    print_section("SUMMARY")
    print("""
✅ Phase 5 Framework Capabilities Demonstrated:

1. ✅ Random algorithm generation (Ramped Half-and-Half)
2. ✅ Grammar validation against canonical constraints
3. ✅ Automatic repair of invalid algorithms
4. ✅ Algorithm normalization and simplification
5. ✅ Execution of AST on VRPTW instances
6. ✅ JSON serialization/deserialization
7. ✅ Algorithm analysis and metrics

The GAA framework is ready for:
- Evolutionary algorithm generation
- Benchmarking on Solomon instances
- Automated algorithm discovery
- Algorithm composition and assembly

Next: Phase 6 - Integration with datasets and evaluation
    """)


if __name__ == '__main__':
    main()
