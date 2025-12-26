# Instrucciones para Ejecutar Protocolo Experimental de 3 Días

## 📋 Resumen del Protocolo

Este protocolo ejecutará pruebas continuas durante 3 días para identificar:
1. **Patrones de algoritmos** que generan tiempos óptimos (~34s)
2. **Efectos de caché** y otros factores de variabilidad
3. **Características** que correlacionan con rendimiento

---

## 🖥️ Cómo Ejecutar en tu PC Local

### Paso 1: Preparar el Entorno

```bash
# 1. Navegar al directorio del proyecto
cd /ruta/a/bestbestGAA/projects/KBP-SA

# 2. Verificar que Python 3 esté instalado
python3 --version  # Debe ser Python 3.8+

# 3. Verificar dependencias
pip3 install numpy  # Si no está instalado
```

### Paso 2: Configurar el Timeout

**⚠️ IMPORTANTE**: El timeout de 60s del protocolo original es muy restrictivo.

Basado en las pruebas, recomiendo usar **180s (3 minutos)**:
- Permite completar ejecuciones normales (~34-120s)
- Descarta solo casos extremos (>180s)
- Genera más datos útiles

```bash
# Editar el timeout en scripts/run_3day_protocol.py
# O pasar como argumento (ver abajo)
```

### Paso 3: Ejecutar el Protocolo

#### Opción A: Ejecución Completa de 3 Días

```bash
cd /ruta/a/bestbestGAA/projects/KBP-SA

# Con timeout de 180s y duración de 3 días
python3 scripts/run_3day_protocol.py 180 3

# El primer argumento es timeout (segundos)
# El segundo argumento es duración (días)
```

#### Opción B: Prueba Corta (1 hora para validar)

```bash
# Timeout 180s, duración 0.042 días ≈ 1 hora
python3 scripts/run_3day_protocol.py 180 0.042
```

#### Opción C: Ejecutar en Background (Recomendado)

```bash
# Ejecutar en background y guardar log
nohup python3 scripts/run_3day_protocol.py 180 3 > experiment.log 2>&1 &

# Ver el PID del proceso
echo $!

# Monitorear progreso en tiempo real
tail -f experiment.log

# Ver estadísticas actuales
grep "PROGRESO EXPERIMENTAL" experiment.log | tail -1
```

### Paso 4: Detener el Experimento

```bash
# Si necesitas detener antes de tiempo
kill <PID>  # Reemplazar <PID> con el número del proceso

# O usando Ctrl+C si está en foreground
```

---

## 🧹 Limpieza de Caché y Otros Factores

### Factores de Variabilidad a Investigar

El protocolo ahora incluye registro de:

1. **Caché de Python**
   - Archivos `.pyc` compilados
   - Cache de imports

2. **Caché del Sistema Operativo**
   - Page cache de archivos
   - Buffer cache

3. **Estado de Memoria**
   - RAM disponible
   - Uso de swap

4. **CPU**
   - Carga del sistema
   - Throttling térmico

5. **Otros Procesos**
   - Competencia por recursos
   - Background tasks

### Script de Limpieza Pre-Ejecución

Voy a crear un script que limpie todo antes de cada corrida:

```bash
# El script limpiará automáticamente:
# - Cache de Python (__pycache__)
# - Archivos .pyc
# - Cache del sistema (si tiene permisos)
```

---

## 📊 Archivos que se Generarán

Durante los 3 días se generarán:

```
output/3day_protocol/
├── 3day_protocol_YYYYMMDD_HHMMSS.csv     # Dataset principal (Excel compatible)
├── 3day_protocol_YYYYMMDD_HHMMSS.json    # Datos completos en JSON
└── 3day_protocol_YYYYMMDD_HHMMSS_features.json  # Features de algoritmos
```

### Formato del CSV

Cada fila = 1 corrida, con columnas:

```
run_id, timestamp, algorithm_id, execution_status,
time_generation, time_initialization, time_search, time_evaluation, time_postprocessing, time_total,
objective_value, optimal_value, absolute_error, relative_error, gap_percent, hit,
constructor_type, num_operators, operator_types, has_loop, loop_budget, acceptance_criterion,
num_evaluations, tree_depth, complexity_score
```

---

## 📈 Monitoreo Durante los 3 Días

### Ver Progreso en Tiempo Real

```bash
# Opción 1: tail del log
tail -f experiment.log

# Opción 2: Contar corridas completadas
wc -l output/3day_protocol/*.csv

# Opción 3: Ver últimas corridas exitosas
tail -20 output/3day_protocol/*.csv
```

### Estadísticas Intermedias

El script imprime automáticamente cada 10 corridas:
- Total de corridas
- Exitosas vs Timeouts
- Tiempos promedio/mín/máx
- Tasa de HITs

---

## 🎯 Ajustes Recomendados Según Resultados Previos

### Timeout Sugerido: 180s

Basado en observaciones:
- Ejecuciones rápidas: ~34-40s
- Ejecuciones medias: ~80-100s
- Ejecuciones lentas: ~120-180s
- Casos extremos: >180s (deberían ser descartados)

**Cambio de 60s → 180s**:
- Permite capturar más variabilidad
- Reduce timeouts al ~20-30%
- Genera datos más útiles

### Alternativas de Timeout

```bash
# Conservador (captura casi todo)
python3 scripts/run_3day_protocol.py 240 3

# Intermedio (recomendado)
python3 scripts/run_3day_protocol.py 180 3

# Agresivo (solo casos óptimos)
python3 scripts/run_3day_protocol.py 120 3

# Original del protocolo (muy restrictivo)
python3 scripts/run_3day_protocol.py 60 3
```

---

## ⚠️ Recomendaciones para los 3 Días

### Antes de Comenzar

1. **Liberar espacio en disco**: Al menos 1GB libre
2. **Conectar a corriente**: Si es laptop, mantener conectado
3. **Desactivar suspensión/hibernación**:
   ```bash
   # Linux
   sudo systemctl mask sleep.target suspend.target hibernate.target

   # macOS
   caffeinate -s &

   # Windows
   powercfg /change standby-timeout-ac 0
   ```
4. **Cerrar aplicaciones pesadas**: Navegadores con muchas tabs, IDEs, etc.

### Durante la Ejecución

1. **No interrumpir manualmente** (usar Ctrl+C solo si es necesario)
2. **Evitar tareas intensivas** en la misma máquina
3. **Verificar progreso 1-2 veces al día**

### Al Finalizar

1. **Backup de archivos CSV/JSON** inmediatamente
2. **No borrar** hasta haber analizado
3. **Ejecutar análisis** (scripts que crearé a continuación)

---

## 🔬 Análisis Post-Experimento

Después de los 3 días, ejecutar:

```bash
# Analizar resultados (script que crearé)
python3 scripts/analyze_3day_results.py output/3day_protocol/*.csv
```

Generará:
- Patrones de algoritmos rápidos vs lentos
- Correlaciones tiempo-features
- Distribuciones temporales
- Recomendaciones para optimización

---

## 📞 Troubleshooting

### Problema: Todos son Timeouts

**Solución**: Aumentar timeout
```bash
python3 scripts/run_3day_protocol.py 240 3  # 4 minutos
```

### Problema: Consume mucha RAM

**Solución**: El script ya minimiza uso de memoria. Si persiste, reiniciar cada N horas:
```bash
# Ejecutar en loop con reinicios
while true; do
  timeout 8h python3 scripts/run_3day_protocol.py 180 0.33
  sleep 60
done
```

### Problema: Disco lleno

**Solución**: Los CSV son compactos (~1KB por corrida). En 3 días con ~1000 corridas = ~1MB

### Problema: Proceso se detuvo

**Solución**: El CSV se guarda después de cada corrida. Los datos ya capturados están guardados.

---

## 📝 Checklist Pre-Ejecución

- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (numpy)
- [ ] Espacio en disco libre (>1GB)
- [ ] Timeout configurado (recomendado: 180s)
- [ ] Duración configurada (3.0 días)
- [ ] Suspensión/hibernación desactivada
- [ ] Corriente conectada (si es laptop)
- [ ] Aplicaciones pesadas cerradas
- [ ] Comando preparado con nohup y background

## 🚀 Comando Final Recomendado

```bash
cd /ruta/a/bestbestGAA/projects/KBP-SA

# Ejecutar con configuración óptima
nohup python3 scripts/run_3day_protocol.py 180 3 > experiment_3days.log 2>&1 &

# Guardar PID
echo $! > experiment.pid

# Verificar que está corriendo
tail -f experiment_3days.log
```

---

**¡Listo para ejecutar el protocolo de 3 días!**

Para cualquier duda, revisar el log o interrumpir con: `kill $(cat experiment.pid)`
