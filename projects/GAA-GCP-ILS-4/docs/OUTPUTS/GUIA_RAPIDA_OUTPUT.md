# 🚀 GUÍA RÁPIDA - DÓNDE VAN LOS OUTPUTS

**Proyecto**: GAA-GCP-ILS-4

---

## 📁 ESTRUCTURA SIMPLE

```
output/
├── results/          ← CSV, JSON, TXT, SOL (datos numéricos)
├── plots/            ← PNG (gráficas)
├── solutions/        ← SOL (soluciones)
└── logs/             ← LOG (registros)
```

---

## 📊 ARCHIVOS POR TIPO

### 1️⃣ DATOS NUMÉRICOS → `output/results/{timestamp}/`
```
summary.csv              ← Tabla resumen
detailed_results.json    ← Datos JSON
statistics.txt           ← Reporte texto
timing_report.txt        ← Tiempos
timing_report.json       ← Tiempos JSON
```

### 2️⃣ GRÁFICAS → `output/plots/{timestamp}/`
```
convergence_plot.png         ← Convergencia
scalability_plot.png         ← Escalabilidad
boxplot_robustness.png       ← Robustez
conflict_heatmap.png         ← Conflictos
time_quality_tradeoff.png    ← Tiempo vs Calidad
```

### 3️⃣ SOLUCIONES → `output/results/{timestamp}/` + `output/solutions/`
```
myciel3_31-12-25_21-46-59.sol
myciel4_31-12-25_21-46-59.sol
DSJC125.1_31-12-25_21-46-59.sol
...
```

### 4️⃣ LOGS → `output/logs/`
```
experiment_31-12-25_21-46-59.log
```

---

## 🎯 RESUMEN RÁPIDO

| Qué | Dónde | Formato |
|-----|-------|---------|
| **Tabla resumen** | `output/results/` | CSV |
| **Datos detallados** | `output/results/` | JSON |
| **Reporte estadístico** | `output/results/` | TXT |
| **Tiempos por etapa** | `output/results/` | TXT + JSON |
| **Gráficas** | `output/plots/` | PNG |
| **Soluciones** | `output/results/` + `output/solutions/` | SOL |
| **Logs** | `output/logs/` | LOG |

---

## ✅ CONCLUSIÓN

**TODOS LOS OUTPUTS VAN EN `output/`**

- ✅ Resultados → `output/results/`
- ✅ Gráficas → `output/plots/`
- ✅ Soluciones → `output/solutions/`
- ✅ Logs → `output/logs/`

---

**Última actualización**: 31 Diciembre 2025
