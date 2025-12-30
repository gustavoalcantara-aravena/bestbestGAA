"""
DataLoader - Carga de instancias DIMACS desde el dataset

Lee archivos .col, crea instancias de problema, gestiona metadatos
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple

try:
    from ..data.parser import DIMACParser, validate_dimacs_file
    from ..core.problem import GraphColoringProblem
except ImportError:
    from data.parser import DIMACParser, validate_dimacs_file
    from core.problem import GraphColoringProblem


class DataLoader:
    """
    Cargador de instancias DIMACS desde los datasets.
    
    Gestiona:
    - Lectura de archivos .col
    - Metadatos (optimal_value, lower_bound, etc.)
    - Validación de instancias
    - Filtrado por familia, tamaño, etc.
    """
    
    def __init__(self, dataset_root: str = None):
        """
        Inicializa el cargador.
        
        Args:
            dataset_root: Raíz del directorio de datasets
                         Si None, usa {project_root}/datasets
        """
        if dataset_root is None:
            # Buscar datasets/ desde el directorio actual
            current_dir = Path(__file__).parent.parent
            dataset_root = current_dir / "datasets"
        else:
            dataset_root = Path(dataset_root)
        
        self.dataset_root = Path(dataset_root)
        self.metadata_file = self.dataset_root / "_metadata.json"
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict:
        """
        Carga metadatos de instancias desde _metadata.json.
        
        Returns:
            Dict con metadatos, o {} si el archivo no existe
        """
        if not self.metadata_file.exists():
            return {}
        
        try:
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Advertencia: No se pudo cargar metadatos: {e}")
            return {}
    
    def list_available_instances(self) -> List[str]:
        """
        Lista todas las instancias disponibles.
        
        Returns:
            Lista de nombres de archivo (sin extensión)
        """
        instances = []
        
        for file in self.dataset_root.glob("**/*.col"):
            # Validar que sea un archivo válido
            is_valid, msg = validate_dimacs_file(str(file))
            if is_valid:
                instances.append(file.stem)
        
        return sorted(instances)
    
    def list_by_family(self, family: str = None) -> List[str]:
        """
        Lista instancias, opcionalmente filtradas por familia.
        
        Args:
            family: Prefijo de familia (ej. 'CUL', 'DSJ'), o None para todas
            
        Returns:
            Lista de nombres de instancias
        """
        instances = self.list_available_instances()
        
        if family is None:
            return instances
        
        family_upper = family.upper()
        return [i for i in instances if i.upper().startswith(family_upper)]
    
    def get_available_families(self) -> List[str]:
        """
        Obtiene lista de familias disponibles.
        
        Returns:
            Lista de prefijos de familia (CUL, DSJ, LEI, MYC, REG, SCH, SGB)
        """
        families = set()
        for instance in self.list_available_instances():
            # Extraer prefijo (primeras 3 letras mayúsculas)
            prefix = instance[:3].upper()
            if prefix in ['CUL', 'DSJ', 'LEI', 'MYC', 'REG', 'SCH', 'SGB']:
                families.add(prefix)
        
        return sorted(list(families))
    
    def get_metadata(self, instance_name: str) -> Dict:
        """
        Obtiene metadatos para una instancia.
        
        Args:
            instance_name: Nombre de la instancia (sin .col)
            
        Returns:
            Dict con metadatos disponibles
        """
        key = instance_name.lower()
        
        if key in self.metadata:
            return self.metadata[key]
        
        # Si no hay en metadata, crear minimal
        return {
            'filename': f"{instance_name}.col",
            'optimal_value': None,
            'lower_bound': None
        }
    
    def load(self, instance_name: str) -> GraphColoringProblem:
        """
        Carga una instancia como GraphColoringProblem.
        
        Args:
            instance_name: Nombre de la instancia (sin .col)
            
        Returns:
            GraphColoringProblem
            
        Raises:
            FileNotFoundError: Si la instancia no existe
            ValueError: Si el archivo no es válido
        """
        # Buscar archivo
        col_file = self._find_col_file(instance_name)
        if col_file is None:
            raise FileNotFoundError(
                f"No se encontró instancia: {instance_name}"
            )
        
        # Validar
        is_valid, msg = validate_dimacs_file(str(col_file))
        if not is_valid:
            raise ValueError(f"Archivo inválido: {msg}")
        
        # Obtener metadatos
        meta = self.get_metadata(instance_name)
        optimal_value = meta.get('optimal_value')
        lower_bound = meta.get('lower_bound')
        
        # Cargar problema
        problem = GraphColoringProblem.from_dimacs_file(
            str(col_file),
            name=instance_name,
            optimal_value=optimal_value,
            lower_bound=lower_bound
        )
        
        return problem
    
    def load_batch(self, instance_names: List[str]) -> List[GraphColoringProblem]:
        """
        Carga un lote de instancias.
        
        Args:
            instance_names: Lista de nombres
            
        Returns:
            Lista de GraphColoringProblem
        """
        problems = []
        for name in instance_names:
            try:
                problem = self.load(name)
                problems.append(problem)
            except Exception as e:
                print(f"Advertencia: Error cargando {name}: {e}")
        
        return problems
    
    def load_by_family(self, family: str) -> List[GraphColoringProblem]:
        """
        Carga todas las instancias de una familia.
        
        Args:
            family: Prefijo de familia (ej. 'CUL')
            
        Returns:
            Lista de GraphColoringProblem
        """
        instances = self.list_by_family(family)
        return self.load_batch(instances)
    
    def load_all(self) -> List[GraphColoringProblem]:
        """
        Carga todas las instancias disponibles.
        
        Returns:
            Lista de GraphColoringProblem
        """
        instances = self.list_available_instances()
        return self.load_batch(instances)
    
    def _find_col_file(self, instance_name: str) -> Optional[Path]:
        """
        Busca un archivo .col en los subdirectorios del dataset.
        
        Args:
            instance_name: Nombre sin extensión
            
        Returns:
            Path si se encuentra, None si no
        """
        # Variaciones posibles del nombre
        variations = [
            f"{instance_name}.col",
            f"{instance_name.lower()}.col",
            f"{instance_name.upper()}.col"
        ]
        
        for variation in variations:
            for col_file in self.dataset_root.glob(f"**/{variation}"):
                return col_file
        
        return None
    
    def get_instance_info(self, instance_name: str) -> Dict:
        """
        Obtiene información completa de una instancia.
        
        Args:
            instance_name: Nombre de la instancia
            
        Returns:
            Dict con información
        """
        try:
            problem = self.load(instance_name)
            meta = self.get_metadata(instance_name)
            
            return {
                'name': instance_name,
                'n': problem.n,
                'm': problem.m,
                'density': problem.density,
                'max_degree': problem.max_degree,
                'min_degree': problem.min_degree,
                'avg_degree': problem.avg_degree,
                'optimal_value': problem.optimal_value,
                'lower_bound': problem.lower_bound,
                'family': instance_name[:3].upper(),
                'is_valid': True
            }
        except Exception as e:
            return {
                'name': instance_name,
                'is_valid': False,
                'error': str(e)
            }
    
    def get_all_info(self) -> List[Dict]:
        """
        Obtiene información de todas las instancias.
        
        Returns:
            Lista de dicts con información
        """
        instances = self.list_available_instances()
        return [self.get_instance_info(name) for name in instances]
    
    def summary(self) -> str:
        """
        Retorna resumen del dataset.
        
        Returns:
            String con información del dataset
        """
        instances = self.list_available_instances()
        families = self.get_available_families()
        
        summary = f"""
Dataset Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Root:             {self.dataset_root}
Total instances:  {len(instances)}
Families:         {', '.join(families)}
Metadata:         {'✓' if self.metadata else '✗ (none loaded)'}
        """
        
        if families:
            summary += "\nInstances by family:\n"
            for family in families:
                count = len(self.list_by_family(family))
                summary += f"  {family}: {count}\n"
        
        return summary
