import sys
import importlib.util
import os

os.chdir('c:/Users/gustavo_windows/Desktop/bestbestGAA/AGENTE-GAA/GAA-projects/ILS-GAA-GCP')

# Add to path
sys.path.insert(0, '.')

# Try direct import first
try:
    from _01_src.core import dimacs_loader
    print("Successfully imported dimacs_loader")
except Exception as e:
    print(f"Error importing dimacs_loader: {e}")
    import traceback
    traceback.print_exc()

# Try loading fitness with proper parent package setup
try:
    import _01_src
    import _01_src.core
    import _01_src.core.dimacs_loader
    import _01_src.gaa
    import _01_src.gaa.fitness
    print("Successfully imported fitness via package")
    print("Dir fitness:", [x for x in dir(_01_src.gaa.fitness) if not x.startswith('_')])
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
