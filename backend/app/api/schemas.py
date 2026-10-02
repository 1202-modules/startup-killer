import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class BootstrapGameRules(BaseModel):
    max_rounds: int = 3
    months_per_round: int = 3
    one_attempt_per_browser: bool = True


class BootstrapFeatures(BaseModel):
    sound_default: bool = False


class BootstrapResponse(BaseModel):
    csrf_token: str
    existing_session_id: Optional[uuid.UUID] = None
    game_rules: BootstrapGameRules = Field(default_factory=BootstrapGameRules)
    features: BootstrapFeatures = Field(default_factory=BootstrapFeatures)


class SessionMeResponse(BaseModel):
    session_id: Optional[uuid.UUID] = None
    status: Optional[str] = None


class CreateSessionRequest(BaseModel):
    nickname: str


class StartupPublicProfile(BaseModel):
    id: str
    name: str
    tagline: str
    description: str
    public_facts: List[str]
    hero_asset: Optional[str] = None


class SessionStatePublic(BaseModel):
    cash_kopeks: int
    monthly_revenue_kopeks: int
    monthly_fixed_cost_kopeks: int
    variable_cost_bps: int
    reputation: int
    active_effects_public: List[str] = Field(default_factory=list)


class AttackChoicePublic(BaseModel):
    id: str
    round_number: int
    title: str
    short_description: str
    attack_narrative: str
    combo_available: bool = False


class CreateSessionResponse(BaseModel):
    session_id: uuid.UUID
    status: str
    next_round: int
    elapsed_months: int
    startup: StartupPublicProfile
    state: SessionStatePublic
    available_choices: List["AttackChoicePublic"] = Field(default_factory=list)
    current_round_id: Optional[uuid.UUID] = None
    can_attack: bool = True
    can_continue: bool = False
    completed: bool = False
    ranking_eligible: bool = True
    reused_existing_session: Optional[bool] = None


class RoundSummaryPublic(BaseModel):
    round_number: int
    event_title: Optional[str] = None
    defense_summary: Optional[str] = None
    new_circumstance: Optional[str] = None


class SessionDetailResponse(BaseModel):
    session_id: uuid.UUID
    status: str
    next_round: int
    elapsed_months: int
    startup: StartupPublicProfile
    state: SessionStatePublic
    rounds: List[RoundSummaryPublic] = Field(default_factory=list)
    current_round_id: Optional[uuid.UUID] = None
    available_choices: List["AttackChoicePublic"] = Field(default_factory=list)
    can_attack: bool
    can_continue: bool
    completed: bool
    ranking_eligible: bool = True


class AttackChoiceRequest(BaseModel):
    choice_id: str = Field(..., min_length=1, max_length=80)
    model_config = ConfigDict(extra="forbid")


class RoundEventPublic(BaseModel):
    title: str
    narrative: str
    scene_type: Optional[str] = None


class RoundDefensePublic(BaseModel):
    type: str
    summary: str
    company_response: Optional[str] = None
    cost_kopeks: int = 0
    reason: str = ""


class RoundDeltasPublic(BaseModel):
    cash_kopeks: int
    monthly_revenue_kopeks: int
    reputation: int


class SessionStateAfterPublic(BaseModel):
    cash_kopeks: int
    monthly_revenue_kopeks: int
    reputation: int


class RoundResultResponse(BaseModel):
    status: str
    round_id: Optional[uuid.UUID] = None
    selected_choice: Optional[AttackChoicePublic] = None
    round_number: Optional[int] = None
    months_simulated: Optional[List[int]] = None
    event: Optional[RoundEventPublic] = None
    defense: Optional[RoundDefensePublic] = None
    deltas: Optional[RoundDeltasPublic] = None
    state_after: Optional[SessionStateAfterPublic] = None
    new_circumstance: Optional[str] = None
    game_completed: Optional[bool] = None
    next_action: Optional[str] = None
    impact: Optional[dict] = None


class ContinueRequest(BaseModel):
    resolved_round_id: uuid.UUID


class ContinueResponse(BaseModel):
    session_id: uuid.UUID
    status: str
    next_round: int


class ResultStartupPublic(BaseModel):
    id: str
    name: str


class ResultFinalMetrics(BaseModel):
    cash_kopeks: int
    runway_months: Optional[float] = None


class ResultScoreBreakdown(BaseModel):
    damage: int
    solvency: int
    bankruptcy_bonus: int = 0


class ResultRoundSummary(BaseModel):
    round_number: int
    event_title: Optional[str] = None


class GameResultResponse(BaseModel):
    session_id: uuid.UUID
    startup_name: Optional[str] = None
    nickname: Optional[str] = None
    final_status: str
    score: int
    final_score: Optional[int] = None
    rank: Optional[int] = None
    total_ranked: Optional[int] = None
    total_cash_kopeks: Optional[int] = None
    baseline_cash_m9_kopeks: Optional[int] = None
    startup: ResultStartupPublic
    final_metrics: ResultFinalMetrics
    score_breakdown: ResultScoreBreakdown
    score_details: Optional[ResultScoreBreakdown] = None
    rounds: List[ResultRoundSummary] = Field(default_factory=list)
    summary: str
    ranking_eligible: bool = True


class LeaderboardEntry(BaseModel):
    rank: int
    nickname: str
    startup_name: str
    score: int
    final_score: Optional[int] = None
    final_status: str
    completed_at: datetime
    is_me: bool = False

    model_config = ConfigDict(from_attributes=True)


class LeaderboardResponse(BaseModel):
    total: int
    items: List[LeaderboardEntry]
    my_entry: Optional[LeaderboardEntry] = None


class ErrorDetail(BaseModel):
    code: str
    message: str
    retryable: bool = False
    details: Dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    error: ErrorDetail
    request_id: str
