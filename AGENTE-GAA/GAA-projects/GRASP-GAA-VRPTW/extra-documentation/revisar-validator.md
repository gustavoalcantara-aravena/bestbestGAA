PARA MEJORAR LUEGO DE VALIDATOR src/ast/validator.py

Qué mejorar en ESTE validator (4 fixes clave)
FIX A — “Choose” en fase construction vs local_search

Ahora Choose permite devolver cualquier tipo, pero en LS tú quieres que el AST devuelva string operador.

✅ Solución: en validate_ls_operator_ast() añade una regla extra:

El AST root debe ser Choose o un If que termine devolviendo str.

Y si devuelve str, los Const(str) deben ser operadores válidos.

Tu código ya chequea expected_return == RET_STR + _collect_invalid_operator_consts(). Bien.

Pero: Choose podría devolver num si alguien mete features/const num. Eso ya lo detienes con Return type mismatch, perfecto.

👉 Solo te falta: permitir que en LS no uses Feature (porque las features en LS son num) como retorno directo (ya lo evita el return type mismatch). OK.

No necesitas cambios aquí, solo asegúrate de que el generator LS solo genere Choose/If/Const(str).

FIX B — Manejo seguro de claves faltantes (evitar KeyError)

Tienes varios accesos directos como node["left"], node["expr"], etc.
Si el JSON viene mal, hoy te hace KeyError y rompe en vez de devolver errores.

✅ Mejora: usar .get() y reportar error.

Ejemplo: en Add/Sub/Mul/Div:

left = node.get("left")
right = node.get("right")
if left is None or right is None:
    errors.append(f"{t} requires 'left' and 'right'")
    return RET_NUM


Esto vale oro porque el generator puede fallar y tú quieres “reintentar”, no crashear.

FIX C — “Const(str)” no siempre es operador (modo estricto vs flexible)

Tu _collect_invalid_operator_consts() asume:

todo Const(str) = operador

Eso está bien si tu DSL no permite strings para otra cosa.

✅ Recomendación: dejarlo estricto (como está) para LS.
Pero para construcción sí podrías querer strings en el futuro (ej. "distance", "urgency" como etiquetas).
Para evitar problemas futuros:

Solo aplica esa verificación en LS (ya lo haces porque lo llamas sólo si expected_return == RET_STR). Perfecto.

FIX D — Stats: features_used debe ser List[str] (ya lo haces)

Tu stats convierte el set a lista al final. Bien.
Solo un matiz: en stats lo defines como set() y luego lo conviertes. OK.

3) Veredicto: ¿Está “adecuado” para tu implementación?

✅ Sí, este validator es el correcto para tu pipeline.

Pero haz FIX B (evitar KeyError) sí o sí, porque si no, cuando el generator produzca un JSON inválido, en vez de devolverte ValidationResult(ok=False, errors=[...]), te crashea y rompes el “reintento” del algorithm_generator.py.

4) Qué versión exacta recomiendo conservar
✅ Tu validator actual + “safe-get” (anti KeyError)

Si quieres, te digo exactamente qué cambiar:

En todos los nodos que usan node["..."], cambia a .get() y agrega error si falta.

Nodos que hoy te pueden romper:

Add/Sub/Mul/Div: left/right

WeightedSum: terms, term["expr"], term["weight"]

Normalize/Clip: expr

Less/Greater: left/right

And/Or: left/right

If: condition/then/else

Choose: options