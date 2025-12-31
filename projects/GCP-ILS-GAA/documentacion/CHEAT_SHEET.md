# ⚡ CHEAT SHEET - run_experiments.py

**Imprime esto o mantenlo en bookmark** 📌

---

## 🚀 COMMAND MÁS IMPORTANTE

```bash
cd projects/GCP-ILS-GAA
python run_experiments.py
```

**↓ Muestra menú interactivo ↓**

---

## 📊 QUÉ VES EN EL MENÚ

```
📊 FAMILIAS DISPONIBLES:

  1. CUL        ( 6) │ ✅ ÓPTIMO
  2. DSJ        (15) │ ❓ ABIERTA
  3. LEI        (12) │ ✅ ÓPTIMO
  4. MYC        ( 5) │ ✅ ÓPTIMO
  5. REG        (14) │ ✅ ÓPTIMO
  6. SCH        ( 2) │ ❓ ABIERTA
  7. SGB        (25) │ 📊 BKS
  8. LAT        ( 1) │ ❓ ABIERTA

¿QUÉ DESEAS EJECUTAR?
  1. Una instancia específica
  2. Una familia COMPLETA
  3. TODAS las familias
  0. Salir
```

---

## 🎮 INTERACTIVE MODE (Paso-a-paso)

```bash
python run_experiments.py
Opción: 1 [ENTER]              ← Una instancia
Opción: 3 [ENTER]              ← LEI familia
Opción: 1 [ENTER]              ← Primera instancia
Confirmar: s [ENTER]           ← Start
```

**Resultado**: 
```
output/LEI_30_12_25_14_30/
├── config.json
└── results.json
```

---

## ⌨️ CLI MODE (Directo)

```bash
# Ejecutar familia completa
python run_experiments.py --family LEI

# Ejecutar instancia específica
python run_experiments.py --family CUL --instance flat300_20_0

# Ejecutar TODAS las familias
python run_experiments.py --all
```

---

## 📊 SÍMBOLOS

```
✅ ÓPTIMO      = Garantizado (CUL, LEI, MYC, REG)
📊 BKS         = Best Known (SGB)
❓ ABIERTA     = Desconocido (DSJ, SCH, LAT)
```

---

## 📁 OUTPUT STRUCTURE

```
output/
├── FAMILY_DD_MM_YY_HH_MM/    ← Folder creado automático
│   ├── config.json           ← Parámetros guardados
│   └── results.json          ← Resultados de GAA
└── ...
```

**Ejemplo**: `output/LEI_30_12_25_14_30/`

---

## 🔍 AFTER EXPERIMENTS

```bash
# Comparar con literatura
python compare_with_bks.py --results-dir output/*/

# Ver un config.json
cat output/LEI_*/config.json
```

---

## 📖 DOCUMENTACIÓN

| Doc | Tiempo | URL |
|-----|--------|-----|
| Quick Start | 2 min | QUICK_START_RUN_EXPERIMENTS.md |
| Manual | 10 min | GUIA_RUN_EXPERIMENTS.md |
| Conceptual | 15 min | OPTIMO_vs_BKS.md |
| Final | 5 min | RESUMEN_FINAL_SESION.md |

---

## ✅ EJEMPLOS DE USO

### Ejemplo 1: Una instancia de LEI
```bash
python run_experiments.py --family LEI --instance le450_5a
```

### Ejemplo 2: Toda la familia CUL
```bash
python run_experiments.py --family CUL
```

### Ejemplo 3: TODAS las familias
```bash
python run_experiments.py --all
```

### Ejemplo 4: Interactivo (recomendado)
```bash
python run_experiments.py
# Sigue prompts
```

---

## 🎯 ESTRATEGIA

| Objetivo | Familia | Comando |
|----------|---------|---------|
| **Validar** | LEI | `--family LEI` |
| **Comparar** | SGB | `--family SGB` |
| **Explorar** | DSJ | `--family DSJ` |
| **Todo** | Todas | `--all` |

---

## 🐛 TROUBLESHOOTING

| Problema | Solución |
|----------|----------|
| "ModuleNotFoundError" | cd projects/GCP-ILS-GAA |
| "BKS.json not found" | Asegúrate de datasets/ |
| "output permission denied" | chmod 755 output |
| Menu no aparece | python --version (≥3.6) |

---

## 📊 QUICK FACTS

```
Total instancias:  81
Familias:          8
Óptimo conocido:   37
BKS:               18
Abierto:           26

Tamaño dataset:    ~500MB
Tiempo per run:    Depende GAA
Output folder:     FAMILY_DD_MM_YY_HH_MM
```

---

## ✨ SUMMARY

```
✅ run_experiments.py   → Script principal
✅ output/FAMILY_*/     → Resultados
✅ config.json          → Parámetros guardados
✅ BKS.json             → 81 instancias
✅ compare_with_bks.py  → Análisis vs literatura
```

---

## 🚀 AHORA

```bash
cd projects/GCP-ILS-GAA
python run_experiments.py
```

**¡LISTO! 🎉**

---

*Generado: 30/12/2025 | Status: ✅ Ready*
