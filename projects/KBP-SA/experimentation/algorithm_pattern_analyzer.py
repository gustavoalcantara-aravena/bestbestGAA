"""
Algorithm Pattern Analyzer - KBP-SA
Sistema para aprender y predecir qué patrones de algoritmos generan ejecuciones más rápidas
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
import numpy as np


@dataclass
class AlgorithmFeatures:
    """Características extraídas de un algoritmo"""
    constructor: str  # GreedyByRatio, GreedyByWeight, GreedyByValue, RandomConstruct
    operators: List[str]  # FlipWorstItem, FlipBestItem, TwoExchange, OneExchange
    acceptance_criteria: Optional[str]  # Metropolis, Improving, None
    has_loop: bool  # Si tiene MIENTRAS o APLICAR_HASTA_NO_MEJORAR
    loop_budget: Optional[int]  # Número de iteraciones si tiene MIENTRAS
    stagnation_limit: Optional[int]  # Límite de estancamiento si tiene APLICAR_HASTA_NO_MEJORAR
    complexity_score: float  # Score estimado de complejidad


@dataclass
class AlgorithmPerformance:
    """Datos de rendimiento de un algoritmo"""
    algorithm_name: str
    features: AlgorithmFeatures
    avg_time_per_experiment: float
    max_time_per_experiment: float
    min_time_per_experiment: float
    timeout_count: int
    total_experiments: int


class AlgorithmPatternAnalyzer:
    """
    Analizador de patrones para identificar características que llevan a ejecuciones rápidas
    """

    def __init__(self):
        """Inicializa el analizador con conocimiento base"""

        # Conocimiento base de complejidad relativa (basado en evidencia empírica)
        self.operator_complexity = {
            'FlipWorstItem': 1.0,  # O(n) - simple flip
            'FlipBestItem': 1.0,   # O(n) - simple flip
            'OneExchange': 2.0,    # O(n) - swap simple
            'TwoExchange': 3.0,    # O(n²) - más complejo pero efectivo
        }

        self.constructor_speed = {
            'RandomConstruct': 1.0,      # O(n) - más rápido
            'GreedyByWeight': 2.0,       # O(n log n) - sorting
            'GreedyByValue': 2.0,        # O(n log n) - sorting
            'GreedyByRatio': 2.5,        # O(n log n) - sorting + ratio calculation
        }

        self.acceptance_overhead = {
            'Improving': 1.0,      # Solo acepta mejoras - rápido
            'Metropolis': 3.0,     # Acepta peores - más evaluaciones
            None: 1.0              # Sin criterio de aceptación
        }

        # Base de datos de patrones observados
        self.pattern_database: List[AlgorithmPerformance] = []

    def extract_features(self, pseudocode: str) -> AlgorithmFeatures:
        """
        Extrae características de un algoritmo a partir de su pseudocódigo

        Args:
            pseudocode: Pseudocódigo completo del algoritmo

        Returns:
            AlgorithmFeatures con todas las características extraídas
        """
        # Extraer constructor
        constructor_match = re.search(r'CONSTRUIR_VORAZ usando (\w+)', pseudocode)
        constructor = constructor_match.group(1) if constructor_match else 'Unknown'

        # Extraer operadores
        operators = []
        operator_patterns = [
            r'LLAMAR (\w+)',
            r'BUSQUEDA_LOCAL en (\w+)',
        ]
        for pattern in operator_patterns:
            matches = re.findall(pattern, pseudocode)
            operators.extend(matches)

        # Eliminar duplicados manteniendo orden
        operators = list(dict.fromkeys(operators))

        # Extraer criterio de aceptación
        acceptance = None
        acceptance_match = re.search(r'aceptación: (\w+)', pseudocode)
        if acceptance_match:
            acceptance = acceptance_match.group(1)

        # Detectar loops
        has_loop = 'MIENTRAS' in pseudocode or 'APLICAR_HASTA_NO_MEJORAR' in pseudocode

        # Extraer presupuesto de iteraciones
        loop_budget = None
        budget_match = re.search(r'presupuesto: (\d+) iteraciones', pseudocode)
        if budget_match:
            loop_budget = int(budget_match.group(1))

        # Extraer límite de estancamiento
        stagnation_limit = None
        stagnation_match = re.search(r'Stagnation=(\d+)', pseudocode)
        if stagnation_match:
            stagnation_limit = int(stagnation_match.group(1))

        # Calcular score de complejidad
        complexity_score = self._calculate_complexity_score(
            constructor, operators, acceptance, loop_budget, stagnation_limit
        )

        return AlgorithmFeatures(
            constructor=constructor,
            operators=operators,
            acceptance_criteria=acceptance,
            has_loop=has_loop,
            loop_budget=loop_budget,
            stagnation_limit=stagnation_limit,
            complexity_score=complexity_score
        )

    def _calculate_complexity_score(
        self,
        constructor: str,
        operators: List[str],
        acceptance: Optional[str],
        loop_budget: Optional[int],
        stagnation_limit: Optional[int]
    ) -> float:
        """
        Calcula un score de complejidad estimada del algoritmo

        Score más alto = más lento esperado
        Score más bajo = más rápido esperado
        """
        score = 0.0

        # Constructor base
        score += self.constructor_speed.get(constructor, 2.0)

        # Operadores (suma de complejidades)
        for op in operators:
            score += self.operator_complexity.get(op, 2.0)

        # Criterio de aceptación
        score *= self.acceptance_overhead.get(acceptance, 1.0)

        # Presupuesto de iteraciones
        if loop_budget:
            score *= (1 + loop_budget / 1000)  # Más iteraciones = más lento

        if stagnation_limit:
            score *= (1 + stagnation_limit / 100)  # Más estancamiento = más lento

        return score

    def add_observed_performance(
        self,
        algorithm_name: str,
        pseudocode: str,
        experiment_times: List[float],
        timeout_count: int = 0
    ):
        """
        Agrega datos de rendimiento observado a la base de datos

        Args:
            algorithm_name: Nombre del algoritmo
            pseudocode: Pseudocódigo completo
            experiment_times: Lista de tiempos de experimentos (en segundos)
            timeout_count: Número de experimentos que hicieron timeout
        """
        features = self.extract_features(pseudocode)

        # Filtrar timeouts (asumiendo que son >60s)
        valid_times = [t for t in experiment_times if t < 60]

        if not valid_times:
            # Todos fueron timeouts, usar tiempo estimado alto
            avg_time = 60.0
            max_time = 60.0
            min_time = 60.0
        else:
            avg_time = np.mean(valid_times)
            max_time = np.max(valid_times)
            min_time = np.min(valid_times)

        performance = AlgorithmPerformance(
            algorithm_name=algorithm_name,
            features=features,
            avg_time_per_experiment=avg_time,
            max_time_per_experiment=max_time,
            min_time_per_experiment=min_time,
            timeout_count=timeout_count,
            total_experiments=len(experiment_times)
        )

        self.pattern_database.append(performance)

    def predict_speed_category(self, pseudocode: str) -> Tuple[str, float, Dict]:
        """
        Predice la categoría de velocidad de un algoritmo

        Args:
            pseudocode: Pseudocódigo del algoritmo

        Returns:
            Tuple de (categoría, score, detalles)
            - categoría: 'RÁPIDO', 'MEDIO', 'LENTO'
            - score: Score de complejidad (menor = más rápido)
            - detalles: Diccionario con detalles del análisis
        """
        features = self.extract_features(pseudocode)
        score = features.complexity_score

        # Categorizar basado en score
        if score < 10:
            category = 'RÁPIDO'
        elif score < 30:
            category = 'MEDIO'
        else:
            category = 'LENTO'

        # Generar detalles
        details = {
            'constructor': features.constructor,
            'operators': features.operators,
            'acceptance': features.acceptance_criteria,
            'loop_budget': features.loop_budget,
            'stagnation_limit': features.stagnation_limit,
            'complexity_score': score,
            'estimated_time_per_experiment': self._estimate_time(score)
        }

        return category, score, details

    def _estimate_time(self, complexity_score: float) -> str:
        """Estima tiempo basado en score de complejidad"""
        if complexity_score < 10:
            return '0.1-2s'
        elif complexity_score < 20:
            return '2-10s'
        elif complexity_score < 30:
            return '10-30s'
        else:
            return '>30s (posible timeout)'

    def rank_algorithms(self, algorithms: List[Tuple[str, str]]) -> List[Tuple[str, str, float, str]]:
        """
        Rankea algoritmos por velocidad esperada

        Args:
            algorithms: Lista de tuplas (nombre, pseudocode)

        Returns:
            Lista ordenada de tuplas (nombre, pseudocode, score, categoría)
            Ordenado de más rápido a más lento
        """
        ranked = []

        for name, pseudocode in algorithms:
            category, score, _ = self.predict_speed_category(pseudocode)
            ranked.append((name, pseudocode, score, category))

        # Ordenar por score (menor = más rápido)
        ranked.sort(key=lambda x: x[2])

        return ranked

    def filter_fast_algorithms(
        self,
        algorithms: List[Tuple[str, str]],
        max_complexity_score: float = 15.0
    ) -> List[Tuple[str, str]]:
        """
        Filtra algoritmos para quedarse solo con los rápidos

        Args:
            algorithms: Lista de tuplas (nombre, pseudocode)
            max_complexity_score: Score máximo de complejidad permitido

        Returns:
            Lista filtrada de algoritmos rápidos
        """
        fast_algorithms = []

        for name, pseudocode in algorithms:
            _, score, _ = self.predict_speed_category(pseudocode)
            if score <= max_complexity_score:
                fast_algorithms.append((name, pseudocode))

        return fast_algorithms

    def analyze_pattern_correlations(self) -> Dict:
        """
        Analiza correlaciones entre características y tiempos de ejecución

        Returns:
            Diccionario con estadísticas de correlaciones
        """
        if not self.pattern_database:
            return {'error': 'No hay datos en la base de patrones'}

        # Agrupar por características
        by_constructor = {}
        by_operator = {}
        by_acceptance = {}

        for perf in self.pattern_database:
            # Por constructor
            if perf.features.constructor not in by_constructor:
                by_constructor[perf.features.constructor] = []
            by_constructor[perf.features.constructor].append(perf.avg_time_per_experiment)

            # Por operador
            for op in perf.features.operators:
                if op not in by_operator:
                    by_operator[op] = []
                by_operator[op].append(perf.avg_time_per_experiment)

            # Por criterio de aceptación
            acc = perf.features.acceptance_criteria or 'None'
            if acc not in by_acceptance:
                by_acceptance[acc] = []
            by_acceptance[acc].append(perf.avg_time_per_experiment)

        # Calcular estadísticas
        stats = {
            'constructors': {k: {'avg': np.mean(v), 'std': np.std(v), 'count': len(v)}
                           for k, v in by_constructor.items()},
            'operators': {k: {'avg': np.mean(v), 'std': np.std(v), 'count': len(v)}
                        for k, v in by_operator.items()},
            'acceptance': {k: {'avg': np.mean(v), 'std': np.std(v), 'count': len(v)}
                         for k, v in by_acceptance.items()},
        }

        return stats

    def generate_report(self, output_file: str):
        """
        Genera un reporte completo de análisis de patrones

        Args:
            output_file: Ruta del archivo markdown de salida
        """
        correlations = self.analyze_pattern_correlations()

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Análisis de Patrones de Algoritmos - KBP-SA\n\n")
            f.write(f"**Algoritmos analizados**: {len(self.pattern_database)}\n\n")
            f.write("---\n\n")

            # Verificar si hay datos
            if 'error' in correlations:
                f.write("## ⚠️ Sin Datos\n\n")
                f.write(f"{correlations['error']}\n\n")
                return

            # Constructores
            if 'constructors' in correlations and correlations['constructors']:
                f.write("## 📊 Rendimiento por Constructor\n\n")
                f.write("| Constructor | Tiempo Promedio | Desv. Estándar | Muestras |\n")
                f.write("|-------------|-----------------|----------------|----------|\n")
                for constructor, stats in sorted(correlations['constructors'].items(),
                                                key=lambda x: x[1]['avg']):
                    f.write(f"| {constructor} | {stats['avg']:.3f}s | {stats['std']:.3f}s | {stats['count']} |\n")
                f.write("\n")

            # Operadores
            if 'operators' in correlations and correlations['operators']:
                f.write("## 🔧 Rendimiento por Operador\n\n")
                f.write("| Operador | Tiempo Promedio | Desv. Estándar | Muestras |\n")
                f.write("|----------|-----------------|----------------|----------|\n")
                for operator, stats in sorted(correlations['operators'].items(),
                                             key=lambda x: x[1]['avg']):
                    f.write(f"| {operator} | {stats['avg']:.3f}s | {stats['std']:.3f}s | {stats['count']} |\n")
                f.write("\n")

            # Criterios de aceptación
            if 'acceptance' in correlations and correlations['acceptance']:
                f.write("## ✅ Rendimiento por Criterio de Aceptación\n\n")
                f.write("| Criterio | Tiempo Promedio | Desv. Estándar | Muestras |\n")
                f.write("|----------|-----------------|----------------|----------|\n")
                for acceptance, stats in sorted(correlations['acceptance'].items(),
                                               key=lambda x: x[1]['avg']):
                    f.write(f"| {acceptance} | {stats['avg']:.3f}s | {stats['std']:.3f}s | {stats['count']} |\n")
                f.write("\n")

            # Recomendaciones
            f.write("## 🎯 Recomendaciones para Algoritmos Rápidos\n\n")

            # Mejor constructor
            if 'constructors' in correlations and correlations['constructors']:
                best_constructor = min(correlations['constructors'].items(),
                                      key=lambda x: x[1]['avg'])
                f.write(f"- **Mejor Constructor**: {best_constructor[0]} ({best_constructor[1]['avg']:.3f}s)\n")

            # Mejor operador
            if 'operators' in correlations and correlations['operators']:
                best_operator = min(correlations['operators'].items(),
                                   key=lambda x: x[1]['avg'])
                f.write(f"- **Mejor Operador**: {best_operator[0]} ({best_operator[1]['avg']:.3f}s)\n")

            # Mejor criterio
            if 'acceptance' in correlations and correlations['acceptance']:
                best_acceptance = min(correlations['acceptance'].items(),
                                     key=lambda x: x[1]['avg'])
                f.write(f"- **Mejor Criterio**: {best_acceptance[0]} ({best_acceptance[1]['avg']:.3f}s)\n")

            f.write("\n---\n\n")
            f.write("**Generado por**: AlgorithmPatternAnalyzer\n")
