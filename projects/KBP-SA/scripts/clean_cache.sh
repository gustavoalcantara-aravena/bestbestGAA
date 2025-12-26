#!/bin/bash
#
# Script de Limpieza de Caché
# Limpia cachés de Python y del sistema antes de cada corrida
#

# Directorio del proyecto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Limpiar __pycache__ y .pyc
echo "🧹 Limpiando caché de Python..."
find "$PROJECT_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find "$PROJECT_DIR" -type f -name "*.pyc" -delete 2>/dev/null
find "$PROJECT_DIR" -type f -name "*.pyo" -delete 2>/dev/null

# Limpiar caché de pytest si existe
if [ -d "$PROJECT_DIR/.pytest_cache" ]; then
    rm -rf "$PROJECT_DIR/.pytest_cache"
fi

# Intentar limpiar page cache del sistema (requiere sudo en Linux)
if command -v sync &> /dev/null && command -v sysctl &> /dev/null; then
    # macOS
    sync
    # sudo purge  # Descomentar si quieres purga completa en macOS
elif command -v sync &> /dev/null && [ -w /proc/sys/vm/drop_caches ]; then
    # Linux con permisos
    sync
    # echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null
fi

echo "✅ Caché limpiado"
