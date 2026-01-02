---
title: "Best Known Solutions (BKS) Reference"
created: "2026-01-02"
version: "1.0.0"
---

# 📊 Best Known Solutions (BKS) Reference

**Propósito**: Mantener referencia centralizada de las mejores soluciones conocidas para las 56 instancias Solomon, usada para validación y cálculo de gaps.

---

## 📁 Archivos Generados

### 1. `best_known_solutions.json`
Archivo principal en formato JSON con estructura jerarquizada.

**Estructura**:
```json
{
  "metadata": {...},
  "families": {
    "C1": {
      "instances": [
        {"id": "C101", "k_bks": 10, "d_bks": 828.93664},
        ...
      ]
    },
    ...
  },
  "summary": {
    "by_family": {...},
    "overall": {...}
  }
}
```

**Uso**: Referencia oficial del sistema.

---

### 2. `best_known_solutions.csv`
Versión tabulada en CSV para análisis con Pandas/Excel.

**Columnas**:
- `instance_id`: C101, C102, ..., RC208
- `family`: C1, C2, R1, R2, RC1, RC2
- `k_bks`: Mejor número de vehículos conocido
- `d_bks`: Mejor distancia total conocida

**Uso**: Análisis estadístico, comparativas, reportes.

---

### 3. `src/core/bks.py`
Módulo Python que carga y gestiona BKS con funciones de validación.

**Clases principales**:

#### `BKSManager`
Gestor central de BKS con métodos:

```python
# Carga
bks = BKSManager()

# Acceso individual
bks.get_instance('C101')           # {'id': 'C101', 'k_bks': 10, 'd_bks': 828.93664}
bks.get_k_bks('C101')              # 10
bks.get_d_bks('C101')              # 828.93664

# Acceso por familia
bks.get_family('C1')               # Datos completos familia C1
bks.get_instances_by_family('C1')  # ['C101', 'C102', ...]
bks.get_all_families()             # ['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2']

# Cálculos de gap
gap_k = bks.compute_k_gap('C101', algo_k=10)  # 0.0 (perfecto)
gap_k = bks.compute_k_gap('C101', algo_k=11) # 10.0 (10% peor)

# Validación jerárquica
is_better, reason = bks.is_better_solution('C101', algo_k=10, algo_d=828.93664)
# Returns: (False, 'Equal to BKS: K=10, D=828.93664')

# Validación completa
validation = bks.validate_solution('C101', algo_k=10, algo_d=900.0)
# Returns comprehensive dict with algorithm vs BKS comparison

# Estadísticas
stats = bks.get_summary()                  # Estadísticas globales
stats_c1 = bks.get_summary('C1')          # Estadísticas familia C1
```

---

## 📈 Datos de Referencia

### Por Familia Solomon

| Familia | Instancias | Descripción | Avg K | Avg D |
|---------|-----------|-------------|-------|-------|
| **C1** | 9 | Clustered, período normal | 10.00 | 827.94 |
| **C2** | 8 | Clustered, período extendido | 3.00 | 590.00 |
| **R1** | 12 | Random, período normal | 12.25 | 1218.34 |
| **R2** | 11 | Random, período extendido | 2.91 | 952.40 |
| **RC1** | 8 | Random+Clustered, período normal | 11.38 | 1441.51 |
| **RC2** | 8 | Random+Clustered, período extendido | 3.38 | 1072.33 |
| **TOTAL** | 56 | - | 7.11 | 1050.38 |

### Rango de Valores

| Métrica | Mínimo | Máximo | Promedio |
|---------|--------|--------|----------|
| **K (vehículos)** | 2 (R2, R207) | 19 (R1, R101) | 7.11 |
| **D (distancia)** | 588.29 (C2, C207) | 1650.80 (R1, R101) | 1050.38 |

---

## 🔄 Uso en el Sistema

### Fase 6: Validación de Datasets
```python
from src.core.bks import BKSManager

bks = BKSManager()
# Verificar que tenemos BKS para todas las 56 instancias
all_instances = bks.get_all_instances()
assert len(all_instances) == 56
```

### Fase 7: Cálculo de Métricas
```python
# Después de ejecutar algoritmo
validation = bks.validate_solution(instance_id='C101', algo_k=10, algo_d=850.0)

# Guardar en CSV
results.loc[idx, 'K_BKS'] = validation['bks']['k']
results.loc[idx, 'D_BKS'] = validation['bks']['d']
results.loc[idx, 'K_gap_%'] = validation['comparison']['k_gap_percent']
results.loc[idx, 'Better_than_BKS'] = validation['comparison']['is_better_than_bks']
```

### Fase 10: Análisis Estadístico
```python
# Comparar contra BKS
for family_id in bks.get_all_families():
    summary = bks.get_summary(family_id)
    print(f"{family_id}: avg_K={summary['avg_k']}, avg_D={summary['avg_distance']}")

# Calcular % instancias donde alcanzamos K_BKS
instances_matching_k_bks = sum(1 for r in results if r['K_gap_%'] == 0.0)
percentage = (instances_matching_k_bks / len(results)) * 100
```

### Fase 14: Experimentos
```python
# Validar cada solución encontrada
for algo_result in experiment_results:
    validation = bks.validate_solution(
        algo_result['instance_id'],
        algo_result['k'],
        algo_result['distance']
    )
    
    if not validation['comparison']['is_better_than_bks']:
        algo_result['status'] = validation['comparison']['reason']
```

---

## 📋 Estructura del JSON Detallada

### metadata
- `source`: Fuente de los datos (Solomon Benchmark)
- `description`: Descripción breve
- `created`: Fecha de creación
- `total_instances`: 56
- `families`: 6 familias
- `note`: Explicación de K_BKS y D_BKS

### families
Seis claves: C1, C2, R1, R2, RC1, RC2

Cada familia contiene:
```json
{
  "name": "Descripción humana",
  "description": "Explicación detallada",
  "num_instances": N,
  "instances": [
    {"id": "XYZT", "k_bks": int, "d_bks": float},
    ...
  ]
}
```

### summary
Estadísticas calculadas:

```json
{
  "by_family": {
    "C1": {
      "avg_k": 10.0,
      "min_k": 10,
      "max_k": 10,
      "avg_distance": 827.94,
      "min_distance": 824.78,
      "max_distance": 828.94
    },
    ...
  },
  "overall": {
    "total_instances": 56,
    "avg_vehicles": 7.11,
    "min_vehicles": 2,
    "max_vehicles": 19,
    "avg_distance": 1050.38,
    "min_distance": 588.29,
    "max_distance": 1650.80
  }
}
```

---

## 🧪 Testing

### Script de prueba: `scripts/test_bks_manager.py`

Ejecutar:
```bash
python scripts/test_bks_manager.py
```

Verifica:
- ✓ Carga del archivo JSON
- ✓ Lookup de instancias
- ✓ Lookup por familia
- ✓ Cálculo de gaps
- ✓ Validaciones jerárquicas
- ✓ Estadísticas

---

## 📝 Notas Importantes

### Jerarquía de Comparación (Canónica)
La comparación contra BKS es **jerárquica**:

1. **Primario**: Número de vehículos (K)
   - Mejor: K < K_BKS
   - Igual: K = K_BKS
   - Peor: K > K_BKS

2. **Secundario**: Distancia total (D) - **solo si K = K_BKS**
   - Mejor: D < D_BKS
   - Igual: D = D_BKS
   - Peor: D > D_BKS

### Interpretación de Gaps

```
K_gap = ((algo_K - bks_K) / bks_K) * 100

- K_gap = 0%:    Algoritmo iguala K_BKS (excelente)
- K_gap > 0%:    Algoritmo usa más vehículos (peor)
- K_gap = None:  Algoritmo usa menos vehículos (mejor que BKS - raro!)
```

---

## 🔗 Referencias

- **Documentación referenciada**:
  - [05-datasets-solomon.md](05-datasets-solomon.md) — Especificación Solomon
  - [07-fitness-canonico.md](07-fitness-canonico.md) — Función fitness jerárquica
  - [08-metricas-canonicas.md](08-metricas-canonicas.md) — Métricas canónicas

- **Fuente de datos**: Solomon benchmark instances (repositorio oficial)

- **Fases que usan BKS**: 6, 7, 10, 14

---

## 🚀 Próximos Pasos

1. **Fase 2**: Integrar BKSManager en carga de instancias
2. **Fase 7**: Usar en cálculo de métricas y gaps
3. **Fase 10**: Análisis comparativo con BKS por familia
4. **Fase 14**: Validación de experimentos contra BKS

---

**Versión**: 1.0.0  
**Última actualización**: 2026-01-02  
**Estado**: Listo para usar en Fase 2+

