11️⃣ Comparación: Vehículos BKS vs Vehículos Utilizados por cada Algoritmo
📊 Qué muestra

Compara el número de vehículos (K) del BKS frente a los usados por cada algoritmo.

Evaluación de factibilidad estructural (usar más vehículos suele ser peor).

Cada grupo corresponde a una instancia Solomon R1xx.

📐 Tipo de gráfico

Bar chart agrupado (4 barras por instancia)

🎨 Estilo visual

BKS: verde (#2ecc71)

Algoritmo 1: rojo claro (#ff9999)

Algoritmo 2: turquesa (#66c2a5)

Algoritmo 3: amarillo (#ffeb84)

Grilla suave

Eje X rotado 45°

🧠 Prompt para LLM
Create a grouped bar chart comparing the number of vehicles (K)
used by each algorithm against the Best Known Solution (BKS).

Details:
- X-axis: Solomon VRPTW instances (R101–R112)
- Y-axis: Number of vehicles (K)
- Four bars per instance: BKS, Algorithm 1, Algorithm 2, Algorithm 3
- Color scheme:
  BKS: green
  Algorithm 1: light red
  Algorithm 2: teal
  Algorithm 3: yellow
- Rotate x-axis labels by 45 degrees
- Add gridlines and legend
- Title: "Comparación: Vehículos BKS vs Vehículos Utilizados por cada Algoritmo"

12️⃣ Comparación: Distancia BKS vs Distancia Total Lograda
📊 Qué muestra

Comparación directa entre la distancia del BKS y la distancia lograda por cada algoritmo.

Permite evaluar calidad absoluta de solución.

📐 Tipo de gráfico

Bar chart agrupado

🎨 Estilo visual

Mismo esquema cromático que el gráfico de vehículos

Barras anchas

Escala en kilómetros

Grilla ligera

🧠 Prompt para LLM
Generate a grouped bar chart comparing total distance (km)
of Best Known Solutions (BKS) versus three algorithms.

Details:
- X-axis: Solomon VRPTW instances
- Y-axis: Total distance (km)
- Bars: BKS, Algorithm 1, Algorithm 2, Algorithm 3
- Use consistent colors with previous vehicle comparison
- Include legend and gridlines
- Title: "Comparación: Distancia BKS vs Distancia Total Lograda por cada Algoritmo"

13️⃣ Performance Heatmap: Average Distance by Family and Algorithm
📊 Qué muestra

Distancia promedio agregada por familia (R1).

Comparación global de rendimiento por algoritmo.

Ideal para resumen ejecutivo.

📐 Tipo de gráfico

Heatmap (matriz 1×3)

🎨 Estilo visual

Colormap secuencial tipo YlGnRd

Verde = mejor (menor distancia)

Rojo = peor

Valor numérico anotado dentro de cada celda

Colorbar lateral

🧠 Prompt para LLM
Create a heatmap showing average distance by instance family and algorithm.

Details:
- Rows: Instance families (e.g., R1)
- Columns: Algorithms
- Cell values: Average distance
- Color scale: green (lower distance) to red (higher distance)
- Annotate each cell with numeric value
- Include colorbar
- Title: "Performance Heatmap: Average Distance by Family and Algorithm"

14️⃣ Multi-Objective Analysis: K vs D (Pareto Front)
📊 Qué muestra

Relación biobjetivo:

K = número de vehículos

D = distancia total

Visualiza trade-offs y dominancia (frente de Pareto implícito).

📐 Tipo de gráfico

Scatter plot multi-serie

🎨 Estilo visual

Algoritmo 1: círculos verdes

Algoritmo 2: cuadrados rojos

Algoritmo 3: triángulos azules

Marcadores grandes

Sin líneas de conexión

Grilla tenue

🧠 Prompt para LLM
Generate a scatter plot for multi-objective analysis (Pareto front)
using number of vehicles (K) and total distance (D).

Details:
- X-axis: Number of vehicles (K)
- Y-axis: Total distance (D)
- Points:
  Algorithm 1: green circles
  Algorithm 2: red squares
  Algorithm 3: blue triangles
- Large markers, no connecting lines
- Include legend and gridlines
- Title: "Multi-Objective Analysis: K vs D (Pareto Front)"

15️⃣ Robustness Analysis: Distance Distribution by Instance
📊 Qué muestra

Robustez por instancia.

Cada subplot corresponde a una instancia.

Compara estabilidad entre algoritmos.

📐 Tipo de gráfico

Grid de boxplots por instancia

🎨 Estilo visual

Subplots organizados en grilla

Un boxplot por algoritmo dentro de cada instancia

Ejes independientes

Estilo limpio, académico

🧠 Prompt para LLM
Create a grid of boxplots showing distance distribution per instance.

Details:
- One subplot per Solomon instance (R101–R106, etc.)
- Each subplot contains boxplots for three algorithms
- Y-axis: Distance
- X-axis: Algorithm
- Clean academic style with gridlines
- Title per subplot: "Instance: Rxxx"
- Overall title: "Robustness Analysis: Distance Distribution by Instance"

16️⃣ K_BKS Feasibility Rate by Algorithm
📊 Qué muestra

Porcentaje de instancias donde K = K_BKS.

Mide factibilidad estricta.

Aquí se observa 0% en todos (resultado fuerte).

📐 Tipo de gráfico

Bar chart simple con línea de referencia

🎨 Estilo visual

Barras verdes

Línea discontinua en 100%

Etiqueta numérica encima de cada barra

🧠 Prompt para LLM
Generate a bar chart showing K_BKS feasibility rate per algorithm.

Details:
- X-axis: Algorithm
- Y-axis: Feasibility rate (%)
- Bars represent percentage of instances where K equals BKS
- Add dashed horizontal line at 100%
- Annotate each bar with percentage value
- Title: "K_BKS Feasibility Rate by Algorithm"

17️⃣ Solved vs Unsolved Instances
📊 Qué muestra

Número de instancias:

Resueltas con K = BKS

No resueltas (K > BKS)

Vista categórica clara.

📐 Tipo de gráfico

Stacked bar chart

🎨 Estilo visual

Verde: solved

Rojo: unsolved

Barras anchas

Leyenda clara

🧠 Prompt para LLM
Create a stacked bar chart showing solved vs unsolved instances per algorithm.

Details:
- X-axis: Algorithm
- Y-axis: Number of instances
- Stack:
  Solved (K = BKS): green
  Unsolved (K > BKS): red
- Include legend and gridlines
- Title: "Solved vs Unsolved Instances"

18️⃣ Algorithm Comparison: Multi-Dimensional Radar
📊 Qué muestra

Comparación multicriterio normalizada:

Distancia promedio

Eficiencia temporal

Consistencia

Excelente para discusión cualitativa.

📐 Tipo de gráfico

Radar / Spider chart

🎨 Estilo visual

Alg 1: verde

Alg 2: rojo

Alg 3: azul

Área semitransparente

Escala [0,1]

🧠 Prompt para LLM
Create a radar chart comparing algorithms across multiple normalized metrics.

Metrics:
- Average Distance
- Time Efficiency
- Consistency

Details:
- Values normalized to [0,1]
- One polygon per algorithm
- Colors:
  Algorithm 1: green
  Algorithm 2: red
  Algorithm 3: blue
- Semi-transparent filled areas
- Include legend
- Title: "Algorithm Comparison: Multi-Dimensional Radar"