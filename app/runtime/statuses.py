ALL_MEMORY_ALLOWED_STATUSES = frozenset({"active", "needs_review", "inactive"})
ASSUMPTION_ALLOWED_STATUSES = frozenset({*ALL_MEMORY_ALLOWED_STATUSES, "invalid"})
RETRIEVABLE_STATUSES = frozenset({"active", "needs_review"})


def validate_memory_status(status: str | None, *, allow_invalid: bool = False) -> str:
    normalized = (status or "").strip()
    allowed = ASSUMPTION_ALLOWED_STATUSES if allow_invalid else ALL_MEMORY_ALLOWED_STATUSES
    if normalized not in allowed:
        allowed_display = ", ".join(sorted(allowed))
        raise ValueError(f"status must be one of: {allowed_display}")
    return normalized


def is_retrievable_status(status: str | None) -> bool:
    return (status or "").strip() in RETRIEVABLE_STATUSES


def status_rank_adjustment(status: str | None) -> int:
    normalized = (status or "").strip()
    if normalized == "needs_review":
        return -1
    return 0
