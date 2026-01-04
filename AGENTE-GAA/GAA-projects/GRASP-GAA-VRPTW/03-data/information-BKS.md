BEST KNOWN SOLUTIONS (BKS) – VRPTW SOLOMON

Para cada instancia del benchmark Solomon VRPTW se utiliza el Best Known Solution (BKS) reportado en la literatura.

El BKS de una instancia i se define como el par ordenado:

(V_i, D_i)

donde:

V*_i es el mínimo número de vehículos alcanzado para la instancia i

D*_i es la menor distancia total asociada a ese número de vehículos

El criterio de comparación entre soluciones sigue el orden lexicográfico canónico del VRPTW:

Una solución s1 es mejor que una solución s2 si:

V(s1) < V(s2), o

V(s1) = V(s2) y D(s1) < D(s2)

Uso del BKS en la evaluación:

Si V(sol) > V*_i, la solución se considera inferior independientemente de la distancia.

Si V(sol) = V*_i, la calidad se evalúa mediante el gap relativo en distancia.

Si V(sol) < V*_i, la solución mejora el BKS.

Definición del gap relativo en distancia:

Gap(i) = (D(sol, i) − D_i) / D_i

El gap solo se calcula cuando V(sol, i) = V*_i.

Almacenamiento de BKS:

Los valores de BKS se almacenan en un archivo CSV externo con el siguiente formato:

instance_id, family, k_bks, d_bks

Este archivo es utilizado directamente por el código experimental para:

evaluación automática de soluciones

cálculo de gaps

penalización por exceso de vehículos

comparación consistente entre instancias

Ruta del dataset Solomon VRPTW:

/c:/Users/gustavo_windows/Desktop/bestbestGAA/AGENTE-GAA/GAA-projects/GRASP-GAA-VRPTW/03-data/Solomon-VRPTW-Dataset/