"""
Operadores Constructivos para Graph Coloring Problem (GCP)

Este módulo implementa tres métodos constructivos clásicos para generar
soluciones iniciales válidas:
- GreedyDSATUR: Basado en el grado de saturación (número cromático mínimo)
- GreedyLF: Largest First - ordena vértices por grado decreciente
- RandomSequential: Asignación aleatoria secuencial

Referencias:
- Brélaz, D. (1979). New methods to color the vertices of a graph
- Leighton, F. T. (1979). A graph coloring algorithm for large scheduling problems
"""

import numpy as np
from typing import List, Set, Dict, Tuple
from core import GraphColoringProblem, ColoringSolution


class GreedyDSATUR:
    """
    Degree of SATUratiom First (DSATUR)
    
    Algoritmo goloso que selecciona vértices por su grado de saturación:
    el número de colores diferentes que usan sus vecinos coloreados.
    
    Ventajas:
    - Típicamente produce coloraciones más compactas
    - Sensible a la estructura local del grafo
    - O(n²) con implementación estándar
    
    Desventajas:
    - Más lento que LargestFirst
    - Puede quedar atrapado en óptimos locales malos
    """
    
    @staticmethod
    def construct(problem: GraphColoringProblem, seed: int = None) -> ColoringSolution:
        """
        Construir solución inicial usando DSATUR.
        
        Algoritmo:
        1. Inicializar todos los vértices como no coloreados
        2. Mientras hay vértices sin colorear:
           a. Seleccionar vértice con mayor grado de saturación
           b. Asignar el color de menor índice que no usa ningún vecino
           c. Actualizar grados de saturación
        
        Parámetros:
            problem: Instancia del problema GCP
            seed: Seed para reproducibilidad (usado en tie-breaking)
        
        Retorna:
            ColoringSolution: Solución válida (sin conflictos)
        
        Complejidad:
            Tiempo: O(n² + m) en promedio
            Espacio: O(n + m)
        """
        if seed is not None:
            np.random.seed(seed)
        
        n = problem.n_vertices
        assignment = {}
        colored = set()
        
        # Inicializar grados de saturación
        saturation_degree = {v: 0 for v in range(1, n + 1)}
        used_colors = {v: set() for v in range(1, n + 1)}  # Colores en vecinos
        
        # Colorear el vértice de mayor grado primero
        first_vertex = max(range(1, n + 1), key=lambda v: problem.degree(v))
        assignment[first_vertex] = 0
        colored.add(first_vertex)
        
        # Actualizar vecinos del primer vértice
        for neighbor in problem.neighbors(first_vertex):
            used_colors[neighbor].add(0)
            saturation_degree[neighbor] = len(used_colors[neighbor])
        
        # Colorear el resto de vértices
        while len(colored) < n:
            # Seleccionar vértice con máximo grado de saturación
            # En caso de empate, usar grado total
            uncolored = [v for v in range(1, n + 1) if v not in colored]
            selected_vertex = max(
                uncolored,
                key=lambda v: (saturation_degree[v], problem.degree(v))
            )
            
            # Asignar menor color disponible
            color = 0
            while color in used_colors[selected_vertex]:
                color += 1
            
            assignment[selected_vertex] = color
            colored.add(selected_vertex)
            
            # Actualizar vecinos no coloreados
            for neighbor in problem.neighbors(selected_vertex):
                if neighbor not in colored:
                    used_colors[neighbor].add(color)
                    saturation_degree[neighbor] = len(used_colors[neighbor])
        
        return ColoringSolution(assignment=assignment)


class GreedyLF:
    """
    Largest First (LF)
    
    Algoritmo goloso que ordena vértices por grado decreciente y los
    colorea secuencialmente con el menor color disponible.
    
    Ventajas:
    - Muy rápido: O(n log n + m)
    - Simple de implementar
    - Frecuentemente usado como baseline
    
    Desventajas:
    - Menos sensible a estructura local que DSATUR
    - A veces produce coloraciones de peor calidad
    """
    
    @staticmethod
    def construct(problem: GraphColoringProblem, seed: int = None) -> ColoringSolution:
        """
        Construir solución inicial usando Largest First.
        
        Algoritmo:
        1. Ordenar vértices por grado decreciente
        2. Para cada vértice en orden:
           a. Asignar el menor color que no use ningún vecino coloreado
           b. Si todos los colores existentes están usados, usar nuevo color
        
        Parámetros:
            problem: Instancia del problema GCP
            seed: Seed para reproducibilidad
        
        Retorna:
            ColoringSolution: Solución válida (sin conflictos)
        
        Complejidad:
            Tiempo: O(n log n + m)
            Espacio: O(n)
        """
        if seed is not None:
            np.random.seed(seed)
        
        n = problem.n_vertices
        
        # Ordenar vértices por grado decreciente
        vertices_by_degree = sorted(
            range(1, n + 1),
            key=lambda v: problem.degree(v),
            reverse=True
        )
        
        assignment = {}
        
        for vertex in vertices_by_degree:
            # Encontrar colores usados por vecinos coloreados
            neighbor_colors = set()
            for neighbor in problem.neighbors(vertex):
                if neighbor in assignment:
                    neighbor_colors.add(assignment[neighbor])
            
            # Asignar menor color disponible
            color = 0
            while color in neighbor_colors:
                color += 1
            
            assignment[vertex] = color
        
        return ColoringSolution(assignment=assignment)


class RandomSequential:
    """
    Construcción Aleatoria Secuencial
    
    Asigna colores a vértices en orden aleatorio, eligiendo el menor color
    disponible para cada vértice.
    
    Ventajas:
    - Diversidad: diferentes soluciones en cada ejecución
    - Útil para inicializar múltiples búsquedas independientes
    - Rápido: O(n log n + m)
    
    Desventajas:
    - Menor calidad que DSATUR o LF
    - Menos estable (varianza alta)
    
    Uso típico:
    - Usado en ILS para generar perturbaciones aleatorias
    - Combinado con búsqueda local para mejorar
    """
    
    @staticmethod
    def construct(problem: GraphColoringProblem, seed: int = None) -> ColoringSolution:
        """
        Construir solución inicial con orden aleatorio.
        
        Algoritmo:
        1. Permutación aleatoria de vértices
        2. Para cada vértice en orden:
           a. Asignar menor color disponible
        
        Parámetros:
            problem: Instancia del problema GCP
            seed: Seed para reproducibilidad (por defecto usa estado actual de RNG)
        
        Retorna:
            ColoringSolution: Solución válida (sin conflictos)
        
        Complejidad:
            Tiempo: O(n + m)
            Espacio: O(n)
        """
        if seed is not None:
            np.random.seed(seed)
        
        n = problem.n_vertices
        
        # Orden aleatorio de vértices
        vertices_order = np.random.permutation(list(range(1, n + 1)))
        
        assignment = {}
        
        for vertex in vertices_order:
            # Colores usados por vecinos ya coloreados
            neighbor_colors = set()
            for neighbor in problem.neighbors(vertex):
                if neighbor in assignment:
                    neighbor_colors.add(assignment[neighbor])
            
            # Menor color disponible
            color = 0
            while color in neighbor_colors:
                color += 1
            
            assignment[vertex] = color
        
        return ColoringSolution(assignment=assignment)


# =============================================================================
# Funciones de utilidad para comparación y análisis
# =============================================================================

def compare_constructives(problem: GraphColoringProblem, 
                          num_trials: int = 5) -> Dict[str, Dict]:
    """
    Comparar los tres operadores constructivos en una instancia.
    
    Parámetros:
        problem: Instancia GCP
        num_trials: Número de intentos para operadores aleatorios
    
    Retorna:
        dict: Estadísticas de cada operador
        {
            'DSATUR': {'mean_colors': 5.2, 'std_colors': 0.1, ...},
            'LF': {...},
            'Random': {...}
        }
    """
    from core import ColoringEvaluator
    
    results = {
        'DSATUR': [],
        'LF': [],
        'Random': []
    }
    
    # DSATUR (determinístico)
    sol = GreedyDSATUR.construct(problem)
    metrics = ColoringEvaluator.evaluate(sol, problem)
    results['DSATUR'] = [metrics['num_colors']]
    
    # LF (determinístico)
    sol = GreedyLF.construct(problem)
    metrics = ColoringEvaluator.evaluate(sol, problem)
    results['LF'] = [metrics['num_colors']]
    
    # Random (múltiples intentos)
    for seed in range(num_trials):
        sol = RandomSequential.construct(problem, seed=seed)
        metrics = ColoringEvaluator.evaluate(sol, problem)
        results['Random'].append(metrics['num_colors'])
    
    # Calcular estadísticas
    stats = {}
    for method, colors_list in results.items():
        stats[method] = {
            'min_colors': min(colors_list),
            'max_colors': max(colors_list),
            'mean_colors': np.mean(colors_list),
            'std_colors': np.std(colors_list),
            'num_trials': len(colors_list)
        }
    
    return stats


if __name__ == "__main__":
    # Ejemplo de uso
    from core import GraphColoringProblem, ColoringEvaluator
    
    # Cargar instancia
    problem = GraphColoringProblem.load_from_dimacs("datasets/myciel3.col")
    
    # Construir soluciones
    print("=== Operadores Constructivos ===\n")
    
    sol_dsatur = GreedyDSATUR.construct(problem)
    print(f"DSATUR: {sol_dsatur.num_colors} colores")
    
    sol_lf = GreedyLF.construct(problem)
    print(f"LF: {sol_lf.num_colors} colores")
    
    sol_random = RandomSequential.construct(problem, seed=42)
    print(f"Random: {sol_random.num_colors} colores")
    
    # Comparación
    print("\n=== Comparación (5 intentos) ===\n")
    stats = compare_constructives(problem, num_trials=5)
    for method, stat in stats.items():
        print(f"{method:8} | min={stat['min_colors']} max={stat['max_colors']} "
              f"mean={stat['mean_colors']:.1f} ± {stat['std_colors']:.2f}")
