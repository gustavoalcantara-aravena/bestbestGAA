#!/bin/bash
# Script wrapper para ejecución consistente de both.py
# Uso: ./run_consistent.sh
# Basado en 5 ejecuciones controladas que confirmaron las causas de variabilidad

set -e

echo "🚀 EJECUCIÓN CONSISTENTE DE both.py (OPTIMIZADO)"
echo "====================================="

# Verificación CRÍTICA
echo -e "\n📊 Verificando condiciones del sistema..."

FREE_RAM=$(free -m | grep "Mem:" | awk '{print $7}')
SWAP_USED=$(free -m | grep "Swap:" | awk '{print $3}')
LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
CORES=$(nproc)

echo "   • RAM libre: ${FREE_RAM}MB"
echo "   • Swap usado: ${SWAP_USED}MB"
echo "   • CPU cores: ${CORES}"
echo "   • Load average: ${LOAD}"

# CRÍTICO: Verificar RAM
if [ $FREE_RAM -lt 1500 ]; then
    echo ""
    echo "❌ ERROR CRÍTICO: RAM insuficiente"
    echo "   Actual: ${FREE_RAM}MB"
    echo "   Requerido: >1500MB"
    echo ""
    echo "   🔍 Top 5 procesos usando más memoria:"
    ps aux --sort=-%mem | head -6
    echo ""
    echo "   💡 SOLUCIÓN: Cerrar aplicaciones pesadas (navegador, IDE, Docker, etc.)"
    exit 1
fi

# CRÍTICO: Verificar Swap (causa #1 de variabilidad >100%)
if [ $SWAP_USED -gt 50 ]; then
    echo ""
    echo "🔴 ERROR CRÍTICO: Swap activo detectado"
    echo "   Swap usado: ${SWAP_USED}MB"
    echo ""
    echo "   🔍 CAUSA RAÍZ IDENTIFICADA:"
    echo "   El sistema está haciendo swap (moviendo RAM a disco)"
    echo "   Esto causará variabilidad de +100-500%"
    echo ""
    echo "   💡 SOLUCIÓN INMEDIATA:"
    echo "   1. Cerrar aplicaciones pesadas"
    echo "   2. Esperar a que swap baje a 0"
    echo "   3. Reintentar"
    exit 1
fi

echo "✅ RAM: OK (${FREE_RAM}MB > 1500MB)"
echo "✅ Swap: OK (${SWAP_USED}MB < 50MB)"

# Limpieza
echo -e "\n🗑️  Limpiando directorio output/..."
rm -rf output/
echo "✅ output/ limpio"

# Forzar GC
echo -e "\n🔄 Forzando garbage collection de Python..."
python3 -c "import gc; gc.collect()" 2>/dev/null || true
echo "✅ GC completado"

# Pausa para estabilizar sistema
echo -e "\n⏸️  Pausando 2 segundos para estabilizar el sistema..."
sleep 2

# Ejecución
echo -e "\n⏱️  Ejecutando script optimizado..."
echo "====================================="
START=$(date +%s.%N)

# Ejecutar con prioridad normal (cambiar a -10 para alta prioridad)
python3 scripts/demo_experimentation_both_OPTIMIZED.py

END=$(date +%s.%N)
ELAPSED=$(echo "$END - $START" | bc)

# Reporte
echo -e "\n====================================="
echo "✅ EJECUCIÓN COMPLETADA"
echo "====================================="
echo "⏱️  Tiempo total: ${ELAPSED}s"

# Verificar estado post-ejecución
FREE_RAM_AFTER=$(free -m | grep "Mem:" | awk '{print $7}')
SWAP_AFTER=$(free -m | grep "Swap:" | awk '{print $3}')

echo ""
echo "📊 Estado post-ejecución:"
echo "   • RAM libre: ${FREE_RAM_AFTER}MB (era ${FREE_RAM}MB)"
echo "   • Swap usado: ${SWAP_AFTER}MB (era ${SWAP_USED}MB)"

if [ $SWAP_AFTER -gt $SWAP_USED ]; then
    SWAP_DELTA=$((SWAP_AFTER - SWAP_USED))
    echo "   ⚠️  Swap aumentó +${SWAP_DELTA}MB durante ejecución"
    echo "   → Ejecutar con más RAM libre la próxima vez"
fi

echo ""
echo "📁 Resultados guardados en: output/"
echo ""

# Guardar tiempo para tracking histórico
mkdir -p logs
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "${TIMESTAMP},${ELAPSED},${FREE_RAM},${SWAP_USED}" >> logs/execution_times.csv

echo "📊 Tiempo registrado en: logs/execution_times.csv"
echo ""
echo "💡 Para ver estadísticas históricas:"
echo "   python3 -c \"import pandas as pd; df=pd.read_csv('logs/execution_times.csv', names=['time','elapsed','ram','swap']); print(f'Media: {df.elapsed.mean():.2f}s, Desv: {df.elapsed.std():.2f}s ({df.elapsed.std()/df.elapsed.mean()*100:.1f}%)')\""
