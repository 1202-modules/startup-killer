"""Exhaustively simulate all reachable catalog paths through the approved engine."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import resource
import statistics
import sys
import time
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.engine.attack_choices import (
    AttackCatalog,
    choices_for,
    load_attack_catalog,
    to_validated_attack,
    validate_attack_catalog,
)
from backend.app.engine.calculator import simulate_round
from backend.app.engine.loader import load_startups
from backend.app.engine.types import GameState, StartupTemplate


@dataclass(frozen=True)
class PathOutcome:
    startup_slug: str
    choice_ids: tuple[str, ...]
    final_status: str
    score: int
    elapsed_months: int
    final_cash_kopeks: int
    bankruptcy_month: int | None


def initial_state(startup: StartupTemplate) -> GameState:
    return GameState(
        session_id=f"balance:{startup.slug}", template_slug=startup.slug,
        round_number=1, elapsed_months=0,
        cash_kopeks=startup.initial_cash_kopeks,
        fixed_cost_kopeks=startup.initial_fixed_cost_kopeks,
        reputation=startup.initial_reputation,
    )


def enumerate_startup_paths(startup: StartupTemplate, catalog: AttackCatalog) -> list[PathOutcome]:
    """Return each terminal path once; bankrupt states do not branch further."""
    def walk(state: GameState, path: tuple[str, ...]) -> list[PathOutcome]:
        if state.is_bankrupt or state.elapsed_months >= 9:
            score = state.score_breakdown
            return [PathOutcome(
                startup_slug=startup.slug, choice_ids=path,
                final_status=score.final_status.value if score else "survived",
                score=score.score if score else 0,
                elapsed_months=state.elapsed_months,
                final_cash_kopeks=state.cash_kopeks,
                bankruptcy_month=state.bankruptcy_month,
            )]

        round_choices = choices_for(catalog, startup.slug, state.round_number)
        if not round_choices:
            raise ValueError(f"catalog has no choices for {startup.slug} round {state.round_number}")
        results: list[PathOutcome] = []
        for choice in round_choices:
            outcome = simulate_round(state, startup, to_validated_attack(choice, startup))
            results.extend(walk(outcome.state_after, path + (choice.id,)))
        return results

    return walk(initial_state(startup), ())


def enumerate_all_paths() -> tuple[dict[str, StartupTemplate], AttackCatalog, dict[str, list[PathOutcome]]]:
    startups = load_startups(ROOT / "data" / "startups.json")
    catalog = load_attack_catalog(ROOT / "data" / "attack_choices.json")
    validate_attack_catalog(catalog, startups)
    paths = {slug: enumerate_startup_paths(startup, catalog) for slug, startup in startups.items()}
    return startups, catalog, paths


def _percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    return ordered[max(0, (int(len(ordered) * fraction + 0.999999) - 1))]


def benchmark_round(startup: StartupTemplate, catalog: AttackCatalog, iterations: int = 1000) -> dict[str, Any]:
    choice = choices_for(catalog, startup.slug, 1)[0]
    state = initial_state(startup)
    samples = []
    for _ in range(iterations):
        started = time.perf_counter_ns()
        simulate_round(state, startup, to_validated_attack(choice, startup))
        samples.append((time.perf_counter_ns() - started) / 1_000_000)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_mib = rss / (1024 * 1024) if __import__("sys").platform == "darwin" else rss / 1024
    return {
        "iterations": iterations,
        "startup_slug": startup.slug,
        "choice_id": choice.id,
        "latency_ms": {
            "mean": round(statistics.fmean(samples), 4),
            "median": round(statistics.median(samples), 4),
            "p95": round(_percentile(samples, 0.95), 4),
            "max": round(max(samples), 4),
        },
        "process_peak_rss_mib": round(rss_mib, 2),
    }


def build_report_data() -> tuple[dict[str, Any], dict[str, StartupTemplate], AttackCatalog]:
    startups, catalog, paths = enumerate_all_paths()
    rows = []
    for slug, outcomes in paths.items():
        scores = [result.score for result in outcomes]
        best = max(outcomes, key=lambda result: (result.score, tuple(reversed(result.choice_ids))))
        worst = min(outcomes, key=lambda result: (result.score, result.choice_ids))
        rows.append({
            "startup_slug": slug,
            "path_count": len(outcomes),
            "score_min": min(scores),
            "score_max": max(scores),
            "score_mean": round(statistics.fmean(scores), 2),
            "score_median": statistics.median(scores),
            "bankruptcy_rate_percent": round(sum(r.final_status == "bankrupt" for r in outcomes) * 100 / len(outcomes), 2),
            "best_path": asdict(best),
            "worst_path": asdict(worst),
        })
    return {"catalog_version": catalog.catalog_version, "choices_per_round": catalog.choices_per_round,
            "startup_count": len(startups), "total_paths": sum(len(v) for v in paths.values()),
            "startups": rows}, startups, catalog


def main() -> None:
    data, startups, catalog = build_report_data()
    report = ROOT / "BALANCE_REPORT.md"
    benchmark = benchmark_round(startups["coffeebot"], catalog)
    lines = [
        "# Deterministic attack catalog balance report", "",
        f"Catalog `{data['catalog_version']}`: {data['startup_count']} startups, {catalog.choices_per_round} choices per round, {data['total_paths']} reachable terminal paths.",
        "Scores use the existing game scoring function. A bankrupt branch ends immediately; no later choices are counted.",
        "These are local engine results, not a production-host CPU or memory benchmark.", "",
        "| Startup | Paths | Score min | Score max | Mean | Median | Bankruptcy | Technical best | Technical worst |",
        "|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in data["startups"]:
        fmt_path = lambda item: f"{item['score']} ({' → '.join(item['choice_ids'])})"
        lines.append(
            f"| {row['startup_slug']} | {row['path_count']} | {row['score_min']} | {row['score_max']} | {row['score_mean']} | {row['score_median']} | {row['bankruptcy_rate_percent']}% | {fmt_path(row['best_path'])} | {fmt_path(row['worst_path'])} |"
        )
    lines += ["", "## Local deterministic round benchmark", "",
              f"{benchmark['iterations']} rounds with `{benchmark['choice_id']}` for `{benchmark['startup_slug']}`; per round: mean {benchmark['latency_ms']['mean']} ms, median {benchmark['latency_ms']['median']} ms, p95 {benchmark['latency_ms']['p95']} ms, max {benchmark['latency_ms']['max']} ms. Peak process RSS observed: {benchmark['process_peak_rss_mib']} MiB.",
              "", "No economy or scoring changes are proposed by this report.", ""]
    report.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"report": str(report), "paths": data["total_paths"], "benchmark": benchmark}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
