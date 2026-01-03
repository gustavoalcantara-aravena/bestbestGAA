# Guía de Uso - Parameter Tuning para Algorithm 3 (Familia C1)

## Resumen Ejecutivo

Se han creado **dos scripts complementarios** para optimizar los parámetros del **Algoritmo 3** en la familia **C1**:

1. **`parameter_optimizer_c1.py`** - Framework completo de optimización (más detallado)
2. **`parameter_tuner_algo3.py`** - Script más ágil y directo (recomendado para iniciar)

---

## Archivo 1: `parameter_tuner_algo3.py` ⭐ RECOMENDADO PARA COMENZAR

### Descripción
Script optimizado para buscar los mejores parámetros del Algoritmo 3.

### Uso Básico

```bash
# Búsqueda de 100 combinaciones (recomendado para inicio)
python parameter_tuner_algo3.py --num-combinations 100

# Búsqueda de 50 combinaciones (prueba rápida)
python parameter_tuner_algo3.py --num-combinations 50 --output-dir test_results

# Búsqueda de 200 combinaciones (búsqueda exhaustiva)
python parameter_tuner_algo3.py --num-combinations 200
```

### Estructura de Salida

```
optimization_results_c1/
├── combinations.json          # Todas las 100 combinaciones generadas
├── results.json              # Resultados detallados por combinación
└── report.txt                # Reporte en texto con Top 10
```

### Ejemplo de Salida en Consola

```
================================================================================
PARAMETER TUNING - Algorithm 3 - Family C1
Combinaciones a probar: 100
Instancias: C1 (9 instancias)
Timestamp: 2026-01-03 10:30:45
================================================================================

[1/4] Generando 100 combinaciones...
      [OK] 100 combinaciones generadas

[2/4] Ejecutando búsqueda de parámetros...

  [  1/100] W:100 2OP:45 DB:1.5 2POST:40 REL:35
       [OK] Score=2.531, GAP_K=1.23%, GAP_D=1.31%, Time=45.3s

  [  2/100] W:120 2OP:65 DB:2.1 2POST:55 REL:28
       [OK] Score=3.845, GAP_K=1.89%, GAP_D=1.96%, Time=48.1s

  [  3/100] W:80 2OP:30 DB:0.8 2POST:25 REL:15
       [OK] Score=4.120, GAP_K=2.12%, GAP_D=2.01%, Time=42.7s

  ...

[3/4] Analizando resultados...

  Top 10 Combinaciones:
    #1: W:95 2OP:50 DB:1.2 2POST:42 REL:32 → Score=1.987
    #2: W:90 2OP:48 DB:1.3 2POST:40 REL:33 → Score=2.012
    #3: W:105 2OP:52 DB:1.1 2POST:44 REL:34 → Score=2.045
    ...

[4/4] Generando reportes...

  Resultados JSON:  optimization_results_c1/results.json
  Reporte Texto:    optimization_results_c1/report.txt

================================================================================
[OK] OPTIMIZACIÓN COMPLETADA
[OK] Tiempo total: 165.3 minutos (2.75 horas)
[OK] Resultados: 100/100
[OK] Archivos: optimization_results_c1
================================================================================
```

---

## Archivo 2: `parameter_optimizer_c1.py` (Alternativa Avanzada)

### Descripción
Framework más completo con análisis estadísticos adicionales.

### Uso

```bash
python parameter_optimizer_c1.py
```

### Estructura Adicional
- Análisis de sensibilidad de parámetros
- Gráficos de convergencia
- Estadísticas de distribución

---

## Flujo de Trabajo Recomendado

### Paso 1: Prueba Rápida (10 min)

```bash
python parameter_tuner_algo3.py --num-combinations 10 --output-dir test_quick
```

**Resultado esperado**: Validar que el script funciona correctamente.

### Paso 2: Búsqueda Principal (3-4 horas)

```bash
python parameter_tuner_algo3.py --num-combinations 100
```

**Resultado esperado**:
- Archivo `optimization_results_c1/results.json` con 100 combinaciones
- Archivo `optimization_results_c1/report.txt` con Top 10
- Identificar mejor combinación

### Paso 3: Refinamiento (Opcional - 1-2 horas)

Si quieres ser más exhaustivo:

```bash
python parameter_tuner_algo3.py --num-combinations 200
```

---

## Interpretación de Resultados

### Archivo `report.txt`

```
TOP 10 BEST COMBINATIONS
================================================================================

#1: Score = 1.987456

  Parámetros: While=95, 2Opt_pre=50, DB=1.2, 2Opt_post=42, Relocate=32
  Avg GAP_K: 0.876%
  Avg GAP_D: 1.111%
  Exec Time: 45.3s

#2: Score = 2.012389

  Parámetros: While=90, 2Opt_pre=48, DB=1.3, 2Opt_post=40, Relocate=33
  Avg GAP_K: 0.923%
  Avg GAP_D: 1.089%
  Exec Time: 44.1s

...

STATISTICS
================================================================================
Best Score:   1.234567
Worst Score:  5.678901
Avg Score:    3.456789
Median Score: 3.234567
Std Dev:      0.987654
```

**Interpretación**:
- **Score = 1.987**: Suma de GAP_K + GAP_D. Menor es mejor.
- **GAP_K = 0.876%**: Desviación respecto a BKS de vehículos (0.876% sobre óptimo)
- **GAP_D = 1.111%**: Desviación respecto a BKS de distancia (1.111% sobre óptimo)

---

## Archivo `results.json`

Contiene toda la información detallada por combinación:

```json
[
  {
    "combo_id": 1,
    "parameters": {
      "while": 95,
      "twoopt_pre": 50,
      "doublebridge": 1.2,
      "twoopt_post": 42,
      "relocate": 32
    },
    "instance_results": {
      "C101": {"k": 10.0, "d": 828.99, "gap_k": 0.0, "gap_d": 0.001},
      "C102": {"k": 10.0, "d": 828.95, "gap_k": 0.0, "gap_d": -0.002},
      ...
    },
    "avg_gap_k": 0.876,
    "avg_gap_d": 1.111,
    "score": 1.987,
    "rank": 1,
    "exec_time": 45.3,
    "timestamp": "2026-01-03T10:30:45.123456"
  },
  ...
]
```

---

## Parámetros Explorados

### Rangos Predeterminados

| Parámetro | Mínimo | Máximo | Descripción |
|-----------|--------|--------|-------------|
| **While** | 50 | 150 | Iteraciones principales del ILS |
| **TwoOpt (pre)** | 20 | 80 | Movimientos 2-opt antes de perturbación |
| **DoubleBridge** | 0.5 | 3.0 | Intensidad de perturbación ILS |
| **TwoOpt (post)** | 20 | 80 | Movimientos 2-opt después de perturbación |
| **Relocate** | 10 | 50 | Movimientos de reubicación final |

### Personalización

Si quieres cambiar los rangos, edita `parameter_tuner_algo3.py`:

```python
# En la clase ParameterGenerator
RANGES = {
    'while': (50, 150, 10),           # Cambiar aquí
    'twoopt_pre': (20, 80, 5),        # Cambiar aquí
    'doublebridge': (0.5, 3.0, 0.5),  # Cambiar aquí
    'twoopt_post': (20, 80, 5),       # Cambiar aquí
    'relocate': (10, 50, 5)           # Cambiar aquí
}
```

---

## Flujo de Actualización de Parámetros

El script realiza estos pasos para cada combinación:

```
1. Generar parámetros aleatorios
   ↓
2. Actualizar src/gaa/algorithm_generator.py con nuevos parámetros del Algo3
   ↓
3. Ejecutar: python scripts/experiments.py --mode QUICK (solo C1)
   ↓
4. Recolectar resultados (K, D para cada instancia C1)
   ↓
5. Calcular GAP_K y GAP_D respecto a BKS
   ↓
6. Guardar resultados y continuar con siguiente combinación
```

---

## Análisis Post-Optimización

Una vez completada la búsqueda de 100 combinaciones:

### 1. Identificar Mejor Combinación

```bash
grep "^#1:" optimization_results_c1/report.txt
```

Resultado:
```
#1: Score = 1.987456
  Parámetros: While=95, 2Opt_pre=50, DB=1.2, 2Opt_post=42, Relocate=32
```

### 2. Extraer Parámetros Óptimos

Desde `results.json`:
```python
import json

with open('optimization_results_c1/results.json') as f:
    results = json.load(f)

best = results[0]  # Ya está ordenado por score
print(f"Mejores parámetros Algo3:")
print(f"  While: {best['parameters']['while']}")
print(f"  TwoOpt (pre): {best['parameters']['twoopt_pre']}")
print(f"  DoubleBridge: {best['parameters']['doublebridge']}")
print(f"  TwoOpt (post): {best['parameters']['twoopt_post']}")
print(f"  Relocate: {best['parameters']['relocate']}")
```

### 3. Aplicar Parámetros al Código

Una vez identificada la mejor combinación, actualizar `src/gaa/algorithm_generator.py`:

```python
def generate_three_algorithms(self, seed: int = 42) -> List[ASTNode]:
    """
    ALGORITMO 3: MÁXIMA EXPLORACIÓN (OPTIMIZADO ITER-8)
    
    Parámetros optimizados para familia C1:
    - While: 95          # Iteraciones principales
    - TwoOpt (pre): 50   # Movimientos pre-perturbación
    - DoubleBridge: 1.2  # Intensidad de perturbación
    - TwoOpt (post): 42  # Movimientos post-perturbación
    - Relocate: 32       # Movimientos finales
    """
    ...
```

---

## Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'experiments'"

**Solución**: Ejecutar desde la raíz del proyecto:
```bash
cd c:\Users\alfab\Desktop\bestbestGAA\projects\GAA-VRPTW-GRASP-2
python parameter_tuner_algo3.py
```

### Problema: "best_known_solutions.json not found"

**Solución**: Verificar que el archivo existe en la raíz:
```bash
ls best_known_solutions.json
```

### Problema: Ejecución muy lenta (más de 3 horas para 100 combos)

**Solución 1**: Reducir a 50 combinaciones
```bash
python parameter_tuner_algo3.py --num-combinations 50
```

**Solución 2**: Aumentar timeout en ExperimentRunner (en script)
```python
timeout=600,  # Cambiar a 300 si es muy lento
```

---

## Próximos Pasos Recomendados

1. **Completar búsqueda C1** (100 combinaciones) ✓
2. **Aplicar mejores parámetros a Algo3** en `algorithm_generator.py`
3. **Validar resultados** ejecutando FULL experiment
4. **Extender a otras familias** (R1, RC1, etc.)
5. **Optimización multi-familia** para encontrar parámetros universales

---

## Referencias

- `PLAN_OPTIMIZACION_C1.md` - Plan detallado
- `parameter_optimizer_c1.py` - Versión alternativa
- `best_known_solutions.json` - Valores de referencia
- `src/gaa/algorithm_generator.py` - Donde se aplican los parámetros

