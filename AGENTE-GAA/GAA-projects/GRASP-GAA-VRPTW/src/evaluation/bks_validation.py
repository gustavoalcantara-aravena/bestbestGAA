"""
============================================================
BKS Validation
VRPTW Solomon - Comparación vs Best-Known-Solutions
============================================================

Responsabilidades:
- Comparar solución contra BKS
- Calcular gap lexicográfico
- Validar si domina BKS
- Generar reporte de comparación
"""

from typing import Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class BKSComparison:
    """
    Resultado de comparación solución vs BKS.
    
    Atributos:
        instance_id: ID de instancia
        solution_vehicles: Número de vehículos en solución
        solution_distance: Distancia total en solución
        bks_vehicles: BKS: número de vehículos
        bks_distance: BKS: distancia total
        feasible: ¿Solución es factible?
        vehicles_gap: Diferencia en vehículos (sol - bks)
        distance_gap: Diferencia en distancia (sol - bks)
        vehicles_gap_percent: Gap % en vehículos
        distance_gap_percent: Gap % en distancia
        dominates_bks: ¿Solución mejora BKS?
        lexicographic_comparison: -1 (peor), 0 (igual), +1 (mejor)
    """
    instance_id: str
    solution_vehicles: int
    solution_distance: float
    bks_vehicles: int
    bks_distance: float
    feasible: bool
    vehicles_gap: int
    distance_gap: float
    vehicles_gap_percent: float
    distance_gap_percent: float
    dominates_bks: bool
    lexicographic_comparison: int  # -1, 0, +1
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializar para logging JSONL."""
        return {
            "instance_id": self.instance_id,
            "solution_vehicles": self.solution_vehicles,
            "solution_distance": round(self.solution_distance, 5),
            "k_bks": self.bks_vehicles,
            "d_bks": round(self.bks_distance, 5),
            "feasible": self.feasible,
            "vehicles_gap": self.vehicles_gap,
            "distance_gap": round(self.distance_gap, 5),
            "vehicles_gap_percent": round(self.vehicles_gap_percent, 2),
            "distance_gap_percent": round(self.distance_gap_percent, 2),
            "dominates_bks": self.dominates_bks,
            "lexicographic_comparison": self.lexicographic_comparison
        }
    
    def summary_str(self) -> str:
        """Resumen legible."""
        status = "✓ MEJOR" if self.dominates_bks else "✗ PEOR"
        return (
            f"{status} | {self.instance_id} | "
            f"V:{self.solution_vehicles} (BKS:{self.bks_vehicles}) | "
            f"D:{self.solution_distance:.2f} (BKS:{self.bks_distance:.2f}) | "
            f"Gap: {self.distance_gap_percent:+.2f}%"
        )


def validate_solution_vs_bks(
    solution_metrics: Dict[str, Any],
    bks_entry: Any  # BKSEntry from bks_loader.py
) -> BKSComparison:
    """
    Valida solución contra BKS y retorna comparación detallada.
    
    Args:
        solution_metrics: {
            "instance_id": str,
            "n_vehicles": int,
            "total_distance": float,
            "feasible": bool (opcional, default=True)
        }
        bks_entry: BKSEntry con (instance_id, n_vehicles, total_distance)
    
    Returns:
        BKSComparison con análisis completo
    
    Ejemplo:
        comparison = validate_solution_vs_bks(
            solution_metrics={
                "instance_id": "C101",
                "n_vehicles": 10,
                "total_distance": 850.5,
                "feasible": True
            },
            bks_entry=bks_loader.get("C101")
        )
        
        if comparison.dominates_bks:
            print("✓ Nueva mejor solución encontrada!")
        else:
            print(f"Gap vs BKS: {comparison.distance_gap_percent:+.2f}%")
    """
    instance_id = solution_metrics["instance_id"]
    solution_vehicles = solution_metrics["n_vehicles"]
    solution_distance = solution_metrics["total_distance"]
    feasible = solution_metrics.get("feasible", True)
    
    bks_vehicles = bks_entry.n_vehicles
    bks_distance = bks_entry.total_distance
    
    # Calcular gaps
    vehicles_gap = solution_vehicles - bks_vehicles
    distance_gap = solution_distance - bks_distance
    
    # Gap en porcentaje
    vehicles_gap_percent = (vehicles_gap / bks_vehicles * 100) if bks_vehicles > 0 else 0.0
    distance_gap_percent = (distance_gap / bks_distance * 100) if bks_distance > 0 else 0.0
    
    # Comparación lexicográfica: (V, D)
    if solution_vehicles < bks_vehicles:
        # Menos vehículos → mejor
        lexicographic_comparison = 1
        dominates_bks = feasible
    elif solution_vehicles > bks_vehicles:
        # Más vehículos → peor
        lexicographic_comparison = -1
        dominates_bks = False
    else:
        # Mismo número de vehículos → comparar distancia
        if solution_distance < bks_distance:
            lexicographic_comparison = 1
            dominates_bks = feasible
        elif solution_distance > bks_distance:
            lexicographic_comparison = -1
            dominates_bks = False
        else:
            # Exactamente igual
            lexicographic_comparison = 0
            dominates_bks = feasible and abs(distance_gap) < 0.01
    
    return BKSComparison(
        instance_id=instance_id,
        solution_vehicles=solution_vehicles,
        solution_distance=solution_distance,
        bks_vehicles=bks_vehicles,
        bks_distance=bks_distance,
        feasible=feasible,
        vehicles_gap=vehicles_gap,
        distance_gap=distance_gap,
        vehicles_gap_percent=vehicles_gap_percent,
        distance_gap_percent=distance_gap_percent,
        dominates_bks=dominates_bks,
        lexicographic_comparison=lexicographic_comparison
    )


def batch_validate_solutions(
    solutions_metrics: list,
    bks_loader: Any  # BKSLoader
) -> list:
    """
    Valida múltiples soluciones contra BKS.
    
    Args:
        solutions_metrics: Lista de dicts con soluciones
        bks_loader: BKSLoader inicializado
    
    Returns:
        Lista de BKSComparison
    
    Ejemplo:
        comparisons = batch_validate_solutions(
            solutions_metrics=[
                {"instance_id": "C101", "n_vehicles": 10, "total_distance": 850.5},
                {"instance_id": "C102", "n_vehicles": 11, "total_distance": 1010.2},
            ],
            bks_loader=bks_loader
        )
        
        for cmp in comparisons:
            print(cmp.summary_str())
    """
    results = []
    
    for metrics in solutions_metrics:
        instance_id = metrics["instance_id"]
        bks_entry = bks_loader.get_or_raise(instance_id)
        
        comparison = validate_solution_vs_bks(metrics, bks_entry)
        results.append(comparison)
    
    return results


def compute_aggregate_statistics(
    comparisons: list
) -> Dict[str, Any]:
    """
    Calcula estadísticas agregadas de un conjunto de comparaciones.
    
    Args:
        comparisons: Lista de BKSComparison
    
    Returns:
        Dict con estadísticas
    
    Ejemplo:
        stats = compute_aggregate_statistics(comparisons)
        print(f"Instancias que mejoran BKS: {stats['num_dominates']}")
        print(f"Gap promedio: {stats['avg_distance_gap_percent']:.2f}%")
    """
    if not comparisons:
        return {
            "total_instances": 0,
            "feasible_count": 0,
            "dominates_count": 0,
            "avg_vehicles_gap_percent": 0.0,
            "avg_distance_gap_percent": 0.0,
            "min_distance_gap_percent": None,
            "max_distance_gap_percent": None,
            "min_vehicles_gap_percent": None,
            "max_vehicles_gap_percent": None
        }
    
    feasible_count = sum(1 for c in comparisons if c.feasible)
    dominates_count = sum(1 for c in comparisons if c.dominates_bks)
    
    vehicle_gaps = [c.vehicles_gap_percent for c in comparisons]
    distance_gaps = [c.distance_gap_percent for c in comparisons]
    
    return {
        "total_instances": len(comparisons),
        "feasible_count": feasible_count,
        "feasible_percent": feasible_count / len(comparisons) * 100,
        "dominates_count": dominates_count,
        "dominates_percent": dominates_count / len(comparisons) * 100,
        "avg_vehicles_gap_percent": sum(vehicle_gaps) / len(vehicle_gaps) if vehicle_gaps else 0.0,
        "avg_distance_gap_percent": sum(distance_gaps) / len(distance_gaps) if distance_gaps else 0.0,
        "min_distance_gap_percent": min(distance_gaps) if distance_gaps else None,
        "max_distance_gap_percent": max(distance_gaps) if distance_gaps else None,
        "min_vehicles_gap_percent": min(vehicle_gaps) if vehicle_gaps else None,
        "max_vehicles_gap_percent": max(vehicle_gaps) if vehicle_gaps else None
    }
