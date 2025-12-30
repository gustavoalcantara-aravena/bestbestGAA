from data.loader import DataLoader

loader = DataLoader()
print('Testing _find_col_file:')
result1 = loader._find_col_file("flat300_20_0")
print(f'  flat300_20_0: {result1}')

result2 = loader._find_col_file("DSJC125.1")
print(f'  DSJC125.1: {result2}')

result3 = loader._find_col_file("myciel3")
print(f'  myciel3: {result3}')

print("\nTesting load method:")
try:
    problem = loader.load("flat300_20_0")
    print(f"✓ Loaded flat300_20_0: n={problem.n}, m={problem.m}")
except Exception as e:
    print(f"✗ Error loading flat300_20_0: {e}")
