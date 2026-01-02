# PARTE 10: ESQUEMA CANÓNICO DE ARCHIVOS CSV PARA GRASP–VRPTW

## Archivo 1: Resultados por Ejecución (Raw Runs)

### Ruta
```
output/raw_runs/raw_results.csv
```

Una fila = una ejecución independiente (Algoritmo × Instancia × Run)

### Columnas

```
algorithm_id
instance_id
family
run_id
random_seed
K_final
D_final
K_BKS
D_BKS
delta_K
gap_distance
gap_percent
total_time_sec
iterations_executed
reached_K_BKS
```

### Notas

- `gap_distance` y `gap_percent` deben ser NA si `delta_K ≠ 0`
- `reached_K_BKS = (K_final == K_BKS)`

---

## Archivo 2: Trazas de Convergencia por Iteración

### Ruta
```
output/convergence/convergence_trace.csv
```

Una fila = una iteración de una ejecución

### Columnas

```
algorithm_id
instance_id
family
run_id
iteration
elapsed_time_sec
K_best_so_far
D_best_so_far
is_K_BKS
```

### Notas

- `is_K_BKS = (K_best_so_far == K_BKS)`
- `D_best_so_far` se registra siempre, pero solo se analiza cuando `is_K_BKS = true`

---

## Archivo 3: Resumen Agregado por Instancia

### Ruta
```
output/aggregated/summary_by_instance.csv
```

Una fila = (Algoritmo × Instancia)

### Columnas

```
algorithm_id
instance_id
family
runs_total
K_best
K_mean
K_std
K_min
K_max
percent_runs_K_min
D_mean_at_K_min
D_std_at_K_min
gap_percent_mean
gap_percent_std
time_mean_sec
```

### Notas

- `K_min` = mínimo K observado
- `percent_runs_K_min` = % de ejecuciones con K = K_min
- `D_*` se calcula solo sobre ejecuciones con K = K_min
- `gap_*` solo se calcula cuando K_min == K_BKS

---

## Archivo 4: Resumen Agregado por Familia

### Ruta
```
output/aggregated/summary_by_family.csv
```

Una fila = (Algoritmo × Familia)

### Columnas

```
algorithm_id
family
instances_count
K_mean
percent_instances_K_BKS
gap_percent_mean
gap_percent_std
time_mean_sec
```

### Notas

- `percent_instances_K_BKS` = % de instancias donde K_min == K_BKS
- `gap_*` se calcula solo sobre esas instancias

---

## Archivo 5: Análisis Temporal (Anytime)

### Ruta
```
output/time_analysis/time_metrics.csv
```

Una fila = una ejecución

### Columnas

```
algorithm_id
instance_id
family
run_id
time_to_K_min_sec
iteration_to_K_min
time_to_best_D_sec
iteration_to_best_D
```

### Notas

- `time_to_K_min_sec` = primer tiempo donde K_best_so_far alcanza K_min
- `time_to_best_D_sec` se mide solo después de alcanzar K_min

---

## Archivo 6: Soluciones Estructurales (Rutas)

### Ruta
```
output/solutions/solutions.csv
```

Una fila = una ruta de una solución final

### Columnas

```
algorithm_id
instance_id
family
run_id
route_id
vehicle_load
route_distance
customer_sequence
```

### Notas

- `customer_sequence` en formato texto, por ejemplo: "0-12-5-8-0"
- Este archivo permite reconstruir rutas completas

---

## Archivo 7: Tiempos de Llegada (Ventanas de Tiempo)

### Ruta
```
output/solutions/time_windows_check.csv
```

Una fila = un cliente en una solución

### Columnas

```
algorithm_id
instance_id
family
run_id
customer_id
arrival_time
window_start
window_end
slack_time
```

### Notas

- `slack_time = window_end − arrival_time`
- Solo se guarda para soluciones con K_final = K_BKS

---

## Archivo 8: Metadatos del Experimento

### Ruta
```
output/metadata/experiment_metadata.csv
```

Una fila = experimento completo

### Columnas

```
experiment_id
experiment_date
algorithm_id
dataset_name
instances_used
stopping_criterion
max_iterations
max_time_sec
alpha_value
hardware_cpu
hardware_ram
os
programming_language
code_version
```

---

## Reglas de Consistencia (Obligatorias)

1. Los nombres de columnas deben ser **EXACTAMENTE** estos
2. Nunca mezclar resultados crudos con agregados
3. Toda figura del paper debe poder reconstruirse leyendo uno o más de estos CSV
4. Toda métrica jerárquica debe poder inferirse sin ambigüedad desde los datos guardados

---

## Resumen Rápido

- **raw_results.csv** → base estadística
- **convergence_trace.csv** → convergencia y anytime
- **summary_by_instance.csv** → tablas principales del paper
- **summary_by_family.csv** → análisis estructural
- **time_metrics.csv** → eficiencia
- **solutions.csv** → rutas
- **time_windows_check.csv** → factibilidad
- **experiment_metadata.csv** → reproducibilidad
