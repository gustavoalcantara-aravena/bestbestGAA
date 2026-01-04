"""
============================================================
BKS Loader
VRPTW Solomon - Best Known Solutions
============================================================

Responsabilidades:
- Cargar best-known-solutions desde archivo
- Acceso rápido por instance_id
- Validar integridad de BKS
- Caché en memoria
"""

import json
from typing import Dict, Tuple, Optional
from pathlib import Path


class BKSEntry:
    """
    Entrada de best-known-solution para una instancia.
    
    Ejemplo:
        BKSEntry("C101", k=10, d=828.94)
        
    Atributos:
        instance_id: ID de instancia (e.g., "C101")
        n_vehicles: Número de vehículos en BKS
        total_distance: Distancia total en BKS
    """
    
    def __init__(self, instance_id: str, n_vehicles: int, total_distance: float):
        self.instance_id = instance_id
        self.n_vehicles = n_vehicles
        self.total_distance = total_distance
    
    def __repr__(self) -> str:
        return (
            f"BKSEntry(instance_id='{self.instance_id}', "
            f"n_vehicles={self.n_vehicles}, "
            f"total_distance={self.total_distance:.2f})"
        )
    
    def to_dict(self) -> Dict:
        """Serializar a dict para logging."""
        return {
            "instance_id": self.instance_id,
            "k_bks": self.n_vehicles,
            "d_bks": self.total_distance
        }


class BKSLoader:
    """
    Cargador de best-known-solutions.
    
    Soporta formatos:
    - JSON: {"C101": {"k": 10, "d": 828.94}, ...}
    - CSV: instance_id,k,d
    
    Ejemplo:
        loader = BKSLoader("data/bks_solomon.json")
        bks = loader.get("C101")
        print(bks.n_vehicles, bks.total_distance)
    """
    
    def __init__(self, file_path: str):
        """
        Inicializa el loader.
        
        Args:
            file_path: Ruta a archivo de BKS (JSON o CSV)
        """
        self.file_path = Path(file_path)
        self.bks_dict: Dict[str, BKSEntry] = {}
        self._load()
    
    def _load(self) -> None:
        """Carga BKS desde archivo."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"BKS file not found: {self.file_path}")
        
        if self.file_path.suffix.lower() == ".json":
            self._load_json()
        elif self.file_path.suffix.lower() == ".csv":
            self._load_csv()
        else:
            raise ValueError(f"Unsupported format: {self.file_path.suffix}")
    
    def _load_json(self) -> None:
        """Carga desde JSON."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for instance_id, entry in data.items():
            # Soporta ambos formatos: "k"/"d" o "n_vehicles"/"total_distance"
            k = entry.get("k") or entry.get("n_vehicles")
            d = entry.get("d") or entry.get("total_distance")
            
            if k is None or d is None:
                raise ValueError(
                    f"Invalid BKS entry for {instance_id}: "
                    f"expected 'k' and 'd' or 'n_vehicles' and 'total_distance'"
                )
            
            self.bks_dict[instance_id] = BKSEntry(instance_id, int(k), float(d))
    
    def _load_csv(self) -> None:
        """Carga desde CSV."""
        import csv
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                instance_id = row["instance_id"].strip()
                k = int(row["k"] or row.get("n_vehicles", 0))
                d = float(row["d"] or row.get("total_distance", 0))
                
                self.bks_dict[instance_id] = BKSEntry(instance_id, k, d)
    
    def get(self, instance_id: str) -> Optional[BKSEntry]:
        """
        Obtiene entrada BKS para una instancia.
        
        Args:
            instance_id: ID de instancia (e.g., "C101")
        
        Returns:
            BKSEntry o None si no existe
        """
        return self.bks_dict.get(instance_id)
    
    def get_or_raise(self, instance_id: str) -> BKSEntry:
        """
        Obtiene entrada BKS, lanza excepción si no existe.
        """
        entry = self.get(instance_id)
        if entry is None:
            raise KeyError(f"BKS not found for instance: {instance_id}")
        return entry
    
    def has(self, instance_id: str) -> bool:
        """Verifica si existe BKS para una instancia."""
        return instance_id in self.bks_dict
    
    def get_all(self) -> Dict[str, BKSEntry]:
        """Retorna todas las entradas BKS."""
        return dict(self.bks_dict)
    
    def get_instance_ids(self) -> list:
        """Retorna lista de todos los instance_ids."""
        return sorted(self.bks_dict.keys())
    
    def validate_all_present(self, required_instances: list) -> bool:
        """
        Valida que todos los instance_ids requeridos tengan BKS.
        
        Args:
            required_instances: Lista de instance_ids requeridos
        
        Returns:
            True si todos están presentes
        
        Raises:
            ValueError si alguno falta
        """
        missing = [inst for inst in required_instances if not self.has(inst)]
        
        if missing:
            raise ValueError(
                f"Missing BKS entries for: {missing}\n"
                f"Available: {self.get_instance_ids()}"
            )
        
        return True
    
    def stats(self) -> Dict:
        """Retorna estadísticas del BKS."""
        if not self.bks_dict:
            return {
                "total_instances": 0,
                "min_vehicles": None,
                "max_vehicles": None,
                "avg_vehicles": None,
                "min_distance": None,
                "max_distance": None,
                "avg_distance": None
            }
        
        vehicles = [entry.n_vehicles for entry in self.bks_dict.values()]
        distances = [entry.total_distance for entry in self.bks_dict.values()]
        
        return {
            "total_instances": len(self.bks_dict),
            "min_vehicles": min(vehicles),
            "max_vehicles": max(vehicles),
            "avg_vehicles": sum(vehicles) / len(vehicles),
            "min_distance": min(distances),
            "max_distance": max(distances),
            "avg_distance": sum(distances) / len(distances)
        }
