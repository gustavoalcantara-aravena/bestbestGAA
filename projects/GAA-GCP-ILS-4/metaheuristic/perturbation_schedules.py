"""
Estrategias de Perturbación para Iterated Local Search

Define diferentes estrategias de control de intensidad de perturbación
para adaptar la búsqueda durante la ejecución:

- ConstantPerturbation: Intensidad fija
- LinearPerturbation: Aumenta linealmente con iteraciones sin mejora
- ExponentialPerturbation: Aumenta exponencialmente
- DynamicPerturbation: Adapta según estadísticas de búsqueda
"""

import numpy as np
from typing import List, Callable


class PerturbationSchedule:
    """Clase base para estrategias de perturbación"""
    
    def get_strength(self, iteration: int, **kwargs) -> float:
        """
        Obtener intensidad de perturbación para la iteración actual.
        
        Retorna:
            float: Intensidad en rango [0.0, 1.0]
        """
        raise NotImplementedError


class ConstantPerturbation(PerturbationSchedule):
    """
    Perturbación Constante: Mantiene intensidad fija
    
    Simple y predecible. Bueno para problemas bien entendidos.
    """
    
    def __init__(self, strength: float = 0.2):
        """
        Parámetros:
            strength: Intensidad fija (0.0 a 1.0)
        """
        self.strength = max(0.0, min(1.0, strength))
    
    def get_strength(self, iteration: int, **kwargs) -> float:
        """Retornar intensidad constante"""
        return self.strength


class LinearPerturbation(PerturbationSchedule):
    """
    Perturbación Lineal: Aumenta linealmente con iteraciones sin mejora
    
    Estrategia simple: perturbación suave al inicio, más fuerte si se estanca.
    """
    
    def __init__(self, initial_strength: float = 0.1, 
                 final_strength: float = 0.5,
                 plateau_iterations: int = 50):
        """
        Parámetros:
            initial_strength: Intensidad al inicio
            final_strength: Intensidad máxima
            plateau_iterations: Iteraciones para alcanzar máximo
        """
        self.initial = initial_strength
        self.final = final_strength
        self.plateau = plateau_iterations
    
    def get_strength(self, iteration: int, 
                     no_improvement_count: int = 0, **kwargs) -> float:
        """
        Aumentar intensidad con iteraciones sin mejora.
        
        Parámetros:
            iteration: Número de iteración actual
            no_improvement_count: Iteraciones consecutivas sin mejora
        """
        strength = self.initial + (self.final - self.initial) * \
                   min(1.0, no_improvement_count / self.plateau)
        return min(1.0, strength)


class ExponentialPerturbation(PerturbationSchedule):
    """
    Perturbación Exponencial: Aumenta exponencialmente si se estanca
    
    Más agresiva que lineal: pequenos cambios al inicio, grandes saltos si estanca.
    """
    
    def __init__(self, initial_strength: float = 0.1,
                 growth_factor: float = 1.1):
        """
        Parámetros:
            initial_strength: Intensidad al inicio
            growth_factor: Factor de crecimiento por iteración sin mejora
        """
        self.initial = initial_strength
        self.growth = growth_factor
    
    def get_strength(self, iteration: int,
                     no_improvement_count: int = 0, **kwargs) -> float:
        """
        Calcular intensidad exponencial.
        
        Parámetros:
            iteration: Número de iteración
            no_improvement_count: Iteraciones sin mejora
        """
        strength = self.initial * (self.growth ** min(no_improvement_count, 20))
        return min(1.0, strength)


class DynamicPerturbation(PerturbationSchedule):
    """
    Perturbación Dinámica: Adapta según historial de mejoras
    
    Más sofisticada: usa estadísticas recientes para decidir intensidad.
    """
    
    def __init__(self, window_size: int = 20):
        """
        Parámetros:
            window_size: Tamaño de ventana para estadísticas (iteraciones recientes)
        """
        self.window_size = window_size
    
    def get_strength(self, iteration: int,
                     improvement_history: List[float] = None, **kwargs) -> float:
        """
        Adaptar intensidad según mejoras recientes.
        
        Parámetros:
            iteration: Número de iteración
            improvement_history: Lista de mejoras recientes
        
        Lógica:
        - Si hay muchas mejoras recientes → perturbación suave (explotar)
        - Si pocas mejoras → perturbación fuerte (explorar)
        """
        if improvement_history is None or len(improvement_history) == 0:
            return 0.2
        
        # Calcular tasa de mejora reciente
        recent_window = improvement_history[-self.window_size:]
        improvement_rate = sum(1 for x in recent_window if x > 0) / len(recent_window)
        
        # Escalar: tasa_mejora → intensidad inversa
        strength = 0.1 + (1.0 - improvement_rate) * 0.4
        
        return min(1.0, strength)


class CyclicalPerturbation(PerturbationSchedule):
    """
    Perturbación Cíclica: Alterna entre intensidades
    
    Útil para evitar patrones predecibles.
    """
    
    def __init__(self, intensities: List[float] = None):
        """
        Parámetros:
            intensities: Lista de intensidades a ciclar (default: [0.1, 0.3, 0.5])
        """
        self.intensities = intensities or [0.1, 0.3, 0.5]
    
    def get_strength(self, iteration: int, **kwargs) -> float:
        """Retornar intensidad según ciclo"""
        return self.intensities[iteration % len(self.intensities)]


class AdaptiveTemperaturePerturbation(PerturbationSchedule):
    """
    Perturbación Adaptativa por Temperatura: Similar a Simulated Annealing
    
    Disminuye intensidad con el tiempo (enfriamiento).
    """
    
    def __init__(self, initial_temperature: float = 1.0,
                 cooling_rate: float = 0.99,
                 min_temperature: float = 0.05):
        """
        Parámetros:
            initial_temperature: Temperatura inicial
            cooling_rate: Factor de enfriamiento por iteración
            min_temperature: Temperatura mínima
        """
        self.initial_temp = initial_temperature
        self.cooling_rate = cooling_rate
        self.min_temp = min_temperature
    
    def get_strength(self, iteration: int, **kwargs) -> float:
        """
        Calcular intensidad como función de temperatura.
        
        Temperatura = inicial * (cooling_rate ^ iteración)
        """
        temperature = self.initial_temp * (self.cooling_rate ** iteration)
        temperature = max(self.min_temp, temperature)
        return temperature


class HybridPerturbation(PerturbationSchedule):
    """
    Híbrida: Combina múltiples estrategias
    
    Permite mezclar comportamientos (ej: empezar lineal, terminar exponencial).
    """
    
    def __init__(self, schedules: List[PerturbationSchedule],
                 thresholds: List[int] = None):
        """
        Parámetros:
            schedules: Lista de estrategias a combinar
            thresholds: Iteraciones donde cambiar de estrategia
                       (default: espaciado igual)
        """
        self.schedules = schedules
        
        if thresholds is None:
            # Distribuir equitativamente
            self.thresholds = [int(x) for x in np.linspace(0, 1000, len(schedules) + 1)[1:]]
        else:
            self.thresholds = thresholds
    
    def get_strength(self, iteration: int, **kwargs) -> float:
        """
        Seleccionar estrategia según iteración actual.
        """
        for threshold, schedule in zip(self.thresholds, self.schedules):
            if iteration < threshold:
                return schedule.get_strength(iteration, **kwargs)
        
        # Por defecto, usar última estrategia
        return self.schedules[-1].get_strength(iteration, **kwargs)


# =============================================================================
# Funciones de utilidad
# =============================================================================

def create_schedule(schedule_type: str, **params) -> PerturbationSchedule:
    """
    Factory function para crear estrategias de perturbación.
    
    Parámetros:
        schedule_type: Tipo de estrategia
            - "constant": ConstantPerturbation
            - "linear": LinearPerturbation
            - "exponential": ExponentialPerturbation
            - "dynamic": DynamicPerturbation
            - "cyclical": CyclicalPerturbation
            - "temperature": AdaptiveTemperaturePerturbation
        **params: Parámetros específicos de la estrategia
    
    Retorna:
        PerturbationSchedule: Instancia de la estrategia
    """
    schedules = {
        'constant': ConstantPerturbation,
        'linear': LinearPerturbation,
        'exponential': ExponentialPerturbation,
        'dynamic': DynamicPerturbation,
        'cyclical': CyclicalPerturbation,
        'temperature': AdaptiveTemperaturePerturbation,
        'hybrid': HybridPerturbation,
    }
    
    if schedule_type not in schedules:
        raise ValueError(f"Estrategia desconocida: {schedule_type}")
    
    return schedules[schedule_type](**params)


def compare_schedules(iterations: int = 200) -> None:
    """
    Visualizar diferentes estrategias de perturbación.
    
    Parámetros:
        iterations: Número de iteraciones a mostrar
    """
    schedules = {
        'Constant': ConstantPerturbation(0.2),
        'Linear': LinearPerturbation(0.1, 0.5, 50),
        'Exponential': ExponentialPerturbation(0.1, 1.1),
        'Dynamic (5% mejora)': DynamicPerturbation(),
        'Cyclical': CyclicalPerturbation([0.1, 0.3, 0.5]),
        'Temperature': AdaptiveTemperaturePerturbation(1.0, 0.98),
    }
    
    print("Evolución de Intensidad de Perturbación\n")
    print(f"{'Iter':<6}", end='')
    for name in schedules.keys():
        print(f" {name:<12}", end='')
    print()
    print("-" * (6 + 14 * len(schedules)))
    
    no_improvement = 0
    improvement_history = [0.0] * 20
    
    for i in range(0, iterations, max(1, iterations // 10)):
        print(f"{i:<6}", end='')
        
        # Simular mejorar ocasionalmente
        if i % 30 == 0:
            improvement_history.append(0.5)
            no_improvement = 0
        else:
            improvement_history.append(0.0)
            no_improvement += 1
        
        for schedule in schedules.values():
            strength = schedule.get_strength(
                i,
                no_improvement_count=no_improvement,
                improvement_history=improvement_history
            )
            print(f" {strength:<12.3f}", end='')
        print()
    
    print("\n✓ Línea base: constant (0.2)")
    print("✓ Linear: Aumenta con iteraciones sin mejora")
    print("✓ Exponential: Aumento agresivo")
    print("✓ Dynamic: Adapta según historial")
    print("✓ Cyclical: Patrón cíclico")
    print("✓ Temperature: Enfriamiento gradual")


if __name__ == "__main__":
    compare_schedules(150)
