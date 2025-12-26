"""
Smart Algorithm Selector - KBP-SA
Sistema para generar y seleccionar automáticamente los algoritmos más rápidos
"""

from typing import List, Tuple, Dict
from pathlib import Path
import json

from gaa.generator import AlgorithmGenerator
from gaa.grammar import Grammar
from experimentation.algorithm_pattern_analyzer import AlgorithmPatternAnalyzer


class SmartAlgorithmSelector:
    """
    Selector inteligente de algoritmos que genera múltiples candidatos
    y selecciona los más rápidos basándose en patrones aprendidos
    """

    def __init__(self, grammar: Grammar, seed: int, analyzer: AlgorithmPatternAnalyzer = None):
        """
        Inicializa el selector

        Args:
            grammar: Grammar para generar algoritmos
            seed: Seed para reproducibilidad
            analyzer: Analizador de patrones (opcional, crea uno nuevo si no se provee)
        """
        self.grammar = grammar
        self.seed = seed
        self.generator = AlgorithmGenerator(grammar=grammar, seed=seed)
        self.analyzer = analyzer or AlgorithmPatternAnalyzer()

    def generate_and_select_fast_algorithms(
        self,
        num_candidates: int = 20,
        num_selected: int = 3,
        max_complexity_score: float = 10.0,
        verbose: bool = True
    ) -> List[Tuple[str, object, float, str]]:
        """
        Genera múltiples algoritmos candidatos y selecciona los más rápidos

        Args:
            num_candidates: Número de algoritmos a generar
            num_selected: Número de algoritmos a seleccionar (los más rápidos)
            max_complexity_score: Score máximo de complejidad permitido
            verbose: Si imprimir información detallada

        Returns:
            Lista de tuplas (nombre, ast, score, categoría) de los algoritmos seleccionados
        """
        if verbose:
            print(f"🧬 Generando {num_candidates} algoritmos candidatos...")

        # Generar candidatos
        candidates = []
        for i in range(num_candidates):
            try:
                ast = self.generator.generate_with_validation()
                pseudocode = ast.to_pseudocode()
                name = f"GAA_Candidate_{i+1}"

                # Predecir velocidad
                category, score, details = self.analyzer.predict_speed_category(pseudocode)

                candidates.append({
                    'name': name,
                    'ast': ast,
                    'pseudocode': pseudocode,
                    'score': score,
                    'category': category,
                    'details': details
                })

                if verbose and (i + 1) % 5 == 0:
                    print(f"   ✅ Generados: {i+1}/{num_candidates}")

            except Exception as e:
                if verbose:
                    print(f"   ⚠️  Error generando algoritmo {i+1}: {e}")
                continue

        if verbose:
            print(f"\n📊 Análisis de {len(candidates)} candidatos generados:")

        # Categorizar
        fast = [c for c in candidates if c['category'] == 'RÁPIDO']
        medium = [c for c in candidates if c['category'] == 'MEDIO']
        slow = [c for c in candidates if c['category'] == 'LENTO']

        if verbose:
            print(f"   • RÁPIDOS: {len(fast)} ({len(fast)/len(candidates)*100:.1f}%)")
            print(f"   • MEDIOS: {len(medium)} ({len(medium)/len(candidates)*100:.1f}%)")
            print(f"   • LENTOS: {len(slow)} ({len(slow)/len(candidates)*100:.1f}%)")
            print()

        # Ordenar por score (menor = más rápido)
        candidates.sort(key=lambda x: x['score'])

        # Filtrar por complexity score
        candidates_filtered = [c for c in candidates if c['score'] <= max_complexity_score]

        if verbose:
            print(f"🎯 Filtrando por complejidad (score ≤ {max_complexity_score}):")
            print(f"   • Candidatos válidos: {len(candidates_filtered)}/{len(candidates)}")
            print()

        # Seleccionar top N
        if len(candidates_filtered) < num_selected:
            if verbose:
                print(f"⚠️  Solo hay {len(candidates_filtered)} candidatos válidos, usando todos")
            selected = candidates_filtered
        else:
            selected = candidates_filtered[:num_selected]

        if verbose:
            print(f"✅ Top {len(selected)} algoritmos seleccionados:")
            print()
            for i, algo in enumerate(selected, 1):
                print(f"   {i}. {algo['name']} (score: {algo['score']:.2f}, categoría: {algo['category']})")
                print(f"      Constructor: {algo['details']['constructor']}")
                print(f"      Operadores: {', '.join(algo['details']['operators'])}")
                print(f"      Aceptación: {algo['details']['acceptance']}")
                print(f"      Tiempo estimado: {algo['details']['estimated_time_per_experiment']}")
                print()

        # Retornar tuplas (nombre, ast, score, categoria)
        return [(s['name'], s['ast'], s['score'], s['category']) for s in selected]

    def generate_with_constraints(
        self,
        num_algorithms: int = 3,
        preferred_constructors: List[str] = None,
        preferred_operators: List[str] = None,
        avoid_acceptance: List[str] = None,
        max_attempts: int = 100,
        verbose: bool = True
    ) -> List[Tuple[str, object]]:
        """
        Genera algoritmos con restricciones específicas

        Args:
            num_algorithms: Número de algoritmos a generar
            preferred_constructors: Lista de constructores preferidos
            preferred_operators: Lista de operadores preferidos
            avoid_acceptance: Lista de criterios de aceptación a evitar
            max_attempts: Número máximo de intentos por algoritmo
            verbose: Si imprimir información

        Returns:
            Lista de tuplas (nombre, ast)
        """
        preferred_constructors = preferred_constructors or ['GreedyByValue', 'GreedyByWeight']
        preferred_operators = preferred_operators or ['TwoExchange', 'FlipBestItem']
        avoid_acceptance = avoid_acceptance or ['Metropolis']

        if verbose:
            print("🎯 Generando algoritmos con restricciones:")
            print(f"   • Constructores preferidos: {', '.join(preferred_constructors)}")
            print(f"   • Operadores preferidos: {', '.join(preferred_operators)}")
            print(f"   • Evitar aceptación: {', '.join(avoid_acceptance)}")
            print()

        selected = []
        attempts = 0

        while len(selected) < num_algorithms and attempts < max_attempts * num_algorithms:
            attempts += 1

            try:
                ast = self.generator.generate_with_validation()
                pseudocode = ast.to_pseudocode()
                features = self.analyzer.extract_features(pseudocode)

                # Verificar restricciones
                if features.constructor in preferred_constructors:
                    if any(op in preferred_operators for op in features.operators):
                        if features.acceptance_criteria not in avoid_acceptance:
                            name = f"GAA_Algorithm_{len(selected) + 1}"
                            selected.append((name, ast))

                            if verbose:
                                category, score, _ = self.analyzer.predict_speed_category(pseudocode)
                                print(f"✅ Algoritmo {len(selected)} generado:")
                                print(f"   Constructor: {features.constructor}")
                                print(f"   Operadores: {', '.join(features.operators)}")
                                print(f"   Aceptación: {features.acceptance_criteria}")
                                print(f"   Score: {score:.2f} ({category})")
                                print()

            except Exception as e:
                if verbose and attempts % 20 == 0:
                    print(f"   ⚠️  Intentos: {attempts}, generados: {len(selected)}")

        if verbose:
            print(f"✅ Generados {len(selected)} algoritmos en {attempts} intentos")

        return selected

    def save_selected_algorithms(
        self,
        algorithms: List[Tuple[str, object]],
        output_file: str
    ):
        """
        Guarda los algoritmos seleccionados en un archivo JSON

        Args:
            algorithms: Lista de tuplas (nombre, ast)
            output_file: Ruta del archivo de salida
        """
        data = {
            'seed': self.seed,
            'num_algorithms': len(algorithms),
            'algorithms': []
        }

        for name, ast in algorithms:
            pseudocode = ast.to_pseudocode()
            features = self.analyzer.extract_features(pseudocode)
            category, score, details = self.analyzer.predict_speed_category(pseudocode)

            data['algorithms'].append({
                'name': name,
                'pseudocode': pseudocode,
                'ast_dict': ast.to_dict(),
                'features': {
                    'constructor': features.constructor,
                    'operators': features.operators,
                    'acceptance': features.acceptance_criteria,
                    'loop_budget': features.loop_budget,
                    'stagnation_limit': features.stagnation_limit,
                    'complexity_score': features.complexity_score
                },
                'prediction': {
                    'category': category,
                    'score': score,
                    'estimated_time': details['estimated_time_per_experiment']
                }
            })

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"💾 Algoritmos guardados en: {output_file}")

    @staticmethod
    def load_algorithms(input_file: str) -> Tuple[List[Tuple[str, dict]], dict]:
        """
        Carga algoritmos desde un archivo JSON

        Args:
            input_file: Ruta del archivo a cargar

        Returns:
            Tupla de (lista de (nombre, ast_dict), metadata)
        """
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        algorithms = [(algo['name'], algo['ast_dict']) for algo in data['algorithms']]
        metadata = {
            'seed': data['seed'],
            'num_algorithms': data['num_algorithms'],
            'features': [algo['features'] for algo in data['algorithms']],
            'predictions': [algo['prediction'] for algo in data['algorithms']]
        }

        return algorithms, metadata
