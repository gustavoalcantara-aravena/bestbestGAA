# ⚡ Quick Reference: GAA vs Literatura en 5 Minutos

**Hoja de referencia rápida para comparar GAA contra Best Known Solutions**

---

## 🎯 Lo Esencial

### ¿Qué es BKS?
**Best Known Solutions** = Valores de referencia de la literatura académica
- 81 instancias totales
- 55 con óptimo conocido (67.9%)
- 26 abiertas/desconocidas (32.1%)

### ¿Dónde está?
```
projects/GCP-ILS-GAA/datasets/BKS.json
```

### ¿Cómo comparar?
```bash
cd projects/GCP-ILS-GAA
python compare_with_bks.py --results-dir results/ --verbose
```

---

## 🚀 Flujo Rápido (5 pasos)

**Paso 1**: Ejecutar GAA
```bash
python 04-Generated/scripts/gaa_family_experiments.py --families CUL LEI REG
```

**Paso 2**: Comparar
```bash
python compare_with_bks.py --results-dir results/ --verbose
```

**Paso 3**: Leer output
```
COMPARISON: CUL Family vs Best Known Solutions
Instance             │ BKS   │ GAA   │ Gap
flat300_20_0         │    20 │    20 │ ✅ 0.0%
flat300_26_0         │    26 │    26 │ ✅ 0.0%
flat300_28_0         │    28 │    29 │ ⚠️ +3.6%

Found optimal:      3/6 (50.0%)
Average gap:        +2.13%
```

**Paso 4**: Interpretar
- ✅ = Óptimo encontrado (perfecto!)
- ⚠️ = Pequeño gap (aceptable)
- 🎉 = Superó BKS (¡nuevo descubrimiento!)

**Paso 5**: Documentar
```markdown
## Resultados
- Total: 32 instancias
- Óptimos: 29/32 (90.6%)
- Gap promedio: +0.84%
- Conclusión: ✅ Competitivo con literatura
```

---

## 📊 Símbolos de Status

| Símbolo | Significa | Interpretación |
|---------|-----------|---|
| ✅ | OPTIMAL | Gap=0%, GAA=BKS |
| 🎉 | BEAT BKS | Gap<0%, GAA<BKS |
| ⚠️ | NEAR BKS | Gap 0-1% |
| ⚠️ | GAP OK | Gap 1-5% |
| ❌ | GAP LARGE | Gap>5% |
| ❓ | OPEN | BKS desconocido |

---

## 🏠 Familias de Instancias

| Familia | Instancias | BKS Conocido | Nota |
|---------|------------|-------------|------|
| **CUL** | 6 | 100% | Validación básica ✅ |
| **LEI** | 12 | 100% | Garantías teóricas ⭐ |
| **REG** | 14 | 100% | Aplicación real |
| **DSJ** | 15 | 0% | ❓ ABIERTAS (oportunidad!) |
| **MYC** | 5 | 100% | Grafos especiales |
| **SGB** | 25 | 72% | Literatura + juegos |
| **SCH** | 2 | 0% | ❓ ABIERTAS |
| **LAT** | 1 | 0% | ❓ ABIERTA |

---

## 🔧 Comandos Útiles

### Comparar todas las familias
```bash
python compare_with_bks.py --results-dir results/ --verbose
```

### Comparar una familia
```bash
python compare_with_bks.py --results-dir results/ --family CUL
```

### Exportar a JSON
```bash
python compare_with_bks.py --results-dir results/ --output-format json --output-file comparison.json
```

### Ver solo resumen
```bash
python compare_with_bks.py --results-dir results/
```

---

## 📈 Métricas Clave

**Optimality Gap** (%)
```
= (GAA_value - BKS) / BKS * 100

0%      → Perfecto
0-1%    → Excelente
1-5%    → Bueno
5-10%   → Aceptable
>10%    → Pobre
```

**Success Rate** (%)
```
= (Instancias con óptimo) / (Total) * 100

Ejemplo: 29/32 = 90.6%
```

**Beat Rate** (%)
```
= (Instancias que superan BKS) / (Total) * 100

Ejemplo: 0/32 = 0% (aún no descubre nuevas)
```

---

## 🎓 Interpretación de Resultados

### Caso 1: ✅ Óptimo encontrado
```
flat300_20_0: BKS=20, GAA=20, Gap=0%
→ Perfecto. GAA iguala la literatura.
```

### Caso 2: ⚠️ Pequeño gap
```
flat300_28_0: BKS=28, GAA=29, Gap=+3.6%
→ Normal. Depende de parámetros.
→ Aún es competitivo (< 5%).
```

### Caso 3: 🎉 Superó BKS
```
DSJC125.1: BKS=?, GAA=13
→ ¡Excelente! GAA descubrió una solución.
→ Potencialmente publicable.
```

### Caso 4: ❓ Instancia abierta
```
school1: BKS=?, GAA=X
→ Sin referencia en literatura.
→ Compara solo contra baselines.
```

---

## 📚 Documentación Disponible

| Documento | Líneas | Cuándo leer |
|-----------|--------|----------|
| **RESUMEN_VALIDACION_LITERATURA.md** | 200 | Overview rápido |
| **GUIA_COMPARACION_LITERATURA.md** | 700 | Primera vez ejecutando |
| **COMPARACION_GAA_VS_LITERATURA.md** | 800 | Referencia detallada |
| **ARQUITECTURA_VALIDACION_LITERATURA.md** | 400 | Entender la arquitectura |
| **INDICE_MAESTRO_VALIDACION_LITERATURA.md** | 300 | Navegar documentación |
| **Este archivo (Quick Reference)** | 150 | Consulta rápida |

---

## ✅ Checklist Pre-Ejecución

- [ ] Verificar `datasets/BKS.json` existe
- [ ] Verificar `compare_with_bks.py` existe
- [ ] Ejecutar `gaa_family_experiments.py` primero
- [ ] Verificar `results/` fue creado
- [ ] Ejecutar `compare_with_bks.py`

---

## 🚨 Problemas Comunes

**Error: "BKS file not found"**
```bash
# Solución: Verificar que estás en el directorio correcto
cd projects/GCP-ILS-GAA
python compare_with_bks.py --bks-file datasets/BKS.json
```

**Error: "Results directory not found"**
```bash
# Solución: Ejecutar gaa_family_experiments.py primero
python 04-Generated/scripts/gaa_family_experiments.py --families CUL
```

**Error: "Family not found"**
```bash
# Solución: Usar nombre correcto (mayúsculas)
python compare_with_bks.py --results-dir results/ --family CUL  # ✅ Correcto
# NO: --family cul  (❌ Incorrecto)
```

---

## 🎯 Métricas Esperadas

Después de ejecutar en CUL, LEI, REG:

```
TYPICAL RESULTS
═══════════════════════════════════════════

CUL (Culberson):
  Óptimos encontrados:  50-80%
  Gap promedio:         0-3%
  Verdict:              ⚠️ Bueno

LEI (Leighton):
  Óptimos encontrados:  100%
  Gap promedio:         0.0%
  Verdict:              ✅ Excelente

REG (Compiladores):
  Óptimos encontrados:  100%
  Gap promedio:         0.0%
  Verdict:              ✅ Excelente

OVERALL:
  Óptimos:              90%+
  Gap promedio:         <1%
  Verdict:              ✅ EXCELLENT
                        (Competitive with SOTA)
```

---

## 💾 Archivos Generados

**Entrada**:
```
datasets/BKS.json               (81 instancias de referencia)
results/FAMILY/results.json     (resultados de GAA)
```

**Salida**:
```
Console output (stdout)          (reporte de comparación)
comparison.json (si --output)   (formato JSON exportado)
```

---

## 🔗 Relación con Otros Scripts

```
gaa_orchestrator.py
    ↓ (ejecuta GAA)
gaa_family_experiments.py
    ↓ (exporta resultados)
results/FAMILY/results.json
    ↓ (lee)
compare_with_bks.py
    ↓ (compara con)
datasets/BKS.json
    ↓ (genera)
REPORTE DE COMPARACIÓN
```

---

## 🏆 Qué Significa Cada Conclusión

### ✅ EXCELLENT
```
Se encontraron óptimos en 90%+ de instancias
Gap promedio < 1%
→ GAA es COMPETITIVO con literatura
→ Algoritmo está funcionando bien
→ Listo para producción
```

### ⚠️ GOOD
```
Se encontraron óptimos en 50-90%
Gap promedio 1-5%
→ GAA es ACEPTABLE pero mejorable
→ Considerar ajustar parámetros
→ Funciona pero no es óptimo
```

### ❌ NEEDS IMPROVEMENT
```
Se encontraron óptimos en <50%
Gap promedio > 5%
→ GAA necesita optimización
→ Revisar generación de algoritmos
→ Ajustar parámetros de búsqueda
```

### 🎉 NOVEL DISCOVERY
```
Beat BKS en instancias DSJ
→ GAA descubrió soluciones nuevas
→ Potencial publicable
→ Contribución a literatura
```

---

## 📞 Preguntas Frecuentes

**P: ¿Cuánto tarda la comparación?**
A: <1 segundo para 81 instancias

**P: ¿Debo ejecutar en todas las familias?**
A: No. Empieza con CUL+LEI+REG. DSJ es para encontrar nuevas soluciones.

**P: ¿Qué pasa si mi GAA no encuentra óptimos?**
A: Es normal. Metaheurísticas no garantizan óptimo. Gap < 5% es aceptable.

**P: ¿Cómo interpreto gap negativo?**
A: GAA superó el BKS documentado. ¡Excelente descubrimiento! 🎉

**P: ¿Puedo publicar si encuentro soluciones nuevas?**
A: Sí, especialmente en DSJ (instancias abiertas).

**P: ¿Necesito modificar BKS.json?**
A: No, es referencia. Solo léelo.

---

## 🎓 Conclusión Rápida

**Tu pregunta**: "¿En los datasets están los best known solutions?"

**Respuesta**: ✅ Sí, en `datasets/BKS.json`

**Qué hacer**:
1. Ejecuta GAA → genera `results/FAMILY/results.json`
2. Ejecuta `compare_with_bks.py` → compara vs BKS
3. Lee output → obtén status (✅, ⚠️, 🎉, ❓)
4. Documenta → guarda conclusiones

**Resultado**: Validación académica de tu GAA

---

## 📝 Template Respuesta Rápida

Cuando alguien te pregunta "¿Qué tal funcionó tu GAA?"

```
Excelente. Lo validé contra literatura:
- Total instancias: 32
- Óptimos encontrados: 29/32 (90.6%)
- Gap promedio: +0.84%
- Conclusión: Competitivo con estado del arte ✅

Ver: projects/GCP-ILS-GAA/RESUMEN_VALIDACION_LITERATURA.md
```

---

**Versión**: 1.0
**Estado**: ✅ Listo para usar
**Última actualización**: 2024
