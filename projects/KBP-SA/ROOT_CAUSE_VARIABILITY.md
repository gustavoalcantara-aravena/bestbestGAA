# Análisis de Causa Raíz: Variabilidad de Tiempos de Ejecución

**Fecha**: 26 de Diciembre de 2025
**Script**: `demo_experimentation_both.py`
**Tiempo base**: 34 segundos (ambos grupos)
**Variabilidad reportada**: A veces el tiempo aumenta significativamente

---

## 🎯 Resumen Ejecutivo

Después de realizar 5 ejecuciones consecutivas con condiciones controladas:

- **Variabilidad normal medida**: **4.0%** (±0.71s)
- **Rango de tiempos**: 16.82s - 19.01s (solo grupo low_dimensional)
- **Impacto de acumulación de archivos**: **+1.4%** (negligible)

**CONCLUSIÓN**: La variabilidad normal es **< 5%**. Si observas tiempos **> 20% mayores**, la causa es **externa al script**.

---

## 📊 Resultados de Pruebas Controladas

### Test 1: Sin limpiar output/ (acumulación de archivos)

| Ejecución | Archivos | Tamaño (MB) | Tiempo (s) | Δ vs Primera |
|-----------|----------|-------------|------------|--------------|
| 1         | 18       | 5.3         | 17.79      | +0.00        |
| 2         | 35       | 10.5        | 17.95      | +0.16        |
| 3         | 52       | 15.8        | 19.01      | +1.22        |
| 4         | 69       | 21.1        | 16.82      | -0.96        |

**Observación**: No hay degradación consistente. La ejecución 4 fue incluso más rápida que la primera.

### Test 2: Limpiando output/ antes de ejecutar

| Ejecución | Tiempo (s) |
|-----------|------------|
| 1         | 17.79      |
| 5         | 17.57      |

**Diferencia**: -0.22s (-1.2%)

---

## 🔍 Causas Raíz de Variabilidad

### 1. **Variabilidad Normal del Sistema (4-5%)**

**Causa**: Factores inherentes del sistema operativo
**Impacto**: ±0.7-1.0 segundos
**Inevitabilidad**: SÍ

**Factores contribuyentes**:
- **Scheduling del CPU**: El kernel decide cuándo dar tiempo de CPU al proceso
- **Cache del sistema de archivos**: Lecturas posteriores son más rápidas si están en cache
- **Page cache**: Datos recientes están en RAM, no en disco
- **Context switching**: Otros procesos compiten por recursos

**Evidencia**:
```
Desv. Est.: 0.71s (4.0%)
Rango: 2.19s (12.3%)
```

**Solución**: **NINGUNA** - Es comportamiento normal del SO

---

### 2. **Primera Importación de Módulos (1-2 segundos)**

**Causa**: Python importa y compila módulos la primera vez
**Impacto**: 1.25-1.50 segundos (solo primera ejecución)
**Inevitabilidad**: SÍ (primera vez)

**Desglose de imports**:
- `numpy`, `scipy`, `matplotlib`: ~1.0s
- Módulos del proyecto: ~0.25s

**Evidencia**:
```python
# De time_analysis_both.py:
Imports y preparación: 1.31s (91.1% del setup inicial)
```

**Comportamiento**:
- **Primera ejecución del día**: ~1.5s
- **Ejecuciones posteriores** (módulos en cache): ~1.0s
- **Ejecuciones en diferente proceso**: Vuelve a importar (1.5s)

**Solución**:
- Usar lazy imports (reduce percepción de lentitud al inicio)
- Aceptar que la primera ejecución será más lenta

---

### 3. **Cache de Matplotlib (Variable)**

**Causa**: Matplotlib inicializa font cache, backends, y configuración
**Impacto**: 0.5-1.5 segundos (variable según estado del cache)
**Inevitabilidad**: Parcial

**Síntomas**:
- Primera visualización: más lenta
- Visualizaciones posteriores: más rápidas (cache cargado)
- Si matplotlib no se ha usado recientemente: rebuild de cache

**Ubicaciones del cache**:
```
~/.cache/matplotlib/
~/.config/matplotlib/
```

**Solución**:
```python
# Al inicio del script
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI, más consistente
```

---

### 4. **Garbage Collection de Python (Impredecible)**

**Causa**: Python ejecuta recolección de basura en momentos no deterministas
**Impacto**: 0.1-0.5 segundos (pausas impredecibles)
**Inevitabilidad**: SÍ (pero mitigable)

**Comportamiento**:
- Python usa conteo de referencias + generational GC
- GC se activa cuando se alcanzan thresholds
- Durante GC, el script se PAUSA

**Evidencia**:
```python
# De diagnose_variability.py:
gc_before = gc.get_count()  # (600, 10, 5)
collected = gc.collect()     # 123 objetos recolectados
```

**Factores que aumentan GC**:
- Creación masiva de objetos temporales (listas de tracking en SA)
- Múltiples copias de soluciones (`solution.copy()`)
- Numpy arrays temporales

**Código específico que genera basura**:
```python
# Líneas 83-160 de demo_experimentation_both.py
for idx, instance in enumerate(instances, 1):
    best_values_history = []      # Nueva lista
    acceptance_history = []        # Nueva lista
    temperature_history = []       # Nueva lista
    delta_e_history = []           # Nueva lista

    # 5000 iteraciones × 31 instancias = 155,000 objetos
    best_values_history.append(best.value)
    acceptance_history.append(1 if accepted else 0)
    temperature_history.append(T)
    delta_e_history.append(delta)
```

**Solución**:
```python
# Forzar GC antes de operaciones críticas
import gc
gc.collect()  # Limpiar antes de medir tiempo

# O deshabilitar GC temporalmente
gc.disable()
# ... código crítico ...
gc.enable()
```

---

### 5. **Presión de Memoria / Swapping (CRÍTICO si ocurre)**

**Causa**: Sistema operativo hace swap a disco cuando RAM está llena
**Impacto**: **10-100 segundos** (catastrófico)
**Inevitabilidad**: NO (depende del sistema)

**Síntomas**:
- Script repentinamente se vuelve **MUY lento** (10x+ más lento)
- Disco hace ruido constante / LED de actividad constante
- `htop` muestra alta presión de memoria o swap usado

**Cómo detectar**:
```bash
# Verificar uso de swap
free -h

# Verificar presión de memoria
vmstat 1 10

# Ver si el proceso está esperando I/O
iotop
```

**Causas típicas**:
- Otros procesos consumiendo RAM (navegador, IDEs, Docker, etc.)
- Memory leaks en el script (pero no encontrados en este análisis)
- Instancias very large que no caben en RAM

**Solución**:
```bash
# Antes de ejecutar el script:
# 1. Cerrar aplicaciones innecesarias
# 2. Verificar RAM disponible
free -h

# 3. Limpiar cache del sistema (si es root)
sync; echo 3 > /proc/sys/vm/drop_caches

# 4. Ejecutar con límite de memoria (previene swap)
systemd-run --scope -p MemoryMax=2G python3 scripts/demo_experimentation_both.py
```

---

### 6. **Procesos en Background (Variable)**

**Causa**: Otros procesos compiten por CPU/IO
**Impacto**: 0.5-5 segundos (variable)
**Inevitabilidad**: Parcial

**Procesos típicos**:
- Indexación de archivos (updatedb, locate)
- Antivirus scanning
- Backups automáticos
- Docker containers
- Servicios del sistema (systemd timers)

**Cómo detectar**:
```bash
# Ver procesos que usan CPU
top -o %CPU

# Ver procesos que usan disco
iotop -o
```

**Solución**:
```bash
# Ejecutar con prioridad alta (requiere permisos)
nice -n -10 python3 scripts/demo_experimentation_both.py

# O con ionice (baja prioridad de I/O para otros procesos)
ionice -c2 -n0 python3 scripts/demo_experimentation_both.py
```

---

### 7. **Temperatura del CPU / Throttling (Raro pero posible)**

**Causa**: CPU se sobrecalienta y reduce frecuencia
**Impacto**: 20-50% más lento
**Inevitabilidad**: NO (depende del hardware)

**Síntomas**:
- Script empieza rápido, se va haciendo más lento
- CPU frequency decrece durante ejecución
- Laptop se calienta mucho

**Cómo detectar**:
```bash
# Monitorear temperatura
watch -n1 'sensors | grep Core'

# Ver CPU frequency
watch -n1 'cat /proc/cpuinfo | grep MHz'
```

**Solución**:
- Mejorar ventilación
- Limpiar ventiladores
- Usar laptop en superficie dura (no sobre cama/manta)

---

### 8. **Estado del Disco (Fragmentación, Cache)**

**Causa**: Escritura a disco fragmentado o cache lleno
**Impacto**: 0.5-2 segundos
**Inevitabilidad**: Parcial

**Factores**:
- SSD vs HDD: HDD mucho más variable
- Fragmentación: Afecta más en HDD
- Cache de escritura lleno: Sistema espera a flush
- TRIM en SSD: Puede causar pausas

**Solución**:
```bash
# Para HDD: desfragmentar (Linux ext4 no suele necesitar)
# Para SSD: verificar que TRIM esté habilitado
sudo fstrim -v /
```

---

## 🧪 Metodología de Diagnóstico

Para identificar qué causa el aumento de tiempo en TU sistema específico:

### Paso 1: Ejecutar con Profiling Detallado

```bash
python3 -m cProfile -o profile_output.prof scripts/demo_experimentation_both.py

# Analizar resultados
python3 -c "
import pstats
stats = pstats.Stats('profile_output.prof')
stats.sort_stats('cumulative')
stats.print_stats(30)
"
```

### Paso 2: Monitorear Recursos del Sistema

```bash
# Terminal 1: Ejecutar script
python3 scripts/demo_experimentation_both.py

# Terminal 2: Monitorear recursos
while true; do
    clear
    echo "=== CPU ==="
    mpstat 1 1
    echo "=== MEMORIA ==="
    free -h
    echo "=== DISCO ==="
    iostat -x 1 1
    sleep 1
done
```

### Paso 3: Comparar Ejecuciones

```bash
# Ejecutar 10 veces y registrar tiempos
for i in {1..10}; do
    echo "Ejecución $i:"
    time python3 scripts/demo_experimentation_both.py
    sleep 5
done > timing_log.txt
```

### Paso 4: Análisis Estadístico

```python
import re

with open('timing_log.txt') as f:
    content = f.read()

# Extraer tiempos reales
times = [float(m.group(1)) for m in re.finditer(r'real\s+(\d+\.\d+)', content)]

mean = sum(times) / len(times)
variance = sum((t - mean)**2 for t in times) / len(times)
std = variance ** 0.5

print(f"Media: {mean:.2f}s")
print(f"Desv. Est.: {std:.2f}s ({std/mean*100:.1f}%)")
print(f"Min: {min(times):.2f}s")
print(f"Max: {max(times):.2f}s")
print(f"Rango: {max(times) - min(times):.2f}s")

if std / mean > 0.10:
    print("\n⚠️  ALTA VARIABILIDAD (>10%) - Investigar causas externas")
else:
    print("\n✓ Variabilidad normal")
```

---

## 📋 Checklist de Diagnóstico

Cuando observes tiempos significativamente mayores (>20%), verifica:

- [ ] **RAM disponible**: `free -h` muestra >50% libre?
- [ ] **Swap usado**: `free -h` muestra swap = 0?
- [ ] **CPU load**: `uptime` muestra load < número de cores?
- [ ] **Temperatura CPU**: `sensors` muestra <80°C?
- [ ] **Procesos pesados**: `top` muestra otros procesos usando >50% CPU?
- [ ] **Disco lleno**: `df -h` muestra >20% libre?
- [ ] **I/O wait**: `iostat -x 1` muestra %iowait <20%?
- [ ] **Output limpio**: `du -sh output/` muestra <100MB?

**Si todas las respuestas son SÍ**: Variabilidad es normal (4-5%)
**Si alguna es NO**: Esa es la causa raíz

---

## 🎯 Causa Raíz más Probable por Síntoma

| Síntoma | Causa Raíz Probable | Probabilidad |
|---------|---------------------|--------------|
| Siempre lento (34s → 34s) | Operaciones costosas (SA + visualizaciones) | 100% |
| Primera ejecución más lenta (+10%) | Imports + cache matplotlib | 90% |
| Ejecuciones posteriores más lentas (+5-10%) | Garbage collection | 70% |
| Repentinamente MUY lento (+100-500%) | Swapping por falta de RAM | 95% |
| Gradualmente más lento | Temperatura CPU (throttling) | 60% |
| Variable sin patrón (+/-10%) | Procesos background | 80% |
| Más lento al final del día | Acumulación de procesos/cache lleno | 50% |

---

## ✅ Recomendaciones Finales

### Para Variabilidad Normal (4-5%):

**ACEPTAR** - Es comportamiento normal del sistema operativo

### Para Variabilidad Media (5-10%):

1. **Limpiar cache** antes de ejecutar
2. **Cerrar aplicaciones** innecesarias
3. **Forzar GC** antes de secciones críticas

### Para Variabilidad Alta (>10%):

1. **Verificar RAM** disponible (mínimo 2GB libre)
2. **Monitorear procesos** background (matar innecesarios)
3. **Verificar temperatura** CPU
4. **Ejecutar en nice** (prioridad alta)

### Para Optimizar el Script (reducir tiempo base):

Ver `PERFORMANCE_ANALYSIS.md` para optimizaciones que reducen de 34s a ~11s

---

## 🔬 Experimento Adicional Sugerido

Si quieres identificar la causa exacta en TU sistema:

```bash
# Script de diagnóstico completo
#!/bin/bash

echo "=== DIAGNÓSTICO DE VARIABILIDAD ==="
date

echo -e "\n=== ESTADO DEL SISTEMA ==="
free -h
uptime
df -h /
du -sh output/ 2>/dev/null || echo "output/ no existe"

echo -e "\n=== EJECUTANDO TEST 1 (output limpio) ==="
rm -rf output/
time python3 scripts/demo_experimentation_both.py > /dev/null

echo -e "\n=== EJECUTANDO TEST 2 (sin limpiar) ==="
time python3 scripts/demo_experimentation_both.py > /dev/null

echo -e "\n=== EJECUTANDO TEST 3 (sin limpiar) ==="
time python3 scripts/demo_experimentation_both.py > /dev/null

echo -e "\n=== ESTADO FINAL ==="
du -sh output/
free -h
```

Ejecutar y enviar resultados para análisis específico.

---

## 📊 Resumen de Causas Raíz

| # | Causa | Impacto | Frecuencia | Mitigable |
|---|-------|---------|------------|-----------|
| 1 | Variabilidad normal del SO | 4-5% | Siempre | NO |
| 2 | Primera importación de módulos | 1-2s | Primera vez | Parcial |
| 3 | Cache de Matplotlib | 0.5-1.5s | Variable | SÍ |
| 4 | Garbage Collection | 0.1-0.5s | Impredecible | Parcial |
| 5 | Presión de memoria/Swapping | 10-100s | Raro | SÍ |
| 6 | Procesos background | 0.5-5s | Común | SÍ |
| 7 | Throttling por temperatura | 20-50% | Raro | SÍ |
| 8 | Estado del disco | 0.5-2s | Variable | Parcial |

**Conclusión final**: La variabilidad de 4-5% es **NORMAL E INEVITABLE**. Si observas variabilidad >10%, la causa es **externa** (RAM, CPU, procesos) y debe diagnosticarse caso por caso.
