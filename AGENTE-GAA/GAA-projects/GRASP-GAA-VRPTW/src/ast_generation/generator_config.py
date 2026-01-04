"""
AST Generator Configuration & Defaults

Define:
- Feature pools for each phase
- Operator lists for local search
- Generation limits
"""

from typing import List, Tuple

# ============================================================
# Construction Phase Features (InsertionState)
# ============================================================

CONSTRUCTION_FEATURES: List[str] = [
    "route_length",               # Number of customers in current route
    "route_load",                 # Current load in route
    "route_capacity_remaining",   # Available capacity
    "route_current_time",         # Current time in route
    "cust_demand",                # Demand of customer to insert
    "cust_ready_time",            # Earliest time window
    "cust_due_time",              # Latest time window
    "delta_distance",             # Distance to insert
    "urgency",                    # Urgency [0,1]
    "utilization",                # Route utilization [0,1]
]

# ============================================================
# Local Search Phase Features (LSState)
# ============================================================

LOCAL_SEARCH_FEATURES: List[str] = [
    "num_routes",                 # Number of routes
    "total_distance",             # Total distance
    "penalty_value",              # Infeasibility penalty
    "iterations_no_improve",      # Iterations without improvement
    "temperature",                # Temperature [0,1]
    "acceptance_threshold",       # Acceptance threshold [0,1]
    "feasibility_score",          # Feasibility score [0,1]
]

# ============================================================
# Local Search Operators
# ============================================================

LOCAL_SEARCH_OPERATORS: List[str] = [
    "TwoOpt",
    "Relocate",
    "OrOpt",
    "CrossExchange",
]

# ============================================================
# Generation Limits
# ============================================================

class GenLimits:
    max_depth: int = 10
    max_function_nodes: int = 50
    max_total_nodes: int = 100
    const_float_range: Tuple[float, float] = (-5.0, 5.0)


# ============================================================
# State Contracts (FROZEN)
# ============================================================

CONSTRUCTION_STATE_CONTRACT = {
    "route_length": float,
    "route_load": float,
    "route_capacity_remaining": float,
    "route_current_time": float,
    "cust_demand": float,
    "cust_ready_time": float,
    "cust_due_time": float,
    "delta_distance": float,
    "urgency": float,
    "utilization": float,
}

LOCAL_SEARCH_STATE_CONTRACT = {
    "num_routes": float,
    "total_distance": float,
    "penalty_value": float,
    "iterations_no_improve": float,
    "temperature": float,
    "acceptance_threshold": float,
    "feasibility_score": float,
}
