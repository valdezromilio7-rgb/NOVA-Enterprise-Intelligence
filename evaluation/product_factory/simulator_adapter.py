"""Bridge deterministic simulator configuration into public discovery signals.

The adapter exposes only simulation metadata and observed benchmark signals. Hidden
truth remains evaluation-only and is never imported here.
"""

from dataclasses import replace
from typing import Tuple

from factory.schemas.domain import Signal
from simulator.config import SimulationConfig
from evaluation.product_factory.signals import BENCHMARK_SIGNALS


def load_simulation_signals(config: SimulationConfig | None = None) -> Tuple[Signal, ...]:
    """Return reproducible observed signals annotated with simulator provenance."""
    cfg = config or SimulationConfig()
    provenance_prefix = f"simulator:seed={cfg.seed}:start={cfg.start_date}:days={cfg.days}"
    return tuple(
        replace(
            signal,
            id=f"{signal.id}:seed-{cfg.seed}",
            provenance=f"{provenance_prefix}:{signal.provenance}",
            metadata={**signal.metadata, "simulation_seed": cfg.seed, "simulation_days": cfg.days},
        )
        for signal in BENCHMARK_SIGNALS
    )
