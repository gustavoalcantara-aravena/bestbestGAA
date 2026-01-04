2️⃣ Ejemplo de Log REAL por Solución

Formato recomendado: CSV o JSON Lines (JSONL)
Ejemplo en JSONL (1 línea = 1 ejecución completa).

Ejemplo REALISTA (JSONL)
{
  "timestamp": "2026-01-04T14:32:11.284Z",
  "experiment_id": "EXP_001",
  "algorithm_id": "ALGO-3-HYBRID",
  "algorithm_hash": "a9f3c21d",
  "run_id": 7,
  "seed": 42007,
  "instance_id": "R101",
  "family": "R1",

  "vehicles": 10,
  "distance": 1108.4325,
  "k_bks": 9,
  "d_bks": 1007.31005,

  "gap_percent": 10.04,
  "feasible": true,
  "capacity_violation": 0,
  "time_window_violation": 0,

  "cpu_time_sec": 3.287,
  "constructive_time_sec": 1.142,
  "local_search_time_sec": 2.145,

  "num_routes": 10,
  "num_customers": 100,
  "avg_route_length": 110.8,

  "ast_depth": 3,
  "ast_function_nodes": 2,
  "ast_terminals": [
    "Urgency",
    "Distance",
    "Regret"
  ],

  "status": "OK"
}

Campos MÍNIMOS (no negociables)
timestamp
algorithm_id
run_id
seed
instance_id
vehicles
distance
gap_percent
feasible
cpu_time_sec

Campos CLAVE para GAA (muy importantes)
algorithm_hash      // reproducibilidad
ast_depth           // complejidad real
ast_function_nodes  // bloat control
ast_terminals       // interpretación heurística

Campos de diagnóstico (debug científico)
capacity_violation
time_window_violation
status

Regla de oro del logging

❌ Si una ejecución no genera log → no existe

❌ Si falta seed → no es reproducible

❌ Si falta algorithm_hash → no es trazable