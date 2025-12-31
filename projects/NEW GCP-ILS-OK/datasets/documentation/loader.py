"""
Instance Loader - Utilidad para cargar instancias del dataset DIMACS
Facilita acceso a instancias por familia, dificultad, tamaño, etc.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional


class InstanceLoader:
    def __init__(self, instances_dir: str = "."):
        """
        Inicializa el loader.
        
        Args:
            instances_dir: Directorio raíz de instancias (donde está metadata.json)
        """
        self.instances_dir = Path(instances_dir)
        self.metadata_path = self.instances_dir / "metadata.json"
        self.raw_dir = self.instances_dir / "raw"
        self.by_family_dir = self.instances_dir / "by_family"
        
        # Cargar metadata
        with open(self.metadata_path) as f:
            self.metadata = json.load(f)
        
        self.instances = self.metadata['instances']
    
    def get_all(self) -> List[Dict]:
        """Retorna todas las instancias."""
        return self.instances
    
    def get_by_source(self, source: str) -> List[Dict]:
        """
        Obtiene instancias por familia (source).
        
        Ejemplo:
            loader.get_by_source('SGB')  # All Stanford GraphBase instances
        """
        return [i for i in self.instances if i['source'] == source]
    
    def get_by_difficulty(self, difficulty: str) -> List[Dict]:
        """
        Obtiene instancias por dificultad.
        
        Dificultades: trivial, easy, medium, hard, very_hard, extremely_hard
        """
        return [i for i in self.instances if i['difficulty'] == difficulty]
    
    def get_by_size(self, min_nodes: int = 0, max_nodes: int = float('inf')) -> List[Dict]:
        """Obtiene instancias en rango de tamaño (nodos)."""
        return [i for i in self.instances 
                if min_nodes <= i['nodes'] <= max_nodes]
    
    def get_optimal_known(self) -> List[Dict]:
        """Obtiene instancias con óptimo confirmado."""
        return [i for i in self.instances if i['optimal_confirmed']]
    
    def get_optimal_unknown(self) -> List[Dict]:
        """Obtiene instancias con óptimo desconocido."""
        return [i for i in self.instances if not i['optimal_confirmed']]
    
    def get_instance(self, name: str) -> Optional[Dict]:
        """Obtiene una instancia específica por nombre."""
        for i in self.instances:
            if i['name'] == name or i['filename'] == name:
                return i
        return None
    
    def get_file_path(self, instance_name: str, use_family_links: bool = False) -> Path:
        """
        Obtiene la ruta del archivo .col.
        
        Args:
            instance_name: Nombre de la instancia (con o sin .col)
            use_family_links: Si True, usa ruta by_family; si False, usa raw
        
        Returns:
            Path al archivo .col
        """
        instance = self.get_instance(instance_name)
        if not instance:
            raise FileNotFoundError(f"Instance '{instance_name}' not found")
        
        filename = instance['filename']
        
        if use_family_links:
            source = instance['source']
            return self.by_family_dir / source / filename
        else:
            return self.raw_dir / filename
    
    def filter(self, 
               source: Optional[str] = None,
               difficulty: Optional[str] = None,
               min_nodes: Optional[int] = None,
               max_nodes: Optional[int] = None,
               optimal_only: Optional[bool] = None) -> List[Dict]:
        """
        Filtro avanzado combinando múltiples criterios.
        
        Ejemplo:
            loader.filter(source='SGB', difficulty='easy', max_nodes=100)
            loader.filter(optimal_only=True)
        """
        results = self.instances
        
        if source:
            results = [i for i in results if i['source'] == source]
        
        if difficulty:
            results = [i for i in results if i['difficulty'] == difficulty]
        
        if min_nodes:
            results = [i for i in results if i['nodes'] >= min_nodes]
        
        if max_nodes:
            results = [i for i in results if i['nodes'] <= max_nodes]
        
        if optimal_only is not None:
            results = [i for i in results if i['optimal_confirmed'] == optimal_only]
        
        return results
    
    def print_summary(self):
        """Imprime resumen del dataset."""
        print("\n" + "="*60)
        print("📊 RESUMEN DEL DATASET")
        print("="*60)
        
        # Por familia
        print("\n📁 Instancias por Familia:")
        families = {}
        for i in self.instances:
            source = i['source']
            families[source] = families.get(source, 0) + 1
        
        for source in sorted(families.keys()):
            print(f"  {source:6s}: {families[source]:3d} instancias")
        
        # Por dificultad
        print("\n⚙️  Instancias por Dificultad:")
        difficulties = {}
        for i in self.instances:
            diff = i['difficulty']
            difficulties[diff] = difficulties.get(diff, 0) + 1
        
        difficulty_order = ['trivial', 'easy', 'medium', 'hard', 'very_hard', 'extremely_hard']
        for diff in difficulty_order:
            if diff in difficulties:
                print(f"  {diff:15s}: {difficulties[diff]:3d} instancias")
        
        # Óptimos conocidos
        optimal = sum(1 for i in self.instances if i['optimal_confirmed'])
        unknown = len(self.instances) - optimal
        print(f"\n✓ Óptimos Conocidos: {optimal}")
        print(f"? Óptimos Desconocidos: {unknown}")
        
        # Estadísticas de tamaño
        nodes = [i['nodes'] for i in self.instances]
        edges = [i['edges'] for i in self.instances]
        print(f"\n📏 Estadísticas de Tamaño:")
        print(f"  Nodos min/max: {min(nodes)} / {max(nodes)}")
        print(f"  Aristas min/max: {min(edges)} / {max(edges)}")
        print(f"  Promedio nodos: {sum(nodes) // len(nodes)}")
        print(f"  Promedio aristas: {sum(edges) // len(edges)}")
        
        print("\n" + "="*60 + "\n")
    
    def export_csv(self, filepath: str):
        """Exporta metadata como CSV."""
        import csv
        
        keys = ['filename', 'name', 'source', 'nodes', 'edges', 'density', 
                'chromatic_number', 'lower_bound', 'upper_bound', 'best_known',
                'optimal_confirmed', 'difficulty']
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            
            for instance in self.instances:
                row = {k: instance.get(k, '') for k in keys}
                writer.writerow(row)
        
        print(f"✓ Exportado a {filepath}")


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    # Inicializar loader
    loader = InstanceLoader(".")
    
    # Ejemplo 1: Mostrar resumen
    loader.print_summary()
    
    # Ejemplo 2: Obtener todas las instancias fáciles
    easy_instances = loader.get_by_difficulty('easy')
    print(f"📚 {len(easy_instances)} instancias fáciles:")
    for inst in easy_instances[:5]:
        print(f"   - {inst['name']}: {inst['nodes']} nodos")
    print()
    
    # Ejemplo 3: Obtener todas las del tipo SGB
    sgb = loader.get_by_source('SGB')
    print(f"📚 {len(sgb)} instancias SGB (Stanford GraphBase)")
    print()
    
    # Ejemplo 4: Instancias pequeñas con óptimo conocido
    small_optimal = loader.filter(
        max_nodes=100,
        optimal_only=True
    )
    print(f"📚 {len(small_optimal)} instancias pequeñas (≤100 nodos) con óptimo conocido:")
    for inst in small_optimal:
        print(f"   - {inst['name']}: {inst['nodes']} nodos, óptimo={inst['best_known']}")
    print()
    
    # Ejemplo 5: Obtener ruta de un archivo
    instance = loader.get_instance('queen12_12')
    if instance:
        path_raw = loader.get_file_path('queen12_12', use_family_links=False)
        print(f"Ruta (raw): {path_raw}")
        path_family = loader.get_file_path('queen12_12', use_family_links=True)
        print(f"Ruta (by_family): {path_family}")
    print()
    
    # Ejemplo 6: Exportar a CSV para análisis
    loader.export_csv("instances_report.csv")
