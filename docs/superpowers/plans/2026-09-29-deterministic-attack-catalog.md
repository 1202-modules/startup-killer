# Deterministic Attack Catalog Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace free-text/AI attacks with trusted deterministic attack choices across the game while preserving the approved economy, scoring, startup baselines, and game history.

**Architecture:** A versioned JSON catalog defines four choices per startup and round and maps directly to the existing `ValidatedAttack` and economy engine. A session pins its startup's catalog snapshot; the API accepts only a choice ID and calculates/commits the round synchronously. A new Alembic revision removes AI-only storage and preserves resolved results and ledgers.

**Tech Stack:** Existing Python 3, FastAPI, SQLAlchemy 2, Alembic, PostgreSQL, React, TypeScript, Vite, Tailwind, Framer Motion, TanStack Query, Zustand, pytest, Vitest.

**Spec:** [2026-09-29-deterministic-attack-catalog-design.md](../specs/2026-09-29-deterministic-attack-catalog-design.md)

## Global Constraints

- “не добавляет новые финансовые формулы, категории защиты, админ-функции, AI/NLP, runtime внешние вызовы или сторонние зависимости.”
- “начальная величина — 4, то есть 12 вариантов на startup и 120 на весь каталог.”
- “Тело хода содержит только `{"choice_id":"..."}`.”
- “Добавить следующую Alembic migration”; preserve `0001_initial_schema.py` and completed financial history.
- Production topology: PostgreSQL, one API, static nginx/frontend; no worker services or AI secrets.
- No Git metadata exists in this workspace. Do not initialize a repository; commits are unavailable here. Keep each task bounded and report its test result.

## Review Focus

- Unknown, cross-startup, wrong-round, or stale choice IDs must never reach the engine. Pin with API tests for rejected choices and a session snapshot that remains stable when the source catalog changes.
- A client-supplied economy field must be rejected, not ignored. Pin with strict request-schema tests using extra fields.
- Repeated requests must not apply a round twice. Pin same-key/same-payload replay and same-key/different-payload conflict tests.
- Upgrade must preserve completed ledgers while removing unresolved old AI jobs without consuming a turn. Pin populated-database Alembic upgrade tests.
- Bankruptcy during an early month must terminate the path and score once. Pin all reachable-path simulation and an early-bankruptcy balance case.

---

### Task 1: Attack catalog and engine adapter

**Files:**
- Create: `data/attack_choices.json`, `data/attack_choices_schema.json`
- Create: `backend/app/engine/attack_choices.py`
- Modify: `backend/app/engine/types.py` only if an immutable `AttackChoice` type is needed
- Test: `backend/tests/test_attack_choices.py`

**Interfaces:**
- Produces `load_attack_catalog(path) -> AttackCatalog`, `choices_for(catalog, startup_slug, round_number) -> list[AttackChoice]`, and `to_validated_attack(choice, startup) -> ValidatedAttack`.
- Produces `validate_attack_catalog(catalog, startups) -> None` for startup, stream, weakness, fact, and coverage checks.
- Catalog root declares `catalog_version` and `choices_per_round`; enforce four initial choices in each of the 30 startup/round slots, but derive the expected count from catalog data.
- Choice fields map only to existing engine enums/inputs; evidence IDs must pass current critical-severity guard; no per-choice business-logic branches.

- [x] Add failing tests `test_catalog_rejects_invalid_references_and_enums`, `test_catalog_requires_every_configured_round_slot`, and `test_catalog_rejects_duplicate_choice_ids` for schema/loader behavior.
- [x] Add failing tests `test_choice_maps_to_validated_attack` and `test_choice_has_no_client_supplied_economic_values` for the engine adapter.
- [x] Run `python3 -m pytest backend/tests/test_attack_choices.py -q`; six tests fail because the catalog API is absent.
- [x] Implement the loader, schema checks, DTO, and adapter; rerun the Task 1 focused tests.
- [x] Author the 120 startup-specific cards using existing facts, weaknesses, streams, and industries; rerun catalog validation for all 30 startup/round slots.
- [x] Run `python3 -m pytest backend/tests/test_attack_choices.py backend/tests/test_golden_cases.py -q`; 42 passed and all existing economy oracles remain unchanged.

### Task 2: Deterministic synchronous API, storage, and backend AI removal

**Files:**
- Modify: `backend/app/db/models.py`, `backend/app/api/routes.py`, `backend/app/api/schemas.py`, `backend/app/db/seed.py`, `backend/app/main.py`, `backend/app/config.py`
- Create: `backend/alembic/versions/0002_attack_choices.py`
- Delete: backend-only AI provider/validator/prompt, worker/queue, AI admin route, and AI-only auth/crypto modules and tests
- Test: `backend/tests/test_api_endpoints.py`, `backend/tests/test_db_models.py`, `backend/tests/test_alembic_migrations.py`

**Interfaces:**
- Request body is strict `AttackRequest(choice_id: str)`; infer current round from the owned session.
- Session stores `attack_catalog_version` and an immutable JSON snapshot of its 12 choices. Resolved round stores nullable `selected_choice_id` and the selected choice snapshot for historical/version safety.
- Public card DTO is `AttackChoicePublic(id, round_number, title, short_description, attack_narrative)`; it exposes no severity, weakness, stream IDs, or coefficients. A successful `POST /api/v1/sessions/{session_id}/choices` returns the resolved round/result; no job ID or polling phase.

- [x] Add failing API tests `test_submit_choice_resolves_synchronously`, `test_rejects_wrong_startup_round_and_unknown_choice`, `test_rejects_extra_economic_fields`, and `test_choice_catalog_snapshot_survives_catalog_update`.
- [x] Add failing API tests `test_choice_idempotency_replay_and_conflict` and `test_choice_result_recovers_after_refresh`.
- [x] Add failing migration tests `test_upgrade_preserves_resolved_financial_history` and `test_upgrade_discards_unresolved_ai_round_without_spending_turn`; scrub legacy raw text/AI fields from columns and JSON snapshots.
- [x] Run `pytest backend/tests/test_api_endpoints.py backend/tests/test_db_models.py backend/tests/test_alembic_migrations.py -q`; confirm new requirements fail.
- [x] Implement migration revision `0002_attack_choices` after `0001_initial_schema`; update row models and perform lock/validate/compute/write in one transaction. Return the stored result on idempotent replay.
- [x] Remove attack submission job creation and job-status/round-polling endpoints after response retrieval is synchronous; remove backend worker/provider/admin AI code and retain session, continue, result, leaderboard, cookie, CSRF, and idempotency behavior.
- [x] Run the focused API/model/migration tests plus `pytest backend/tests/test_golden_cases.py -q`; expect preserved legacy ledger and unchanged economy oracle values.

### Task 3: Card UI and player flow

**Files:**
- Modify: `apps/web/src/App.tsx`, `apps/web/src/api/types.ts`, `apps/web/src/api/endpoints.ts`, `apps/web/src/hooks/useAttack.ts`, `apps/web/src/views/GameView.tsx`, `apps/web/src/views/WelcomeView.tsx`
- Create: `apps/web/src/components/game/AttackChoiceGrid.tsx`
- Delete: `apps/web/src/components/game/AttackInput.tsx`, `apps/web/src/hooks/useJobPoller.ts`, AI-only banners/admin views/components/hooks/API clients and their tests
- Test: `apps/web/src/__tests__/components/AttackChoiceGrid.test.tsx`, `apps/web/src/__tests__/views/GameView.test.tsx`, related API tests

**Interfaces:**
- Session response exposes only public choice fields for the pinned startup and active round.
- `useAttack` sends `{ choice_id }` with existing CSRF/idempotency headers and receives a resolved result.
- Result display uses selected-card and server outcome text; no model-wait/retry/provider/demo states.

- [x] Add failing tests `test_renders_current_round_choices`, `test_keyboard_can_select_attack_choice`, `test_attack_choice_cards_fit_mobile_layout`, `test_attack_sends_only_choice_id`, and `test_resolved_result_uses_card_narrative`.
- [x] Run `cd apps/web && npm test -- --run src/__tests__/components/AttackChoiceGrid.test.tsx src/__tests__/views/GameView.test.tsx src/__tests__/api/client.test.ts`; confirm new tests fail.
- [x] Implement the card selection flow and synchronous result handling while retaining current visual system, motion, reduced-motion, startup art, finance panel, and final screens.
- [x] Remove free-text attack controls, polling, outage/demo copy, and admin UI/API routes/components/tests that serve only AI management.
- [x] Run `cd apps/web && npm test -- --run`; expect all retained and new Vitest tests to pass.

### Task 4: Remove AI dependencies and deployment services

**Files:**
- Delete: `ai/`, AI-quality data/schema/runner; update/delete obsolete `apps/web/generate_*.py` scripts that recreate removed AI screens
- Modify: `backend/requirements.txt`, `Dockerfile.backend`, `docker-compose.yml`, `.env.example`, `apps/web/package.json`, `apps/web/package-lock.json`
- Test: `backend/tests/` remaining game/API/security tests and deployment/config checks

**Interfaces:**
- Production starts PostgreSQL, one FastAPI process, and static Nginx/frontend. No AI key, worker, queue, provider client, test provider, admin AI route, or polling contract is required.
- Keep a dependency if another retained runtime path imports it.

- [x] Add failing static/config tests `test_runtime_config_needs_no_ai_credentials`, `test_compose_has_no_worker`, and `test_configured_healthchecks_match_api_routes`.
- [x] Run focused tests for startup, runtime configuration, dependency/import checks, and remaining security/session behavior; record failures before deleting modules.
- [x] Remove unused worker service, AI-only dependencies, and environment keys; retain libraries only if used by retained features.
- [x] Update lockfiles with the package manager already in use; do not add dependencies.
- [x] Run `python3 -m compileall backend/app` and the affected backend test modules; expect imports and application startup to succeed without AI settings.

### Task 5: Exhaustive balance and round benchmark

**Files:**
- Create: `tools/balance_simulation.py`, root `BALANCE_REPORT.md`
- Modify: `tools/load_test_benchmark.py`, `backend/tests/test_load_test_benchmark.py` as needed to remove worker/provider setup
- Test: `backend/tests/test_balance_simulation.py`

**Interfaces:**
- Enumerate only reachable choice paths for each startup and stop each path on bankruptcy; report path count and score min/max/mean/median, bankruptcy rate, and technical best/worst path.
- Benchmark one deterministic engine round with local startup/catalog fixtures; do not claim target-host RAM/CPU from local results.

- [x] Add failing assertions for exact path enumeration on a small synthetic catalog, terminal bankruptcy pruning, and stable repeated-path outputs.
- [x] Run `pytest backend/tests/test_balance_simulation.py -q`; confirm new tests fail.
- [x] Implement exhaustive enumerator and benchmark using existing engine functions; avoid a second scoring/economy implementation.
- [x] Run it across all ten startups, save measured figures and any imbalance proposals to `BALANCE_REPORT.md`, and record actual per-round latency.
- [x] Run `pytest backend/tests/test_balance_simulation.py backend/tests/test_golden_cases.py -q`; expect stable exhaustive results and unchanged golden outputs.

### Task 6: Migrate normative docs and static acceptance checks

**Files:**
- Modify: `AGENTS.md`, `ANTIGRAVITY_START_HERE.md`, `README.md`, `docs/PRODUCT.md`, `docs/GAME_RULES.md`, `docs/ECONOMY.md`, `docs/SCORING.md`, `docs/ENGINE_CONTRACT.md`, `docs/API.md`, `docs/DATABASE.md`, architecture/design/UI/narrative/release documents, `implementation/*`, `tools/spec_check.py`, `tools/contract_lint.py`
- Delete: obsolete AI routing/schema/quality documents and fixtures; retain `assets/`, `assets/prompts/`, static image instructions, and generated images
- Create/refresh: `MANIFEST.sha256`
- Test: `tools/spec_check.py`, `tools/contract_lint.py`, `tools/verify_assets.py`

**Interfaces:**
- All normative gameplay docs describe server-trusted choice IDs and deterministic rounds. G0 validates attack catalog/schema and economy; it does not require deleted AI schemas or fixtures.
- Runtime AI search returns no matches. Any remaining AI-related references are documented development-time image tooling or explicit historical migration context.

- [x] Add G0 assertions for all 10×3 slots, deterministic schemas, and runtime contract removal.
- [x] Run `python3 tools/spec_check.py && python3 tools/contract_lint.py`; both PASS.
- [x] Update product/API/database/economy/design/release docs and remove obsolete AI docs/fixtures while retaining static asset-production guidance.
- [x] Update catalog static checks and regenerate/verify `MANIFEST.sha256` (188 entries).
- [x] Run G0 checks and `python3 tools/verify_assets.py`; all PASS, 30/30 WebP.

### Task 7: Integrated acceptance and final audit

**Files:** all files above; no new runtime subsystem

**Interfaces:** final API, catalog, UI, migration, docs, and production build satisfy the approved spec together.

- [x] Run `python3 -m pytest backend/tests -q`: 100 passed, one deprecation warning.
- [x] Run `npm test -- --run && npm run build` in `apps/web`: 35 passed and build PASS.
- [x] Run G0 and asset checks: all PASS.
- [x] Search runtime source/config for provider credentials, free-text fields, jobs, admin routes, and known provider names: no matches; historical migration/test and development-time static asset references are documented.
- [x] Record results in `CONFORMANCE_MATRIX.md` and `BALANCE_REPORT.md`; production host and migration remain explicitly unverified.
