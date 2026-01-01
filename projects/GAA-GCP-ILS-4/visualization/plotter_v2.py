"""
visualization/plotter_v2.py

Gestor mejorado de ploteos con estructura multinivel:
- Nivel 1: Ploteos individuales por instancia
- Nivel 2: Ploteos agregados por familia
- Nivel 3: Ploteos comparativos entre familias
- Nivel 4: Resumen y síntesis

Estructura de outputs:
output/{timestamp}/plots/
├── 1_individual/
│   ├── instance_name/
│   │   ├── 01_convergence.png
│   │   ├── 02_fitness_distribution.png
│   │   ├── 03_conflict_heatmap.png
│   │   ├── 04_algorithm_performance.png
│   │   ├── 05_algorithm_gaps.png
│   │   └── 06_time_vs_quality.png
│   └── ...
├── 2_family/
│   ├── family_name/
│   │   ├── 01_scalability_time.png
│   │   ├── 02_scalability_quality.png
│   │   ├── 03_robustness_boxplot.png
│   │   ├── 04_algorithm_ranking.png
│   │   ├── 05_algorithm_comparison.png
│   │   ├── 06_gap_analysis.png
│   │   ├── 07_convergence_ensemble.png
│   │   └── 08_family_statistics.png
│   └── ...
├── 3_comparison/
│   ├── 01_families_scalability.png
│   ├── 02_families_robustness.png
│   ├── 03_families_algorithm_ranking.png
│   ├── 04_families_gap_distribution.png
│   ├── 05_families_convergence_speed.png
│   └── 06_all_families_summary.png
└── 4_summary/
    ├── README.md
    ├── experiment_summary.txt
    ├── key_findings.txt
    └── statistical_summary.txt
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime


class PlotManagerV2:
    """Gestor mejorado de ploteos con estructura multinivel"""
    
    def __init__(self, session_dir: str):
        """
        Inicializar PlotManagerV2
        
        Args:
            session_dir: Directorio de sesión (output/{timestamp}/)
        """
        self.session_dir = Path(session_dir)
        self.plots_dir = self.session_dir / "plots"
        
        # Crear estructura de directorios
        self.individual_dir = self.plots_dir / "1_individual"
        self.family_dir = self.plots_dir / "2_family"
        self.comparison_dir = self.plots_dir / "3_comparison"
        self.summary_dir = self.plots_dir / "4_summary"
        
        # Crear directorios
        for d in [self.individual_dir, self.family_dir, self.comparison_dir, self.summary_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        # Logger
        self.logger = logging.getLogger(__name__)
    
    # ========================================================================
    # NIVEL 1: PLOTEOS INDIVIDUALES POR INSTANCIA
    # ========================================================================
    
    def plot_instance_convergence(self, 
                                  instance_name: str,
                                  fitness_history: List[float],
                                  times: Optional[List[float]] = None) -> str:
        """Ploteo 01: Convergencia de instancia individual"""
        try:
            instance_dir = self.individual_dir / instance_name
            instance_dir.mkdir(parents=True, exist_ok=True)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if times:
                ax.plot(times, fitness_history, 'b-', linewidth=2, label='Fitness')
            else:
                ax.plot(fitness_history, 'b-', linewidth=2, label='Fitness')
            
            ax.set_xlabel('Iteration' if not times else 'Time (s)', fontsize=12)
            ax.set_ylabel('Fitness (Number of Colors)', fontsize=12)
            ax.set_title(f'Current fitness trajectory during ILS execution: {instance_name}', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            filepath = instance_dir / "01_current_fitness_trajectory_ils.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Ploteo individual current fitness trajectory: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error en ploteo convergencia: {e}")
            return ""
    
    def plot_instance_fitness_distribution(self,
                                          instance_name: str,
                                          fitness_values: List[float]) -> str:
        """Ploteo 02: Distribución de fitness"""
        try:
            instance_dir = self.individual_dir / instance_name
            instance_dir.mkdir(parents=True, exist_ok=True)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            ax.hist(fitness_values, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
            ax.axvline(np.mean(fitness_values), color='red', linestyle='--', 
                      linewidth=2, label=f'Mean (visited): {np.mean(fitness_values):.2f}')
            ax.axvline(np.median(fitness_values), color='green', linestyle='--',
                      linewidth=2, label=f'Median (visited): {np.median(fitness_values):.2f}')
            
            ax.set_xlabel('Fitness (Number of Colors)', fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.set_title(f'Distribution of visited solutions during ILS execution: {instance_name}', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
            
            filepath = instance_dir / "02_visited_solutions_distribution_ils.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Ploteo individual distribución: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error en ploteo distribución: {e}")
            return ""
    
    def plot_instance_algorithm_performance(self,
                                           instance_name: str,
                                           algorithm_results: Dict[str, float]) -> str:
        """Ploteo 04: Desempeño de 3 algoritmos en instancia"""
        try:
            instance_dir = self.individual_dir / instance_name
            instance_dir.mkdir(parents=True, exist_ok=True)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            algorithms = list(algorithm_results.keys())
            colors_obtained = list(algorithm_results.values())
            
            bars = ax.bar(algorithms, colors_obtained, color=['#1f77b4', '#ff7f0e', '#2ca02c'],
                         edgecolor='black', linewidth=1.5)
            
            # Agregar valores en las barras
            for bar, value in zip(bars, colors_obtained):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(value)}',
                       ha='center', va='bottom', fontsize=11, fontweight='bold')
            
            ax.set_xlabel('Algorithm', fontsize=12)
            ax.set_ylabel('Number of Colors', fontsize=12)
            ax.set_title(f'Final solution quality per algorithm (measured as number of colors): {instance_name}', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            
            filepath = instance_dir / "04_final_solution_quality_per_algorithm_measured_num_colors.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Ploteo individual desempeño: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error en ploteo desempeño: {e}")
            return ""
    
    def plot_instance_algorithm_gaps(self,
                                    instance_name: str,
                                    algorithm_gaps: Dict[str, float]) -> str:
        """Ploteo 05: Gaps de algoritmos en instancia"""
        try:
            instance_dir = self.individual_dir / instance_name
            instance_dir.mkdir(parents=True, exist_ok=True)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            algorithms = list(algorithm_gaps.keys())
            gaps = list(algorithm_gaps.values())
            
            colors = ['green' if g == 0 else 'orange' if g > 0 else 'red' for g in gaps]
            bars = ax.bar(algorithms, gaps, color=colors, edgecolor='black', linewidth=1.5, alpha=0.7)
            
            # Agregar valores en las barras
            for bar, value in zip(bars, gaps):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{value:+.2f}%',
                       ha='center', va='bottom' if value >= 0 else 'top', 
                       fontsize=11, fontweight='bold')
            
            ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
            ax.set_xlabel('Algorithm', fontsize=12)
            ax.set_ylabel('Optimality Gap (%)', fontsize=12)
            ax.set_title(f'Optimality gaps per algorithm relative to the best known solution (BKS): {instance_name}', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            
            filepath = instance_dir / "05_optimality_gaps_per_algorithm_bks.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Ploteo individual gaps: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error en ploteo gaps: {e}")
            return ""
    
    def plot_instance_conflict_heatmap(self,
                                      instance_name: str,
                                      conflict_matrix: np.ndarray) -> str:
        """Ploteo 03: Matriz de conflictos (aristas mal coloreadas)"""
        try:
            instance_dir = self.individual_dir / instance_name
            instance_dir.mkdir(parents=True, exist_ok=True)
            
            fig, ax = plt.subplots(figsize=(10, 10))
            
            im = ax.imshow(conflict_matrix, cmap='RdYlGn_r', aspect='auto')
            ax.set_xlabel('Vertex', fontsize=12)
            ax.set_ylabel('Vertex', fontsize=12)
            ax.set_title(f'Adjacency matrix (conflict structure) of instance {instance_name}', fontsize=14, fontweight='bold')
            
            plt.colorbar(im, ax=ax, label='Edge')
            
            filepath = instance_dir / "03_graph_adjacency_matrix.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Ploteo individual heatmap: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error en ploteo heatmap: {e}")
            return ""
    
    def plot_instance_time_vs_quality(self,
                                     instance_name: str,
                                     times: List[float],
                                     fitness_values: List[float]) -> str:
        """Ploteo 06: Tiempo vs Calidad"""
        try:
            instance_dir = self.individual_dir / instance_name
            instance_dir.mkdir(parents=True, exist_ok=True)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            ax.scatter(times, fitness_values, s=100, alpha=0.6, edgecolor='black', linewidth=1.5)
            ax.plot(times, fitness_values, 'b-', alpha=0.3, linewidth=1)
            
            ax.set_xlabel('Time (s)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Fitness (Number of Colors)', fontsize=12, fontweight='bold')
            ax.set_title(f'Temporal evolution of visited solution quality during ILS execution: {instance_name}', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            filepath = instance_dir / "06_visited_quality_time_evolution_ils.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Ploteo individual tiempo-calidad: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error en ploteo tiempo-calidad: {e}")
            return ""
    
    # ========================================================================
    # NIVEL 2: PLOTEOS AGREGADOS POR FAMILIA
    # ========================================================================
    
    def plot_family_scalability_time(self,
                                    family_name: str,
                                    instances: List[str],
                                    vertices: List[int],
                                    times: List[float]) -> str:
        """Ploteo 01: Escalabilidad (Tiempo vs Tamaño)"""
        try:
            family_dir = self.family_dir / family_name
            family_dir.mkdir(parents=True, exist_ok=True)
            
            fig, ax = plt.subplots(figsize=(12, 7))
            
            ax.plot(vertices, times, 'o-', linewidth=2.5, markersize=8, color='#1f77b4')
            
            # Anotaciones
            for i, (v, t, inst) in enumerate(zip(vertices, times, instances)):
                ax.annotate(inst, (v, t), textcoords="offset points", 
                           xytext=(0,10), ha='center', fontsize=9)
            
            ax.set_xlabel('Número de Vértices', fontsize=12, fontweight='bold')
            ax.set_ylabel('Tiempo de Ejecución (s)', fontsize=12, fontweight='bold')
            ax.set_title(f'Escalabilidad (Tiempo): Familia {family_name}', 
                        fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.set_xscale('log')
            ax.set_yscale('log')
            
            filepath = family_dir / "01_scalability_time.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Ploteo familia escalabilidad tiempo: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error en ploteo escalabilidad tiempo: {e}")
            return ""
    
    def plot_family_scalability_quality(self,
                                       family_name: str,
                                       instances: List[str],
                                       vertices: List[int],
                                       gaps: List[float]) -> str:
        """Ploteo 02: Escalabilidad (Calidad vs Tamaño)"""
        try:
            family_dir = self.family_dir / family_name
            family_dir.mkdir(parents=True, exist_ok=True)
            
            fig, ax = plt.subplots(figsize=(12, 7))
            
            colors = ['green' if g == 0 else 'orange' if g > 0 else 'red' for g in gaps]
            ax.scatter(vertices, gaps, s=200, c=colors, edgecolor='black', 
                      linewidth=1.5, alpha=0.7, zorder=3)
            
            # Anotaciones
            for i, (v, g, inst) in enumerate(zip(vertices, gaps, instances)):
                ax.annotate(inst, (v, g), textcoords="offset points",
                           xytext=(0,10), ha='center', fontsize=9)
            
            ax.axhline(y=0, color='black', linestyle='-', linewidth=1, zorder=1)
            ax.set_xlabel('Número de Vértices', fontsize=12, fontweight='bold')
            ax.set_ylabel('Gap (%)', fontsize=12, fontweight='bold')
            ax.set_title(f'Escalabilidad (Calidad): Familia {family_name}',
                        fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.set_xscale('log')
            
            filepath = family_dir / "02_scalability_quality.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Ploteo familia escalabilidad calidad: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error en ploteo escalabilidad calidad: {e}")
            return ""
    
    def plot_family_robustness_boxplot(self,
                                      family_name: str,
                                      algorithm_results: Dict[str, List[float]]) -> str:
        """Ploteo 03: Robustez (Boxplot de 3 algoritmos)"""
        try:
            family_dir = self.family_dir / family_name
            family_dir.mkdir(parents=True, exist_ok=True)
            
            fig, ax = plt.subplots(figsize=(12, 7))
            
            data = [algorithm_results[algo] for algo in sorted(algorithm_results.keys())]
            labels = sorted(algorithm_results.keys())
            
            bp = ax.boxplot(data, labels=labels, patch_artist=True,
                           notch=True, showmeans=True)
            
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            
            ax.set_ylabel('Colores Obtenidos', fontsize=12, fontweight='bold')
            ax.set_title(f'Robustez de Algoritmos: Familia {family_name}',
                        fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            
            filepath = family_dir / "03_robustness_boxplot.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Ploteo familia robustez: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error en ploteo robustez: {e}")
            return ""
    
    def plot_family_algorithm_ranking(self,
                                     family_name: str,
                                     algorithm_rankings: Dict[str, float]) -> str:
        """Ploteo 04: Ranking promedio de algoritmos"""
        try:
            family_dir = self.family_dir / family_name
            family_dir.mkdir(parents=True, exist_ok=True)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            algorithms = list(algorithm_rankings.keys())
            rankings = list(algorithm_rankings.values())
            
            bars = ax.barh(algorithms, rankings, color=['#1f77b4', '#ff7f0e', '#2ca02c'],
                          edgecolor='black', linewidth=1.5)
            
            # Agregar valores
            for bar, value in zip(bars, rankings):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2.,
                       f'{value:.2f}',
                       ha='left', va='center', fontsize=11, fontweight='bold')
            
            ax.set_xlabel('Ranking Promedio (menor = mejor)', fontsize=12, fontweight='bold')
            ax.set_title(f'Ranking de Algoritmos: Familia {family_name}',
                        fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='x')
            
            filepath = family_dir / "04_algorithm_ranking.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Ploteo familia ranking: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error en ploteo ranking: {e}")
            return ""
    
    def plot_family_gap_analysis(self,
                                family_name: str,
                                instances: List[str],
                                algorithm_gaps: Dict[str, List[float]]) -> str:
        """Ploteo 06: Análisis de gaps por instancia"""
        try:
            family_dir = self.family_dir / family_name
            family_dir.mkdir(parents=True, exist_ok=True)
            
            fig, ax = plt.subplots(figsize=(14, 7))
            
            x = np.arange(len(instances))
            width = 0.25
            
            for i, (algo, gaps) in enumerate(sorted(algorithm_gaps.items())):
                offset = (i - 1) * width
                ax.bar(x + offset, gaps, width, label=algo, alpha=0.8)
            
            ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
            ax.set_xlabel('Instancia', fontsize=12, fontweight='bold')
            ax.set_ylabel('Gap (%)', fontsize=12, fontweight='bold')
            ax.set_title(f'Análisis de Gaps: Familia {family_name}',
                        fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(instances, rotation=45, ha='right')
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
            
            filepath = family_dir / "06_gap_analysis.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Ploteo familia análisis gaps: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error en ploteo análisis gaps: {e}")
            return ""
    
    # ========================================================================
    # NIVEL 3: PLOTEOS COMPARATIVOS ENTRE FAMILIAS
    # ========================================================================
    
    def plot_families_scalability_comparison(self,
                                            families_data: Dict[str, Dict[str, Any]]) -> str:
        """Ploteo 01: Escalabilidad comparativa entre familias"""
        try:
            fig, ax = plt.subplots(figsize=(14, 8))
            
            colors_map = {'MYCIEL': '#1f77b4', 'DSJ': '#ff7f0e', 'LEI': '#2ca02c',
                         'REG': '#d62728', 'SCH': '#9467bd', 'SGB': '#8c564b'}
            
            for family_name, data in families_data.items():
                if 'vertices' in data and 'times' in data:
                    color = colors_map.get(family_name, '#1f77b4')
                    ax.plot(data['vertices'], data['times'], 'o-', 
                           linewidth=2.5, markersize=8, label=family_name, color=color)
            
            ax.set_xlabel('Número de Vértices', fontsize=12, fontweight='bold')
            ax.set_ylabel('Tiempo de Ejecución (s)', fontsize=12, fontweight='bold')
            ax.set_title('Escalabilidad Comparativa: Todas las Familias',
                        fontsize=14, fontweight='bold')
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3)
            ax.set_xscale('log')
            ax.set_yscale('log')
            
            filepath = self.comparison_dir / "01_families_scalability.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Ploteo comparativo escalabilidad: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error en ploteo comparativo escalabilidad: {e}")
            return ""
    
    def plot_families_robustness_comparison(self,
                                           families_data: Dict[str, Dict[str, Any]]) -> str:
        """Ploteo 02: Robustez comparativa entre familias"""
        try:
            fig, ax = plt.subplots(figsize=(14, 8))
            
            colors_map = {'MYCIEL': '#1f77b4', 'DSJ': '#ff7f0e', 'LEI': '#2ca02c',
                         'REG': '#d62728', 'SCH': '#9467bd', 'SGB': '#8c564b'}
            
            positions = []
            labels = []
            pos = 0
            
            for family_name, data in families_data.items():
                if 'algorithm_results' in data:
                    for algo_name, results in data['algorithm_results'].items():
                        color = colors_map.get(family_name, '#1f77b4')
                        bp = ax.boxplot([results], positions=[pos], widths=0.6,
                                       patch_artist=True, showmeans=True)
                        for patch in bp['boxes']:
                            patch.set_facecolor(color)
                            patch.set_alpha(0.7)
                        positions.append(pos)
                        labels.append(f"{family_name}\n{algo_name}")
                        pos += 1
                    pos += 1
            
            ax.set_xticks(positions)
            ax.set_xticklabels(labels, fontsize=9)
            ax.set_ylabel('Colores Obtenidos', fontsize=12, fontweight='bold')
            ax.set_title('Robustez Comparativa: Todas las Familias',
                        fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            
            filepath = self.comparison_dir / "02_families_robustness.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Ploteo comparativo robustez: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error en ploteo comparativo robustez: {e}")
            return ""
    
    # ========================================================================
    # NIVEL 4: RESUMEN Y SÍNTESIS
    # ========================================================================
    
    def create_summary_readme(self) -> str:
        """Crear README con guía de interpretación"""
        try:
            readme_content = """# 📊 Guía de Interpretación de Ploteos

## Estructura de Directorios

### 1_individual/
Ploteos específicos de cada instancia del problema:
- **01_convergence.png**: Convergencia del algoritmo ILS en esta instancia
- **02_fitness_distribution.png**: Distribución de soluciones encontradas
- **03_conflict_heatmap.png**: Matriz de conflictos (aristas mal coloreadas)
- **04_algorithm_performance.png**: Comparación de 3 algoritmos GAA
- **05_algorithm_gaps.png**: Gaps de los 3 algoritmos respecto a BKS
- **06_time_vs_quality.png**: Relación tiempo vs calidad

### 2_family/
Ploteos agregados de cada familia de datasets:
- **01_scalability_time.png**: Cómo escala el tiempo con el tamaño
- **02_scalability_quality.png**: Cómo escala la calidad con el tamaño
- **03_robustness_boxplot.png**: Robustez de los 3 algoritmos
- **04_algorithm_ranking.png**: Ranking promedio de algoritmos
- **05_algorithm_comparison.png**: Comparación detallada
- **06_gap_analysis.png**: Análisis de gaps por instancia
- **07_convergence_ensemble.png**: Convergencia promediada
- **08_family_statistics.png**: Estadísticas de la familia

### 3_comparison/
Ploteos comparativos entre familias:
- **01_families_scalability.png**: Escalabilidad de todas las familias
- **02_families_robustness.png**: Robustez de todas las familias
- **03_families_algorithm_ranking.png**: Ranking entre familias
- **04_families_gap_distribution.png**: Distribución de gaps
- **05_families_convergence_speed.png**: Velocidad de convergencia
- **06_all_families_summary.png**: Resumen general

### 4_summary/
Documentación y síntesis:
- **README.md**: Esta guía
- **experiment_summary.txt**: Resumen ejecutivo
- **key_findings.txt**: Hallazgos principales
- **statistical_summary.txt**: Resumen estadístico

## Cómo Interpretar los Ploteos

### Convergencia
- Línea descendente = Mejora progresiva
- Línea plana = Estancamiento
- Descensos abruptos = Perturbaciones efectivas

### Escalabilidad
- Línea recta en log-log = Complejidad polinomial
- Línea exponencial = Complejidad exponencial
- Puntos dispersos = Variabilidad en instancias

### Robustez (Boxplot)
- Caja pequeña = Resultados consistentes
- Caja grande = Resultados variables
- Outliers = Instancias problemáticas

### Gaps
- Gap = 0% = Óptimo encontrado
- Gap > 0% = Peor que óptimo
- Gap < 0% = Mejor que óptimo (imposible, indica error)

## Análisis Recomendado

1. **Comienza por 2_family/**: Entiende el desempeño general
2. **Luego 1_individual/**: Identifica instancias problemáticas
3. **Finalmente 3_comparison/**: Valida generalización
4. **Consulta 4_summary/**: Lee conclusiones

---

Documento generado: {timestamp}
"""
            
            filepath = self.summary_dir / "README.md"
            with open(filepath, 'w') as f:
                f.write(readme_content.format(timestamp=datetime.now().isoformat()))
            
            self.logger.info(f"README creado: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error creando README: {e}")
            return ""
