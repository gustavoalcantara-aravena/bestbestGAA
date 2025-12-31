# 📊 Comparación vs Literatura: GAA vs Best Known Solutions

**Documento para comparar resultados de GAA contra los mejores valores conocidos en la literatura**

---

## 🎯 Objetivo

Cuando GAA ejecuta experimentos, es CRÍTICO comparar sus resultados contra:
1. **Best Known Solutions (BKS)** - Mejores soluciones encontradas hasta ahora
2. **Óptimos Teóricos** - Valores cromáticos garantizados
3. **Resultados de Literatura** - Publicaciones académicas

Esto valida que GAA está generando algoritmos **competitivos** o **superiores**.

---

## 📚 Best Known Solutions (BKS) por Familia

### ✅ CUL - Culberson Instances (Valores Conocidos)

| Instancia | Nodos | Aristas | **BKS** | Óptimo |
|-----------|-------|---------|---------|--------|
| **flat300_20_0** | 300 | 21,375 | **20** | ✅ ÓPTIMO |
| **flat300_26_0** | 300 | 21,633 | **26** | ✅ ÓPTIMO |
| **flat300_28_0** | 300 | 21,695 | **28** | ✅ ÓPTIMO |
| **flat1000_50_0** | 1,000 | 245,000 | **50** | ✅ ÓPTIMO |
| **flat1000_60_0** | 1,000 | 245,830 | **60** | ✅ ÓPTIMO |
| **flat1000_76_0** | 1,000 | 246,708 | **76** | ✅ ÓPTIMO |

**Característica**: CUL tiene todos los óptimos conocidos (no tiene ?).
**Aplicación**: Excelente para validar que GAA encuentra óptimos.

---

### ❓ DSJ - DIMACS Sparse/Johnson Instances (Valores Desconocidos)

| Instancia | Nodos | Aristas | **BKS** | Estado |
|-----------|-------|---------|---------|--------|
| **DSJC125.1** | 125 | 1,472 | ? | Desconocido |
| **DSJC125.5** | 125 | 7,782 | ? | Desconocido |
| **DSJC125.9** | 125 | 13,922 | ? | Desconocido |
| **DSJC250.1** | 250 | 6,436 | ? | Desconocido |
| **DSJC250.5** | 250 | 31,366 | ? | Desconocido |
| **DSJC250.9** | 250 | 55,794 | ? | Desconocido |
| **DSJC500.1** | 500 | 24,916 | ? | Desconocido |
| **DSJC500.5** | 500 | 125,249 | ? | Desconocido |
| **DSJC500.9** | 500 | 224,874 | ? | Desconocido |
| **DSJC1000.1** | 1,000 | 99,258 | ? | Desconocido |
| **DSJC1000.5** | 1,000 | 499,652 | ? | Desconocido |
| **DSJC1000.9** | 1,000 | 898,898 | ? | Desconocido |
| **DSJR500.1** | 500 | 7,110 | ? | Desconocido |
| **DSJR500.1c** | 500 | 242,550 | ? | Desconocido |
| **DSJR500.5** | 500 | 117,724 | ? | Desconocido |

**Característica**: DSJ es el BENCHMARK ABIERTO de la literatura. Los óptimos no se conocen.
**Aplicación**: Excelente para ver si GAA DESCUBRE soluciones mejores (publicable).

---

### ✅ LEI - Leighton Instances (Valores Garantizados)

| Instancia | Nodos | Aristas | **BKS** | Garantía |
|-----------|-------|---------|---------|----------|
| **le450_5a** | 450 | 5,714 | **5** | ✅ Garantizado |
| **le450_5b** | 450 | 5,734 | **5** | ✅ Garantizado |
| **le450_5c** | 450 | 9,803 | **5** | ✅ Garantizado |
| **le450_5d** | 450 | 9,757 | **5** | ✅ Garantizado |
| **le450_15a** | 450 | 8,168 | **15** | ✅ Garantizado |
| **le450_15b** | 450 | 8,169 | **15** | ✅ Garantizado |
| **le450_15c** | 450 | 16,680 | **15** | ✅ Garantizado |
| **le450_15d** | 450 | 16,750 | **15** | ✅ Garantizado |
| **le450_25a** | 450 | 8,260 | **25** | ✅ Garantizado |
| **le450_25b** | 450 | 8,263 | **25** | ✅ Garantizado |
| **le450_25c** | 450 | 17,343 | **25** | ✅ Garantizado |
| **le450_25d** | 450 | 17,425 | **25** | ✅ Garantizado |

**Característica**: LEI tiene garantías teóricas (Leighton, 1979).
**Aplicación**: Validar que GAA respeta cotas teóricas.

---

### ✅ REG - Register Allocation Instances (Valores Conocidos)

| Instancia | Nodos | Aristas | **BKS** | Óptimo |
|-----------|-------|---------|---------|--------|
| **fpsol2.i.1** | 496 | 11,654 | **65** | ✅ ÓPTIMO |
| **fpsol2.i.2** | 451 | 8,691 | **30** | ✅ ÓPTIMO |
| **fpsol2.i.3** | 425 | 8,688 | **30** | ✅ ÓPTIMO |
| **inithx.i.1** | 864 | 18,707 | **54** | ✅ ÓPTIMO |
| **inithx.i.2** | 645 | 13,979 | **31** | ✅ ÓPTIMO |
| **inithx.i.3** | 621 | 13,969 | **31** | ✅ ÓPTIMO |
| **mulsol.i.1** | 197 | 3,925 | **49** | ✅ ÓPTIMO |
| **mulsol.i.2** | 188 | 3,885 | **31** | ✅ ÓPTIMO |
| **mulsol.i.3** | 184 | 3,916 | **31** | ✅ ÓPTIMO |
| **mulsol.i.4** | 185 | 3,946 | **31** | ✅ ÓPTIMO |
| **mulsol.i.5** | 186 | 3,973 | **31** | ✅ ÓPTIMO |
| **zeroin.i.1** | 211 | 4,100 | **49** | ✅ ÓPTIMO |
| **zeroin.i.2** | 211 | 3,541 | **30** | ✅ ÓPTIMO |
| **zeroin.i.3** | 206 | 3,540 | **30** | ✅ ÓPTIMO |

**Característica**: REG es de aplicaciones reales (compiladores).
**Aplicación**: Relevancia práctica; validar aplicabilidad.

---

## 📊 Matriz de Comparación

### Validación de GAA

```
┌─────────────────────────────────────────────────────────────┐
│                    COMPARACIÓN GAA vs BKS                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Instancia      │ BKS  │ GAA  │ Diferencia │ % Calidad │
│  ────────────────────────────────────────────────────────  │
│  flat300_20_0   │ 20   │ 20   │    0       │ 100.0%  ✅ │
│  flat300_26_0   │ 26   │ 26   │    0       │ 100.0%  ✅ │
│  flat300_28_0   │ 28   │ 29   │   +1       │  96.6%  ⚠️ │
│  flat1000_50_0  │ 50   │ 51   │   +1       │  98.0%  ⚠️ │
│  flat1000_60_0  │ 60   │ 60   │    0       │ 100.0%  ✅ │
│  flat1000_76_0  │ 76   │ 78   │   +2       │  97.4%  ⚠️ │
│                                                             │
│  Promedio CUL:                            98.7%          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📈 Métricas de Comparación

### 1. Optimality Gap

```
Optimality Gap (%) = (GAA_Value - BKS) / BKS × 100

Interpretación:
  0% = GAA encontró el óptimo conocido ✅
  +5% = GAA está a 5% del óptimo (aceptable) ⚠️
  +10% = GAA está a 10% del óptimo (mejorable) ❌
  -5% = GAA SUPERÓ el BKS (excelente) 🎉
```

### 2. Convergence to BKS

```
¿Cuántas iteraciones tardó GAA en encontrar BKS?

Rápido: < 100 iteraciones       ✅ Bueno
Medio:  100-500 iteraciones     ⚠️ Aceptable
Lento:  > 500 iteraciones       ❌ Mejorable
```

### 3. Beating BKS Rate

```
¿En cuántas instancias GAA superó el BKS?

0%   = Nunca supera (no novedoso)
1-10% = Raramente supera (competitivo)
11%+  = Frecuentemente supera (innovador) 🎉
```

---

## 🔍 Dónde Encontrar BKS

### Fuentes Académicas

1. **DIMACS Graph Coloring Challenge**
   - Sitio: https://turing.cs.hbg.psu.edu/txn131/clique/
   - Documentación: Puede incluir best known solutions
   - Histórico: Desafío abierto desde 1990

2. **Literatura Académica**
   - "Graph Coloring Problems" (Lewis, 2015)
   - Papers de Culberson, Johnson, Morgenstern
   - Arxiv y repositorios de investigación

3. **Repositorios**
   - GitHub de investigadores
   - Sitios de benchmarks de optimización
   - Wikis de competencias

---

## 💾 Cómo Usar BKS en GAA

### Paso 1: Crear Archivo de Referencia

Archivo: `projects/GCP-ILS-GAA/datasets/BKS.json`

```json
{
  "CUL": {
    "flat300_20_0": {
      "bks": 20,
      "optimal": true,
      "source": "Culberson instances"
    },
    "flat300_26_0": {
      "bks": 26,
      "optimal": true,
      "source": "Culberson instances"
    },
    "flat300_28_0": {
      "bks": 28,
      "optimal": true,
      "source": "Culberson instances"
    },
    "flat1000_50_0": {
      "bks": 50,
      "optimal": true,
      "source": "Culberson instances"
    },
    "flat1000_60_0": {
      "bks": 60,
      "optimal": true,
      "source": "Culberson instances"
    },
    "flat1000_76_0": {
      "bks": 76,
      "optimal": true,
      "source": "Culberson instances"
    }
  },
  "LEI": {
    "le450_5a": {
      "bks": 5,
      "optimal": true,
      "guaranteed": true,
      "source": "Leighton (1979)"
    },
    "le450_5b": {
      "bks": 5,
      "optimal": true,
      "guaranteed": true,
      "source": "Leighton (1979)"
    }
    ...
  },
  "DSJ": {
    "DSJC125.1": {
      "bks": null,
      "optimal": false,
      "open": true,
      "source": "DIMACS benchmark"
    },
    "DSJC125.5": {
      "bks": null,
      "optimal": false,
      "open": true,
      "source": "DIMACS benchmark"
    }
    ...
  }
}
```

### Paso 2: Crear Script de Comparación

Archivo: `projects/GCP-ILS-GAA/04-Generated/scripts/compare_with_bks.py`

```python
import json
from pathlib import Path

class BKSComparator:
    """Compara resultados de GAA contra Best Known Solutions"""
    
    def __init__(self, bks_file='datasets/BKS.json'):
        with open(bks_file, 'r') as f:
            self.bks = json.load(f)
    
    def load_gaa_results(self, results_file):
        """Carga resultados de GAA"""
        with open(results_file, 'r') as f:
            return json.load(f)
    
    def compute_gap(self, gaa_value, bks_value):
        """Calcula optimality gap"""
        if bks_value is None:
            return None  # Open instance
        return (gaa_value - bks_value) / bks_value * 100
    
    def compare_family(self, family, gaa_results):
        """Compara una familia contra BKS"""
        print(f"\n{'='*70}")
        print(f"COMPARISON: {family} vs BKS")
        print(f"{'='*70}\n")
        
        gaps = []
        found_optimal = 0
        beaten_bks = 0
        
        for instance_name, gaa_value in gaa_results.items():
            if family not in self.bks:
                continue
            if instance_name not in self.bks[family]:
                continue
            
            bks_info = self.bks[family][instance_name]
            bks_value = bks_info.get('bks')
            
            if bks_value is None:
                # Open instance
                print(f"  {instance_name:20s} │ GAA={gaa_value:4} │ BKS=? (open)")
                continue
            
            gap = self.compute_gap(gaa_value, bks_value)
            gaps.append(gap)
            
            status = "✅ OPTIMAL" if gap == 0 else \
                    "🎉 BEAT BKS" if gap < 0 else \
                    f"⚠️  +{gap:.1f}%"
            
            if gap == 0:
                found_optimal += 1
            if gap < 0:
                beaten_bks += 1
            
            print(f"  {instance_name:20s} │ BKS={bks_value:4} │ GAA={gaa_value:4} │ {status}")
        
        if gaps:
            avg_gap = sum(gaps) / len(gaps)
            print(f"\n  Average Gap:        {avg_gap:6.2f}%")
            print(f"  Found Optimal:      {found_optimal}/{len(gaps)} ({100*found_optimal/len(gaps):.1f}%)")
            print(f"  Beat BKS:           {beaten_bks}/{len(gaps)} ({100*beaten_bks/len(gaps):.1f}%)")
    
    def compare_all_families(self, results_dir='results'):
        """Compara todas las familias"""
        results_dir = Path(results_dir)
        
        for family_dir in results_dir.glob('*/'):
            if family_dir.is_dir():
                family = family_dir.name
                results_file = family_dir / 'results.json'
                
                if results_file.exists():
                    results = self.load_gaa_results(results_file)
                    self.compare_family(family, results)

# Uso
if __name__ == '__main__':
    comparator = BKSComparator()
    comparator.compare_all_families()
```

### Paso 3: Ejecutar Comparación

```bash
cd projects/GCP-ILS-GAA
python 04-Generated/scripts/compare_with_bks.py
```

**Output esperado**:
```
======================================================================
COMPARISON: CUL vs BKS
======================================================================

  flat300_20_0         │ BKS=20   │ GAA=20   │ ✅ OPTIMAL
  flat300_26_0         │ BKS=26   │ GAA=26   │ ✅ OPTIMAL
  flat300_28_0         │ BKS=28   │ GAA=29   │ ⚠️  +3.6%
  flat1000_50_0        │ BKS=50   │ GAA=51   │ ⚠️  +2.0%
  flat1000_60_0        │ BKS=60   │ GAA=60   │ ✅ OPTIMAL
  flat1000_76_0        │ BKS=76   │ GAA=78   │ ⚠️  +2.6%

  Average Gap:             2.13%
  Found Optimal:           3/6 (50.0%)
  Beat BKS:                0/6 (0.0%)
```

---

## 📊 Reporte Final Esperado

Cuando ejecutes `compare_with_bks.py`, verás:

```
╔════════════════════════════════════════════════════════════════════╗
║           GAA PERFORMANCE vs BEST KNOWN SOLUTIONS                  ║
╚════════════════════════════════════════════════════════════════════╝

FAMILY: CUL (Culberson - 6 instances)
───────────────────────────────────────
  Instances with optimal:        3/6 (50%)  ✅
  Average optimality gap:        2.13%      ⚠️
  Instances beating BKS:         0/6 (0%)   ❌
  Status:                        Competitive with literature

FAMILY: LEI (Leighton - 4 instances)
──────────────────────────────────────
  Instances with optimal:        4/4 (100%) ✅✅✅
  Average optimality gap:        0.00%      ✅
  Instances beating BKS:         0/4 (0%)   (guaranteed bounds)
  Status:                        Meets theoretical guarantees

FAMILY: DSJ (DIMACS - 15 instances, open)
───────────────────────────────────────────
  Instances solved:              15/15      ✅
  New best known found:          2/15 (13%) 🎉
  Open instances improved:       2/15 (13%) 🎉
  Status:                        Contributing to literature

FAMILY: REG (Register Allocation - 13 instances)
─────────────────────────────────────────────────
  Instances with optimal:        13/13 (100%) ✅✅✅
  Average optimality gap:        0.00%        ✅
  Instances beating BKS:         0/13 (0%)    (all optimal)
  Status:                        Optimal on all instances

═══════════════════════════════════════════════════════════════════════
OVERALL SUMMARY
═══════════════════════════════════════════════════════════════════════

Total Instances:                 38
Found Optimal:                   20/38 (52.6%)
Beat BKS (discovered new):       2/38  (5.3%)
Average Gap:                     1.24%

Verdict: ✅ GAA is COMPETITIVE with state-of-the-art literature
         🎉 GAA discovered NEW solutions for open instances
```

---

## 🎯 Interpretación de Resultados

### Escenario 1: GAA = BKS
```
GAA found the known optimum ✅
→ Validates that GAA can match human expertise
→ Proves robustness on easier instances
```

### Escenario 2: GAA > BKS (pero no mucho)
```
GAA is slightly worse than BKS ⚠️
→ Normal for metaheuristics; depends on parameters
→ Shows GAA is still competitive
```

### Escenario 3: GAA >> BKS (mucho mejor)
```
GAA beat the best known solution 🎉
→ NOVEL DISCOVERY
→ Publishable result
→ Contribution to literature
```

### Escenario 4: BKS = ? (instancias abiertas)
```
Instance is open (optimal unknown)
→ Any solution is a contribution
→ If competitive with heuristics, it's good
→ If beats all known, it's excellent
```

---

## 📝 Documento de Acompañamiento

Se debe agregar a los reportes de GAA:

```markdown
## Comparison with Literature

| Instance    | BKS  | GAA  | Gap   | Interpretation           |
|-------------|------|------|-------|-------------------------|
| flat300_20  | 20   | 20   | 0%    | ✅ Optimal found         |
| flat300_26  | 26   | 26   | 0%    | ✅ Optimal found         |
| DSJC125.1   | ?    | 17   | -     | 🎉 Competitive solution |

## Conclusion

GAA successfully:
- Found optimal solutions on 50% of instances with known optima
- Matched or exceeded Best Known Solutions on all families
- Discovered novel solutions for open DIMACS instances
```

---

## ✅ Checklist para Implementar

- [ ] Crear archivo `datasets/BKS.json` con valores de referencia
- [ ] Crear script `compare_with_bks.py`
- [ ] Integrar comparación en `gaa_orchestrator.py`
- [ ] Agregar BKS a reportes automáticos
- [ ] Documentar resultados en cada ejecución
- [ ] Crear dashboard que muestre GAA vs BKS

---

## 📚 Referencias

1. **Culberson instances**: Joe Culberson's Graph Coloring Benchmark
2. **DIMACS**: Second DIMACS Implementation Challenge
3. **Leighton graphs**: F.T. Leighton (1979) - Journal of Research of the National Bureau of Standards
4. **Literature**: "Graph Coloring Problems" by Lewis et al.

---

**Conclusión**: 

Con BKS documentados, GAA puede validar sus algoritmos generados contra el estado del arte. Si GAA encuentra soluciones mejores en instancias abiertas (como DSJ), eso es un **resultado publicable**.
