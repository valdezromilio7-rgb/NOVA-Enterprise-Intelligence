"""Bounded build plan generated from a product specification."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
from factory.product_specification import ProductSpecification

@dataclass(frozen=True)
class BuildTask:
    id: str
    specification_id: str
    role: str
    objective: str
    deliverable: str
    dependencies: Sequence[str] = ()
    risk_level: str = "low"

@dataclass(frozen=True)
class BuildPlan:
    id: str
    specification_id: str
    tasks: Sequence[BuildTask]
    approval_required: bool = True

def create_build_plan(*, specification: ProductSpecification, tasks: Sequence[BuildTask]) -> BuildPlan:
    if not specification.id.strip(): raise ValueError("specification id required")
    if not tasks: raise ValueError("build plan requires at least one task")
    if any(t.specification_id != specification.id for t in tasks): raise ValueError("all tasks must reference the specification")
    return BuildPlan(id="build_"+specification.id.removeprefix("spec_"),specification_id=specification.id,tasks=tuple(tasks),approval_required=True)
