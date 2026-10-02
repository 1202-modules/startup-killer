import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Dict, List

from backend.app.engine.types import (
    StartupTemplate,
    RevenueStreamConfig,
    FinanceConfig,
    BaselineMonth,
    PublicProfile,
    PrivateProfile,
    FactItem,
    WeaknessItem,
    DefenseType,
)


def quantize_kopeks(val: Decimal) -> int:
    return int(val.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def calculate_startup_baseline(
    initial_cash_kopeks: int,
    initial_fixed_cost_kopeks: int,
    revenue_streams: List[RevenueStreamConfig],
) -> List[BaselineMonth]:
    months: List[BaselineMonth] = []
    
    # Month 0: Initial state before game starts
    months.append(
        BaselineMonth(
            month=0,
            closing_cash_kopeks=initial_cash_kopeks,
            revenue_kopeks=0,
            variable_cost_kopeks=0,
            profit_kopeks=0,
        )
    )
    
    current_cash = initial_cash_kopeks
    for m in range(1, 10):
        month_revenue = 0
        month_variable_cost = 0
        for stream in revenue_streams:
            growth_mult = (
                Decimal(1) + Decimal(stream.monthly_growth_bps) / Decimal(10000)
            ) ** (m - 1)
            stream_rev = quantize_kopeks(
                Decimal(stream.initial_monthly_revenue_kopeks) * growth_mult
            )
            stream_var = quantize_kopeks(
                Decimal(stream_rev) * Decimal(stream.variable_cost_bps) / Decimal(10000)
            )
            month_revenue += stream_rev
            month_variable_cost += stream_var
            
        profit = month_revenue - month_variable_cost - initial_fixed_cost_kopeks
        current_cash += profit
        
        months.append(
            BaselineMonth(
                month=m,
                revenue_kopeks=month_revenue,
                variable_cost_kopeks=month_variable_cost,
                profit_kopeks=profit,
                closing_cash_kopeks=current_cash,
            )
        )
        
    return months


def load_startups(path: Path) -> Dict[str, StartupTemplate]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    startups_list = data.get("startups", [])
    result: Dict[str, StartupTemplate] = {}
    
    for item in startups_list:
        slug = item["slug"]
        
        streams = [
            RevenueStreamConfig(
                id=s["id"],
                name=s["name"],
                initial_monthly_revenue_kopeks=s["initial_monthly_revenue_kopeks"],
                variable_cost_bps=s["variable_cost_bps"],
                monthly_growth_bps=s["monthly_growth_bps"],
                weight_bps=s["weight_bps"],
            )
            for s in item["finance_config"]["revenue_streams"]
        ]
        
        finance_config = FinanceConfig(
            initial_cash_kopeks=item["finance_config"]["initial_cash_kopeks"],
            initial_fixed_cost_kopeks=item["finance_config"]["initial_fixed_cost_kopeks"],
            initial_reputation=item["finance_config"]["initial_reputation"],
            revenue_streams=streams,
        )
        
        public_facts = [
            FactItem(id=fact["id"], text=fact["text"])
            for fact in item["public_profile"]["facts"]
        ]
        
        public_profile = PublicProfile(
            tagline=item["public_profile"]["tagline"],
            description=item["public_profile"]["description"],
            facts=public_facts,
            strengths=list(item["public_profile"]["strengths"]),
        )
        
        weaknesses = [
            WeaknessItem(
                id=w["id"],
                description=w["description"],
                attack_type=w["attack_type"],
            )
            for w in item["private_profile"]["weaknesses"]
        ]
        
        allowed_defenses = [
            DefenseType(d) for d in item["private_profile"]["allowed_defenses"]
        ]
        
        private_profile = PrivateProfile(
            weaknesses=weaknesses,
            allowed_defenses=allowed_defenses,
            pivot_compatible=item["private_profile"]["pivot_compatible"],
            production_partner_alternative=item["private_profile"]["production_partner_alternative"],
        )
        
        calculated_baseline = calculate_startup_baseline(
            initial_cash_kopeks=finance_config.initial_cash_kopeks,
            initial_fixed_cost_kopeks=finance_config.initial_fixed_cost_kopeks,
            revenue_streams=streams,
        )
        
        # Verify against stored baseline_series in JSON
        for m_idx, stored_m in enumerate(item["baseline_series"]):
            calc_m = calculated_baseline[m_idx]
            assert calc_m.month == stored_m["month"], f"Month mismatch {slug} month {m_idx}"
            assert calc_m.closing_cash_kopeks == stored_m["closing_cash_kopeks"], f"Cash mismatch {slug} month {m_idx}"
            if m_idx > 0:
                assert calc_m.revenue_kopeks == stored_m["revenue_kopeks"], f"Revenue mismatch {slug} month {m_idx}"
                assert calc_m.variable_cost_kopeks == stored_m["variable_cost_kopeks"], f"Var cost mismatch {slug} month {m_idx}"
                assert calc_m.profit_kopeks == stored_m["profit_kopeks"], f"Profit mismatch {slug} month {m_idx}"
            
        assert calculated_baseline[9].closing_cash_kopeks == item["baseline_cash_m9_kopeks"]
        
        template = StartupTemplate(
            slug=slug,
            version=item["version"],
            name=item["name"],
            industry=item["industry"],
            asset_key=item["asset_key"],
            engine_version=item["engine_version"],
            finance_config=finance_config,
            public_profile=public_profile,
            private_profile=private_profile,
            baseline_series=calculated_baseline,
            baseline_cash_m9_kopeks=item["baseline_cash_m9_kopeks"],
        )
        result[slug] = template
        
    return result


def build_startup_template_from_version(version_obj: Any, slug: str) -> StartupTemplate:
    """Builds a typed StartupTemplate dataclass from a StartupTemplateVersion DB model or dict."""
    finance_raw = getattr(version_obj, "finance_config", version_obj.get("finance_config") if isinstance(version_obj, dict) else {})
    public_raw = getattr(version_obj, "public_profile", version_obj.get("public_profile") if isinstance(version_obj, dict) else {})
    private_raw = getattr(version_obj, "private_profile", version_obj.get("private_profile") if isinstance(version_obj, dict) else {})
    
    streams = [
        RevenueStreamConfig(
            id=s["id"],
            name=s["name"],
            initial_monthly_revenue_kopeks=s["initial_monthly_revenue_kopeks"],
            variable_cost_bps=s["variable_cost_bps"],
            monthly_growth_bps=s["monthly_growth_bps"],
            weight_bps=s["weight_bps"],
        )
        for s in finance_raw.get("revenue_streams", [])
    ]
    finance_config = FinanceConfig(
        initial_cash_kopeks=finance_raw["initial_cash_kopeks"],
        initial_fixed_cost_kopeks=finance_raw["initial_fixed_cost_kopeks"],
        initial_reputation=finance_raw["initial_reputation"],
        revenue_streams=streams,
    )
    public_facts = [
        FactItem(id=f["id"], text=f["text"])
        for f in public_raw.get("facts", [])
    ]
    public_profile = PublicProfile(
        tagline=public_raw.get("tagline", ""),
        description=public_raw.get("description", ""),
        facts=public_facts,
        strengths=list(public_raw.get("strengths", [])),
    )
    weaknesses = [
        WeaknessItem(
            id=w["id"],
            description=w["description"],
            attack_type=w["attack_type"],
        )
        for w in private_raw.get("weaknesses", [])
    ]
    allowed_defenses = [
        DefenseType(d) for d in private_raw.get("allowed_defenses", [])
    ]
    private_profile = PrivateProfile(
        weaknesses=weaknesses,
        allowed_defenses=allowed_defenses,
        pivot_compatible=private_raw.get("pivot_compatible", False),
        production_partner_alternative=private_raw.get("production_partner_alternative", False),
    )
    calculated_baseline = calculate_startup_baseline(
        initial_cash_kopeks=finance_config.initial_cash_kopeks,
        initial_fixed_cost_kopeks=finance_config.initial_fixed_cost_kopeks,
        revenue_streams=streams,
    )
    
    ver_num = getattr(version_obj, "version", version_obj.get("version", 1) if isinstance(version_obj, dict) else 1)
    name = getattr(version_obj, "name", version_obj.get("name", slug) if isinstance(version_obj, dict) else slug)
    industry = getattr(version_obj, "industry", version_obj.get("industry", "") if isinstance(version_obj, dict) else "")
    asset_key = getattr(version_obj, "asset_key", version_obj.get("asset_key", slug) if isinstance(version_obj, dict) else slug)
    engine_ver = getattr(version_obj, "engine_version", version_obj.get("engine_version", "v1.0") if isinstance(version_obj, dict) else "v1.0")
    m9_cash = getattr(version_obj, "baseline_cash_m9_kopeks", version_obj.get("baseline_cash_m9_kopeks", calculated_baseline[9].closing_cash_kopeks) if isinstance(version_obj, dict) else calculated_baseline[9].closing_cash_kopeks)

    return StartupTemplate(
        slug=slug,
        version=ver_num,
        name=name,
        industry=industry,
        asset_key=asset_key,
        engine_version=engine_ver,
        finance_config=finance_config,
        public_profile=public_profile,
        private_profile=private_profile,
        baseline_series=calculated_baseline,
        baseline_cash_m9_kopeks=m9_cash,
    )

