from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any


class Severity(str, Enum):
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"
    CRITICAL = "critical"


class Scale(str, Enum):
    LOCAL = "local"
    REGIONAL = "regional"
    COMPANY_WIDE = "company_wide"


class Feasibility(str, Enum):
    UNSUPPORTED = "unsupported"
    PLAUSIBLE = "plausible"
    ESTABLISHED_IN_STATE = "established_in_state"


class WeaknessMatch(str, Enum):
    INDIRECT = "indirect"
    NORMAL = "normal"
    EXACT = "exact"


class Duration(str, Enum):
    TEMPORARY = "temporary"
    PERSISTENT = "persistent"
    STRUCTURAL = "structural"


class AttackType(str, Enum):
    COMPETITION = "competition"
    PRODUCT = "product"
    DEMAND = "demand"
    SUPPLY = "supply"
    TECHNOLOGY = "technology"
    REPUTATION = "reputation"
    COST = "cost"
    FINANCE = "finance"
    ABSURD = "absurd"


class DefenseType(str, Enum):
    NONE = "none"
    COST_CUT = "cost_cut"
    PR = "pr"
    SUPPLIER_SWITCH = "supplier_switch"
    PIVOT = "pivot"
    INDEPENDENT_AUDIT = "independent_audit"
    SECOND_FACTORY = "second_factory"
    RETENTION_OFFER = "retention_offer"
    CAMPUS_REDEPLOY = "campus_redeploy"
    SERVICE_RESERVE = "service_reserve"
    LOYALTY_PROGRAM = "loyalty_program"
    SLA_GUARANTEE = "sla_guarantee"
    ROUTE_REBUILD = "route_rebuild"
    BATTERY_RESERVE = "battery_reserve"
    RESTAURANT_RETENTION = "restaurant_retention"
    PARTNER_SERVICE = "partner_service"
    QUALITY_AUDIT = "quality_audit"
    BACKUP_PROVIDER = "backup_provider"
    STUDENT_RETENTION = "student_retention"
    SCHOOL_SUCCESS_TEAM = "school_success_team"
    FLEXIBLE_LEASE = "flexible_lease"
    COMPACT_REDEPLOY = "compact_redeploy"
    DIGITAL_WELLNESS = "digital_wellness"
    PRICE_RETENTION = "price_retention"
    FINANCING_TRADEIN = "financing_tradein"
    BUNDLED_SUBSCRIPTION = "bundled_subscription"
    MOBILE_MODE = "mobile_mode"
    RETAIL_BUYBACK = "retail_buyback"
    DIRECT_CHANNEL = "direct_channel"
    SECOND_SUPPLIER = "second_supplier"
    UNIQUE_MENU_LOYALTY = "unique_menu_loyalty"
    CORPORATE_RETENTION = "corporate_retention"
    SEASONAL_LEASING = "seasonal_leasing"
    COMPONENT_RESERVE = "component_reserve"
    DRONE_AS_A_SERVICE = "drone_as_a_service"
    DEALER_SUBSIDY = "dealer_subsidy"
    PRIVACY_SAFE_MODE = "privacy_safe_mode"
    ALTERNATIVE_DATA = "alternative_data"
    CONTEXTUAL_MODE = "contextual_mode"
    ANALYTICS_BUNDLE = "analytics_bundle"
    REPAIR_RESERVE = "repair_reserve"
    TRANSPARENT_INSURANCE = "transparent_insurance"
    LOWER_DEPOSIT = "lower_deposit"
    PARTNER_COMMISSION_CUT = "partner_commission_cut"


class SceneType(str, Enum):
    DEMAND = "demand"
    REPUTATION = "reputation"
    COMPETITION = "competition"
    SUPPLY = "supply"
    TECHNOLOGY = "technology"
    FINANCE = "finance"
    PIVOT = "pivot"
    ABSURD = "absurd"


class FinalStatus(str, Enum):
    BANKRUPT = "bankrupt"
    NEAR_BANKRUPTCY = "near_bankruptcy"
    DEEP_CRISIS = "deep_crisis"
    SURVIVED = "survived"


@dataclass(frozen=True)
class RevenueStreamConfig:
    id: str
    name: str
    initial_monthly_revenue_kopeks: int
    variable_cost_bps: int
    monthly_growth_bps: int
    weight_bps: int


@dataclass(frozen=True)
class BaselineMonth:
    month: int
    closing_cash_kopeks: int
    revenue_kopeks: int = 0
    variable_cost_kopeks: int = 0
    profit_kopeks: int = 0


@dataclass(frozen=True)
class FactItem:
    id: str
    text: str


@dataclass(frozen=True)
class PublicProfile:
    tagline: str
    description: str
    facts: List[FactItem]
    strengths: List[str]


@dataclass(frozen=True)
class WeaknessItem:
    id: str
    description: str
    attack_type: str


@dataclass(frozen=True)
class PrivateProfile:
    weaknesses: List[WeaknessItem]
    allowed_defenses: List[DefenseType]
    pivot_compatible: bool
    production_partner_alternative: bool


@dataclass(frozen=True)
class FinanceConfig:
    initial_cash_kopeks: int
    initial_fixed_cost_kopeks: int
    initial_reputation: int
    revenue_streams: List[RevenueStreamConfig]


@dataclass(frozen=True)
class StartupTemplate:
    slug: str
    version: int
    name: str
    industry: str
    asset_key: str
    engine_version: str
    finance_config: FinanceConfig
    public_profile: PublicProfile
    private_profile: PrivateProfile
    baseline_series: List[BaselineMonth]
    baseline_cash_m9_kopeks: int

    @property
    def initial_cash_kopeks(self) -> int:
        return self.finance_config.initial_cash_kopeks

    @property
    def initial_fixed_cost_kopeks(self) -> int:
        return self.finance_config.initial_fixed_cost_kopeks

    @property
    def initial_reputation(self) -> int:
        return self.finance_config.initial_reputation

    @property
    def revenue_streams(self) -> List[RevenueStreamConfig]:
        return self.finance_config.revenue_streams


@dataclass
class ActiveEffect:
    stack_group: str
    target_stream_id: str
    magnitude_bps: int
    duration_type: Duration
    months_remaining: int
    decay_bps: int
    source_round: int
    origin_attack_type: AttackType


@dataclass(frozen=True)
class StreamLedgerRow:
    id: str
    baseline_revenue_kopeks: int
    shock_bps: int
    revenue_kopeks: int
    variable_cost_kopeks: int


@dataclass(frozen=True)
class MonthlyLedgerRow:
    month: int
    streams: List[StreamLedgerRow]
    revenue_kopeks: int
    variable_cost_kopeks: int
    fixed_cost_kopeks: int
    profit_kopeks: int
    closing_cash_kopeks: int
    unpaid_obligations_kopeks: int
    incident_cost_kopeks: int = 0
    defense_cost_kopeks: int = 0


@dataclass
class DefenseDecision:
    defense_type: DefenseType
    cost_kopeks: int
    effective_from_month: int
    detail: str
    reason: str = ""


@dataclass
class FinalScore:
    damage: float
    solvency: float
    early_bankruptcy: float
    score: int
    final_status: FinalStatus


@dataclass
class ActiveDefenseModifier:
    defense_type: DefenseType
    activated_round: int
    activated_month: int
    target_stream_id: Optional[str] = None


@dataclass
class GameState:
    session_id: str
    template_slug: str
    round_number: int
    elapsed_months: int
    cash_kopeks: int
    fixed_cost_kopeks: int
    reputation: int
    active_effects: List[ActiveEffect] = field(default_factory=list)
    used_defenses: List[DefenseType] = field(default_factory=list)
    active_defense_modifiers: List[ActiveDefenseModifier] = field(default_factory=list)
    is_bankrupt: bool = False
    bankruptcy_month: Optional[int] = None
    unpaid_obligations_kopeks: int = 0
    score_breakdown: Optional[FinalScore] = None
    v2_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidatedAttack:
    attack_type: AttackType
    target_stream_ids: List[str]
    scale: Scale
    feasibility: Feasibility
    severity: Severity
    duration: Duration
    evidence_fact_ids: List[str]
    weakness_match: WeaknessMatch = WeaknessMatch.NORMAL
    defense_hint: DefenseType = DefenseType.NONE
    scene_type: SceneType = SceneType.DEMAND
    intent: str = ""
    adapted_event: str = ""
    headline: str = ""
    narrative: str = ""
    v2_effect: Optional[Dict[str, Any]] = None


@dataclass
class EngineOutcome:
    round_number: int
    months_simulated: int
    monthly_ledger: List[MonthlyLedgerRow]
    state_after: GameState
    cash_delta_kopeks: int
    revenue_delta_kopeks: int
    reputation_delta: int
    defense: DefenseDecision
    new_circumstance: Optional[str] = None
    final_status: Optional[FinalStatus] = None
    score_breakdown: Optional[FinalScore] = None
    engine_version: str = "v1.0"
    details: Dict[str, Any] = field(default_factory=dict)
    audit: Dict[str, Any] = field(default_factory=dict)
