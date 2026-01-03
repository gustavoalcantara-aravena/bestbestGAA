# 🎯 GUÍA PASO A PASO - OPTIMIZACIÓN DE PARÁMETROS

## 📍 PASO 1: PREPARACIÓN (5 minutos)

### 1.1 Abrir terminal PowerShell

```powershell
# En VS Code: Ctrl + `  (backtick)
# O: Terminal → Nueva terminal
```

### 1.2 Navegar al proyecto

```powershell
cd c:\Users\alfab\Desktop\bestbestGAA\projects\GAA-VRPTW-GRASP-2
```

### 1.3 Verificar que estamos en el lugar correcto

```powershell
# Debe mostrar todos estos archivos:
ls best_known_solutions.json
ls parameter_tuner_algo3.py
ls src/gaa/algorithm_generator.py
ls scripts/experiments.py
```

**Esperado**:
```
    Directory: C:\Users\alfab\Desktop\bestbestGAA\projects\GAA-VRPTW-GRASP-2

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          1/3/2026   9:45 AM       125478 best_known_solutions.json
-a---          1/3/2026   9:50 AM        45389 parameter_tuner_algo3.py
```

---

## 📍 PASO 2: LECTURA RÁPIDA (5 minutos)

Lee estas 2 secciones rápidamente:

### 2.1 Ver el plan visual

```powershell
# Abre en VS Code y lee:
code VISUALIZACION_PLAN.md
```

**Puntos clave**:
- Familia C1: 9 instancias
- Parámetros a optimizar: 5 parámetros
- Duración: ~3 horas para 100 combos
- Métrica: Minimizar SCORE = GAP_K + GAP_D

### 2.2 Ver opciones de ejecución

```powershell
# Ver RESUMEN_PLAN_OPTIMIZACION.md
code RESUMEN_PLAN_OPTIMIZACION.md
```

**Secciones**:
- Objetivo principal
- Familia C1
- Metodología
- Ejemplo de salida esperada

---

## 📍 PASO 3A: PRUEBA RÁPIDA (10 minutos) - OPCIONAL

Si quieres validar que todo funciona antes de 3 horas:

```powershell
# Ejecutar con solo 5 combinaciones
python parameter_tuner_algo3.py --num-combinations 5
```

**Esperado**:
```
================================================================================
PARAMETER TUNING - Algorithm 3 - Family C1
Combinaciones a probar: 5
Timestamp: 2026-01-03 10:30:45
================================================================================

[1/4] Generando 5 combinaciones...
      [OK] 5 combinaciones generadas

[2/4] Ejecutando búsqueda de parámetros...

  [  1/5] W:100 2OP:45 DB:1.5 2POST:40 REL:35
       [OK] Score=2.531, GAP_K=1.23%, GAP_D=1.31%, Time=45.3s

  [  2/5] W:120 2OP:65 DB:2.1 2POST:55 REL:28
       [OK] Score=3.845, GAP_K=1.89%, GAP_D=1.96%, Time=48.1s

  ... 3 más ...
```

**Si todo OK** → Puedes pasar a Paso 3B (ejecución principal)

**Si hay error** → Revisa sección Troubleshooting en GUIA_PARAMETER_TUNING.md

---

## 📍 PASO 3B: BÚSQUEDA PRINCIPAL (3-4 horas) ⭐ RECOMENDADO

Este es el paso PRINCIPAL. Ejecuta con 100 combinaciones:

```powershell
python parameter_tuner_algo3.py --num-combinations 100
```

### 3B.1 Qué esperar durante la ejecución

```
[1/4] Generando 100 combinaciones...
      [OK] 100 combinaciones generadas          ← ~10 segundos

[2/4] Ejecutando búsqueda de parámetros...

  [  1/100] W:100 2OP:45 DB:1.5 2POST:40 REL:35
       [OK] Score=2.531, GAP_K=1.23%, GAP_D=1.31%, Time=45.3s

  [  2/100] W:120 2OP:65 DB:2.1 2POST:55 REL:28
       [OK] Score=3.845, GAP_K=1.89%, GAP_D=1.96%, Time=48.1s

  ... esperará aquí por ~3 horas ejecutando 100 combos ...
```

### 3B.2 Durante la ejecución

```
TIEMPO        ESTADO                                  
─────────────────────────────────────────────────────
00:00:00      Generando combinaciones (10 min)
00:10:00      Combo 1/100 (1.6 min)
00:11:36      Combo 2/100
...
02:50:00      Combo 100/100
02:51:36      Finalizando y generando reportes
```

**IMPORTANTE**: 
- ✅ Puedes dejar la ventana ejecutándose
- ✅ Puedes minimizar VS Code
- ✅ No cierre la terminal
- ❌ No interrumpa la ejecución (Ctrl+C)

---

## 📍 PASO 4: REVISAR RESULTADOS (10 minutos)

Cuando termine la ejecución (después de ~3 horas):

### 4.1 Ver el reporte

```powershell
# Opción 1: Ver en terminal
type optimization_results_c1/report.txt

# Opción 2: Abrir en VS Code
code optimization_results_c1/report.txt
```

**Verás algo así**:
```
TOP 10 BEST COMBINATIONS
================================================================================

#1: Score = 1.987456
  Parámetros: While=75, 2Opt_pre=35, DB=1.8, 2Opt_post=35, Relocate=25
  Avg GAP_K: 0.920%
  Avg GAP_D: 1.067%
  Exec Time: 44.1s

#2: Score = 2.012389
  Parámetros: While=85, 2Opt_pre=40, DB=1.7, 2Opt_post=38, Relocate=28
  Avg GAP_K: 0.945%
  Avg GAP_D: 1.067%
  Exec Time: 45.3s

... 8 más ...

STATISTICS
================================================================================
Best Score:   1.234567
Worst Score:  5.678901
Avg Score:    3.456789
Median Score: 3.234567
```

### 4.2 Extraer los mejores parámetros

```powershell
# Los MEJORES parámetros están en la línea de "#1"
# En el ejemplo anterior:
#   While:       75
#   TwoOpt (pre): 35
#   DoubleBridge: 1.8
#   TwoOpt (post): 35
#   Relocate:    25
```

### 4.3 Ver todos los resultados en JSON

```powershell
# Abrir el JSON detallado
code optimization_results_c1/results.json
```

---

## 📍 PASO 5: APLICAR PARÁMETROS ÓPTIMOS (15 minutos)

Una vez identificados los mejores parámetros:

### 5.1 Abrir el archivo de algoritmos

```powershell
code src/gaa/algorithm_generator.py
```

### 5.2 Buscar la sección ALGORITMO 3

Usa Ctrl+F para buscar:
```
# ALGORITMO 3: MÁXIMA EXPLORACIÓN
```

### 5.3 Actualizar los valores

**Busca estas líneas** (alrededor de línea 100-140):

```python
# ALGORITMO 3: MÁXIMA EXPLORACIÓN
def generate_three_algorithms(self, seed: int = 42) -> List[ASTNode]:
    ...
    # ALGORITMO 3 - Máxima exploración
    while_iter = 100        # ← CAMBIAR aquí
    twoopt_pre = 45         # ← CAMBIAR aquí
    doublebridge = 1.5      # ← CAMBIAR aquí
    twoopt_post = 40        # ← CAMBIAR aquí
    relocate = 35           # ← CAMBIAR aquí
```

**Reemplaza con los valores del #1** (del ejemplo anterior):

```python
# ALGORITMO 3 - OPTIMIZADO ITER-8
while_iter = 75         # Cambio de 100 a 75
twoopt_pre = 35         # Cambio de 45 a 35
doublebridge = 1.8      # Cambio de 1.5 a 1.8
twoopt_post = 35        # Cambio de 40 a 35
relocate = 25           # Cambio de 35 a 25
```

### 5.4 Guardar el archivo

```powershell
# Ctrl+S en VS Code
# O: File → Save
```

---

## 📍 PASO 6: VALIDAR RESULTADOS (30 minutos) - OPCIONAL

Para verificar que los nuevos parámetros son mejores:

### 6.1 Ejecutar un experimento FULL

```powershell
# Ejecutar con los nuevos parámetros
python scripts/experiments.py --mode FULL
```

**Duración**: ~10-15 minutos

**Esperado**:
```
========================================
FULL EXPERIMENT: All 6 families
========================================

... resultados de todas las 56 instancias ...

SUMMARY
Completados: 56/56
Algoritmo 2 (Control): D=1182.19
Algoritmo 3 (OPTIMIZADO): D=1400.00  (mejor que antes)
```

### 6.2 Comparar con ITER-7

```
ITER-7 (parámetros anteriores):
  Algo 3: D=1408.04

ITER-8 (optimizado):
  Algo 3: D=1400.00

Mejora: 8.04 km (0.57%)
```

---

## 📍 PASO 7: GIT COMMIT (5 minutos)

Guardar los cambios en repositorio:

### 7.1 Ver cambios

```powershell
git status
```

**Verás**:
```
modified:   src/gaa/algorithm_generator.py
```

### 7.2 Commit de cambios

```powershell
git add src/gaa/algorithm_generator.py
git commit -m "ITER-8: Parámetros optimizados para Algoritmo 3 en familia C1 - While=75, 2Opt_pre=35, DB=1.8, 2Opt_post=35, Relocate=25"
```

### 7.3 Push a repositorio

```powershell
git push origin main
```

---

## 🎓 RESUMEN DE PASOS

| Paso | Tarea | Duración | Obligatorio |
|------|-------|----------|------------|
| 1 | Preparación | 5 min | ✅ |
| 2 | Lectura rápida | 5 min | ✅ |
| 3A | Prueba rápida | 10 min | ⚠️ Opcional |
| 3B | Búsqueda principal | 3h | ✅ |
| 4 | Revisar resultados | 10 min | ✅ |
| 5 | Aplicar parámetros | 15 min | ✅ |
| 6 | Validar (FULL test) | 30 min | ⚠️ Opcional |
| 7 | Git commit | 5 min | ✅ |
| **TOTAL** | | **4.5h** | |

---

## ⚠️ PROBLEMAS COMUNES

### Problema: "ModuleNotFoundError"

```powershell
# Solución: Estar en directorio correcto
cd c:\Users\alfab\Desktop\bestbestGAA\projects\GAA-VRPTW-GRASP-2
python parameter_tuner_algo3.py --num-combinations 100
```

### Problema: "best_known_solutions.json not found"

```powershell
# Verificar que el archivo existe
ls best_known_solutions.json

# Si no existe, buscar:
cd ..
cd ..
ls best_known_solutions.json
```

### Problema: Ejecución muy lenta

```powershell
# Normal: ~1.6 minutos por combinación × 100 = 160 minutos

# Si tarda MÁS, puede ser:
# 1. Computadora ocupada
# 2. Disco duro lento
# 3. SSD lleno

# Solución: Ejecutar cuando no haya otros programas
```

---

## ✅ CHECKLIST FINAL

Antes de empezar:
- [ ] Estoy en `GAA-VRPTW-GRASP-2/`
- [ ] He leído VISUALIZACION_PLAN.md
- [ ] He verificado que existen los 4 archivos requeridos
- [ ] Tengo tiempo disponible (~3-4 horas o más)

Para ejecutar:
- [ ] Abro terminal PowerShell
- [ ] Ejecuto: `python parameter_tuner_algo3.py --num-combinations 100`
- [ ] Dejo ejecutándose

Después de 3-4 horas:
- [ ] Reviso `optimization_results_c1/report.txt`
- [ ] Extraigo parámetros del #1
- [ ] Actualizo `src/gaa/algorithm_generator.py`
- [ ] Hago git commit y push

---

## 🚀 ¡LISTO PARA COMENZAR!

```powershell
# En PowerShell, ejecuta:
cd c:\Users\alfab\Desktop\bestbestGAA\projects\GAA-VRPTW-GRASP-2
python parameter_tuner_algo3.py --num-combinations 100

# Luego... espera 3-4 horas 😊
```

---

**¡Buena suerte!** 🎯

