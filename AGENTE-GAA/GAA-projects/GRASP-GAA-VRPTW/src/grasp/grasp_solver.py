"""
============================================================
GRASP Solver (Constructive + Local Search)
VRPTW Solomon - GAA driven
============================================================

- Constructive phase: greedy randomized insertion guided by a construction AST (score)
- Local Search phase: apply neighborhood operators guided by an LS AST (operator selector)
- Evaluation: uses evaluation.solution_evaluator

This solver expects:
- instance dict from utils.dataset_loader.load_solomon_instance
- algorithm dict (descriptor) containing:
    algorithm["construction_ast"] : JSON AST to score insertions (numeric)
    algorithm["ls_operator_ast"]  : JSON AST to select operator (string)
  If not present, it can fall back to:
    algorithm["ast"] with algorithm["phase"] == "construction" or "local_search"
"""

from __future__ import annotations

import random
from typing import Dict, Any, List, Tuple, Optional

from evaluation.solution_evaluator import evaluate_solution_full, evaluate_route


# ============================================================
# JSON AST Evaluator (direct from JSON)
# ============================================================

def eval_ast_json(ast: Dict[str, Any], features: Dict[str, float]) -> Any:
    """
    Evaluates the JSON AST using provided numeric features.
    Returns: float/int for construction or str for operator selector.
    """
    t = ast["type"]

    if t == "Feature":
        return float(features.get(ast["name"], 0.0))

    if t == "Const":
        return ast["value"]

    if t == "Add":
        return eval_ast_json(ast["left"], features) + eval_ast_json(ast["right"], features)

    if t == "Sub":
        return eval_ast_json(ast["left"], features) - eval_ast_json(ast["right"], features)

    if t == "Mul":
        return eval_ast_json(ast["left"], features) * eval_ast_json(ast["right"], features)

    if t == "Div":
        denom = eval_ast_json(ast["right"], features)
        if denom == 0:
            return 0.0
        return eval_ast_json(ast["left"], features) / denom

    if t == "WeightedSum":
        s = 0.0
        for term in ast["terms"]:
            w = float(term["weight"])
            s += w * float(eval_ast_json(term["expr"], features))
        return s

    if t == "Normalize":
        x = float(eval_ast_json(ast["expr"], features))
        mn = float(ast.get("min", 0.0))
        mx = float(ast.get("max", 1.0))
        if mx == mn:
            return 0.0
        return (x - mn) / (mx - mn)

    if t == "Clip":
        x = float(eval_ast_json(ast["expr"], features))
        mn = float(ast["min"])
        mx = float(ast["max"])
        return max(mn, min(mx, x))

    if t == "Less":
        return float(eval_ast_json(ast["left"], features)) < float(eval_ast_json(ast["right"], features))

    if t == "Greater":
        return float(eval_ast_json(ast["left"], features)) > float(eval_ast_json(ast["right"], features))

    if t == "And":
        return bool(eval_ast_json(ast["left"], features)) and bool(eval_ast_json(ast["right"], features))

    if t == "Or":
        return bool(eval_ast_json(ast["left"], features)) or bool(eval_ast_json(ast["right"], features))

    if t == "If":
        cond = bool(eval_ast_json(ast["condition"], features))
        return eval_ast_json(ast["then"], features) if cond else eval_ast_json(ast["else"], features)

    if t == "Choose":
        # Choose returns one of the options deterministically by max score (numeric)
        # Options can be:
        # - Simple values: [op1, op2, op3] (strings)
        # - Weighted values: [{"weight": w, "value": op}, ...]
        if ast["options"] and isinstance(ast["options"][0], dict) and "value" in ast["options"][0]:
            # Weighted format: extract values
            values = [o["value"] for o in ast["options"]]
            return values[0] if values else None
        else:
            # Simple format: evaluate each option
            opts = [eval_ast_json(o, features) for o in ast["options"]]
            # If strings -> pick first (deterministic)
            if opts and isinstance(opts[0], str):
                return opts[0]
            return max(opts) if opts else 0.0

    raise ValueError(f"Unknown AST node type: {t}")


# ============================================================
# GRASP Solver
# ============================================================

class GRASPSolver:
    """
    GRASP for VRPTW (Solomon).
    """

    def __init__(self, algorithm: Dict[str, Any], instance: Dict[str, Any], bks: Dict[str, Any], config: Dict[str, Any]):
        self.algorithm = algorithm
        self.instance = instance
        self.bks = bks
        self.cfg = config

        seed = int(config.get("experiment", {}).get("seed", 42))
        self.rng = random.Random(seed)

        # Constructive params
        grasp_cfg = config.get("grasp", {})
        self.rcl_size = int(grasp_cfg.get("rcl_size", 5))
        self.max_construct_iters = int(grasp_cfg.get("max_construct_iters", 10_000))

        # Local search params
        ls_cfg = config.get("local_search", {})
        self.max_ls_iters = int(ls_cfg.get("max_iters", 500))
        self.max_no_improve = int(ls_cfg.get("max_no_improve", 100))

        # Penalty / fitness
        self.penalty_cfg = config.get("penalty", {"alpha_capacity": 1000.0, "alpha_time": 10.0})
        self.fitness_cfg = config.get("fitness", {"w_vehicles": 1000.0, "w_distance": 1.0})

        # Allowed LS operators
        self.allowed_ops = set(ls_cfg.get("operators", ["relocate", "swap", "two_opt", "or_opt"]))

        # Resolve ASTs
        self.construction_ast = self._pick_ast("construction")
        self.ls_operator_ast = self._pick_ast("local_search")

    # --------------------------------------------------------
    # Public API
    # --------------------------------------------------------

    def solve(self) -> Dict[str, Any]:
        """
        Returns:
        {
          "routes": ...,
          "vehicles": int,
          "distance": float,
          "feasible": bool,
          "capacity_violation": float,
          "time_violation": float
        }
        """
        sol = self._construct_solution()
        sol = self._local_search(sol)

        ev = evaluate_solution_full(
            solution=sol,
            instance=self.instance,
            penalty_cfg=self.penalty_cfg,
            fitness_cfg=self.fitness_cfg
        )

        metrics = ev["metrics"]
        return {
            "routes": sol["routes"],
            "vehicles": metrics["num_vehicles"],
            "distance": metrics["total_distance"],
            "feasible": metrics["feasible"],
            "capacity_violation": metrics["capacity_violation"],
            "time_violation": metrics["time_violation"]
        }

    # --------------------------------------------------------
    # AST selection helper
    # --------------------------------------------------------

    def _pick_ast(self, phase: str) -> Optional[Dict[str, Any]]:
        """
        Accepts:
        - algorithm["construction_ast"], algorithm["ls_operator_ast"]
        Or fallback:
        - algorithm["phase"] == phase and algorithm["ast"]
        """
        if phase == "construction" and "construction_ast" in self.algorithm:
            return self.algorithm["construction_ast"]
        if phase == "local_search" and "ls_operator_ast" in self.algorithm:
            return self.algorithm["ls_operator_ast"]

        # fallback if descriptor is a single-phase
        if self.algorithm.get("phase") == phase and "ast" in self.algorithm:
            return self.algorithm["ast"]

        return None

    # =========================================================
    # CONSTRUCTIVE PHASE
    # =========================================================

    def _construct_solution(self) -> Dict[str, Any]:
        """
        Sequential insertion GRASP:
        - start with empty routes
        - iteratively insert an unrouted customer into best position across all routes
        - use AST score to rank candidates, then choose from RCL
        """
        n = self.instance["num_customers"]
        unrouted = set(range(1, n + 1))  # customer indices 1..n
        routes: List[List[int]] = []

        # Start: seed route with one customer (random or heuristic)
        # Solomon style: choose farthest or earliest due. We'll keep simple but deterministic-ish.
        seed_customer = self._select_seed_customer(unrouted)
        routes.append([0, seed_customer, 0])
        unrouted.remove(seed_customer)

        iters = 0
        while unrouted and iters < self.max_construct_iters:
            iters += 1

            candidates = []  # (score, customer, route_idx, insert_pos, cand_features)

            for u in list(unrouted):
                # try inserting u into any existing route, any position
                best_for_u = self._best_insertion_for_customer(u, routes)
                if best_for_u is not None:
                    candidates.append(best_for_u)

            # if no feasible insertion exists, open a new route with some remaining customer
            if not candidates:
                u = self._select_seed_customer(unrouted)
                routes.append([0, u, 0])
                unrouted.remove(u)
                continue

            # sort by score ascending (lower is better)
            candidates.sort(key=lambda x: x[0])

            # build RCL
            rcl = candidates[: max(1, min(self.rcl_size, len(candidates)))]
            chosen = self.rng.choice(rcl)

            score, u, r_idx, pos, _ = chosen
            routes[r_idx].insert(pos, u)
            unrouted.remove(u)

        # any leftovers -> open separate routes (should be rare in Solomon if feasible exists)
        while unrouted:
            u = unrouted.pop()
            routes.append([0, u, 0])

        return {"routes": routes}

    def _select_seed_customer(self, unrouted: set) -> int:
        """
        Simple robust seeding:
        - pick customer with earliest due date among unrouted with small randomness
        """
        nodes = self.instance["nodes"]
        cand = list(unrouted)
        cand.sort(key=lambda i: nodes[i]["due_date"])
        top = cand[: min(5, len(cand))]
        return self.rng.choice(top)

    def _best_insertion_for_customer(self, u: int, routes: List[List[int]]):
        """
        Find best feasible insertion for customer u across all routes.
        Returns tuple:
          (score, u, route_idx, insert_pos, features)
        """
        best = None

        for r_idx, route in enumerate(routes):
            # insertion positions: between route[k] and route[k+1]
            for pos in range(1, len(route)):  # insert before route[pos]
                new_route = route[:pos] + [u] + route[pos:]

                # hard-feasibility check (time/cap)
                rm = evaluate_route(new_route, self.instance)
                if not rm["feasible"]:
                    continue

                features = self._build_construction_features(route, new_route, u, pos, rm)
                score = self._score_construction(features)

                tup = (score, u, r_idx, pos, features)
                if best is None or tup[0] < best[0]:
                    best = tup

        return best

    def _score_construction(self, features: Dict[str, float]) -> float:
        """
        Evaluate construction AST score. Lower is better.
        If no AST provided, fallback to classic: delta_distance + big*urgency
        """
        if self.construction_ast is None:
            return features["delta_distance"] + 0.01 * features["urgency"]

        val = eval_ast_json(self.construction_ast, features)
        return float(val)

    def _build_construction_features(
        self,
        old_route: List[int],
        new_route: List[int],
        u: int,
        insert_pos: int,
        new_route_metrics: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Feature set for insertion scoring (minimal, robust).
        You can extend later to Savelsbergh slacks etc.
        """
        dist = self.instance["distance_matrix"]
        nodes = self.instance["nodes"]
        Q = self.instance["capacity"]

        old_m = evaluate_route(old_route, self.instance)
        delta_distance = new_route_metrics["distance"] - old_m["distance"]

        # compute load of new route
        load = 0
        for node_idx in new_route:
            if node_idx != 0:
                load += nodes[node_idx]["demand"]
        cap_rem = Q - load
        load_ratio = load / Q if Q > 0 else 0.0

        # urgency: due_date - ready_time (smaller windows are more urgent)
        w = nodes[u]["due_date"] - nodes[u]["ready_time"]
        urgency = 1.0 / max(1.0, float(w))

        # position bias: earlier insertions may be safer in tight TW
        pos_ratio = insert_pos / max(1, (len(new_route) - 1))

        # distance to depot
        dist_depot = dist[0][u]

        return {
            "delta_distance": float(delta_distance),
            "route_capacity_remaining": float(cap_rem),
            "route_load_ratio": float(load_ratio),
            "urgency": float(urgency),
            "insert_pos_ratio": float(pos_ratio),
            "dist_depot": float(dist_depot),

            # should be zero here due to feasibility filter, but kept for safety
            "time_violation": float(new_route_metrics["time_violation"]),
            "capacity_violation": float(new_route_metrics["capacity_violation"]),
        }

    # =========================================================
    # LOCAL SEARCH PHASE
    # =========================================================

    def _local_search(self, sol: Dict[str, Any]) -> Dict[str, Any]:
        """
        Iterative improvement:
        - choose operator via LS AST (or random fallback)
        - apply best-improving move (first improvement for speed)
        - stop on max iters or stagnation
        """
        best = sol
        best_ev = evaluate_solution_full(best, self.instance, self.penalty_cfg, self.fitness_cfg)
        best_fit = best_ev["fitness"]

        no_improve = 0

        for it in range(self.max_ls_iters):
            if no_improve >= self.max_no_improve:
                break

            op = self._select_ls_operator(best, it, no_improve, best_ev)
            if op not in self.allowed_ops:
                op = self.rng.choice(sorted(list(self.allowed_ops)))

            neighbor = self._apply_operator_first_improvement(best, op)
            if neighbor is None:
                no_improve += 1
                continue

            nev = evaluate_solution_full(neighbor, self.instance, self.penalty_cfg, self.fitness_cfg)
            nfit = nev["fitness"]

            if nfit > best_fit:
                best, best_ev, best_fit = neighbor, nev, nfit
                no_improve = 0
            else:
                no_improve += 1

        return best

    def _select_ls_operator(self, sol: Dict[str, Any], it: int, no_improve: int, ev: Dict[str, Any]) -> str:
        """
        LS operator selector via AST. Must return a string operator.
        Fallback: random among allowed operators.
        """
        if self.ls_operator_ast is None:
            return self.rng.choice(sorted(list(self.allowed_ops)))

        features = self._build_ls_features(sol, it, no_improve, ev)
        val = eval_ast_json(self.ls_operator_ast, features)

        # if AST returns non-string -> fallback
        if not isinstance(val, str):
            return self.rng.choice(sorted(list(self.allowed_ops)))

        return val

    def _build_ls_features(self, sol: Dict[str, Any], it: int, no_improve: int, ev: Dict[str, Any]) -> Dict[str, float]:
        """
        Minimal LS state features (extend later).
        """
        metrics = ev["metrics"]
        num_routes = float(metrics["num_vehicles"])
        total_distance = float(metrics["total_distance"])
        penalty = float(ev["penalty"])

        # rough indicators of “tightness”
        min_slack = self._min_route_slack_proxy(sol)

        return {
            "ls_iteration": float(it),
            "iterations_no_improve": float(no_improve),
            "num_routes": num_routes,
            "total_distance": total_distance,
            "penalty_value": penalty,
            "min_route_slack": float(min_slack),
        }

    def _min_route_slack_proxy(self, sol: Dict[str, Any]) -> float:
        """
        Proxy slack: for each route compute total time window lateness margin at visits (approx).
        This is NOT Savelsbergh slack; it’s a cheap indicator.
        """
        nodes = self.instance["nodes"]
        dist = self.instance["distance_matrix"]
        min_margin = float("inf")

        for route in sol["routes"]:
            t = 0.0
            for i in range(len(route) - 1):
                u = route[i]
                v = route[i + 1]
                t += dist[u][v]
                if u != 0:
                    t += nodes[u]["service_time"]
                if t < nodes[v]["ready_time"]:
                    t = nodes[v]["ready_time"]
                margin = nodes[v]["due_date"] - t
                min_margin = min(min_margin, margin)

        if min_margin == float("inf"):
            return 0.0
        return min_margin

    # --------------------------------------------------------
    # Apply neighborhood operators
    # --------------------------------------------------------

    def _apply_operator_first_improvement(self, sol: Dict[str, Any], op: str) -> Optional[Dict[str, Any]]:
        """
        Tries to find first improving neighbor (fitness-based).
        """
        base_ev = evaluate_solution_full(sol, self.instance, self.penalty_cfg, self.fitness_cfg)
        base_fit = base_ev["fitness"]

        routes = sol["routes"]

        if op == "relocate":
            for r1 in range(len(routes)):
                for r2 in range(len(routes)):
                    for i in range(1, len(routes[r1]) - 1):
                        node = routes[r1][i]
                        for j in range(1, len(routes[r2])):
                            if r1 == r2 and (j == i or j == i + 1):
                                continue
                            cand = self._relocate(sol, r1, i, r2, j)
                            if cand is None:
                                continue
                            ev = evaluate_solution_full(cand, self.instance, self.penalty_cfg, self.fitness_cfg)
                            if ev["fitness"] > base_fit:
                                return cand
            return None

        if op == "swap":
            for r1 in range(len(routes)):
                for r2 in range(r1, len(routes)):
                    for i in range(1, len(routes[r1]) - 1):
                        for j in range(1, len(routes[r2]) - 1):
                            if r1 == r2 and i == j:
                                continue
                            cand = self._swap(sol, r1, i, r2, j)
                            if cand is None:
                                continue
                            ev = evaluate_solution_full(cand, self.instance, self.penalty_cfg, self.fitness_cfg)
                            if ev["fitness"] > base_fit:
                                return cand
            return None

        if op == "two_opt":
            for r in range(len(routes)):
                cand = self._two_opt_first_improvement(sol, r, base_fit)
                if cand is not None:
                    return cand
            return None

        if op == "or_opt":
            for r in range(len(routes)):
                cand = self._or_opt_first_improvement(sol, r, base_fit)
                if cand is not None:
                    return cand
            return None

        return None

    # =========================================================
    # Move implementations
    # =========================================================

    def _clean_empty_routes(self, routes: List[List[int]]) -> List[List[int]]:
        # remove routes like [0,0] or [0,x,0] keep
        out = []
        for r in routes:
            if len(r) <= 2:
                continue
            out.append(r)
        return out

    def _relocate(self, sol: Dict[str, Any], r1: int, i: int, r2: int, j: int) -> Optional[Dict[str, Any]]:
        routes = [rt[:] for rt in sol["routes"]]
        node = routes[r1].pop(i)
        routes[r2].insert(j, node)

        # hard feasibility quick check on affected routes only
        if not evaluate_route(routes[r1], self.instance)["feasible"]:
            return None
        if not evaluate_route(routes[r2], self.instance)["feasible"]:
            return None

        routes = self._clean_empty_routes(routes)
        return {"routes": routes}

    def _swap(self, sol: Dict[str, Any], r1: int, i: int, r2: int, j: int) -> Optional[Dict[str, Any]]:
        routes = [rt[:] for rt in sol["routes"]]
        routes[r1][i], routes[r2][j] = routes[r2][j], routes[r1][i]

        if not evaluate_route(routes[r1], self.instance)["feasible"]:
            return None
        if not evaluate_route(routes[r2], self.instance)["feasible"]:
            return None

        routes = self._clean_empty_routes(routes)
        return {"routes": routes}

    def _two_opt_first_improvement(self, sol: Dict[str, Any], r: int, base_fit: float) -> Optional[Dict[str, Any]]:
        routes = sol["routes"]
        route = routes[r]
        if len(route) <= 4:
            return None

        for i in range(1, len(route) - 2):
            for k in range(i + 1, len(route) - 1):
                new_route = route[:i] + list(reversed(route[i:k+1])) + route[k+1:]

                if not evaluate_route(new_route, self.instance)["feasible"]:
                    continue

                new_routes = [rt[:] for rt in routes]
                new_routes[r] = new_route
                cand = {"routes": new_routes}

                ev = evaluate_solution_full(cand, self.instance, self.penalty_cfg, self.fitness_cfg)
                if ev["fitness"] > base_fit:
                    return cand

        return None

    def _or_opt_first_improvement(self, sol: Dict[str, Any], r: int, base_fit: float) -> Optional[Dict[str, Any]]:
        """
        Or-opt: move chain of length 1..3 within same route.
        """
        routes = sol["routes"]
        route = routes[r]
        if len(route) <= 4:
            return None

        max_k = 3
        for k in range(1, max_k + 1):
            for i in range(1, len(route) - 1 - k):
                segment = route[i:i+k]
                remaining = route[:i] + route[i+k:]

                for j in range(1, len(remaining) - 1):
                    if j == i:
                        continue
                    new_route = remaining[:j] + segment + remaining[j:]

                    if not evaluate_route(new_route, self.instance)["feasible"]:
                        continue

                    new_routes = [rt[:] for rt in routes]
                    new_routes[r] = new_route
                    cand = {"routes": new_routes}

                    ev = evaluate_solution_full(cand, self.instance, self.penalty_cfg, self.fitness_cfg)
                    if ev["fitness"] > base_fit:
                        return cand

        return None
