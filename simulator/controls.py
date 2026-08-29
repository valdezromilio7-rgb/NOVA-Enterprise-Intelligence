class IntegrityError(Exception):
    """Raised when a simulation invariant does not reconcile."""


def require_equal(expected: int, actual: int, label: str) -> None:
    if expected != actual:
        raise IntegrityError(f"{label}: expected {expected}, got {actual}")


def require_non_negative(value: int, label: str) -> None:
    if value < 0:
        raise IntegrityError(f"{label}: negative value {value}")
