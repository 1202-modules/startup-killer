"""Exhaustively simulate all reachable catalog paths through the approved engine."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_HALF_UP
from itertools import product
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
from backend.app.engine.types import DefenseType, GameState, StartupTemplate


@dataclass(frozen=True)
class PathOutcome:
    startup_slug: str
    choice_ids: tuple[str, ...]
    final_status: str
    score: int
    elapsed_months: int
    final_cash_kopeks: int
    bankruptcy_month: int | None
    combo_flags: tuple[str, ...] = ()
    defenses: tuple[str, ...] = ()
    baseline_cash_kopeks: int = 0
    player_damage_kopeks: int = 0
    active_causes: tuple[str, ...] = ()
    final_revenue_kopeks: int = 0
    unpaid_obligations_kopeks: int = 0


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
    def walk(state: GameState, path: tuple[str, ...], cumulative_revenue: int = 0) -> list[PathOutcome]:
        if state.is_bankrupt or state.elapsed_months >= 9:
            score = state.score_breakdown
            return [PathOutcome(
                startup_slug=startup.slug, choice_ids=path,
                final_status=score.final_status.value if score else "survived",
                score=score.score if score else 0,
                elapsed_months=state.elapsed_months,
                final_cash_kopeks=state.cash_kopeks,
                bankruptcy_month=state.bankruptcy_month,
                combo_flags=tuple(state.v2_data.get('flags', [])),
                defenses=tuple(d['name'] for d in state.v2_data.get('defenses', [])),
                baseline_cash_kopeks=startup.baseline_series[state.elapsed_months].closing_cash_kopeks,
                player_damage_kopeks=startup.baseline_series[state.elapsed_months].closing_cash_kopeks - state.cash_kopeks,
                active_causes=tuple(f"{e['group']}:{e['cause']}" for e in state.v2_data.get('effects', [])),
                final_revenue_kopeks=cumulative_revenue,
                unpaid_obligations_kopeks=state.unpaid_obligations_kopeks,
            )]

        round_choices = choices_for(catalog, startup.slug, state.round_number)
        if not round_choices:
            raise ValueError(f"catalog has no choices for {startup.slug} round {state.round_number}")
        results: list[PathOutcome] = []
        for choice in round_choices:
            outcome = simulate_round(state, startup, to_validated_attack(choice, startup))
            results.extend(walk(outcome.state_after, path + (choice.id,), cumulative_revenue + sum(row.revenue_kopeks for row in outcome.monthly_ledger)))
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


def percent(count: int, total: int) -> Decimal:
    return (Decimal(count) * 100 / Decimal(total)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def path_label(choice_ids: tuple[str, ...]) -> str:
    """Normalize legacy numeric choice suffixes to the report's A/B/C/D notation."""
    labels = {'1': 'A', '2': 'B', '3': 'C', '4': 'D'}
    return ''.join(labels.get(choice_id.rsplit('_', 1)[-1], choice_id.rsplit('_', 1)[-1].upper()) for choice_id in choice_ids)


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
            "score_p25": _percentile(scores, 0.25),
            "score_p75": _percentile(scores, 0.75),
            "bankruptcy_rate_percent": percent(sum(r.final_status == "bankrupt" for r in outcomes), len(outcomes)),
            "best_path": asdict(best),
            "worst_path": asdict(worst),
        })
    return {"catalog_version": catalog.catalog_version, "choices_per_round": catalog.choices_per_round,
            "startup_count": len(startups), "total_paths": sum(len(v) for v in paths.values()),
            "startups": rows}, startups, catalog


def main() -> None:
    data, startups, catalog = build_report_data()
    _, _, all_paths = enumerate_all_paths()
    all_slugs = tuple(startups)
    report = ROOT / "BALANCE_REPORT.md"
    benchmark = benchmark_round(startups["coffeebot"], catalog)
    lines = [
        "# Deterministic attack catalog balance report", "",
        f"Catalog `{data['catalog_version']}`: {data['startup_count']} startups, {catalog.choices_per_round} choices per round, {data['total_paths']} reachable terminal paths.",
        "Scores use the existing game scoring function. A bankrupt branch ends immediately; no later choices are counted.",
        "These are local engine results, not a production-host CPU or memory benchmark.", "",
        "| Startup | Paths | Score min | Score max | P25 | Mean | Median | P75 | Bankruptcy | Technical best | Technical worst |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in data["startups"]:
        fmt_path = lambda item: f"{item['score']} ({' → '.join(item['choice_ids'])})"
        lines.append(
            f"| {row['startup_slug']} | {row['path_count']} | {row['score_min']} | {row['score_max']} | {row['score_p25']} | {row['score_mean']} | {row['score_median']} | {row['score_p75']} | {row['bankruptcy_rate_percent']}% | {fmt_path(row['best_path'])} | {fmt_path(row['worst_path'])} |"
        )
    lines += ["", "## All ten v2 startups: exhaustive outcome summary", "",
              "Each startup has 64 choice sequences. Cash and damage are in RUB below; the raw path table retains kopeks. Player damage uses baseline at the same terminal month; score A uses baseline M9, including when bankruptcy ends a game early.",
              "A bankrupt game stops immediately. The listed sequence is the actual played prefix.", "",
              "| Startup | Min | Max | Mean | Median | Bankrupt | Near | Deep | Survived | Best coherent | DDD | Mixed mean |",
              "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|"]
    for slug in all_slugs:
        outcomes = all_paths[slug]
        scores = [o.score for o in outcomes]
        by_path = {path_label(o.choice_ids): o for o in outcomes}
        coherent = max((by_path[p] for p in ('AAA', 'BBB', 'CCC', 'DDD')), key=lambda o: o.score)
        mixed = [o.score for path, o in by_path.items() if path not in ('AAA', 'BBB', 'CCC', 'DDD')]
        pct = lambda status: percent(sum(o.final_status == status for o in outcomes), len(outcomes))
        lines.append(f"| {slug} | {min(scores)} | {max(scores)} | {statistics.fmean(scores):.2f} | {statistics.median(scores)} | {pct('bankrupt')}% | {pct('near_bankruptcy')}% | {pct('deep_crisis')}% | {pct('survived')}% | {path_label(coherent.choice_ids)}: {coherent.score} | {by_path['DDD'].score} | {statistics.fmean(mixed):.2f} |")
    lines += ["", "## Six-startup first-pass and final record", "",
              "The first exhaustive pass is the final pass for SleepWork, FitMirror, CloudKitchen, AgroDrone, MoodAds and RentEverything. No permitted tuning field was changed, so both columns are the preserved first-pass and final result.", "",
              "| Startup | First mean | Final mean | First bankruptcy | Final bankruptcy | First DDD | Final DDD |", "|---|---:|---:|---:|---:|---:|---:|"]
    for slug in all_slugs[4:]:
        row = next(item for item in data['startups'] if item['startup_slug'] == slug)
        outcomes = all_paths[slug]
        by_path = {path_label(o.choice_ids): o for o in outcomes}
        bankruptcy = percent(sum(o.final_status == 'bankrupt' for o in outcomes), len(outcomes))
        lines.append(f"| {slug} | {row['score_mean']} | {row['score_mean']} | {bankruptcy}% | {bankruptcy}% | {by_path['DDD'].score} | {by_path['DDD'].score} |")
    lines += ["", "## First-four shared-engine regression", "",
              "The four reference catalogs were byte-for-byte unchanged. Their before values are from the preceding v2 report; after values include only the shared defense max-use and inevitable-bankruptcy selection fixes.", "",
              "| Startup | Before mean | After mean | Before bankruptcy | After bankruptcy |", "|---|---:|---:|---:|---:|"]
    before = {'petmind': (463.28, '0.00%'), 'coffeebot': (454.56, '1.56%'),
              'foodrover': (510.05, '1.56%'), 'studygenie': (412.77, '1.56%')}
    for slug in ('petmind', 'coffeebot', 'foodrover', 'studygenie'):
        row = next(item for item in data['startups'] if item['startup_slug'] == slug)
        lines.append(f"| {slug} | {before[slug][0]} | {row['score_mean']} | {before[slug][1]} | {row['bankruptcy_rate_percent']}% |")
    lines += ["", "## Explicit chains and prerequisite bypass controls", "",
              "Controls ABB, CBB, DBB and AAC, ABC, ACB verify that a later same-letter card gets only base effects when the prerequisite chain was broken.", "",
              "| Startup | Path | Score | Status | Cash RUB | Damage RUB | Flags | Defenses | Bankruptcy month |",
              "|---|---|---:|---|---:|---:|---|---|---:|"]
    controls = ('AAA', 'BBB', 'CCC', 'DDD', 'ABB', 'CBB', 'DBB', 'AAC', 'ABC', 'ACB')
    for slug in all_slugs:
        by_path = {path_label(o.choice_ids): o for o in all_paths[slug]}
        for path in controls:
            o = by_path[path]
            lines.append(f"| {slug} | {path} | {o.score} | {o.final_status} | {o.final_cash_kopeks / 100:,.0f} | {o.player_damage_kopeks / 100:,.0f} | {', '.join(o.combo_flags) or '—'} | {', '.join(o.defenses) or 'NONE'} | {o.bankruptcy_month or '—'} |")
    lines += ["", "## Matched BBB defense controls", "",
              "The same BBB choices are simulated with normal deterministic defense selection and with defense forced to NONE; coefficients and incident costs are identical.", "",
              "| Startup | Selected/no-defense cash RUB | Selected/no-defense bankruptcy month | Selected/no-defense total revenue RUB | Selected defense cost RUB | Selected/no-defense score |",
              "|---|---:|---|---:|---:|---:|"]
    for slug in all_slugs:
        startup = startups[slug]
        controls = []
        for forced in (None, DefenseType.NONE):
            state = initial_state(startup)
            revenue = defense_cost = 0
            for round_number in range(1, 4):
                choice = choices_for(catalog, slug, round_number)[1]
                outcome = simulate_round(state, startup, to_validated_attack(choice, startup), forced_defense=forced)
                revenue += sum(row.revenue_kopeks for row in outcome.monthly_ledger)
                defense_cost += sum(row.defense_cost_kopeks for row in outcome.monthly_ledger)
                state = outcome.state_after
                if state.is_bankrupt:
                    break
            controls.append((state, revenue, defense_cost))
        selected, no_defense = controls
        lines.append(f"| {slug} | {selected[0].cash_kopeks / 100:,.0f} / {no_defense[0].cash_kopeks / 100:,.0f} | {selected[0].bankruptcy_month or '—'} / {no_defense[0].bankruptcy_month or '—'} | {selected[1] / 100:,.0f} / {no_defense[1] / 100:,.0f} | {selected[2] / 100:,.0f} | {selected[0].score_breakdown.score if selected[0].score_breakdown else '—'} / {no_defense[0].score_breakdown.score if no_defense[0].score_breakdown else '—'} |")
    lines += ["", "## All 64 paths per v2 startup", "",
              "Monetary values in this table are integer kopeks; flags and defenses are server-side simulation observations.", "",
              "| Startup | Choices | Combo flags | Active causes | Defenses | Final revenue | Final cash | Same-month baseline cash | Player damage | Unpaid obligations | Score | Status | Bankruptcy month |",
              "|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|"]
    for slug in all_slugs:
        for o in all_paths[slug]:
            path = path_label(o.choice_ids)
            lines.append(f"| {slug} | {path} | {', '.join(o.combo_flags) or '—'} | {', '.join(o.active_causes) or '—'} | {', '.join(o.defenses) or 'NONE'} | {o.final_revenue_kopeks} | {o.final_cash_kopeks} | {o.baseline_cash_kopeks} | {o.player_damage_kopeks} | {o.unpaid_obligations_kopeks} | {o.score} | {o.final_status} | {o.bankruptcy_month or '—'} |")
    lines += ["", "## Balance observations", "",
              "First pass is final: approved coefficients were not tuned after the exhaustive run. Review the reported DDD and mixed-path spreads before treating the shared leaderboard as fair.",
              "",
              "## Defense usage distribution",
              "",
              "Every named strategic defense has max_uses=1 per game; emergency cost cut is also single-use. Counts below are path-level usages across the 64 reachable sequences.",
              "",
              "| Startup | Paths with a defense | Paths with 2+ defenses | Most-used defenses |",
              "|---|---:|---:|---|"]
    for slug in all_slugs:
        outcomes = all_paths[slug]
        counts: dict[str, int] = {}
        for outcome in outcomes:
            for defense in outcome.defenses:
                counts[defense] = counts.get(defense, 0) + 1
        ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:4]
        lines.append(f"| {slug} | {sum(bool(o.defenses) for o in outcomes)} | {sum(len(o.defenses) >= 2 for o in outcomes)} | {', '.join(f'{name} ({count})' for name, count in ranked) or 'NONE'} |")
    lines += [
              "", "## Local deterministic round benchmark", "",
              f"{benchmark['iterations']} rounds with `{benchmark['choice_id']}` for `{benchmark['startup_slug']}`; per round: mean {benchmark['latency_ms']['mean']} ms, median {benchmark['latency_ms']['median']} ms, p95 {benchmark['latency_ms']['p95']} ms, max {benchmark['latency_ms']['max']} ms. Peak process RSS observed: {benchmark['process_peak_rss_mib']} MiB.",
              "", "All ten catalogs use explicit v2 effects and ending thresholds. This local benchmark is not a target-host benchmark.", ""]
    report.write_text("\n".join(lines), encoding="utf-8")
    audit = []
    for slug in all_slugs:
        startup = startups[slug]
        for sequence in product('ABCD', repeat=3):
            state = initial_state(startup)
            rounds = []
            for round_number, letter in enumerate(sequence, 1):
                choice = choices_for(catalog, slug, round_number)['ABCD'.index(letter)]
                outcome = simulate_round(state, startup, to_validated_attack(choice, startup))
                rounds.append({
                    'choice': letter, 'combo_triggered': outcome.details['combo_triggered'],
                    'applied_stream_loss_bps': outcome.details['affected_streams'],
                    'active_causes_after_round': [f"{effect['group']}:{effect['cause']}" for effect in outcome.state_after.v2_data.get('effects', [])],
                    'defense': outcome.details['defense_name'],
                    'defense_reason': outcome.details.get('defense_reason', ''),
                    'defense_cost_kopeks': outcome.details['defense_cost_kopeks'],
                    'defense_candidates': outcome.audit.get('defense_candidates', []),
                    'monthly_ledger': [asdict(row) for row in outcome.monthly_ledger],
                    'baseline_cash_at_endpoint_kopeks': outcome.details['baseline_cash_kopeks'],
                    'player_damage_at_endpoint_kopeks': outcome.details['player_damage_kopeks'],
                })
                state = outcome.state_after
                if state.is_bankrupt:
                    break
            audit.append({
                'startup': slug, 'sequence': ''.join(sequence),
                'played_prefix': ''.join(r['choice'] for r in rounds),
                'baseline_cash_m9_kopeks': startup.baseline_cash_m9_kopeks,
                'final_cash_kopeks': state.cash_kopeks,
                'final_revenue_kopeks': sum(r['monthly_ledger'][i]['revenue_kopeks'] for r in rounds for i in range(len(r['monthly_ledger']))),
                'bankruptcy_month': state.bankruptcy_month,
                'unpaid_obligations_kopeks': state.unpaid_obligations_kopeks,
                'score': asdict(state.score_breakdown) if state.score_breakdown else None,
                'rounds': rounds,
            })
    audit_path = ROOT / 'BALANCE_AUDIT.json'
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({"report": str(report), "paths": data["total_paths"], "benchmark": benchmark}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
