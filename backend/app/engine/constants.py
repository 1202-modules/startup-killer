from backend.app.engine.types import (
    Severity,
    Scale,
    Feasibility,
    WeaknessMatch,
    Duration,
    DefenseType,
)

BPS_DENOMINATOR = 10000

SEVERITY_BPS = {
    Severity.WEAK: 1200,
    Severity.MEDIUM: 3000,
    Severity.STRONG: 5500,
    Severity.CRITICAL: 8000,
}

SCALE_BPS = {
    Scale.LOCAL: 4000,
    Scale.REGIONAL: 6500,
    Scale.COMPANY_WIDE: 10000,
}

FEASIBILITY_BPS = {
    Feasibility.UNSUPPORTED: 5000,
    Feasibility.PLAUSIBLE: 8000,
    Feasibility.ESTABLISHED_IN_STATE: 10000,
}

WEAKNESS_MATCH_BPS = {
    WeaknessMatch.INDIRECT: 8000,
    WeaknessMatch.NORMAL: 10000,
    WeaknessMatch.EXACT: 12500,
}

DECAY_BPS = {
    Duration.TEMPORARY: 6000,
    Duration.PERSISTENT: 8500,
    Duration.STRUCTURAL: 10000,
}

MAX_DURATION_MONTHS = {
    Duration.TEMPORARY: 3,
    Duration.PERSISTENT: 6,
    Duration.STRUCTURAL: 9,
}

INCIDENT_COST_BPS = {
    Severity.WEAK: 1500,
    Severity.MEDIUM: 3500,
    Severity.STRONG: 7000,
    Severity.CRITICAL: 12000,
}

REPUTATION_DELTAS = {
    Severity.WEAK: -3,
    Severity.MEDIUM: -8,
    Severity.STRONG: -15,
    Severity.CRITICAL: -24,
}

DEFENSE_COST_BPS = {
    DefenseType.NONE: 0,
    DefenseType.COST_CUT: 2500,
    DefenseType.PR: 2500,
    DefenseType.SUPPLIER_SWITCH: 4500,
    DefenseType.PIVOT: 7000,
}

DEFAULT_STREAM_CAP_BPS = 9500
