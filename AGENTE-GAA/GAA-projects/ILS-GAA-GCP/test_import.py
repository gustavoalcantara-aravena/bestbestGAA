import sys
import os

os.chdir('c:/Users/gustavo_windows/Desktop/bestbestGAA/AGENTE-GAA/GAA-projects/ILS-GAA-GCP')

# Try to import and capture any errors
try:
    from src.core.ast_interpreter import ASTInterpreter
    print("ASTInterpreter imported successfully")
except Exception as e:
    print(f"Error importing ASTInterpreter: {e}")
    import traceback
    traceback.print_exc()

try:
    from src.core.dimacs_loader import load_dimacs_col
    print("load_dimacs_col imported successfully")
except Exception as e:
    print(f"Error importing load_dimacs_col: {e}")
    import traceback
    traceback.print_exc()

# Now try fitness
try:
    exec(open('src/gaa/fitness.py').read())
    print("fitness.py executed successfully")
except Exception as e:
    print(f"Error executing fitness.py: {e}")
    import traceback
    traceback.print_exc()
