# 🚀 Ejecutar Protocolo de 3 Días - Guía Rápida

## Objetivo

**Descubrir por qué a veces se logran ~34 segundos** al ejecutar `demo_experimentation_both.py` y otras veces >100s.

El protocolo capturará datos durante 3 días para identificar qué **características de los algoritmos generados** causan esta variabilidad.

---

## ⚙️ Configuración Final

- **Timeout**: 300 segundos (5 minutos)
- **Duración**: 3 días continuos
- **Enfoque**: Variabilidad basada en características del algoritmo (constructor, operadores, criterios de aceptación, complejidad)

---

## 📋 Antes de Comenzar

```bash
# 1. Verificar Python 3
python3 --version  # Debe ser 3.8+

# 2. Instalar dependencia
pip3 install numpy

# 3. Navegar al proyecto
cd /ruta/a/bestbestGAA/projects/KBP-SA

# 4. Limpiar caché (opcional pero recomendado)
./scripts/clean_cache.sh
```

### Desactivar Suspensión

**Linux:**
```bash
sudo systemctl mask sleep.target suspend.target hibernate.target
```

**macOS:**
```bash
caffeinate -s &
```

**Windows:**
```bash
powercfg /change standby-timeout-ac 0
```

---

## 🎯 Comando Principal

### Ejecución Completa (3 días)

```bash
cd /ruta/a/bestbestGAA/projects/KBP-SA

# Ejecutar en background
nohup python3 scripts/run_3day_protocol.py > experiment_3days.log 2>&1 &

# Guardar PID
echo $! > experiment.pid

# Monitorear progreso
tail -f experiment_3days.log
```

**Nota**: No necesitas pasar argumentos - el timeout de 300s y duración de 3 días ya están configurados por defecto.

### Prueba Corta (2 horas para validar)

```bash
# Timeout 300s, duración 0.083 días ≈ 2 horas
python3 scripts/run_3day_protocol.py 300 0.083
```

---

## 📊 Durante la Ejecución

### Ver Progreso

```bash
# Progreso en tiempo real
tail -f experiment_3days.log

# Cuántas corridas llevamos
wc -l output/3day_protocol/*.csv

# Estadísticas cada 10 corridas
grep "PROGRESO EXPERIMENTAL" experiment_3days.log | tail -1
```

### Estadísticas Automáticas

El script imprime cada 10 corridas:
- Total de corridas
- Exitosas vs Timeouts (%)
- Tiempos: promedio, mínimo, máximo, mediana
- **Corridas que lograron ≤40s** (el objetivo)

---

## 📁 Archivos Generados

```
output/3day_protocol/
└── 3day_protocol_YYYYMMDD_HHMMSS.csv  ← Dataset principal
```

Cada fila = 1 corrida con:
- **Tiempos**: time_total, time_search, time_generation, etc.
- **Features del algoritmo**: constructor_type, operator_types, acceptance_criterion, complexity_score
- **Calidad**: gap_percent, hit (TRUE si gap ≤5%)

---

## 🔍 Análisis de Resultados

### Al Finalizar los 3 Días

```bash
# Analizar causas de variabilidad
python3 scripts/analyze_variability_causes.py output/3day_protocol/*.csv
```

Este script generará:

1. **Estadísticas Generales**
   - Tiempo promedio, mínimo, máximo
   - Variabilidad (factor de diferencia)

2. **Distribución de Tiempos**
   - RÁPIDAS (≤40s) - El objetivo ~34s
   - MEDIAS (40-100s)
   - LENTAS (>100s)

3. **Análisis Comparativo: RÁPIDAS vs LENTAS**
   - Constructores predominantes en cada categoría
   - Operadores predominantes
   - Criterios de aceptación
   - Scores de complejidad

4. **CONCLUSIONES**
   - ✅ Qué usar para lograr ~34s
   - ❌ Qué evitar para no superar 100s

### Ejemplo de Salida

```
📊 Estadísticas Generales (1500 corridas exitosas)
   • Promedio: 75.3s
   • Mínimo: 32.1s ⚡
   • Máximo: 285.4s
   • Variabilidad: 8.9x

📈 Distribución de Tiempos:
   • RÁPIDAS (≤40s): 245 (16.3%)
     - Promedio: 35.2s
     - Rango: 32.1s - 39.8s

   • MEDIAS (40-100s): 890 (59.3%)
   • LENTAS (>100s): 365 (24.3%)

🔍 ANÁLISIS COMPARATIVO: RÁPIDAS vs LENTAS

1️⃣  CONSTRUCTORES

Corridas RÁPIDAS (≤40s):
   • GreedyByValue: 98 veces (40.0%)
   • GreedyByWeight: 85 veces (34.7%)
   • RandomConstruct: 62 veces (25.3%)

Corridas LENTAS (>100s):
   • GreedyByRatio: 215 veces (58.9%)
   • GreedyByWeight: 95 veces (26.0%)
   • GreedyByValue: 55 veces (15.1%)

✅ Constructor predominante en RÁPIDAS: GreedyByValue
❌ Constructor predominante en LENTAS: GreedyByRatio

💡 CONCLUSIONES Y CAUSAS DE VARIABILIDAD

Para lograr tiempos ≤40s (objetivo ~34s), preferir:
   ✅ Constructor: GreedyByValue
   ✅ Operador: TwoExchange
   ✅ Aceptación: None

Para EVITAR tiempos >100s, NO usar:
   ❌ Constructor: GreedyByRatio
   ❌ Operador: FlipWorstItem
   ❌ Aceptación: Metropolis
```

---

## ⏹️ Detener el Experimento

```bash
# Método 1: Usar PID guardado
kill $(cat experiment.pid)

# Método 2: Ctrl+C si está en foreground

# Método 3: Buscar proceso
ps aux | grep run_3day_protocol
kill <PID>
```

**Importante**: Los datos ya capturados están guardados en el CSV, incluso si detienes antes de tiempo.

---

## 🎯 Qué Descubriremos

Al final de los 3 días, sabremos:

1. **Causa principal de variabilidad**: Qué características del algoritmo generado causan tiempos de ~34s vs >100s

2. **Receta óptima**: Combinación exacta de constructor + operador + aceptación para lograr ~34s

3. **Patrones a evitar**: Qué combinaciones generan timeouts o tiempos >100s

4. **Correlación complejidad-tiempo**: Si el score de complejidad predice el tiempo de ejecución

5. **Distribución real**: Qué % de algoritmos generados aleatoriamente caen en RÁPIDO/MEDIO/LENTO

---

## 📞 Soporte

Si todo va bien, verás:
```
[45] ⏱️  Iniciando - 14:23:45 (quedan 71.2h) ✅ 38.2s - 3 algoritmos
```

Si ves muchos timeouts:
```
[45] ⏱️  Iniciando - 14:23:45 (quedan 71.2h) ⚠️  TIMEOUT (300s)
```
→ Es normal, el timeout de 300s permite capturar toda la variabilidad

---

## ✅ Checklist Final

- [ ] Python 3.8+ instalado
- [ ] `pip3 install numpy`
- [ ] Suspensión/hibernación desactivada
- [ ] Conectado a corriente (si es laptop)
- [ ] Espacio en disco (>2GB recomendado)
- [ ] Navegado a: `/ruta/a/bestbestGAA/projects/KBP-SA`

## 🚀 Comando Final

```bash
nohup python3 scripts/run_3day_protocol.py > experiment_3days.log 2>&1 &
echo $! > experiment.pid
tail -f experiment_3days.log
```

**¡Eso es todo! El protocolo se ejecutará durante 3 días capturando todas las características de los algoritmos generados.**

Después de 3 días, ejecuta el análisis para descubrir la causa raíz de por qué a veces se logran ~34s.
