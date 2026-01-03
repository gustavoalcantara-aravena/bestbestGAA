# Cálculo de GAP: Métricas de Desempeño

**Documentación técnica del cálculo de brecha (Gap) respecto a Best Known Solutions**

---

## 1. ¿Qué es el GAP?

El **GAP (Brecha)** es la diferencia entre la solución encontrada por un algoritmo y la mejor solución conocida (Best Known Solution - BKS) para una instancia específica.

### Fórmula

```
gap_percent = ((d_final - d_bks) / d_bks) × 100%
```

**Donde:**
- `d_final` = distancia total encontrada por el algoritmo
- `d_bks` = distancia total de la mejor solución conocida

### Interpretación

```
gap_percent = 0%   → Solución óptima (igual a BKS)
gap_percent > 0%   → Solución peor que BKS
gap_percent < 0%   → Solución mejor que BKS (raro)
```

---

## 2. Archivo de Best Known Solutions (BKS)

### Ubicación
```
datasets/bks.json
```

### Estructura
```json
{
  "C1/C101": {
    "K": 10,
    "D": 828.94,
    "Description": "Clustered instance 1"
  },
  "C1/C102": {
    "K": 10,
    "D": 828.94
  },
  "R1/R101": {
    "K": 19,
    "D": 1650.8
  },
  ...
}
```

**Formato clave:**
- `"{FAMILY}/{INSTANCE_ID}"` → ejemplo: `"R1/R101"`, `"C1/C101"`, `"RC1/RC101"`

**Valores BKS:**
- `K` = número de vehículos (solución óptima o mejor conocida)
- `D` = distancia total mínima (mejor solución conocida)

### Ejemplo Real
```json
{
  "R1/R101": { "K": 19, "D": 1650.8 },
  "R1/R102": { "K": 17, "D": 1487.0 },
  "R1/R103": { "K": 13, "D": 1292.7 },
  "R1/R104": { "K": 9, "D": 1084.4 },
  "R1/R105": { "K": 14, "D": 1377.0 },
  "R1/R106": { "K": 12, "D": 1251.1 },
  "R1/R107": { "K": 10, "D": 1104.1 },
  "R1/R108": { "K": 9, "D": 960.8 },
  "R1/R109": { "K": 11, "D": 1194.7 },
  "R1/R110": { "K": 10, "D": 1118.6 },
  "R1/R111": { "K": 10, "D": 1096.7 },
  "R1/R112": { "K": 9, "D": 982.1 }
}
```

---

## 3. Flujo de Cálculo en `experiments.py`

### Paso 1: Carga de BKS

```python
# scripts/experiments.py :: ExperimentExecutor.__init__()

def _load_bks(self) -> Dict:
    """Load Best Known Solutions from JSON"""
    bks_file = Path('datasets') / 'bks.json'
    if bks_file.exists():
        with open(bks_file) as f:
            return json.load(f)  # Retorna dict con BKS
    return {}

# En __init__:
self.bks_data = self._load_bks()
# Resultado: {
#   "R1/R101": {"K": 19, "D": 1650.8},
#   "R1/R102": {"K": 17, "D": 1487.0},
#   ...
# }
```

### Paso 2: Búsqueda de BKS para cada Instancia

```python
# scripts/experiments.py :: ExperimentExecutor.add_result()

def add_result(self, metric_dict: Dict = None):
    """Add experiment result with BKS lookup"""
    
    result = metric_dict.copy()
    
    instance_id = result.get('instance_id')  # ej: 'R101'
    family = result.get('family')             # ej: 'R1'
    
    # Búsqueda: "R1/R101"
    if instance_id and family:
        bks_key = f"{family}/{instance_id}"   # Construct key
        
        if bks_key in self.bks_data:
            bks = self.bks_data[bks_key]       # Obtener BKS
            result['k_bks'] = bks.get('K')     # K BKS
            result['d_bks'] = bks.get('D')     # D BKS
        # Si no existe BKS, queda como None
    
    self.raw_results.append(result)
```

### Paso 3: Cálculo de GAP en Resultados

```python
# scripts/experiments.py :: ExperimentExecutor.add_result()

# Después de obtener BKS:
result = {
    'algorithm': algo_name,           # GRASP, VND, ILS
    'instance_id': instance_id,       # R101, C102, etc
    'family': family,                 # R1, C1, RC2, etc
    'k_final': k_final,               # Vehículos encontrados
    'd_final': d_final,               # Distancia encontrada
    'k_bks': bks.get('K'),           # Vehículos BKS
    'd_bks': bks.get('D'),           # Distancia BKS
    'time_sec': elapsed,              # Tiempo ejecución
    'status': 'success',
    
    # CÁLCULOS DERIVADOS:
    'delta_K': k_final - k_bks if (k_final is not None and k_bks is not None) else None,
    'reached_K_BKS': (k_final == k_bks) if (k_final is not None and k_bks is not None) else None,
    'gap_distance': d_final - d_bks if (k_final == k_bks and d_final is not None and d_bks is not None) else None,
    'gap_percent': ((d_final - d_bks) / d_bks * 100) if (k_final == k_bks and d_final is not None and d_bks is not None) else None,
}
```

---

## 4. Métricas Calculadas

### 4.1 Delta K (Diferencia de Vehículos)
```python
delta_K = k_final - k_bks

Ejemplo:
  BKS: K=10 vehículos
  Encontrado: K=12 vehículos
  delta_K = 12 - 10 = +2

Interpretación:
  delta_K = 0  → Mismo número de vehículos
  delta_K > 0  → Usamos más vehículos (peor)
  delta_K < 0  → Usamos menos vehículos (mejor)
```

### 4.2 Reached K BKS (Alcanzó BKS)
```python
reached_K_BKS = (k_final == k_bks)

Retorna: True/False
  True  → Encontramos la misma cantidad de vehículos que BKS
  False → Diferente cantidad de vehículos

Importancia:
  Solo se calcula GAP si reached_K_BKS == True
```

### 4.3 GAP Distance (Brecha en Distancia)
```python
gap_distance = d_final - d_bks

SOLO se calcula si k_final == k_bks

Ejemplo:
  BKS: D=1650.8 km
  Encontrado: D=1670.5 km
  gap_distance = 1670.5 - 1650.8 = +19.7 km

Interpretación:
  gap_distance = 0    → Distancia óptima
  gap_distance > 0    → Distancia mayor (peor)
  gap_distance < 0    → Distancia menor (mejor)
```

### 4.4 GAP Percent (Brecha Porcentual)
```python
gap_percent = ((d_final - d_bks) / d_bks) * 100

SOLO se calcula si k_final == k_bks

Ejemplo:
  BKS: D=1650.8 km
  Encontrado: D=1670.5 km
  gap_percent = ((1670.5 - 1650.8) / 1650.8) * 100
              = (19.7 / 1650.8) * 100
              = 1.19%

Interpretación:
  gap_percent = 0%   → Óptimo
  gap_percent = 1.5% → Solución a 1.5% de óptimo
  gap_percent = 5%   → Solución a 5% de óptimo
```

---

## 5. Flujo Completo en Experimento QUICK

```
┌──────────────────────────────────────────────────────────────┐
│         INICIO EXPERIMENTO QUICK                            │
│         12 instancias × 3 algoritmos = 36 ejecuciones      │
└──────────────────────────────────────────────────────────────┘
                              │
                              ↓
                 ┌────────────────────────┐
                 │  CARGAR BKS (Paso 1)  │
                 │                        │
                 │ bks_data = {           │
                 │   "R1/R101": {...},    │
                 │   "R1/R102": {...},    │
                 │   ...                  │
                 │ }                      │
                 └────────────────────────┘
                              │
                              ↓
                 FOR familia IN ['R1']:
                   FOR instancia IN [R101..R112]:
                     FOR algoritmo IN [GRASP, VND, ILS]:
                              │
                              ↓
                     ┌────────────────────────┐
                     │  EJECUTAR ALGORITMO    │
                     │                        │
                     │ resultado = algo.solve │
                     │ k_final = resultado.k  │
                     │ d_final = resultado.d  │
                     │ time_sec = elapsed     │
                     └────────────────────────┘
                              │
                              ↓
                     ┌────────────────────────┐
                     │  BUSCAR BKS (Paso 2)   │
                     │                        │
                     │ key = "R1/R101"        │
                     │ bks = bks_data[key]    │
                     │ k_bks = bks['K']       │
                     │ d_bks = bks['D']       │
                     └────────────────────────┘
                              │
                              ↓
                     ┌────────────────────────┐
                     │  CALCULAR GAP (Paso 3) │
                     │                        │
                     │ delta_K = k-k_bks      │
                     │ reached = (k==k_bks)   │
                     │                        │
                     │ if reached:            │
                     │   gap_d = d - d_bks    │
                     │   gap_% = (d-d_bks)/d_ │
                     │           bks * 100    │
                     └────────────────────────┘
                              │
                              ↓
                     ┌────────────────────────┐
                     │  GUARDAR RESULTADO     │
                     │                        │
                     │ raw_results.append({   │
                     │   algorithm,           │
                     │   instance_id,         │
                     │   k_final, k_bks,      │
                     │   d_final, d_bks,      │
                     │   delta_K,             │
                     │   reached_K_BKS,       │
                     │   gap_distance,        │
                     │   gap_percent,         │
                     │   time_sec             │
                     │ })                     │
                     └────────────────────────┘
                              │
                              ↓
                 [Repetir 36 veces]
                              │
                              ↓
                 ┌────────────────────────┐
                 │  GUARDAR CSV (Paso 4)  │
                 │                        │
                 │ raw_results.csv        │
                 │ (36 filas con GAP)     │
                 └────────────────────────┘
                              │
                              ↓
        ┌─────────────────────────────────────┐
        │  GENERAR VISUALIZACIONES (Paso 5)   │
        │                                     │
        │  gap_distribution.png               │
        │  gap_by_family.png                  │
        │  gap_vs_time.png                    │
        │  gap_comparison_boxplot.png         │
        └─────────────────────────────────────┘
```

---

## 6. Archivo raw_results.csv

### Estructura Completa

```csv
algorithm,instance_id,family,k_final,d_final,time_sec,k_bks,d_bks,delta_K,reached_K_BKS,gap_distance,gap_percent,status
GRASP,R101,R1,19,1687.5,2.34,19,1650.8,0,True,36.7,2.22,success
VND,R101,R1,19,1665.2,3.21,19,1650.8,0,True,14.4,0.87,success
ILS,R101,R1,19,1650.8,5.45,19,1650.8,0,True,0.0,0.00,success
GRASP,R102,R1,17,1520.3,2.51,17,1487.0,0,True,33.3,2.24,success
VND,R102,R1,17,1495.2,3.45,17,1487.0,0,True,8.2,0.55,success
ILS,R102,R1,17,1487.0,5.67,17,1487.0,0,True,0.0,0.00,success
...
```

### Columnas Clave

| Columna | Tipo | Descripción |
|---------|------|-------------|
| algorithm | str | GRASP, VND, o ILS |
| instance_id | str | R101, C102, RC203, etc |
| family | str | R1, C1, RC2, etc |
| k_final | int | Vehículos encontrados |
| d_final | float | Distancia encontrada |
| time_sec | float | Tiempo de ejecución |
| **k_bks** | int | **Vehículos BKS** |
| **d_bks** | float | **Distancia BKS** |
| **delta_K** | int | **Diferencia en vehículos** |
| **reached_K_BKS** | bool | **¿Alcanzó K de BKS?** |
| **gap_distance** | float | **Brecha en km** |
| **gap_percent** | float | **Brecha en %** |
| status | str | success, failed, timeout |

---

## 7. Ejemplos Prácticos

### Ejemplo 1: Solución Óptima

```
Instancia: R1/R101

BKS:
  K = 19 vehículos
  D = 1650.8 km

GRASP:
  K = 19 vehículos ✅
  D = 1650.8 km ✅

Cálculos:
  delta_K = 19 - 19 = 0
  reached_K_BKS = (19 == 19) = True
  gap_distance = 1650.8 - 1650.8 = 0.0 km
  gap_percent = (0.0 / 1650.8) * 100 = 0.00%

Interpretación:
  ✅ Encontró solución óptima conocida
  GAP = 0.00% (mejor posible)
```

### Ejemplo 2: Solución Subóptima (Mismo K)

```
Instancia: R1/R101

BKS:
  K = 19 vehículos
  D = 1650.8 km

VND:
  K = 19 vehículos ✅
  D = 1670.5 km

Cálculos:
  delta_K = 19 - 19 = 0
  reached_K_BKS = (19 == 19) = True
  gap_distance = 1670.5 - 1650.8 = 19.7 km
  gap_percent = (19.7 / 1650.8) * 100 = 1.19%

Interpretación:
  ✅ Alcanzó número de vehículos BKS
  ⚠️  Distancia 1.19% peor que BKS
  Típico para heurísticas
```

### Ejemplo 3: Solución Peor (Diferente K)

```
Instancia: R1/R101

BKS:
  K = 19 vehículos
  D = 1650.8 km

GRASP (malo):
  K = 21 vehículos ❌
  D = 1580.0 km

Cálculos:
  delta_K = 21 - 19 = +2
  reached_K_BKS = (21 == 19) = False
  gap_distance = NULL (no se calcula)
  gap_percent = NULL (no se calcula)

Interpretación:
  ❌ Usó 2 vehículos más que BKS
  ⚠️  No se calcula GAP en % (K diferente)
  Métrica: delta_K = +2 indica problema
```

---

## 8. Estadísticas Agregadas

### Cálculos Post-Experimento

```python
# En generate_summary_report():

for resultado in raw_results:
    if resultado['reached_K_BKS']:
        # Incluir en estadísticas GAP
        gap_values.append(resultado['gap_percent'])
    else:
        # Contar como no alcanzado
        not_reached += 1

# Estadísticas:
media_gap = mean(gap_values)           # GAP promedio
std_gap = std(gap_values)              # Desviación estándar
min_gap = min(gap_values)              # Mejor GAP
max_gap = max(gap_values)              # Peor GAP
median_gap = median(gap_values)        # Mediana

# Contador:
pct_reached_K = (instances_reached_K / total_instances) * 100
```

### Ejemplo de Reporte

```
═══════════════════════════════════════════════════════════
                  SUMMARY REPORT - QUICK
═══════════════════════════════════════════════════════════

TOTAL EXPERIMENTS: 36 (12 instancias × 3 algoritmos)

RESULTS BY ALGORITHM:
────────────────────────────────────────────────────────
GRASP:
  Instances reached K_BKS: 10/12 (83.3%)
  GAP Statistics (when K reached):
    Mean: 2.34%
    Std Dev: 1.23%
    Min: 0.00%
    Max: 4.56%
  Avg Time: 2.34 sec
  
VND:
  Instances reached K_BKS: 11/12 (91.7%)
  GAP Statistics (when K reached):
    Mean: 0.89%
    Std Dev: 0.65%
    Min: 0.00%
    Max: 2.15%
  Avg Time: 3.45 sec
  
ILS:
  Instances reached K_BKS: 12/12 (100%)
  GAP Statistics (when K reached):
    Mean: 0.12%
    Std Dev: 0.08%
    Min: 0.00%
    Max: 0.45%
  Avg Time: 5.56 sec

────────────────────────────────────────────────────────

CONCLUSIONES:
  ✅ ILS alcanza BKS en 100% de instancias
  ✅ VND mejor GAP que GRASP (0.89% vs 2.34%)
  ⚠️  ILS tarda ~2.4x más que GRASP
  ✅ Mejora en calidad justifica tiempo extra
```

---

## 9. Visualizaciones Generadas

### 9.1 Gap Distribution

```
Gráfico: histograma de distribución de GAP

        Instancias
            ^
            |     ┌─┐
            |     │ │
         5 |  ┌──┘ └─┐
            |  │      │
         3 |  │ ┌──┐ │ ┌──┐
            |  │ │  │ │ │  │
         1 |┌─┘ │  └─┘ │  └──┐
            └─────────────────────> GAP (%)
            0   1   2   3   4   5

Interpretación:
  - Campana hacia izquierda = buenos GAPs
  - Concentración en 0-1% = soluciones buenas
  - Cola hacia derecha = outliers
```

### 9.2 GAP by Family

```
Gráfico: boxplot GAP por familia

      R1    C1    RC1
      |     |     |
    5 +     +     +
      | o   |     |
    4 +--+--+--+--+
      | +---+ | +
    2 +-+   +-+-+
      | |   | |
    0 +-+-+-+-+-+-
        R1  C1  RC1

Interpretación:
  - R1 mejor GAP que C1
  - RC1 variable
  - Caja baja = consistencia
```

### 9.3 GAP vs Time

```
Gráfico: scatter plot GAP vs Tiempo

GAP %
  5 |     GRASP
    |   ●  ●  ●
  3 |   ●  ●  ●
    |        
  1 | ●     VND
    |   ●● ● ● ● ILS
    |   ●●●●●
  0 +───────────────> Tiempo (sec)
    0  2   4   6   8

Interpretación:
  - VND mejor trade-off
  - ILS lento pero mejor GAP
  - GRASP rápido pero GAP mayor
```

---

## 10. Casos Especiales

### Caso 1: BKS No Disponible

```python
bks_key = "R1/R101"
if bks_key not in bks_data:
    # No tenemos BKS para esta instancia
    k_bks = None
    d_bks = None
    gap_percent = None
    
    # Se reporta en CSV
    # ...,"<NULL>","<NULL>","<NULL>",False,"<NULL>","<NULL>",...
```

### Caso 2: K Diferente de BKS

```python
if k_final != k_bks:
    # No calculamos GAP en %
    gap_distance = None
    gap_percent = None
    
    # Reportamos delta_K en su lugar
    # delta_K = +2 indica "2 vehículos extras"
```

### Caso 3: Error en Ejecución

```python
if algoritmo.solve(instance) fails:
    resultado = {
        'algorithm': algo,
        'instance_id': instance,
        'status': 'failed',
        'error': str(exception),
        
        # Campos vacíos por error
        'k_final': None,
        'd_final': None,
        'gap_percent': None,
        'time_sec': elapsed_before_crash
    }
```

---

## 11. Reproducibilidad de GAP

### Factores que Afectan GAP

```
GAP depende de:
  1. ✅ BKS (constante, no cambia)
  2. ✅ Algoritmo (GRASP, VND, ILS - igual cada vez)
  3. ✅ Seed (determinístico si seed=42)
  4. ✅ Instancia (Solomon definida)
  5. ✅ Parámetros del algoritmo

Resultado: GAP es REPRODUCIBLE
```

### Verificación

```bash
# Ejecución 1
$ python scripts/experiments.py --mode QUICK
# raw_results.csv → GRASP R101: GAP = 2.22%

# Ejecución 2 (mismo día, mismo código, seed=42)
$ python scripts/experiments.py --mode QUICK
# raw_results.csv → GRASP R101: GAP = 2.22% ✅

# Mismo GAP exacto = sistema reproducible
```

---

## 12. Resumen: Flujo GAP en 4 Pasos

```
┌────────────────────────────────────────────────┐
│ PASO 1: CARGAR BKS                            │
│ bks.json → dict en memoria                     │
└────────────────────────────────────────────────┘
                        │
                        ↓
┌────────────────────────────────────────────────┐
│ PASO 2: EJECUTAR ALGORITMO                     │
│ GRASP/VND/ILS.solve(instance)                  │
│ → k_final, d_final, time_sec                   │
└────────────────────────────────────────────────┘
                        │
                        ↓
┌────────────────────────────────────────────────┐
│ PASO 3: BUSCAR BKS Y CALCULAR GAP             │
│ k_bks, d_bks = bks_data["familia/instancia"]  │
│ gap_percent = ((d_final - d_bks) / d_bks)*100 │
└────────────────────────────────────────────────┘
                        │
                        ↓
┌────────────────────────────────────────────────┐
│ PASO 4: GUARDAR EN CSV + VISUALIZAR           │
│ raw_results.csv                                │
│ Gráficos: gap_distribution.png, etc.           │
└────────────────────────────────────────────────┘
```

**Total: Automatizado en cada experimento, calculado para cada algoritmo × instancia.**

