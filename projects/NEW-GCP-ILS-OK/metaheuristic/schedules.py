"""
Perturbation Schedules for ILS

Define como cambia la intensidad de perturbacion durante la busqueda.
"""

from typing import Optional, Callable
import numpy as np


class PerturbationSchedule:
    """
    Base class para estrategias de perturbacion
    """
    
    def get_strength(self, iteration: int, max_iterations: int) -> float:
        """
        Obtiene fuerza de perturbacion para iteracion dada
        
        Args:
            iteration: Iteracion actual (0-based)
            max_iterations: Total de iteraciones
        
        Returns:
            Fuerza (0-1)
        """
        raise NotImplementedError


class ConstantPerturbation(PerturbationSchedule):
    """
    Perturbacion constante
    
    Mantiene la misma fuerza durante toda la busqueda.
    """
    
    def __init__(self, strength: float = 0.1):
        """
        Args:
            strength: Fuerza constante
        """
        self.strength = strength
    
    def get_strength(self, iteration: int, max_iterations: int) -> float:
        return self.strength


class LinearDecayPerturbation(PerturbationSchedule):
    """
    Decaimiento lineal de perturbacion
    
    Comienza con fuerza alta y disminuye linealmente a cero.
    Efecto: Exploracion intensa al inicio, explotacion al final.
    """
    
    def __init__(self, initial_strength: float = 0.3, final_strength: float = 0.01):
        """
        Args:
            initial_strength: Fuerza inicial
            final_strength: Fuerza final
        """
        self.initial_strength = initial_strength
        self.final_strength = final_strength
    
    def get_strength(self, iteration: int, max_iterations: int) -> float:
        if max_iterations == 0:
            return self.initial_strength
        
        ratio = iteration / max_iterations
        return self.initial_strength - ratio * (self.initial_strength - self.final_strength)


class ExponentialDecayPerturbation(PerturbationSchedule):
    """
    Decaimiento exponencial de perturbacion
    
    Decae exponencialmente: strength = initial * exp(-rate * t)
    Efecto: Decaimiento rapido al inicio, luego lento
    """
    
    def __init__(self, initial_strength: float = 0.3, decay_rate: float = 5.0):
        """
        Args:
            initial_strength: Fuerza inicial
            decay_rate: Tasa de decaimiento
        """
        self.initial_strength = initial_strength
        self.decay_rate = decay_rate
    
    def get_strength(self, iteration: int, max_iterations: int) -> float:
        if max_iterations == 0:
            return self.initial_strength
        
        ratio = iteration / max_iterations
        return self.initial_strength * np.exp(-self.decay_rate * ratio)


class ExplorationExploitationPerturbation(PerturbationSchedule):
    """
    Balanceo dinámico de exploracion-explotacion
    
    Comienza con exploracion (fuerza alta), transiciona a explotacion (fuerza baja).
    """
    
    def __init__(self, initial_strength: float = 0.3, final_strength: float = 0.01,
                 transition_point: float = 0.5):
        """
        Args:
            initial_strength: Fuerza en fase de exploracion
            final_strength: Fuerza en fase de explotacion
            transition_point: Punto de transicion (0-1, fraccion de iteraciones)
        """
        self.initial_strength = initial_strength
        self.final_strength = final_strength
        self.transition_point = transition_point
    
    def get_strength(self, iteration: int, max_iterations: int) -> float:
        if max_iterations == 0:
            return self.initial_strength
        
        ratio = iteration / max_iterations
        
        if ratio < self.transition_point:
            # Fase de exploracion: mantener fuerza
            return self.initial_strength
        else:
            # Fase de explotacion: decrecer linealmente
            decay_ratio = (ratio - self.transition_point) / (1.0 - self.transition_point)
            return self.initial_strength - decay_ratio * (self.initial_strength - self.final_strength)


class AdaptivePerturbationSchedule(PerturbationSchedule):
    """
    Adaptacion basada en progreso de busqueda
    
    Aumenta fuerza si no hay mejora, disminuye si hay mejora.
    """
    
    def __init__(self, initial_strength: float = 0.1,
                 min_strength: float = 0.01,
                 max_strength: float = 0.5,
                 increase_factor: float = 1.1,
                 decrease_factor: float = 0.9):
        """
        Args:
            initial_strength: Fuerza inicial
            min_strength: Fuerza minima
            max_strength: Fuerza maxima
            increase_factor: Factor para aumentar fuerza
            decrease_factor: Factor para disminuir fuerza
        """
        self.strength = initial_strength
        self.min_strength = min_strength
        self.max_strength = max_strength
        self.increase_factor = increase_factor
        self.decrease_factor = decrease_factor
    
    def adapt(self, improved: bool):
        """
        Adapta fuerza basada en si hubo mejora
        
        Args:
            improved: Si la iteracion anterior mejoro
        """
        if improved:
            self.strength *= self.decrease_factor
        else:
            self.strength *= self.increase_factor
        
        # Clampear a limites
        self.strength = np.clip(self.strength, self.min_strength, self.max_strength)
    
    def get_strength(self, iteration: int, max_iterations: int) -> float:
        return self.strength


class CyclicPerturbation(PerturbationSchedule):
    """
    Perturbacion ciclica
    
    La fuerza oscila entre valores minimo y maximo.
    Efecto: Alternar entre fases de exploracion y explotacion
    """
    
    def __init__(self, min_strength: float = 0.05,
                 max_strength: float = 0.3,
                 cycle_length: int = 50):
        """
        Args:
            min_strength: Fuerza minima
            max_strength: Fuerza maxima
            cycle_length: Iteraciones por ciclo
        """
        self.min_strength = min_strength
        self.max_strength = max_strength
        self.cycle_length = cycle_length
    
    def get_strength(self, iteration: int, max_iterations: int) -> float:
        # Onda seno escalada
        cycle_position = (iteration % self.cycle_length) / self.cycle_length
        strength = self.min_strength + (self.max_strength - self.min_strength) * \
                   (0.5 + 0.5 * np.sin(2 * np.pi * cycle_position - np.pi / 2))
        return strength


class DynamicPerturbationSchedule(PerturbationSchedule):
    """
    Perturbacion dinamica basada en velocidad de mejora
    
    Si mejoras son lentas: aumentar exploracion
    Si mejoras son rapidas: mantener explotacion actual
    """
    
    def __init__(self, initial_strength: float = 0.15,
                 min_strength: float = 0.05,
                 max_strength: float = 0.4,
                 window_size: int = 10,
                 threshold_improvements: float = 0.2):
        """
        Args:
            initial_strength: Fuerza inicial
            min_strength: Fuerza minima
            max_strength: Fuerza maxima
            window_size: Ventana para calcular velocidad de mejora
            threshold_improvements: Umbral de mejoras (0-1) para adaptar
        """
        self.strength = initial_strength
        self.min_strength = min_strength
        self.max_strength = max_strength
        self.window_size = window_size
        self.threshold_improvements = threshold_improvements
        self.improvement_history = []
    
    def record_improvement(self, improved: bool):
        """Registra si hubo mejora"""
        self.improvement_history.append(improved)
        if len(self.improvement_history) > self.window_size:
            self.improvement_history.pop(0)
    
    def adapt(self):
        """Adapta fuerza basada en historial de mejoras"""
        if len(self.improvement_history) == self.window_size:
            improvement_rate = sum(self.improvement_history) / self.window_size
            
            if improvement_rate < self.threshold_improvements:
                # Pocas mejoras: aumentar exploracion
                self.strength *= 1.1
            else:
                # Muchas mejoras: mantener/reducir
                self.strength *= 0.95
            
            self.strength = np.clip(self.strength, self.min_strength, self.max_strength)
    
    def get_strength(self, iteration: int, max_iterations: int) -> float:
        return self.strength
