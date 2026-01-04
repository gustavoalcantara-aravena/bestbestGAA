✅ Checklist Final Antes de Testeo Intensivo en VS Code
1️⃣ Alineación total: Generator → Validator → Parser (CRÍTICO)

Antes de cualquier test funcional:

Verifica explícitamente que:

 Cada type que genera el AST generator:

Está en DEFAULT_ALLOWED_NODE_TYPES

Tiene implementación en ASTParser.evaluate()

 Cada campo usado por el generator:

Coincide con los nombres del validator y parser
(left/right, condition, terms.weight, etc.)

👉 Test recomendado

def test_ast_language_alignment():
    for node_type in GENERATED_NODE_TYPES:
        assert node_type in DEFAULT_ALLOWED_NODE_TYPES
        assert node_type in AST_RUNTIME_SUPPORTED_TYPES


Si esta alineación falla, TODO lo demás falla.

2️⃣ Tests de “Round-trip” de AST (MUY IMPORTANTE)

Antes de probar GRASP o GAA.

Test mínimo obligatorio:
def test_ast_roundtrip():
    gen = ASTGenerator(seed=123)
    ast = gen.generate(phase="construction")

    validator = ASTValidator(...)
    res = validator.validate_construction_ast(ast)
    assert res.ok, res.errors

    parser = ASTParser()
    state = FAKE_STATE_CONSTRUCTION
    value = parser.evaluate(ast, state)

    assert isinstance(value, float)


Y lo mismo para local_search → str.

👉 Esto detecta:

bugs de tipos

bugs de campos

bugs de features faltantes

crashes en runtime

3️⃣ Estados (state) EXACTAMENTE DEFINIDOS (fuente típica de bugs)

Te sugiero congelar estos contratos en tests:

Construction State
CONSTRUCTION_STATE_KEYS = {
    "route_length",
    "route_load",
    "route_capacity_remaining",
    "route_current_time",
    "cust_demand",
    "cust_ready_time",
    "cust_due_time",
    "delta_distance",
    "urgency",
    ...
}

Local Search State
LS_STATE_KEYS = {
    "num_routes",
    "total_distance",
    "penalty_value",
    "iterations_no_improve",
    ...
}


👉 Test recomendado

def test_ast_features_exist():
    for f in ast_stats["features_used"]:
        assert f in state

4️⃣ Determinismo total (científicamente CRÍTICO)

Asegúrate de que:

 ASTGenerator es 100% determinista con seed

 ASTParser NO usa RNG

 GRASP usa RNG solo donde corresponde

 ExperimentRunner fija seed global + por run

👉 Test obligatorio:

def test_determinism():
    algo1 = gen.generate(seed=42)
    algo2 = gen.generate(seed=42)
    assert algo1 == algo2

5️⃣ Evaluador: tests “duros” contra Solomon
Tests mínimos obligatorios:
a) Parser Solomon
def test_parse_solomon():
    inst = parse_solomon_instance("C101.txt")
    assert inst["capacity"] == 200
    assert len(inst["nodes"]) == 101
    assert inst["nodes"][0]["id"] == 0

b) BKS loading
def test_bks():
    bks = load_bks_file("best_known_solutions.json")
    assert bks["C101"] == (10, 828.93664)

c) Gap computation
def test_gap_exact_bks():
    sol = {"vehicles": 10, "distance": 828.93664}
    gap = compute_gap(sol, bks["C101"])
    assert abs(gap) < 1e-9

6️⃣ SolutionPool: propiedad crítica que suele olvidarse

Verifica que:

 Nunca almacena soluciones dominadas

 Compara lexicográficamente

 No mezcla instancias ni algoritmos

👉 Test típico:

def test_solution_pool_dominance():
    pool.add(sol1)
    pool.add(sol_worse)
    assert pool.best == sol1

7️⃣ Logging: prueba de “auditoría científica”

Pregunta clave:

¿Podrías reconstruir un experimento SOLO con logs?

Checklist:

 Cada log tiene: algorithm_id, seed, instance_id

 Métricas completas (V, D, gap, feasible)

 Timestamp o cpu_time

 AST hash o id

👉 Test:

def test_log_schema():
    assert set(log.keys()) >= REQUIRED_LOG_FIELDS

8️⃣ “Canary run” (última prueba antes del experimento grande)

Corre una sola instancia:

C101

1 algoritmo

1 run

seed fija

Verifica:

 No warnings

 No excepciones

 Gap razonable (≠ NaN, ≠ infinito)

 Log generado correctamente

9️⃣ Regla de Oro (para el LLM en VS Code)

Cuando interactúes con el LLM, dile explícitamente:

“No agregues nuevas features, nodos o lógica fuera de los archivos md existentes.
Todo debe cumplir los contratos definidos.”

Esto evita:

expansión descontrolada del DSL

inconsistencias sutiles

deuda técnica invisible