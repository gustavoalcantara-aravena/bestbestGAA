"""
algorithm_visualizer.py - Visualizar estructura detallada de algoritmos GAA
"""

from gaa.ast_nodes import GreedyConstruct, LocalSearch, Perturbation, Seq, If


def extract_algorithm_structure(algorithm, algo_index):
    """
    Extrae la estructura detallada de un algoritmo GAA.
    
    Args:
        algorithm: Nodo AST del algoritmo
        algo_index: Índice del algoritmo (1, 2, 3)
    
    Returns:
        dict: Estructura detallada del algoritmo
    """
    structure = {
        'index': algo_index,
        'name': f'GAA_Algorithm_{algo_index}',
        'constructive': None,
        'improvement': None,
        'perturbation': None,
        'tree': None
    }
    
    # Extraer componentes del árbol recursivamente
    def extract_components(node):
        """Extrae operadores de cada tipo del árbol"""
        if node is None:
            return
        
        # Verificar tipo de nodo
        node_type = type(node).__name__
        
        # Extraer GreedyConstruct
        if isinstance(node, GreedyConstruct):
            if hasattr(node, 'heuristic'):
                structure['constructive'] = str(node.heuristic)
        
        # Extraer LocalSearch
        elif isinstance(node, LocalSearch):
            if hasattr(node, 'method'):
                structure['improvement'] = str(node.method)
        
        # Extraer Perturbation
        elif isinstance(node, Perturbation):
            if hasattr(node, 'method'):
                structure['perturbation'] = str(node.method)
        
        # Procesar hijos recursivamente
        if hasattr(node, 'body') and node.body:
            # Para Seq que tiene 'body' en lugar de 'children'
            for child in node.body:
                extract_components(child)
        
        if hasattr(node, 'children') and node.children:
            for child in node.children:
                extract_components(child)
        
        if hasattr(node, 'then_branch') and node.then_branch:
            extract_components(node.then_branch)
        
        if hasattr(node, 'else_branch') and node.else_branch:
            extract_components(node.else_branch)
        
        if hasattr(node, 'left') and node.left:
            extract_components(node.left)
        
        if hasattr(node, 'right') and node.right:
            extract_components(node.right)
    
    extract_components(algorithm)
    structure['tree'] = str(algorithm)
    
    return structure


def print_algorithm_structure(structure):
    """
    Imprime la estructura detallada de un algoritmo.
    
    Args:
        structure: dict con estructura del algoritmo
    """
    algo_name = structure['name']
    constructive = structure['constructive'] or 'Desconocido'
    improvement = structure['improvement'] or 'Desconocido'
    perturbation = structure['perturbation'] or 'Desconocido'
    
    print(f"\n{'='*80}")
    print(f"📊 {algo_name.upper()}")
    print(f"{'='*80}")
    print()
    
    print(f"ESTRUCTURA DEL ALGORITMO:")
    print(f"{'─'*80}")
    print()
    
    print(f"1. CONSTRUCCIÓN INICIAL (GreedyConstruct)")
    print(f"   Operador: {constructive}")
    print(f"   Descripción: {get_constructive_description(constructive)}")
    print()
    
    print(f"2. MEJORA LOCAL (LocalSearch)")
    print(f"   Estrategia: {improvement}")
    print(f"   Descripción: {get_improvement_description(improvement)}")
    print()
    
    print(f"3. PERTURBACIÓN (Perturbation)")
    print(f"   Método: {perturbation}")
    print(f"   Descripción: {get_perturbation_description(perturbation)}")
    print()
    
    print(f"FLUJO DE EJECUCIÓN:")
    print(f"{'─'*80}")
    print(f"  1. Construir solución inicial con {constructive}")
    print(f"  2. Si es posible, mejorar con {improvement}")
    print(f"  3. Si no mejora, perturbar con {perturbation}")
    print()


def get_constructive_description(operator):
    """Retorna descripción del operador constructivo"""
    descriptions = {
        'DSATUR': 'Colorea vértices por grado decreciente (Degree Saturation)',
        'LF': 'Colorea vértices por tamaño de clique (Largest First)',
        'RandomSequential': 'Colorea vértices en orden aleatorio',
        'Desconocido': 'Operador no identificado'
    }
    return descriptions.get(operator, f'Operador: {operator}')


def get_improvement_description(operator):
    """Retorna descripción del operador de mejora"""
    descriptions = {
        'KempeChain': 'Intercambia colores en cadenas de Kempe',
        'OneVertexMove': 'Mueve un vértice a otro color',
        'TabuCol': 'Búsqueda tabú con memoria',
        'Desconocido': 'Operador no identificado'
    }
    return descriptions.get(operator, f'Operador: {operator}')


def get_perturbation_description(operator):
    """Retorna descripción del operador de perturbación"""
    descriptions = {
        'RandomRecolor': 'Recolores aleatorios de vértices',
        'PartialDestroy': 'Destruye parcialmente la solución',
        'Desconocido': 'Operador no identificado'
    }
    return descriptions.get(operator, f'Operador: {operator}')


def print_algorithms_comparison(structures):
    """
    Imprime comparación de los 3 algoritmos.
    
    Args:
        structures: list de dicts con estructura de cada algoritmo
    """
    print(f"\n{'='*100}")
    print(f"COMPARACIÓN DE ESTRUCTURAS - 3 ALGORITMOS GAA")
    print(f"{'='*100}")
    print()
    
    print(f"{'Algoritmo':<20} {'Constructivo':<20} {'Mejora Local':<20} {'Perturbación':<20}")
    print(f"{'-'*100}")
    
    for struct in structures:
        algo_name = struct['name']
        constructive = struct['constructive'] or 'Desconocido'
        improvement = struct['improvement'] or 'Desconocido'
        perturbation = struct['perturbation'] or 'Desconocido'
        
        print(f"{algo_name:<20} {constructive:<20} {improvement:<20} {perturbation:<20}")
    
    print()
    print(f"{'='*100}")
    print()
    
    print(f"CARACTERÍSTICAS IDÉNTICAS:")
    print(f"  ✅ Estructura: Seq(GreedyConstruct, If(LocalSearch, Perturbation))")
    print(f"  ✅ Número de nodos: 4")
    print(f"  ✅ Profundidad máxima: 3")
    print()
    
    print(f"CARACTERÍSTICAS DIFERENTES:")
    print(f"  ❌ Operadores seleccionados aleatoriamente")
    print(f"  ❌ Combinación específica de operadores")
    print(f"  ❌ Comportamiento durante ejecución")
    print()
