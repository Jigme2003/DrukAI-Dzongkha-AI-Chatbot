# Person 1 – Data pipeline, baselines & evaluation metrics

## Files
| File | Purpose |
|---|---|
| `data_utils.py` | TSPLIB parser (.tsp/.opt.tour, gz ok), min-max normalisation, distance matrices, `TSPInstance`, optimal-edge matrix `T_ij` for Person 2 |
| `baselines.py` | Nearest Neighbour, Pure GA (tournament k=3, OX, inversion, elitism); `init_population` hook for Person 3 |
| `metrics.py` | % gap, runtime, convergence generation, paired Wilcoxon test, convergence curves |
| `run_baselines.py` | Runs NN + Pure GA (30 seeds/instance), saves CSV/pickle/plot |

## Setup
```
data/berlin52.tsp[.gz], st70, kroA100, ch130 (+ optional tsp225)   # from TSPLIB95
data/<name>.opt.tour[.gz]                                           # optimal tours (needed for BCE labels)
python run_baselines.py --data data --runs 30
```

## Interface contract with teammates
* Person 2: `inst = load_instance(...)`; input `inst.D_norm`; label `inst.optimal_edge_matrix()`.
* Person 3: `run_ga(inst, seed, init_population=pop)` with the SAME seeds 0..29 so the Wilcoxon test is paired.
  Compare with `metrics.wilcoxon_vs_ga(ga_lengths, hybrid_lengths)`.
