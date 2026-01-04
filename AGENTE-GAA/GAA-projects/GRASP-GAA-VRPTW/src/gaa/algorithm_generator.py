"""
============================================================
Algorithm Generator (GAA)
GRASP + VRPTW (Solomon)
============================================================

Responsibilities:
- Generate N candidate algorithms (ASTs)
- Validate them strictly
- Retry generation if invalid
- Export valid algorithms as JSON
- Log generation metadata for reproducibility
"""

from __future__ import annotations

import json
import uuid
import random
from typing import List, Dict, Any

from ast.generator import ASTGenerator
from ast.validator import ASTValidator, ASTValidationConfig


# ============================================================
# Algorithm Descriptor (JSON-level)
# ============================================================

def build_algorithm_descriptor(
    ast_json: Dict[str, Any],
    phase: str,
    seed: int,
    attempt: int
) -> Dict[str, Any]:
    """
    Wrap AST JSON with metadata.
    """
    return {
        "algorithm_id": str(uuid.uuid4()),
        "phase": phase,
        "seed": seed,
        "generation_attempt": attempt,
        "ast": ast_json
    }


# ============================================================
# Algorithm Generator
# ============================================================

class AlgorithmGenerator:
    """
    High-level wrapper for generating valid algorithms (ASTs).
    """

    def __init__(
        self,
        rng_seed: int,
        ast_generator: ASTGenerator,
        ast_validator: ASTValidator,
        max_attempts_per_algorithm: int = 50
    ):
        self.rng = random.Random(rng_seed)
        self.ast_generator = ast_generator
        self.ast_validator = ast_validator
        self.max_attempts = max_attempts_per_algorithm

    # --------------------------------------------------------
    # Public API
    # --------------------------------------------------------

    def generate_algorithms(
        self,
        n_algorithms: int,
        phase: str,
        export_path: str
    ) -> List[Dict[str, Any]]:
        """
        Generate N valid algorithms and export them to JSON.

        phase: "construction" or "local_search"
        """
        assert phase in {"construction", "local_search"}

        algorithms: List[Dict[str, Any]] = []
        generation_log: List[Dict[str, Any]] = []

        for idx in range(n_algorithms):
            algo_json, meta = self._generate_single(idx, phase)
            algorithms.append(algo_json)
            generation_log.append(meta)

        # Export algorithms
        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(algorithms, f, indent=2)

        # Export generation log (same path + .log.json)
        with open(export_path.replace(".json", ".log.json"), "w", encoding="utf-8") as f:
            json.dump(generation_log, f, indent=2)

        return algorithms

    # --------------------------------------------------------
    # Internal: generate one algorithm with retries
    # --------------------------------------------------------

    def _generate_single(self, index: int, phase: str) -> (Dict[str, Any], Dict[str, Any]):
        """
        Generate one valid AST with retry logic.
        """
        attempt = 0
        validation_errors = []

        while attempt < self.max_attempts:
            attempt += 1

            # Generate candidate AST
            ast_json = self.ast_generator.generate(phase=phase)

            # Validate
            if phase == "construction":
                result = self.ast_validator.validate_construction_ast(ast_json)
            else:
                result = self.ast_validator.validate_ls_operator_ast(ast_json)

            if result.ok:
                descriptor = build_algorithm_descriptor(
                    ast_json=ast_json,
                    phase=phase,
                    seed=self.rng.seed,
                    attempt=attempt
                )

                meta = {
                    "algorithm_id": descriptor["algorithm_id"],
                    "phase": phase,
                    "index": index,
                    "valid": True,
                    "attempts_needed": attempt,
                    "stats": result.stats
                }

                return descriptor, meta

            validation_errors.append({
                "attempt": attempt,
                "errors": result.errors,
                "stats": result.stats
            })

        # ----------------------------------------------------
        # Hard failure
        # ----------------------------------------------------

        raise RuntimeError(
            f"Failed to generate valid algorithm after {self.max_attempts} attempts.\n"
            f"Last errors: {validation_errors[-1]}"
        )


# ============================================================
# Convenience factory
# ============================================================

def create_algorithm_generator(
    seed: int,
    construction_features: set,
    ls_features: set,
    allowed_ls_ops: set,
    max_depth: int,
    max_function_nodes: int
) -> AlgorithmGenerator:
    """
    One-stop factory to build a fully wired AlgorithmGenerator.
    """
    rng = random.Random(seed)

    ast_gen = ASTGenerator(
        rng=rng,
        max_depth=max_depth,
        max_function_nodes=max_function_nodes
    )

    cfg = ASTValidationConfig(
        max_depth=max_depth,
        max_function_nodes=max_function_nodes
    )

    ast_val = ASTValidator(
        config=cfg,
        construction_feature_names=construction_features,
        local_search_feature_names=ls_features,
        allowed_operator_values=allowed_ls_ops
    )

    return AlgorithmGenerator(
        rng_seed=seed,
        ast_generator=ast_gen,
        ast_validator=ast_val
    )
