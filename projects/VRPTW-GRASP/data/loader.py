"""
Data Loader - Módulo para cargar instancias VRPTW desde archivos

Proporciona carga de benchmarks Solomon de múltiples familias.
"""

from typing import Dict, List, Optional
from pathlib import Path
import numpy as np
from data.parser import SolomonParser, VRPTWInstance
from core.problem import VRPTWProblem


class VRPTWDataLoader:
    """
    Cargador de instancias VRPTW desde benchmarks Solomon.
    
    Soporta familias: C1, C2, R1, R2, RC1, RC2
    """
    
    # Configuración de familias
    FAMILIES = ['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2']
    
    FAMILY_PROPERTIES = {
        'C1': {'description': 'Clustered, narrow time windows', 'tight_tw': True},
        'C2': {'description': 'Clustered, wide time windows', 'tight_tw': False},
        'R1': {'description': 'Random, narrow time windows', 'tight_tw': True},
        'R2': {'description': 'Random, wide time windows', 'tight_tw': False},
        'RC1': {'description': 'Mixed, narrow time windows', 'tight_tw': True},
        'RC2': {'description': 'Mixed, wide time windows', 'tight_tw': False},
    }
    
    def __init__(self, data_dir: str):
        """
        Inicializa loader.
        
        Args:
            data_dir: Directorio raíz de datasets
        """
        self.data_dir = Path(data_dir)
        self._cache: Dict[str, VRPTWProblem] = {}
    
    @classmethod
    def from_workspace(cls, workspace_path: str) -> 'VRPTWDataLoader':
        """
        Crea loader desde ruta del workspace.
        
        Args:
            workspace_path: Path a bestbestGAA
            
        Returns:
            VRPTWDataLoader configurado
        """
        data_dir = Path(workspace_path) / 'projects' / 'VRPTW-GRASP' / 'datasets'
        return cls(str(data_dir))
    
    def list_families(self) -> List[str]:
        """Retorna familias disponibles"""
        return self.FAMILIES
    
    def get_family_info(self, family: str) -> Optional[Dict]:
        """Retorna información sobre una familia"""
        return self.FAMILY_PROPERTIES.get(family)
    
    def list_instances(self, family: Optional[str] = None) -> Dict[str, List[str]]:
        """
        Lista instancias disponibles.
        
        Args:
            family: Familia específica (None = todas)
            
        Returns:
            Dict {family: [instance_names]}
        """
        result = {}
        families = [family] if family else self.FAMILIES
        
        for fam in families:
            family_dir = self.data_dir / fam
            
            if not family_dir.exists():
                result[fam] = []
                continue
            
            # Buscar archivos CSV
            instances = []
            for csv_file in sorted(family_dir.glob('*.csv')):
                instance_name = csv_file.stem
                instances.append(instance_name)
            
            result[fam] = instances
        
        return result
    
    def get_instance_path(self, family: str, instance: str) -> Optional[Path]:
        """
        Obtiene ruta a una instancia.
        
        Args:
            family: Nombre de familia
            instance: Nombre de instancia
            
        Returns:
            Path al archivo CSV o None
        """
        path = self.data_dir / family / f"{instance}.csv"
        
        if path.exists():
            return path
        
        return None
    
    def load_instance(self, family: str, instance: str,
                      vehicle_capacity: int = 200,
                      use_cache: bool = True) -> Optional[VRPTWProblem]:
        """
        Carga una instancia VRPTW.
        
        Args:
            family: Nombre de familia (C1, C2, R1, R2, RC1, RC2)
            instance: Nombre de instancia
            vehicle_capacity: Capacidad de vehículos
            use_cache: Si usar caché
            
        Returns:
            VRPTWProblem o None si no existe
        """
        # Buscar en caché
        cache_key = f"{family}/{instance}"
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]
        
        # Buscar archivo
        path = self.get_instance_path(family, instance)
        if path is None:
            return None
        
        # Cargar
        try:
            parsed = SolomonParser.parse(str(path))
            problem = VRPTWProblem(parsed, vehicle_capacity)
            
            # Cachear
            if use_cache:
                self._cache[cache_key] = problem
            
            return problem
        except Exception as e:
            print(f"Error cargando {family}/{instance}: {e}")
            return None
    
    def load_family(self, family: str,
                    vehicle_capacity: int = 200,
                    use_cache: bool = True) -> Dict[str, VRPTWProblem]:
        """
        Carga todas las instancias de una familia.
        
        Args:
            family: Nombre de familia
            vehicle_capacity: Capacidad de vehículos
            use_cache: Si usar caché
            
        Returns:
            Dict {instance_name: VRPTWProblem}
        """
        instances = self.list_instances(family).get(family, [])
        result = {}
        
        for instance in instances:
            problem = self.load_instance(family, instance, vehicle_capacity, use_cache)
            if problem:
                result[instance] = problem
        
        return result
    
    def load_all(self, vehicle_capacity: int = 200,
                 use_cache: bool = True) -> Dict[str, Dict[str, VRPTWProblem]]:
        """
        Carga todas las familias.
        
        Args:
            vehicle_capacity: Capacidad de vehículos
            use_cache: Si usar caché
            
        Returns:
            Dict {family: {instance: VRPTWProblem}}
        """
        result = {}
        
        for family in self.FAMILIES:
            result[family] = self.load_family(family, vehicle_capacity, use_cache)
        
        return result
    
    def get_statistics(self) -> Dict:
        """
        Calcula estadísticas de los datasets cargados.
        
        Returns:
            Dict con info de familias
        """
        stats = {}
        
        for family in self.FAMILIES:
            family_path = self.data_dir / family
            
            if not family_path.exists():
                stats[family] = {'count': 0, 'exists': False}
                continue
            
            instances = list(family_path.glob('*.csv'))
            stats[family] = {
                'exists': True,
                'count': len(instances),
                'info': self.get_family_info(family),
            }
        
        return stats
    
    def print_summary(self) -> str:
        """Retorna resumen de datasets disponibles"""
        stats = self.get_statistics()
        
        summary = f"""
VRPTW Dataset Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Data Directory: {self.data_dir}

"""
        
        total_instances = 0
        
        for family in self.FAMILIES:
            family_info = stats.get(family, {})
            
            if not family_info.get('exists', False):
                summary += f"  {family}: NOT FOUND\n"
                continue
            
            count = family_info['count']
            total_instances += count
            info = family_info.get('info', {})
            desc = info.get('description', 'Unknown')
            
            summary += f"  {family}: {count:2d} instances - {desc}\n"
        
        summary += f"\nTotal Instances: {total_instances}\n"
        
        return summary
