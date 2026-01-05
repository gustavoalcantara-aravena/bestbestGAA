Formato del AST
DSL + JSON para GRASP + GAA (VRPTW Solomon)
1. Principios del AST

El AST describe la lógica del algoritmo, no las rutas.

El AST no modifica estado, solo decide.

El AST es puro: misma entrada → misma salida.

El AST es serializable a JSON (obligatorio).

El AST opera sobre features agregadas (no estructuras grandes).

2. DSL (Gramática Informal)
2.1 Programa
<Program> ::= Seq(<Statement>*)

2.2 Statements (nodos internos)
<Statement> ::=
    If(<Condition>, <Statement>, <Statement>)
  | Choose(<Statement>+)                 # devuelve un valor
  | WeightedSum(<Expr>+)                 # score
  | Normalize(<Expr>)
  | Clip(<Expr>, min, max)
  | Const(<Float>)

2.3 Condiciones
<Condition> ::=
    Less(<Expr>, <Expr>)
  | Greater(<Expr>, <Expr>)
  | And(<Condition>, <Condition>)
  | Or(<Condition>, <Condition>)

2.4 Expresiones (nodos hoja / terminales)
<Expr> ::=
    Feature(name)
  | Const(value)
  | Add(<Expr>, <Expr>)
  | Sub(<Expr>, <Expr>)
  | Mul(<Expr>, <Expr>)
  | Div(<Expr>, <Expr>)

3. Tipos de AST por Fase

Se usan dos ASTs independientes (recomendado):

AST_Construction
AST_LocalSearch


Ambos comparten el mismo formato, cambian las features disponibles.

4. Esquema JSON Canónico
4.1 Encabezado del AST
{
  "algorithm_id": "AST_001",
  "seed": 42,
  "max_depth": 3,
  "nodes": {
    ...
  }
}

4.2 Nodo Genérico
{
  "type": "NODE_TYPE",
  "params": { ... },
  "children": [ ... ]
}

5. Catálogo de Nodos
5.1 Nodos de Control
If
{
  "type": "If",
  "condition": { ... },
  "then": { ... },
  "else": { ... }
}


Devuelve el valor del branch ejecutado.

Choose (selección discreta)
{
  "type": "Choose",
  "options": [
    { "type": "Const", "value": "relocate" },
    { "type": "Const", "value": "swap" }
  ]
}


Usado para selección de operador.

5.2 Nodos Numéricos
WeightedSum (muy importante)
{
  "type": "WeightedSum",
  "terms": [
    { "weight": 1.0, "expr": { "type": "Feature", "name": "delta_distance" } },
    { "weight": 5.0, "expr": { "type": "Feature", "name": "time_violation" } }
  ]
}


Devuelve un score escalar.

Normalize
{
  "type": "Normalize",
  "expr": { "type": "Feature", "name": "delta_distance" }
}


Normaliza a [0,1] usando rangos predefinidos.

Clip
{
  "type": "Clip",
  "expr": { ... },
  "min": 0.0,
  "max": 1.0
}

5.3 Operadores Aritméticos
{ "type": "Add", "left": {...}, "right": {...} }
{ "type": "Sub", "left": {...}, "right": {...} }
{ "type": "Mul", "left": {...}, "right": {...} }
{ "type": "Div", "left": {...}, "right": {...} }


⚠️ Div debe manejar división por cero.

5.4 Terminales (Features)
{
  "type": "Feature",
  "name": "urgency"
}


La name debe existir en el InsertionState o LocalSearchState.

5.5 Constantes
{
  "type": "Const",
  "value": 0.75
}

6. Contrato de Ejecución
6.1 En Construcción
score = AST_Construction.evaluate(InsertionState)


Retorna float

Menor score = mejor candidato

6.2 En Búsqueda Local
operator = AST_LocalSearch.select_operator(LocalSearchState)
accept   = AST_LocalSearch.accept_move(LocalSearchState)


operator: string (relocate, swap, or_opt, two_opt)

accept: bool

7. Ejemplo Completo – Construcción
7.1 DSL Conceptual
score =
  delta_distance
+ 5 * time_violation
+ 2 * capacity_violation
- 0.5 * urgency

7.2 JSON
{
  "type": "WeightedSum",
  "terms": [
    { "weight": 1.0, "expr": { "type": "Feature", "name": "delta_distance" } },
    { "weight": 5.0, "expr": { "type": "Feature", "name": "time_violation" } },
    { "weight": 2.0, "expr": { "type": "Feature", "name": "capacity_violation" } },
    { "weight": -0.5, "expr": { "type": "Feature", "name": "urgency" } }
  ]
}

8. Ejemplo Completo – Local Search (Selección Operador)
8.1 DSL Conceptual
if iterations_no_improve > 10:
    choose(relocate, swap)
else:
    choose(or_opt, two_opt)

8.2 JSON
{
  "type": "If",
  "condition": {
    "type": "Greater",
    "left": { "type": "Feature", "name": "iterations_no_improve" },
    "right": { "type": "Const", "value": 10 }
  },
  "then": {
    "type": "Choose",
    "options": [
      { "type": "Const", "value": "relocate" },
      { "type": "Const", "value": "swap" }
    ]
  },
  "else": {
    "type": "Choose",
    "options": [
      { "type": "Const", "value": "or_opt" },
      { "type": "Const", "value": "two_opt" }
    ]
  }
}

9. Control de Bloat (CRÍTICO)

Imponer siempre:

profundidad máxima (≤ 3)

número máximo de nodos internos (≤ 5)

número máximo de features distintas (≤ 6)

Esto es clave para GAA.

10. Validación del AST

Antes de usar un AST:

verificar profundidad

verificar features válidas

verificar tipos de retorno

asignar ast_signature (hash del JSON)

11. Resumen

Este formato:

✔ es expresivo
✔ es minimalista
✔ es serializable
✔ es interpretable
✔ es compatible con GAA
✔ permite evolución automática