import enum
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    JSON,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.session import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class SessionStatus(str, enum.Enum):
    ready = "ready"
    result_pending = "result_pending"
    completed = "completed"


class FinalStatus(str, enum.Enum):
    survived = "survived"
    deep_crisis = "deep_crisis"
    near_bankruptcy = "near_bankruptcy"
    bankrupt = "bankrupt"


class RoundStatus(str, enum.Enum):
    resolved = "resolved"



class StartupTemplate(Base):
    __tablename__ = "startup_templates"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    current_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )

    # Relationships
    versions: Mapped[List["StartupTemplateVersion"]] = relationship(
        "StartupTemplateVersion",
        back_populates="template",
        cascade="all, delete-orphan",
        order_by="StartupTemplateVersion.version",
    )


class StartupTemplateVersion(Base):
    __tablename__ = "startup_template_versions"

    template_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("startup_templates.id", ondelete="CASCADE"),
        primary_key=True,
    )
    version: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    industry: Mapped[str] = mapped_column(String(64), nullable=False)
    public_profile: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    private_profile: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    finance_config: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    asset_key: Mapped[str] = mapped_column(String(80), nullable=False)
    baseline_series: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, nullable=False)
    baseline_cash_m9_kopeks: Mapped[int] = mapped_column(BigInteger, nullable=False)
    content_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    engine_version: Mapped[str] = mapped_column(String(32), default="economy-v1", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )

    # Relationships
    template: Mapped["StartupTemplate"] = relationship(
        "StartupTemplate",
        back_populates="versions",
    )


class BrowserInstallation(Base):
    __tablename__ = "browser_installations"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )

    # Relationships
    session: Mapped[Optional["GameSession"]] = relationship(
        "GameSession",
        back_populates="browser_installation",
        uselist=False,
        cascade="all, delete-orphan",
    )


class GameSession(Base):
    __tablename__ = "game_sessions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    browser_installation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("browser_installations.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    startup_template_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    startup_version: Mapped[int] = mapped_column(Integer, nullable=False)
    nickname: Mapped[str] = mapped_column(String(24), nullable=False)
    status: Mapped[SessionStatus] = mapped_column(
        Enum(SessionStatus, name="session_status", native_enum=False),
        default=SessionStatus.ready,
        nullable=False,
        index=True,
    )
    next_round: Mapped[int] = mapped_column(
        SmallInteger,
        CheckConstraint("next_round >= 1 AND next_round <= 3", name="chk_session_next_round"),
        default=1,
        nullable=False,
    )
    elapsed_months: Mapped[int] = mapped_column(
        SmallInteger,
        CheckConstraint("elapsed_months >= 0 AND elapsed_months <= 9", name="chk_session_elapsed_months"),
        default=0,
        nullable=False,
    )
    template_snapshot: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    state: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    engine_version: Mapped[str] = mapped_column(String(32), default="economy-v1", nullable=False)
    attack_catalog_version: Mapped[str] = mapped_column(String(32), default="attack-choices-v1", nullable=False)
    attack_choices_snapshot: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    scoring_version: Mapped[str] = mapped_column(String(32), default="scoring-v1", nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    ranking_eligible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    final_status: Mapped[Optional[FinalStatus]] = mapped_column(
        Enum(FinalStatus, name="final_status", native_enum=False),
        nullable=True,
    )
    final_score: Mapped[Optional[int]] = mapped_column(
        SmallInteger,
        CheckConstraint("final_score >= 0 AND final_score <= 1000", name="chk_session_final_score"),
        nullable=True,
    )
    bankruptcy_month: Mapped[Optional[int]] = mapped_column(
        SmallInteger,
        CheckConstraint("bankruptcy_month >= 1 AND bankruptcy_month <= 9", name="chk_session_bankruptcy_month"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["startup_template_id", "startup_version"],
            ["startup_template_versions.template_id", "startup_template_versions.version"],
            name="fk_game_sessions_startup_template_version",
            ondelete="RESTRICT",
        ),
        Index("ix_game_sessions_leaderboard", "final_score", "completed_at"),
        Index("ix_game_sessions_status_score", "status", "final_score"),
    )

    # Relationships
    browser_installation: Mapped["BrowserInstallation"] = relationship(
        "BrowserInstallation",
        back_populates="session",
    )
    template_version: Mapped["StartupTemplateVersion"] = relationship(
        "StartupTemplateVersion",
        foreign_keys=[startup_template_id, startup_version],
        primaryjoin="and_(GameSession.startup_template_id == StartupTemplateVersion.template_id, GameSession.startup_version == StartupTemplateVersion.version)",
    )
    rounds: Mapped[List["GameRound"]] = relationship(
        "GameRound",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="GameRound.round_number",
    )
    ledgers: Mapped[List["MonthlyLedger"]] = relationship(
        "MonthlyLedger",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="MonthlyLedger.month_no",
    )


class GameRound(Base):
    __tablename__ = "game_rounds"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("game_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    round_number: Mapped[int] = mapped_column(
        SmallInteger,
        CheckConstraint("round_number >= 1 AND round_number <= 3", name="chk_round_number"),
        nullable=False,
    )
    idempotency_key: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    request_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    selected_choice_id: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    choice_snapshot: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    status: Mapped[RoundStatus] = mapped_column(
        Enum(RoundStatus, name="round_status", native_enum=False),
        default=RoundStatus.resolved,
        nullable=False,
    )
    outcome: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    event_title: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    event_narrative: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    defense_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    new_circumstance: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    resolved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        UniqueConstraint("session_id", "round_number", name="uq_game_rounds_session_round"),
        UniqueConstraint("session_id", "idempotency_key", name="uq_game_rounds_session_idempotency"),
    )

    # Relationships
    session: Mapped["GameSession"] = relationship(
        "GameSession",
        back_populates="rounds",
    )
    ledgers: Mapped[List["MonthlyLedger"]] = relationship(
        "MonthlyLedger",
        back_populates="round",
        cascade="all, delete-orphan",
        order_by="MonthlyLedger.month_no",
    )


class MonthlyLedger(Base):
    __tablename__ = "monthly_ledger"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("game_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    round_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("game_rounds.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    month_no: Mapped[int] = mapped_column(
        SmallInteger,
        CheckConstraint("month_no >= 1 AND month_no <= 9", name="chk_ledger_month_no"),
        nullable=False,
    )
    opening_cash_kopeks: Mapped[int] = mapped_column(BigInteger, nullable=False)
    revenue_by_stream: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    variable_cost_kopeks: Mapped[int] = mapped_column(BigInteger, nullable=False)
    fixed_cost_kopeks: Mapped[int] = mapped_column(BigInteger, nullable=False)
    incident_cost_kopeks: Mapped[int] = mapped_column(BigInteger, nullable=False)
    defense_cost_kopeks: Mapped[int] = mapped_column(BigInteger, nullable=False)
    closing_cash_kopeks: Mapped[int] = mapped_column(
        BigInteger,
        CheckConstraint("closing_cash_kopeks >= 0", name="chk_ledger_closing_cash_non_negative"),
        nullable=False,
    )
    unpaid_obligations_kopeks: Mapped[int] = mapped_column(
        BigInteger,
        CheckConstraint("unpaid_obligations_kopeks >= 0", name="chk_ledger_unpaid_obligations_non_negative"),
        default=0,
        nullable=False,
    )
    reputation_after: Mapped[int] = mapped_column(
        SmallInteger,
        CheckConstraint("reputation_after >= 0 AND reputation_after <= 100", name="chk_ledger_reputation"),
        nullable=False,
    )
    applied_effects: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )

    __table_args__ = (
        UniqueConstraint("session_id", "month_no", name="uq_monthly_ledger_session_month"),
    )

    # Relationships
    session: Mapped["GameSession"] = relationship(
        "GameSession",
        back_populates="ledgers",
    )
    round: Mapped["GameRound"] = relationship(
        "GameRound",
        back_populates="ledgers",
    )
