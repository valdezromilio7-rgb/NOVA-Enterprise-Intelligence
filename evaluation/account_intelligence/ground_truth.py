"""Hidden labels for the Account Intelligence synthetic benchmark."""

from __future__ import annotations

EXPECTED_SIGNAL_IDS = frozenset(
    f"sig-fixture-{index:03d}" for index in range(5, 101, 5)
)
