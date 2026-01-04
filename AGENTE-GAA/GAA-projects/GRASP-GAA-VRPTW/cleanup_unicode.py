#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para limpiar caracteres unicode problemáticos"""

import sys

files = [
    'generate_extra_visualizations.py',
    'generate_extra_visualizations_set2.py'
]

for filename in files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar caracteres unicode por ASCII
        content = content.replace('✓', '[OK]')
        content = content.replace('✗', '[FAIL]')
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] {filename}: Unicode removido")
    except Exception as e:
        print(f"[ERROR] {filename}: {str(e)}")
        sys.exit(1)

print("\nTodos los archivos limpiados exitosamente")
