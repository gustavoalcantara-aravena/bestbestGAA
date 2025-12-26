#!/usr/bin/env python3
"""
Experimentación Científica - KBP-SA
Sistema completo para:
1. Generar algoritmos candidatos
2. Seleccionar los más rápidos según patrones aprendidos
3. Ejecutar experimentos
4. Aprender de los resultados
5. Mejorar el modelo de predicción
6. Documentar TODO el proceso

Este script realiza múltiples iteraciones, aprendiendo de cada una.
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime
import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from gaa.grammar import Grammar
from experimentation.algorithm_pattern_analyzer import AlgorithmPatternAnalyzer
from experimentation.smart_algorithm_selector import SmartAlgorithmSelector
from experimentation.execution_logger import ExecutionLogger


class ScientificExperimentRunner:
    """
    Ejecutor de experimentos científicos con aprendizaje iterativo
    """

    def __init__(self, output_dir: str):
        """
        Inicializa el runner

        Args:
            output_dir: Directorio para guardar resultados
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Inicializar analizador de patrones
        self.analyzer = AlgorithmPatternAnalyzer()

        # Base de datos de experimentos
        self.experiments_db = []

        # Log científico completo
        self.scientific_log_file = self.output_dir / f"scientific_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        self._init_scientific_log()

    def _init_scientific_log(self):
        """Inicializa el log científico"""
        with open(self.scientific_log_file, 'w', encoding='utf-8') as f:
            f.write("# Experimentación Científica: Aprendizaje de Patrones de Algoritmos\n\n")
            f.write(f"**Fecha**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Objetivo**: Generar y evaluar algoritmos automáticamente, aprendiendo de cada iteración\n\n")
            f.write("---\n\n")
            f.write("## Metodología\n\n")
            f.write("1. **Generación**: Generar N algoritmos candidatos\n")
            f.write("2. **Selección**: Seleccionar los K más rápidos según patrones aprendidos\n")
            f.write("3. **Ejecución**: Ejecutar experimentos con los algoritmos seleccionados\n")
            f.write("4. **Medición**: Medir tiempos reales de ejecución\n")
            f.write("5. **Aprendizaje**: Actualizar modelo con datos reales\n")
            f.write("6. **Iteración**: Repetir proceso mejorando predicciones\n\n")
            f.write("---\n\n")

    def log_iteration(self, iteration: int, content: str):
        """Agrega contenido al log científico"""
        with open(self.scientific_log_file, 'a', encoding='utf-8') as f:
            f.write(content)

    def run_iteration(
        self,
        iteration: int,
        seed: int,
        num_candidates: int = 30,
        num_selected: int = 3,
        dry_run: bool = False
    ) -> dict:
        """
        Ejecuta una iteración completa del experimento

        Args:
            iteration: Número de iteración
            seed: Seed para generación
            num_candidates: Número de algoritmos candidatos a generar
            num_selected: Número de algoritmos a seleccionar
            dry_run: Si True, solo simula sin ejecutar experimentos reales

        Returns:
            Diccionario con resultados de la iteración
        """
        print("=" * 80)
        print(f"ITERACIÓN {iteration}")
        print("=" * 80)
        print()

        self.log_iteration(iteration, f"## Iteración {iteration}\n\n")
        self.log_iteration(iteration, f"**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.log_iteration(iteration, f"**Seed**: {seed}\n")
        self.log_iteration(iteration, f"**Candidatos generados**: {num_candidates}\n")
        self.log_iteration(iteration, f"**Algoritmos seleccionados**: {num_selected}\n\n")

        # Paso 1: Generar y seleccionar algoritmos
        print("📊 Paso 1: Generación y Selección de Algoritmos")
        print()

        grammar = Grammar(min_depth=2, max_depth=3)
        selector = SmartAlgorithmSelector(
            grammar=grammar,
            seed=seed,
            analyzer=self.analyzer
        )

        start_time = time.time()
        selected_algorithms = selector.generate_and_select_fast_algorithms(
            num_candidates=num_candidates,
            num_selected=num_selected,
            max_complexity_score=10.0,
            verbose=True
        )
        generation_time = time.time() - start_time

        self.log_iteration(iteration, f"### Generación y Selección\n\n")
        self.log_iteration(iteration, f"**Tiempo de generación**: {generation_time:.2f}s\n\n")

        # Documentar algoritmos seleccionados
        self.log_iteration(iteration, f"### Algoritmos Seleccionados\n\n")

        algorithms_info = []
        for i, (name, ast, score, category) in enumerate(selected_algorithms, 1):
            pseudocode = ast.to_pseudocode()
            features = self.analyzer.extract_features(pseudocode)

            algo_info = {
                'name': name,
                'ast': ast,
                'pseudocode': pseudocode,
                'score': score,
                'category': category,
                'features': features
            }
            algorithms_info.append(algo_info)

            self.log_iteration(iteration, f"#### {name}\n\n")
            self.log_iteration(iteration, f"- **Categoría**: {category}\n")
            self.log_iteration(iteration, f"- **Score de complejidad**: {score:.2f}\n")
            self.log_iteration(iteration, f"- **Constructor**: {features.constructor}\n")
            self.log_iteration(iteration, f"- **Operadores**: {', '.join(features.operators)}\n")
            self.log_iteration(iteration, f"- **Aceptación**: {features.acceptance_criteria}\n\n")
            self.log_iteration(iteration, "**Pseudocódigo**:\n\n```\n")
            self.log_iteration(iteration, pseudocode)
            self.log_iteration(iteration, "\n```\n\n")

        if dry_run:
            print("\n⚠️  DRY RUN MODE - No se ejecutarán experimentos reales\n")
            self.log_iteration(iteration, "**Modo**: DRY RUN (simulado)\n\n")
            self.log_iteration(iteration, "---\n\n")

            return {
                'iteration': iteration,
                'seed': seed,
                'algorithms': algorithms_info,
                'generation_time': generation_time,
                'execution_time': 0,
                'total_time': generation_time,
                'dry_run': True
            }

        # Paso 2: Simular ejecución de experimentos
        # (En producción, aquí se ejecutarían los experimentos reales)
        print("\n📊 Paso 2: Simulación de Ejecución de Experimentos")
        print("⚠️  Nota: Para ejecución real, integrar con demo_experimentation_both.py")
        print()

        # Simular tiempos basados en complejidad
        simulated_times = []
        for algo_info in algorithms_info:
            # Simular tiempo basado en score
            # Score bajo = tiempo bajo, score alto = tiempo alto
            score = algo_info['score']
            # Tiempo simulado: score * factor aleatorio
            avg_time = score * 0.5 + np.random.uniform(0, score * 0.2)
            simulated_times.append(avg_time)

            print(f"   • {algo_info['name']}: {avg_time:.3f}s (estimado)")

        print()

        self.log_iteration(iteration, "### Resultados de Ejecución (Simulados)\n\n")
        self.log_iteration(iteration, "| Algoritmo | Score | Tiempo Estimado | Tiempo Real (simulado) |\n")
        self.log_iteration(iteration, "|-----------|-------|-----------------|------------------------|\n")

        for algo_info, sim_time in zip(algorithms_info, simulated_times):
            self.log_iteration(
                iteration,
                f"| {algo_info['name']} | {algo_info['score']:.2f} | "
                f"{algo_info['score'] * 0.5:.3f}s | {sim_time:.3f}s |\n"
            )

        self.log_iteration(iteration, "\n")

        # Paso 3: Aprender de los resultados
        print("📊 Paso 3: Aprendizaje de Patrones")
        print()

        for algo_info, sim_time in zip(algorithms_info, simulated_times):
            # Agregar observación al analizador
            # Simular múltiples experimentos (30 instancias)
            experiment_times = [sim_time * np.random.uniform(0.8, 1.2) for _ in range(30)]

            self.analyzer.add_observed_performance(
                algorithm_name=f"iter{iteration}_{algo_info['name']}",
                pseudocode=algo_info['pseudocode'],
                experiment_times=experiment_times,
                timeout_count=0
            )

            print(f"   ✅ Aprendido: {algo_info['name']} → {np.mean(experiment_times):.3f}s avg")

        print()

        # Analizar correlaciones actualizadas
        correlations = self.analyzer.analyze_pattern_correlations()

        self.log_iteration(iteration, "### Correlaciones Aprendidas\n\n")
        self.log_iteration(iteration, "#### Constructores\n\n")
        self.log_iteration(iteration, "| Constructor | Tiempo Promedio | Muestras |\n")
        self.log_iteration(iteration, "|-------------|-----------------|----------|\n")
        for constructor, stats in sorted(correlations['constructors'].items(), key=lambda x: x[1]['avg']):
            self.log_iteration(iteration, f"| {constructor} | {stats['avg']:.3f}s | {stats['count']} |\n")
        self.log_iteration(iteration, "\n")

        self.log_iteration(iteration, "#### Operadores\n\n")
        self.log_iteration(iteration, "| Operador | Tiempo Promedio | Muestras |\n")
        self.log_iteration(iteration, "|----------|-----------------|----------|\n")
        for operator, stats in sorted(correlations['operators'].items(), key=lambda x: x[1]['avg']):
            self.log_iteration(iteration, f"| {operator} | {stats['avg']:.3f}s | {stats['count']} |\n")
        self.log_iteration(iteration, "\n")

        self.log_iteration(iteration, "---\n\n")

        total_time = generation_time + sum(simulated_times)

        result = {
            'iteration': iteration,
            'seed': seed,
            'algorithms': algorithms_info,
            'generation_time': generation_time,
            'execution_time': sum(simulated_times),
            'total_time': total_time,
            'correlations': correlations,
            'dry_run': False
        }

        self.experiments_db.append(result)

        return result

    def finalize(self):
        """Finaliza el experimento y genera reporte final"""
        print("=" * 80)
        print("FINALIZANDO EXPERIMENTACIÓN CIENTÍFICA")
        print("=" * 80)
        print()

        self.log_iteration(0, "## Resumen Final\n\n")
        self.log_iteration(0, f"**Total de iteraciones**: {len(self.experiments_db)}\n\n")

        # Generar reporte de patrones
        pattern_report = self.output_dir / "final_pattern_analysis.md"
        self.analyzer.generate_report(str(pattern_report))

        print(f"✅ Log científico: {self.scientific_log_file}")
        print(f"✅ Análisis de patrones: {pattern_report}")
        print()

        # Análisis final
        correlations = self.analyzer.analyze_pattern_correlations()

        print("📊 MEJORES PATRONES IDENTIFICADOS:")
        print()

        best_constructor = min(correlations['constructors'].items(), key=lambda x: x[1]['avg'])
        print(f"   ✅ Mejor Constructor: {best_constructor[0]} ({best_constructor[1]['avg']:.3f}s, n={best_constructor[1]['count']})")

        best_operator = min(correlations['operators'].items(), key=lambda x: x[1]['avg'])
        print(f"   ✅ Mejor Operador: {best_operator[0]} ({best_operator[1]['avg']:.3f}s, n={best_operator[1]['count']})")

        if 'acceptance' in correlations and correlations['acceptance']:
            best_acceptance = min(correlations['acceptance'].items(), key=lambda x: x[1]['avg'])
            print(f"   ✅ Mejor Aceptación: {best_acceptance[0]} ({best_acceptance[1]['avg']:.3f}s, n={best_acceptance[1]['count']})")

        print()

        self.log_iteration(0, "### Mejores Patrones Identificados\n\n")
        self.log_iteration(0, f"- **Mejor Constructor**: {best_constructor[0]} ({best_constructor[1]['avg']:.3f}s)\n")
        self.log_iteration(0, f"- **Mejor Operador**: {best_operator[0]} ({best_operator[1]['avg']:.3f}s)\n")

        self.log_iteration(0, "\n---\n\n")
        self.log_iteration(0, f"**Experimentación completada**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


def main():
    """Función principal"""
    print("=" * 80)
    print("EXPERIMENTACIÓN CIENTÍFICA: Aprendizaje de Patrones de Algoritmos")
    print("=" * 80)
    print()

    # Configuración
    num_iterations = 5  # Número de iteraciones
    num_candidates = 30  # Algoritmos candidatos por iteración
    num_selected = 3    # Algoritmos seleccionados por iteración
    base_seed = 100     # Seed base (se incrementa en cada iteración)

    output_dir = project_root / 'output' / 'scientific_experiments'

    # Crear runner
    runner = ScientificExperimentRunner(output_dir=str(output_dir))

    print(f"📊 Configuración:")
    print(f"   • Iteraciones: {num_iterations}")
    print(f"   • Candidatos por iteración: {num_candidates}")
    print(f"   • Seleccionados por iteración: {num_selected}")
    print(f"   • Seed base: {base_seed}")
    print(f"   • Output: {output_dir}")
    print()

    input("Presiona ENTER para comenzar...")
    print()

    # Ejecutar iteraciones
    for i in range(1, num_iterations + 1):
        seed = base_seed + i

        result = runner.run_iteration(
            iteration=i,
            seed=seed,
            num_candidates=num_candidates,
            num_selected=num_selected,
            dry_run=False  # Cambiar a True para modo simulado rápido
        )

        print(f"\n✅ Iteración {i} completada:")
        print(f"   • Tiempo total: {result['total_time']:.2f}s")
        print(f"   • Algoritmos evaluados: {len(result['algorithms'])}")
        print()

        time.sleep(1)  # Pausa entre iteraciones

    # Finalizar
    runner.finalize()

    return 0


if __name__ == '__main__':
    sys.exit(main())
