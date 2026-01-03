# ITER-4 Ejecución: Metodología Científica

## Objetivo

Probar si un **constructor adaptativo** (RandomizedInsertion para familias clustered) mejora significativamente el desempeño en instancias C2 (clustered largo-horizon).

## Problema a Resolver

**ITER-3 Problema Identificado:**
```
Familia C2: Algoritmo 2 obtiene siempre distancia = 1148.78
BKS publicado = 589.86
GAP = +94.76% (INACEPTABLE)

Todas las 8 instancias C2 tienen exactamente el mismo valor.
Esto sugiere convergencia a un mínimo local único.
```

## Hipótesis Científica

**H0 (Nula):** Constructor RandomizedInsertion NO mejora C2 significativamente  
**H1 (Alternativa):** Constructor RandomizedInsertion MEJORA C2 con GAP reducido > 15%

## Diseño Experimental

### Comparación

| Aspecto | ITER-3 (Baseline) | ITER-4 (Propuesta) |
|---------|------------------|-------------------|
| **Constructor C1/C2** | NearestNeighbor | RandomizedInsertion |
| **Constructor R1/R2/RC** | NearestNeighbor | NearestNeighbor (sin cambios) |
| **Max Iteraciones** | 80 | 100 (+25%) |
| **TwoOpt Iteraciones** | 50 | 60 (+20%) |
| **Hipótesis** | Generic | Family-aware |

### Instancias

- C201, C202, C203, C204, C205, C206, C207, C208
- Total: 8 instancias
- Familia: Clustered, 100 clientes, horizon largo
- Tiempo estimado: 2-3 minutos

### Métrica de Éxito

```
Δ GAP = GAP_ITER3 - GAP_ITER4

Éxito si: Δ GAP > 15 puntos porcentuales
  (Significa reducir +94.76% a < 80%)
```

## Evidencia Teórica

**Por qué RandomizedInsertion podría funcionar mejor:**

1. **NearestNeighbor ignora clustering:**
   - Busca cliente más cercano globalmente
   - Cruza clusters innecesariamente
   - Viola implícitamente ventanas de tiempo

2. **RandomizedInsertion respeta estructura:**
   - Inicia con 3 clientes dispersos
   - Inserta clientes en posición de costo mínimo
   - Mantiene coherencia de clusters naturales

3. **Aleatoriedad permite escape:**
   - 25% de randomness permite diversificación
   - Múltiples runs pueden encontrar soluciones distintas
   - No converge siempre al mismo mínimo local

## Ejecución

```bash
python run_iter4_c2.py
```

**Resultado esperado:**
- Salida en consola mostrando resultados por instancia
- Tabla comparativa ITER-3 vs ITER-4
- Test de hipótesis automático
- Archivos de salida: JSON + CSV

## Decisiones Post-Experimento

### Si Δ GAP > 15% (ÉXITO)
✅ **Mantener ITER-4 como configuración final**
- Algoritmo 2 con constructor adaptativo es superior
- Documentar en paper como "family-aware construction"
- Listo para publicación académica

### Si 5% < Δ GAP ≤ 15% (ÉXITO PARCIAL)
⚠️ **Investigación adicional (ITER-5)**
- Constructor adaptativo ayuda pero no resuelve
- Probar perturbación más agresiva en C2
- O parámetros de iteración más altos

### Si Δ GAP ≤ 5% (FRACASO)
❌ **Aceptar limitación**
- Especialidad comprobada: R1, RC1, RC2
- Debilidad intrínseca en C2 (problema del dominio)
- Publicar con disclaimer claro
- Recomendación: híbridos para C2

## Documentación Esperada

Al completar ITER-4:

1. ✅ `ITER4_PLAN.md` - Diseño científico (este archivo)
2. ✅ `run_iter4_c2.py` - Código experimental (listo para ejecutar)
3. ⏳ `output/ITER4_C2_*/iter4_results.json` - Datos completos
4. ⏳ `output/ITER4_C2_*/iter4_results.csv` - Formato tabulado
5. ⏳ `ITERACIONES_COMPLETAS_ANALISIS.md` Sección 11 - Conclusiones ITER-4

---

## Próximo Paso

**Ejecutar el experimento:**
```bash
python run_iter4_c2.py
```

El script:
1. Cargará 8 instancias C2
2. Ejecutará Algoritmo 2 ITER-3 en cada una
3. Ejecutará Algoritmo 2 ITER-4 en cada una
4. Calculará mejoras
5. Hará test de hipótesis
6. Guardará resultados

Tiempo esperado: 2-3 minutos
