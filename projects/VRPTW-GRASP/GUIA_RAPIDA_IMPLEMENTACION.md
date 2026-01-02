# 🚀 GUÍA RÁPIDA DE IMPLEMENTACIÓN - VRPTW-GRASP con GAA

**Fecha**: 1 de Enero de 2026  
**Audiencia**: Desarrollador que comienza implementación  
**Duración**: Lectura 10 minutos | Implementación 8-10 semanas

---

## 📌 LA ESENCIA EN 60 SEGUNDOS

**¿Qué necesita VRPTW-GRASP?**

Implementar un sistema que **genere automáticamente 3 algoritmos GRASP diferentes** y los **execute en 56 instancias Solomon** para medir su performance.

**¿Cómo?**

1. **GAA (Generación Automática)**: Crea árboles sintácticos (AST) de algoritmos
2. **Operadores**: Ya existen 22 operadores VRPTW (constructivos, mejora, reparación)
3. **Scripts**: Ejecutan los algoritmos generados contra instancias Solomon
4. **Visualización**: Gráficas de resultados comparativos

**¿Cuánto código?**

- **Falta crear**: ~6,000 líneas (gaa/, utils/, config/, tests/, scripts/, visualization/, experimentation/)
- **Ya existe**: ~4,000 líneas (core/, operators/, metaheuristic/, data/)
- **Total proyecto**: ~10,000 líneas

---

## 🗂️ ESTRUCTURA VISUAL

```
┌─────────────────────────────────────────────────────────┐
│  scripts/                                              │
│  ├─ demo_experimentation_quick.py  (36 experimentos)  │
│  └─ demo_experimentation_full.py   (168 experimentos) │
└────────────────┬────────────────────────────────────────┘
                 │
     ┌───────────┼───────────┐
     │           │           │
┌────▼────┐ ┌────▼────┐ ┌────▼────────┐
│   gaa/  │ │operators/│ │visualization/
│ Genera  │ │ Ejecuta  │ │  Grafica
│algoritmo│ │ operador │ │  Resultado
└────┬────┘ └────┬────┘ └────┬────────┘
     │           │           │
     └───────────┼───────────┘
                 │
         ┌───────▼───────┐
         │     core/     │
         │ Problema +    │
         │ Solución      │
         └───────────────┘
```

---

## 📋 4 FASES DE IMPLEMENTACIÓN

### FASE 1️⃣: CREAR INFRAESTRUCTURA (Semana 1)

**Qué hacer**: Crear módulos base sin implementar lógica compleja

```
☐ Crear carpeta gaa/
  ├─ __init__.py
  ├─ ast_nodes.py (esqueleto)
  ├─ grammar.py (esqueleto)
  ├─ generator.py (esqueleto)
  ├─ interpreter.py (esqueleto)
  └─ README.md

☐ Crear carpeta utils/
  ├─ config.py (cargar config.yaml)
  ├─ output_manager.py (adaptar de GAA-GCP-ILS-4)
  └─ algorithm_visualizer.py

☐ Crear carpeta config/
  └─ config.yaml (parámetros centralizados)

☐ Crear carpeta tests/
  └─ conftest.py (fixtures pytest)
```

**Tiempo**: 15-20 horas

---

### FASE 2️⃣: IMPLEMENTAR GAA (Semana 2)

**Qué hacer**: Completar módulo gaa/ que genera algoritmos

```
☐ ast_nodes.py (450 líneas)
  └─ Clases: ASTNode, Seq, Call, ChooseBestOf, 
             ApplyUntilNoImprove, etc.

☐ grammar.py (250 líneas)
  └─ Clase Grammar con:
     • CONSTRUCTIVE_TERMINALS (4 operadores)
     • IMPROVEMENT_TERMINALS (8 operadores)
     • REPAIR_TERMINALS (3 operadores)
     • validate_algorithm()

☐ generator.py (300 líneas)
  └─ Clase AlgorithmGenerator que:
     • generate_with_validation() → AST válido
     • Respeta restricciones GRASP
     • seed=42 para reproducibilidad

☐ interpreter.py (350 líneas)
  └─ Clase ASTInterpreter que:
     • execute(ast) → solución VRPTW
     • Ejecuta cada nodo del AST
     • Retorna métricas (distance, vehicles, gap)
```

**Tiempo**: 40-60 horas

**Dependencia**: Operadores VRPTW deben estar listos

---

### FASE 3️⃣: CREAR SCRIPTS EXPERIMENTALES (Semana 3)

**Qué hacer**: Scripts que orquestan todo

```
☐ demo_experimentation_quick.py (400 líneas)
  ├─ Genera 3 algoritmos (seed=42)
  ├─ Carga familia R1 (12 instancias)
  ├─ Ejecuta 3 algoritmos × 12 instancias = 36 experimentos
  ├─ Guarda resultados JSON
  └─ Genera 20 gráficas PNG

☐ demo_experimentation_full.py (500 líneas)
  ├─ Reutiliza 3 algoritmos de quick
  ├─ Carga TODAS familias (56 instancias)
  ├─ Ejecuta 3 algoritmos × 56 instancias = 168 experimentos
  ├─ Análisis por familia
  └─ Genera 70+ gráficas PNG

☐ Tests unitarios (1,500 líneas)
  ├─ test_gaa.py (20 tests)
  ├─ test_operators.py (25 tests)
  ├─ test_grasp.py (15 tests)
  └─ Cobertura ≥70%
```

**Tiempo**: 40-50 horas

**Dependencia**: GAA y utils listos

---

### FASE 4️⃣: VISUALIZACIÓN Y ANÁLISIS (Semana 4)

**Qué hacer**: Gráficas y análisis estadístico

```
☐ visualization/
  ├─ plotter.py (gráficas de gaps, tiempo, vehículos)
  ├─ route_visualizer.py (dibuja rutas en mapa)
  └─ convergence.py (curvas de convergencia)

☐ experimentation/
  ├─ statistics.py (análisis estadístico)
  └─ comparative_analysis.py (comparativas)
```

**Tiempo**: 25-35 horas

**Dependencia**: Scripts experimentales completados

---

## 🎯 ORDEN DE IMPLEMENTACIÓN RECOMENDADO

```
SEMANA 1:
  1. Crear estructura gaa/, utils/, config/
  2. Implementar base de clases en cada módulo
  3. setup.py y requirements.txt
  
SEMANA 2:
  1. ast_nodes.py (completo)
  2. grammar.py (completo)
  3. Validar con tests unitarios
  
SEMANA 3:
  1. generator.py (completo)
  2. interpreter.py (completo)
  3. Tests de gaa/ (completo)
  
SEMANA 4:
  1. Reestructurar operators/ (agregar base.py)
  2. Implementar demo_experimentation_quick.py
  3. Validación end-to-end
  
SEMANA 5:
  1. Implementar demo_experimentation_full.py
  2. Agregar tests de integración
  
SEMANA 6-7:
  1. visualization/
  2. experimentation/
  
SEMANA 8-9:
  1. Testing exhaustivo
  2. Documentación
  3. Optimizaciones
  
SEMANA 10:
  1. Validación final
  2. Reportes
```

---

## 🔧 HERRAMIENTAS Y REFERENCIAS

### Copiar de GAA-GCP-ILS-4

Estos archivos ya funcionan y puedes adaptarlos:

```
GAA-GCP-ILS-4/
├── utils/output_manager.py          → utils/output_manager.py
├── visualization/plotter.py         → visualization/plotter.py
├── tests/conftest.py                → tests/conftest.py
└── scripts/gaa_quick_demo.py        → scripts/ (referencia)
```

### Adaptaciones Principales

| Componente | GAA-GCP-ILS-4 | VRPTW-GRASP | Cambio |
|-----------|---------------|-------------|--------|
| Problema | GraphColoringProblem | VRPTWProblem | Distinto dominio |
| Solución | ColoringSolution | VRPTWSolution | Distinto dominio |
| Operadores | DSATUR, LF, KempeChain | RandomizedInsertion, TwoOpt, CrossExchange | 22 operadores |
| Métrica | Número colores | Distancia + vehículos | Multi-objetivo |
| GAA | Misma idea | Misma idea | Reutilizable |
| Output | OutputManager | **Reutilizable** | Solo adaptar formato |

---

## 📁 ARCHIVOS A CREAR POR ORDEN

### PRIORIDAD CRÍTICA 🔴

```
1. config/config.yaml              [150 líneas]   ← Empieza aquí
2. gaa/ast_nodes.py                [450 líneas]   ← Luego esto
3. gaa/grammar.py                  [250 líneas]   ← Luego esto
4. gaa/generator.py                [300 líneas]   ← Luego esto
5. gaa/interpreter.py              [350 líneas]   ← Luego esto
6. utils/output_manager.py         [250 líneas]   ← Adaptar de GCP
7. scripts/demo_experimentation_quick.py [400 líneas] ← Validación
```

**Total**: ~2,150 líneas para MVP funcional

### PRIORIDAD ALTA 🟠

```
8. scripts/demo_experimentation_full.py  [500 líneas]
9. tests/test_gaa.py                     [350 líneas]
10. tests/conftest.py                    [300 líneas]
```

**Total**: ~1,150 líneas más

### PRIORIDAD MEDIA 🟡

```
11. visualization/plotter.py        [400 líneas]
12. visualization/route_visualizer.py [300 líneas]
13. experimentation/statistics.py   [300 líneas]
```

**Total**: ~1,000 líneas más

---

## 💡 CONSEJOS PRÁCTICOS

### 1. Validación Temprana
```python
# Prueba cada módulo mientras lo creas:
pytest tests/test_gaa.py -v
pytest tests/test_operators.py -v
```

### 2. Prototipa Primero
```python
# Genera 1 algoritmo manualmente:
grammar = Grammar()
gen = AlgorithmGenerator(grammar, seed=42)
ast = gen.generate_with_validation()
print(ast.to_pseudocode())
```

### 3. Usa Fixtures
```python
# conftest.py proporciona:
@pytest.fixture
def small_problem():
    return load_test_instance()

@pytest.fixture
def test_algorithm():
    return generate_test_algorithm()
```

### 4. Documenta Mientras Codificas
```python
# Cada módulo necesita README.md:
# - Qué hace
# - Ejemplo de uso
# - Dependencias
```

---

## 🧪 VALIDACIÓN MÍNIMA PARA MVP

Para considerar que está **LISTO** (`demo_quick.py` ejecuta exitosamente):

```
✅ 3 algoritmos generados con seed=42
✅ Pseudocódigo legible de cada algoritmo
✅ 12 instancias de R1 cargadas correctamente
✅ 36 experimentos ejecutados sin errores
✅ 100% soluciones factibles (sin violaciones)
✅ Output JSON con resultados estructurados
✅ 20 gráficas PNG generadas
✅ Tiempo total < 15 minutos
✅ Tests pasen con ≥70% coverage
```

---

## 📊 CHECKLIST RÁPIDO

### Pre-Implementación (YA HECHO)
- ✅ Especificación GAA completada (GAA_IMPLEMENTACION_VRPTW.md)
- ✅ Estructura documentada (ESTRUCTURA_CARPETAS_FUNCIONALES.md)
- ✅ Mapeo actual (MAPEO_ACTUAL_FUTURO.md)
- ✅ Checklist detallado (CHECKLIST_IMPLEMENTACION.md)

### Semana 1
- [ ] config/ creada
- [ ] gaa/ creada (esqueleto)
- [ ] utils/ creada (esqueleto)
- [ ] tests/ creada con conftest.py

### Semana 2
- [ ] ast_nodes.py completado
- [ ] grammar.py completado
- [ ] generator.py completado
- [ ] Tests de gaa funcionando

### Semana 3
- [ ] interpreter.py completado
- [ ] demo_experimentation_quick.py completado
- [ ] 36 experimentos ejecutándose

### Semana 4+
- [ ] demo_experimentation_full.py completado
- [ ] visualization/ completada
- [ ] experimentation/ completada
- [ ] Documentación final

---

## 🆘 CUANDO DUDES

**"¿Por dónde empiezo?"**
→ Crea `config/config.yaml` con parámetros básicos

**"¿Cómo estructuro ast_nodes.py?"**
→ Mira `GAA-GCP-ILS-4/gaa/ast_nodes.py` como referencia

**"¿Cómo valido que funciona?"**
→ Corre `pytest` frecuentemente, no esperes al final

**"¿Qué hago si un operador no funciona?"**
→ Crea test unitario para ese operador específico

**"¿Es necesario tests desde el inicio?"**
→ Sí, te ahorra debugging futuro (test-driven development)

---

## 📞 RESUMEN EJECUTIVO

| Aspecto | Detalle |
|---------|---------|
| **Total Líneas de Código** | ~10,000 |
| **Ya Implementadas** | ~4,000 (core, operators, metaheuristic, data) |
| **Falta Implementar** | ~6,000 (gaa, utils, tests, scripts, visualization, experimentation) |
| **Tiempo Estimado** | 8-10 semanas (1-2 personas FTE) |
| **MVP Mínimo** | 2,150 líneas (Semana 2) |
| **Componentes Críticos** | gaa/, utils/, scripts/ |
| **Reutilizable de GCP** | output_manager.py, test fixtures, visualization patterns |
| **Métricas de Éxito** | 3 algoritmos generados, 36/168 experimentos ejecutados, 100% factibilidad |

---

## 🎓 SIGUIENTE LECTURA

1. **Entender GAA**: Lee `GAA_IMPLEMENTACION_VRPTW.md`
2. **Estructura Carpetas**: Lee `ESTRUCTURA_CARPETAS_FUNCIONALES.md`
3. **Checklist Detallado**: Lee `CHECKLIST_IMPLEMENTACION.md`
4. **Mapeo Actual**: Lee `MAPEO_ACTUAL_FUTURO.md`
5. **Empezar Código**: Abre Visual Studio Code y crea `config/config.yaml`

---

**Documento**: Guía Rápida de Implementación  
**Status**: Listo para Empezar  
**Próximo**: Crear primer archivo en código
