1️⃣ Comparación GAP: 3 Algoritmos vs Best Known Solutions

(barras agrupadas por instancia)

📊 Qué muestra

Compara el GAP (%) respecto al BKS para tres algoritmos.

Cada grupo corresponde a una instancia Solomon R1xx.

La línea horizontal en GAP = 0 representa el Best Known Solution (BKS).

GAP negativo = mejor que BKS.

📐 Tipo de gráfico

Bar chart agrupado

Línea horizontal de referencia

🎨 Estilo visual

Algoritmo 1: rojo claro (#ff9999)

Algoritmo 2: turquesa (#66c2a5)

Algoritmo 3: amarillo (#ffeb84)

Línea BKS: roja discontinua

Fondo blanco, grilla suave

Eje X inclinado (45°)

🧠 Prompt para LLM
Generate a grouped bar chart comparing GAP (%) to Best Known Solution (BKS)
for three algorithms across Solomon VRPTW instances (R101–R112).

Details:
- X-axis: Instance name (categorical)
- Y-axis: GAP (%) relative to BKS
- Three bars per instance (Algorithm 1, Algorithm 2, Algorithm 3)
- Add a horizontal dashed red line at y = 0 labeled "BKS"
- Color scheme:
  Algorithm 1: light red (#ff9999)
  Algorithm 2: teal (#66c2a5)
  Algorithm 3: light yellow (#ffeb84)
- Include gridlines and legend
- Rotate x-axis labels by 45 degrees
- Title: "Comparación GAP: 3 Algoritmos vs Best Known Solutions"

2️⃣ Performance Comparison: Average Distance by Algorithm

(barras simples)

📊 Qué muestra

Distancia promedio obtenida por cada algoritmo.

Comparación directa de calidad promedio.

📐 Tipo de gráfico

Bar chart simple

🎨 Estilo visual

Barras grandes, colores sólidos:

Alg 1: verde

Alg 2: rojo

Alg 3: azul

Valor numérico encima de cada barra

Sin exceso de decoración

🧠 Prompt para LLM
Create a bar chart showing the average distance achieved by three algorithms.

Details:
- X-axis: Algorithm name
- Y-axis: Average distance
- Colors:
  Algorithm 1: green
  Algorithm 2: salmon/red
  Algorithm 3: blue
- Display numeric value on top of each bar
- Title: "Performance Comparison: Average Distance by Algorithm"
- Clean style with gridlines

3️⃣ Distance per Instance by Algorithm

(líneas por instancia)

📊 Qué muestra

Evolución de la distancia por instancia.

Permite ver estabilidad y variabilidad por algoritmo.

📐 Tipo de gráfico

Line chart multi-serie

🎨 Estilo visual

Alg 1: verde con círculos

Alg 2: rojo con cuadrados

Alg 3: azul con triángulos

Marcadores visibles

Líneas suaves

Grilla tenue

🧠 Prompt para LLM
Generate a multi-line chart showing distance per instance for three algorithms.

Details:
- X-axis: Instance index
- Y-axis: Distance
- Lines:
  Algorithm 1: green line with circle markers
  Algorithm 2: red line with square markers
  Algorithm 3: blue line with triangle markers
- Include legend and gridlines
- Title: "Distance per Instance by Algorithm"

4️⃣ Evolución del GAP por Instancia

(líneas + línea BKS)

📊 Qué muestra

Evolución del GAP (%) por instancia.

Comparación directa con el BKS (0%).

📐 Tipo de gráfico

Line chart multi-serie

Línea horizontal de referencia

🎨 Estilo visual

Alg 1: rojo

Alg 2: turquesa

Alg 3: amarillo

Línea BKS: roja discontinua

Marcadores visibles

🧠 Prompt para LLM
Create a line chart showing GAP (%) evolution per instance for three algorithms.

Details:
- X-axis: Solomon VRPTW instances
- Y-axis: GAP (%)
- Lines:
  Algorithm 1: red
  Algorithm 2: teal
  Algorithm 3: yellow
- Add a dashed red horizontal line at y = 0 labeled "BKS"
- Include markers, legend, and gridlines
- Title: "Evolución de GAP por Instancia"

5️⃣ Performance by Instance Family

(barra agregada por familia)

📊 Qué muestra

Distancia promedio por familia de instancias (R1 en este caso).

📐 Tipo de gráfico

Bar chart simple (agregado)

🎨 Estilo visual

Barra única color púrpura

Valor numérico encima

Enfoque minimalista

🧠 Prompt para LLM
Generate a bar chart showing average distance by instance family.

Details:
- X-axis: Instance family
- Y-axis: Average distance
- Single purple bar
- Display numeric value above the bar
- Title: "Performance by Instance Family"

6️⃣ Distribución de GAP por Familia (Boxplot)
📊 Qué muestra

Distribución estadística del GAP:

mediana, cuartiles, dispersión

Comparación de robustez entre algoritmos.

📐 Tipo de gráfico

Boxplot múltiple

🎨 Estilo visual

Cajas coloreadas (rojo, turquesa, amarillo)

Línea BKS en y = 0

Fondo limpio

🧠 Prompt para LLM
Create a boxplot comparing GAP (%) distributions for three algorithms
within the Solomon R1 family.

Details:
- Y-axis: GAP (%)
- Three boxplots:
  Algorithm 1: light red
  Algorithm 2: teal
  Algorithm 3: yellow
- Add dashed horizontal line at y = 0 labeled "BKS"
- Title: "Distribución de GAP por Familia"

7️⃣ Execution Time Comparison

(barras simples)

📊 Qué muestra

Tiempo promedio de ejecución.

Comparación eficiencia vs calidad.

📐 Tipo de gráfico

Bar chart simple

🎨 Estilo visual

Colores sólidos

Etiquetas con segundos (ej. “0.18s”)

Minimalista

🧠 Prompt para LLM
Generate a bar chart comparing average execution time of three algorithms.

Details:
- X-axis: Algorithm
- Y-axis: Time in seconds
- Display value labels with 's'
- Clean style with gridlines
- Title: "Execution Time Comparison"

8️⃣ Heatmap: GAP de cada Algoritmo vs Instancia
📊 Qué muestra

Vista global de qué algoritmo funciona mejor/peor por instancia.

📐 Tipo de gráfico

Heatmap

🎨 Estilo visual

Colormap divergente:

Verde = mejor (GAP negativo)

Rojo = peor

Valores numéricos dentro de cada celda

🧠 Prompt para LLM
Create a heatmap showing GAP (%) values for each algorithm and instance.

Details:
- Rows: Solomon instances
- Columns: Algorithms
- Color scale: green (low / better) to red (high / worse)
- Display numeric GAP value inside each cell
- Title: "Heatmap: GAP de cada Algoritmo vs Instancia"

9️⃣ Comparación de GAP por Familia (Grid de subplots)
📊 Qué muestra

GAP por algoritmo separado por familia Solomon.

Aquí solo R1 tiene datos, el resto aparece vacío (correcto).

📐 Tipo de gráfico

Grid de subplots (bar charts)

🎨 Estilo visual

Subplots organizados por familia

Línea BKS en cada subplot

Colores consistentes por algoritmo

🧠 Prompt para LLM
Generate a grid of subplots comparing GAP (%) per instance family.

Details:
- One subplot per Solomon family (C1, C2, R1, R2, RC1, RC2)
- Use grouped bar charts inside each subplot
- Add dashed horizontal BKS line at y = 0
- Only R1 contains data; others remain empty
- Consistent colors per algorithm

🔟 Distance Distribution by Algorithm (Boxplot)
📊 Qué muestra

Distribución completa de distancias por algoritmo.

Permite ver variabilidad y outliers.

📐 Tipo de gráfico

Boxplot

🎨 Estilo visual

Cajas grandes, colores suaves

Mediana destacada

Fondo limpio

🧠 Prompt para LLM
Create a boxplot showing distance distribution for three algorithms.

Details:
- X-axis: Algorithm
- Y-axis: Distance
- Use distinct colors per algorithm
- Show median and quartiles clearly
- Title: "Distance Distribution by Algorithm"

🧩 Prompt global (opcional)

Si quieres que el LLM genere todo el set completo, puedes usar esto:

Generate a full experimental visualization suite for comparing three
metaheuristic algorithms on Solomon VRPTW instances.

Include:
- Grouped bar charts for GAP vs BKS
- Line charts for distance and GAP evolution
- Boxplots for GAP and distance distributions
- Heatmap for GAP by instance and algorithm
- Execution time bar chart
- Consistent color scheme across all figures
- Clean academic style suitable for a journal paper