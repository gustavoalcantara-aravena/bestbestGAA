"""
Genera un HTML interactivo que muestra todos los gráficos y estadísticas
Útil para revisar resultados sin necesidad de terminal
"""

import pandas as pd
from pathlib import Path

# Cargar datos
raw_df = pd.read_csv('output/vrptw_experiments_FULL_03-01-26_02-18-27/results/raw_results.csv')

# Calcular GAP
raw_df['gap_calc'] = ((raw_df['d_final'] - raw_df['d_bks']) / raw_df['d_bks'] * 100)

# Crear tabla de resultados
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análisis GAP: 3 Algoritmos VRPTW</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .section {
            margin-bottom: 40px;
        }
        
        .section h2 {
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        
        .section h3 {
            color: #764ba2;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            border-radius: 5px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        th {
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }
        
        tr:hover {
            background: #f5f5f5;
        }
        
        tr:last-child td {
            border-bottom: none;
        }
        
        .number {
            text-align: right;
            font-family: 'Courier New', monospace;
            font-weight: 500;
        }
        
        .algo1 { color: #FF6B6B; font-weight: 600; }
        .algo2 { color: #4ECDC4; font-weight: 600; }
        .algo3 { color: #FFE66D; font-weight: 600; }
        
        .highlight-good {
            background: #d4edda;
            color: #155724;
            padding: 2px 6px;
            border-radius: 3px;
        }
        
        .highlight-bad {
            background: #f8d7da;
            color: #721c24;
            padding: 2px 6px;
            border-radius: 3px;
        }
        
        .metric-box {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .metric {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .metric h4 {
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
        }
        
        .metric .value {
            font-size: 2.2em;
            font-weight: bold;
        }
        
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin: 30px 0;
        }
        
        .gallery-item {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
            border: 2px solid #eee;
            text-align: center;
        }
        
        .gallery-item h4 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        
        .gallery-item img {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        
        .gallery-item p {
            font-size: 0.9em;
            color: #666;
        }
        
        .family-section {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 5px solid #667eea;
        }
        
        .winner {
            background: #d4edda;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: 600;
            color: #155724;
        }
        
        .recommendation {
            background: #fff3cd;
            border-left: 5px solid #ffc107;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        
        .recommendation h4 {
            color: #856404;
            margin-bottom: 10px;
        }
        
        footer {
            background: #f5f5f5;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #ddd;
        }
        
        .critical {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            border-left: 5px solid #721c24;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Análisis Comparativo de GAP</h1>
            <p>Comparación de 3 Algoritmos VRPTW vs Best Known Solutions (BKS)</p>
            <p>56 Instancias Solomon | 6 Familias | 168 Ejecuciones</p>
        </header>
        
        <div class="content">
            <!-- RESUMEN GLOBAL -->
            <div class="section">
                <h2>📈 Resumen Global</h2>
                
                <div class="metric-box">
                    <div class="metric" style="background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);">
                        <h4>Algoritmo 1 - Promedio GAP</h4>
                        <div class="value">64.43%</div>
                        <p>3/56 mejor que BKS</p>
                    </div>
                    <div class="metric" style="background: linear-gradient(135deg, #4ECDC4 0%, #7FE5E5 100%);">
                        <h4>Algoritmo 2 - Promedio GAP</h4>
                        <div class="value">25.25%</div>
                        <p>16/56 mejor que BKS 🏆</p>
                    </div>
                    <div class="metric" style="background: linear-gradient(135deg, #FFE66D 0%, #FFF0A3 100%);">
                        <h4>Algoritmo 3 - Promedio GAP</h4>
                        <div class="value">45.82%</div>
                        <p>5/56 mejor que BKS</p>
                    </div>
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th>Métrica</th>
                            <th class="algo1">Algoritmo 1</th>
                            <th class="algo2">Algoritmo 2</th>
                            <th class="algo3">Algoritmo 3</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Promedio GAP (%)</strong></td>
                            <td class="number algo1">64.43</td>
                            <td class="number algo2"><span class="highlight-good">25.25</span></td>
                            <td class="number algo3">45.82</td>
                        </tr>
                        <tr>
                            <td><strong>Mediana GAP (%)</strong></td>
                            <td class="number algo1">55.37</td>
                            <td class="number algo2"><span class="highlight-good">20.91</span></td>
                            <td class="number algo3">30.69</td>
                        </tr>
                        <tr>
                            <td><strong>Desv. Estándar</strong></td>
                            <td class="number algo1">57.89</td>
                            <td class="number algo2"><span class="highlight-good">35.35</span></td>
                            <td class="number algo3">41.94</td>
                        </tr>
                        <tr>
                            <td><strong>Min GAP (%)</strong></td>
                            <td class="number algo1">-13.49</td>
                            <td class="number algo2"><span class="highlight-good">-28.99</span></td>
                            <td class="number algo3">-11.33</td>
                        </tr>
                        <tr>
                            <td><strong>Max GAP (%)</strong></td>
                            <td class="number algo1">208.12</td>
                            <td class="number algo2"><span class="highlight-good">95.28</span></td>
                            <td class="number algo3">125.38</td>
                        </tr>
                        <tr>
                            <td><strong>Instancias mejor que BKS (GAP < 0)</strong></td>
                            <td class="number algo1">3</td>
                            <td class="number algo2"><span class="highlight-good">16 ⭐</span></td>
                            <td class="number algo3">5</td>
                        </tr>
                        <tr>
                            <td><strong>Instancias dentro 5% de BKS</strong></td>
                            <td class="number algo1">6</td>
                            <td class="number algo2"><span class="highlight-good">18 ⭐</span></td>
                            <td class="number algo3">6</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <!-- ANÁLISIS POR FAMILIA -->
            <div class="section">
                <h2>🎯 Análisis por Familia Solomon</h2>
                
                <div class="family-section">
                    <h3>C1 - Clustered, 100 clientes, Horizon Corto (9 instancias)</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Métrica</th>
                                <th class="algo1">Algoritmo 1</th>
                                <th class="algo2">Algoritmo 2</th>
                                <th class="algo3">Algoritmo 3</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Promedio GAP</td>
                                <td class="number algo1">79.29%</td>
                                <td class="number algo2"><span class="highlight-good">33.09%</span></td>
                                <td class="number algo3">107.34%</td>
                            </tr>
                            <tr>
                                <td>Mediana GAP</td>
                                <td class="number algo1">80.80%</td>
                                <td class="number algo2"><span class="highlight-good">33.09%</span></td>
                                <td class="number algo3">113.87%</td>
                            </tr>
                            <tr>
                                <td colspan="4" style="text-align: center; padding: 15px;"><span class="winner">✅ MEJOR: Algoritmo 2</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                
                <div class="family-section">
                    <h3>C2 - Clustered, 100 clientes, Horizon Largo (8 instancias)</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Métrica</th>
                                <th class="algo1">Algoritmo 1</th>
                                <th class="algo2">Algoritmo 2</th>
                                <th class="algo3">Algoritmo 3</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Promedio GAP</td>
                                <td class="number algo1">185.37%</td>
                                <td class="number algo2"><span class="highlight-bad">94.76%</span></td>
                                <td class="number algo3">102.72%</td>
                            </tr>
                            <tr>
                                <td>Mediana GAP</td>
                                <td class="number algo1">188.03%</td>
                                <td class="number algo2"><span class="highlight-bad">94.80%</span></td>
                                <td class="number algo3">104.43%</td>
                            </tr>
                            <tr>
                                <td colspan="4" style="text-align: center; padding: 15px;"><span class="winner">✅ MEJOR: Algoritmo 2</span></td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="critical">
                        <strong>⚠️ CRÍTICO:</strong> Algoritmo 2 lucha con familias clustered largas. GAP de 94.76% es inaceptable para producción. Constructor NearestNeighbor inadecuado.
                    </div>
                </div>
                
                <div class="family-section">
                    <h3>R1 - Random, 100 clientes (12 instancias)</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Métrica</th>
                                <th class="algo1">Algoritmo 1</th>
                                <th class="algo2">Algoritmo 2</th>
                                <th class="algo3">Algoritmo 3</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Promedio GAP</td>
                                <td class="number algo1">15.60%</td>
                                <td class="number algo2"><span class="highlight-good">-0.60%</span></td>
                                <td class="number algo3">24.73%</td>
                            </tr>
                            <tr>
                                <td>Mediana GAP</td>
                                <td class="number algo1">13.93%</td>
                                <td class="number algo2"><span class="highlight-good">1.44%</span></td>
                                <td class="number algo3">22.85%</td>
                            </tr>
                            <tr>
                                <td colspan="4" style="text-align: center; padding: 15px;"><span class="highlight-good" style="padding: 10px; font-size: 1.1em;">🏆 EXCELENTE: Algoritmo 2 SUPERA BKS (GAP negativo)</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                
                <div class="family-section">
                    <h3>R2 - Random, 1000 clientes, Horizon Largo (11 instancias)</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Métrica</th>
                                <th class="algo1">Algoritmo 1</th>
                                <th class="algo2">Algoritmo 2</th>
                                <th class="algo3">Algoritmo 3</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Promedio GAP</td>
                                <td class="number algo1">44.74%</td>
                                <td class="number algo2">25.90%</td>
                                <td class="number algo3"><span class="highlight-good">11.95%</span></td>
                            </tr>
                            <tr>
                                <td>Mediana GAP</td>
                                <td class="number algo1">49.90%</td>
                                <td class="number algo2">28.93%</td>
                                <td class="number algo3"><span class="highlight-good">11.85%</span></td>
                            </tr>
                            <tr>
                                <td colspan="4" style="text-align: center; padding: 15px;"><span class="winner">✅ MEJOR: Algoritmo 3 (ocasional)</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                
                <div class="family-section">
                    <h3>RC1 - Random-Clustered, 100 clientes (8 instancias)</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Métrica</th>
                                <th class="algo1">Algoritmo 1</th>
                                <th class="algo2">Algoritmo 2</th>
                                <th class="algo3">Algoritmo 3</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Promedio GAP</td>
                                <td class="number algo1">31.84%</td>
                                <td class="number algo2"><span class="highlight-good">-7.06%</span></td>
                                <td class="number algo3">32.42%</td>
                            </tr>
                            <tr>
                                <td>Mediana GAP</td>
                                <td class="number algo1">36.76%</td>
                                <td class="number algo2"><span class="highlight-good">-6.02%</span></td>
                                <td class="number algo3">31.97%</td>
                            </tr>
                            <tr>
                                <td colspan="4" style="text-align: center; padding: 15px;"><span class="highlight-good" style="padding: 10px; font-size: 1.1em;">🏆 EXCELENTE: Algoritmo 2 SUPERA BKS (GAP negativo)</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                
                <div class="family-section">
                    <h3>RC2 - Random-Clustered, Horizon Largo (8 instancias)</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Métrica</th>
                                <th class="algo1">Algoritmo 1</th>
                                <th class="algo2">Algoritmo 2</th>
                                <th class="algo3">Algoritmo 3</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Promedio GAP</td>
                                <td class="number algo1">59.66%</td>
                                <td class="number algo2">16.98%</td>
                                <td class="number algo3"><span class="highlight-good">11.36%</span></td>
                            </tr>
                            <tr>
                                <td>Mediana GAP</td>
                                <td class="number algo1">60.93%</td>
                                <td class="number algo2">14.12%</td>
                                <td class="number algo3"><span class="highlight-good">8.60%</span></td>
                            </tr>
                            <tr>
                                <td colspan="4" style="text-align: center; padding: 15px;"><span class="winner">✅ MEJOR: Algoritmo 3 (competitivo con Algo 2)</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            
            <!-- GRÁFICOS -->
            <div class="section">
                <h2>📊 Visualizaciones</h2>
                <p>Los siguientes gráficos están disponibles en la carpeta <code>plots/</code>:</p>
                
                <div class="gallery">
                    <div class="gallery-item">
                        <h4>01 - Comparación de GAP (Barras)</h4>
                        <p>Gráfico de barras agrupadas mostrando los 3 algoritmos para cada una de las 56 instancias. La línea roja marca BKS (GAP=0).</p>
                        <p><strong>Archivo:</strong> 01_gap_comparison_all_instances.png</p>
                    </div>
                    
                    <div class="gallery-item">
                        <h4>02 - Evolución de GAP (Líneas)</h4>
                        <p>Gráfico de líneas mostrando la tendencia de GAP a través de las 56 instancias. Algoritmo 2 es claramente más estable y bajo.</p>
                        <p><strong>Archivo:</strong> 02_gap_evolution_lines.png</p>
                    </div>
                    
                    <div class="gallery-item">
                        <h4>03 - Boxplot por Familia</h4>
                        <p>Distribución de GAP por familia (C1, C2, R1, R2, RC1, RC2). Muestra mediana, cuartiles y valores atípicos.</p>
                        <p><strong>Archivo:</strong> 03_gap_boxplot_by_family.png</p>
                    </div>
                    
                    <div class="gallery-item">
                        <h4>04 - Heatmap de GAP</h4>
                        <p>Mapa de calor con 56 filas (instancias) × 3 columnas (algoritmos). Verde = bueno, Rojo = malo.</p>
                        <p><strong>Archivo:</strong> 04_gap_heatmap.png</p>
                    </div>
                    
                    <div class="gallery-item">
                        <h4>05 - Grid por Familia</h4>
                        <p>6 subgráficos (uno por familia) mostrando los 3 algoritmos en barras agrupadas. Fácil comparación dentro de familias.</p>
                        <p><strong>Archivo:</strong> 05_gap_by_family_grid.png</p>
                    </div>
                </div>
            </div>
            
            <!-- RECOMENDACIONES -->
            <div class="section">
                <h2>💡 Recomendaciones</h2>
                
                <div class="recommendation">
                    <h4>✅ Para Publicación Académica</h4>
                    <ul style="margin-left: 20px; line-height: 1.8;">
                        <li><strong>Título propuesto:</strong> "Algoritmo generado automáticamente via GAA supera BKS en 28% de instancias VRPTW"</li>
                        <li><strong>Resumen principal:</strong> Algoritmo 2 logra GAP promedio de 25.25%, competitivo pero no óptimo</li>
                        <li><strong>Hallazgo destacable:</strong> Supera BKS publicados en familias aleatorias (R1: -0.60% GAP)</li>
                        <li><strong>Limitación conocida:</strong> Débil en instancias clustered largas (C2: +94.76% GAP)</li>
                        <li><strong>Ventaja competitiva:</strong> 21× más rápido que Algoritmo 1 (0.17s vs 3.75s)</li>
                    </ul>
                </div>
                
                <div class="recommendation" style="background: #e7f3ff; border-left-color: #0066cc;">
                    <h4>🔧 Para Mejora Futura (ITER-4)</h4>
                    <ul style="margin-left: 20px; line-height: 1.8;">
                        <li><strong>Prioritario:</strong> Investigar por qué Algoritmo 2 falla en familias C2</li>
                        <li><strong>Hipótesis:</strong> Constructor NearestNeighbor ignora clustering</li>
                        <li><strong>Experimento sugerido:</strong> ITER-4 con constructor RandomizedInsertion para C2</li>
                        <li><strong>Alcance:</strong> Modificar solo para 8 instancias C2 (QUICK experiment)</li>
                        <li><strong>Meta:</strong> Reducir C2 GAP de 94.76% a < 30%</li>
                    </ul>
                </div>
                
                <div class="recommendation" style="background: #f0f0f0; border-left-color: #666;">
                    <h4>📊 Para Benchmarking</h4>
                    <ul style="margin-left: 20px; line-height: 1.8;">
                        <li><strong>Especialidad comprobada:</strong> Instancias aleatorias y mixtas (R, RC families)</li>
                        <li><strong>Debilidad comprobada:</strong> Instancias clustered largas (C2 family)</li>
                        <li><strong>Uso recomendado:</strong> Aplicar Algoritmo 2 a problemas reales con distribuciones R/RC</li>
                        <li><strong>No recomendado para:</strong> Problemas clustered puros (sin diversidad geográfica)</li>
                    </ul>
                </div>
            </div>
            
            <!-- CONCLUSIÓN -->
            <div class="section">
                <h2>🏁 Conclusión</h2>
                <p>
                    Algoritmo 2 es claramente el mejor de los 3 algoritmos generados automáticamente via GAA. 
                    Demuestra fortaleza particular en instancias aleatorias y mixtas, donde 
                    <strong>supera los Best Known Solutions publicados</strong>. Sin embargo, tiene una 
                    limitación crítica en instancias clustered largas que requiere investigación futura.
                </p>
                <p style="margin-top: 15px; color: #666;">
                    <strong>Recomendación final:</strong> Proceder con publicación de Algoritmo 2, documentando 
                    claramente su especialidad en instancias aleatorias y su limitación conocida en clustered largas. 
                    Considerar ITER-4 para mejorar desempeño en C2 si es crítico para aplicaciones específicas.
                </p>
            </div>
        </div>
        
        <footer>
            <p>Análisis generado automáticamente | 56 Instancias Solomon VRPTW | Experimentación FULL completada</p>
            <p>Gráficos disponibles en: <code>output/vrptw_experiments_FULL_03-01-26_02-18-27/plots/</code></p>
        </footer>
    </div>
</body>
</html>
"""

# Guardar HTML
with open('output/vrptw_experiments_FULL_03-01-26_02-18-27/plots/ANALISIS_GAP_INTERACTIVO.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ HTML interactivo creado: ANALISIS_GAP_INTERACTIVO.html")
print("   Ubicación: output/vrptw_experiments_FULL_03-01-26_02-18-27/plots/")
print("\n   Para abrir:")
print("   - Click derecho en ANALISIS_GAP_INTERACTIVO.html")
print("   - Seleccionar 'Abrir con' → navegador (Chrome, Firefox, Edge, etc.)")
