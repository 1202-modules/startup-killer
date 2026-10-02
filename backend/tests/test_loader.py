from pathlib import Path
import pytest
from backend.app.engine.loader import load_startups
from backend.app.engine.types import StartupTemplate

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

def test_load_startups_returns_ten_valid_templates():
    startups = load_startups(DATA_DIR / "startups.json")
    assert len(startups) == 10
    assert "coffeebot" in startups
    assert "petmind" in startups
    
    for slug, template in startups.items():
        assert isinstance(template, StartupTemplate)
        assert template.slug == slug
        assert len(template.revenue_streams) == 2
        assert sum(s.weight_bps for s in template.revenue_streams) == 10000
        assert template.initial_cash_kopeks > 0
        assert template.initial_fixed_cost_kopeks > 0
        assert len(template.baseline_series) == 10
        assert template.baseline_cash_m9_kopeks > 0
        assert template.baseline_series[9].closing_cash_kopeks == template.baseline_cash_m9_kopeks
