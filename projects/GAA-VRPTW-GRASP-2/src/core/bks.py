"""
Best Known Solutions (BKS) Manager for Solomon Benchmark Instances

This module loads and manages the BKS data for all 56 Solomon instances,
providing utilities for comparison and validation.

Usage:
    from src.core.bks import BKSManager
    bks = BKSManager()
    bks_c101 = bks.get_instance('C101')
    print(f"C101: K={bks_c101['k_bks']}, D={bks_c101['d_bks']}")
"""

import json
from pathlib import Path
from typing import Dict, Optional, Tuple, List


class BKSManager:
    """Manager for Best Known Solutions of Solomon benchmark instances."""
    
    def __init__(self, bks_file: Optional[str] = None):
        """
        Initialize BKS Manager.
        
        Args:
            bks_file: Path to best_known_solutions.json. If None, searches in config.
        """
        if bks_file is None:
            # Try to find the file in common locations
            possible_paths = [
                Path(__file__).parent.parent.parent / "best_known_solutions.json",
                Path("best_known_solutions.json"),
                Path("config") / "best_known_solutions.json",
            ]
            
            bks_file = None
            for p in possible_paths:
                if p.exists():
                    bks_file = str(p)
                    break
            
            if bks_file is None:
                raise FileNotFoundError(
                    "best_known_solutions.json not found. "
                    "Please provide explicit path or ensure file is in project root."
                )
        
        self.bks_file = Path(bks_file)
        self._load_bks()
    
    def _load_bks(self) -> None:
        """Load BKS data from JSON file."""
        with open(self.bks_file, 'r') as f:
            self.data = json.load(f)
        
        # Create flat dictionary for quick lookup
        self._instance_cache: Dict[str, Dict] = {}
        for family in self.data['families'].values():
            for instance in family['instances']:
                instance_id = instance['id']
                self._instance_cache[instance_id] = instance
    
    def get_instance(self, instance_id: str) -> Dict:
        """
        Get BKS for a specific instance.
        
        Args:
            instance_id: Instance ID (e.g., 'C101', 'R102')
        
        Returns:
            Dictionary with 'id', 'k_bks', and 'd_bks'
        
        Raises:
            ValueError: If instance not found
        """
        if instance_id not in self._instance_cache:
            raise ValueError(f"Unknown instance: {instance_id}")
        return self._instance_cache[instance_id]
    
    def get_k_bks(self, instance_id: str) -> int:
        """Get best known number of vehicles."""
        return self.get_instance(instance_id)['k_bks']
    
    def get_d_bks(self, instance_id: str) -> float:
        """Get best known total distance."""
        return self.get_instance(instance_id)['d_bks']
    
    def get_family(self, family_id: str) -> Dict:
        """
        Get all instances in a family.
        
        Args:
            family_id: Family ID (e.g., 'C1', 'R2', 'RC1')
        
        Returns:
            Dictionary with family info and instances
        """
        if family_id not in self.data['families']:
            raise ValueError(f"Unknown family: {family_id}")
        return self.data['families'][family_id]
    
    def get_all_families(self) -> List[str]:
        """Get list of all family IDs."""
        return list(self.data['families'].keys())
    
    def get_all_instances(self) -> List[str]:
        """Get list of all instance IDs."""
        return sorted(list(self._instance_cache.keys()))
    
    def get_instances_by_family(self, family_id: str) -> List[str]:
        """Get all instance IDs in a family."""
        family = self.get_family(family_id)
        return [inst['id'] for inst in family['instances']]
    
    def compute_k_gap(self, instance_id: str, algo_k: int) -> Optional[float]:
        """
        Compute the gap in number of vehicles (percentage).
        
        Args:
            instance_id: Instance ID
            algo_k: Algorithm's number of vehicles
        
        Returns:
            Gap percentage if algo_k >= bks_k, else None (worse than BKS)
        """
        bks_k = self.get_k_bks(instance_id)
        
        if algo_k < bks_k:
            return None  # Better than BKS (shouldn't happen)
        
        if algo_k == bks_k:
            return 0.0
        
        return ((algo_k - bks_k) / bks_k) * 100
    
    def compute_d_gap(self, instance_id: str, algo_d: float) -> Optional[float]:
        """
        Compute the gap in distance (percentage).
        Only valid if algo_k == bks_k.
        
        Args:
            instance_id: Instance ID
            algo_d: Algorithm's total distance
        
        Returns:
            Gap percentage if distance is comparable, else None
        """
        bks_d = self.get_d_bks(instance_id)
        
        if algo_d < bks_d:
            return None  # Better than BKS (shouldn't happen)
        
        if algo_d == bks_d:
            return 0.0
        
        return ((algo_d - bks_d) / bks_d) * 100
    
    def is_better_solution(
        self, 
        instance_id: str, 
        algo_k: int, 
        algo_d: float
    ) -> Tuple[bool, str]:
        """
        Check if solution is better than BKS (hierarchical comparison).
        
        Args:
            instance_id: Instance ID
            algo_k: Algorithm's number of vehicles
            algo_d: Algorithm's total distance
        
        Returns:
            Tuple (is_better, reason)
        """
        bks_k = self.get_k_bks(instance_id)
        bks_d = self.get_d_bks(instance_id)
        
        if algo_k < bks_k:
            return True, f"Better K: {algo_k} < {bks_k}"
        elif algo_k > bks_k:
            return False, f"Worse K: {algo_k} > {bks_k}"
        else:  # algo_k == bks_k
            if algo_d < bks_d:
                return True, f"Better D at K={algo_k}: {algo_d:.2f} < {bks_d:.2f}"
            elif algo_d > bks_d:
                return False, f"Worse D at K={algo_k}: {algo_d:.2f} > {bks_d:.2f}"
            else:
                return False, f"Equal to BKS: K={algo_k}, D={algo_d:.2f}"
    
    def get_summary(self, family_id: Optional[str] = None) -> Dict:
        """
        Get summary statistics.
        
        Args:
            family_id: If provided, get summary for that family. Else overall.
        
        Returns:
            Dictionary with statistics
        """
        if family_id:
            if family_id not in self.data['families']:
                raise ValueError(f"Unknown family: {family_id}")
            return self.data['summary']['by_family'][family_id]
        else:
            return self.data['summary']['overall']
    
    def validate_solution(
        self,
        instance_id: str,
        algo_k: int,
        algo_d: float
    ) -> Dict:
        """
        Comprehensive validation against BKS.
        
        Args:
            instance_id: Instance ID
            algo_k: Algorithm's number of vehicles
            algo_d: Algorithm's total distance
        
        Returns:
            Dictionary with validation results
        """
        bks_k = self.get_k_bks(instance_id)
        bks_d = self.get_d_bks(instance_id)
        
        k_gap = self.compute_k_gap(instance_id, algo_k)
        is_better, reason = self.is_better_solution(instance_id, algo_k, algo_d)
        
        return {
            'instance_id': instance_id,
            'algorithm': {
                'k': algo_k,
                'd': algo_d
            },
            'bks': {
                'k': bks_k,
                'd': bks_d
            },
            'comparison': {
                'k_matches_bks': algo_k == bks_k,
                'k_gap_percent': k_gap,
                'is_better_than_bks': is_better,
                'reason': reason
            }
        }


# Convenience functions
def load_bks(file_path: Optional[str] = None) -> BKSManager:
    """Load BKS manager."""
    return BKSManager(file_path)


def get_bks_for_instance(instance_id: str) -> Dict:
    """Quick access to single instance BKS."""
    manager = BKSManager()
    return manager.get_instance(instance_id)
