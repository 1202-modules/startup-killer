# План реализации Gate 1: Детерминированный экономический движок (T01–T06)

Реализация чистого, детерминированного ядра симуляции экономики для игры «Убей стартап» (FastAPI backend). Движок производит помесячный расчёт финансовых показателей (выручка по потокам, переменные и фиксированные расходы, разовые инциденты, защита, остаток на счетах и непокрытые обязательства), детерминированный выбор защиты, фиксацию банкротства и расчёт итогового рейтинга (700/200/100).
Движок не зависит от внешних LLM и верифицируется всеми 30 эталонными сценариями из `data/economy_golden_cases.json`.

## Требуется согласование пользователя

> [!IMPORTANT]
> **Исключение по субагентам:** Согласно вашему указанию, для данного проекта сделано исключение: разработка ведётся в основном контексте через строгий TDD, без частого создания субагентов. Субагент будет вызван на этапе независимого код-ревью перед утверждением завершения Gate 1.
>
> **Чистый Python без внешних зависимостей:** Экономический движок реализуется на стандартной библиотеке Python (`Decimal`, `math`, `dataclasses`, `json`, `enum`) и тестируется через `pytest`.

## Открытые вопросы

Открытых вопросов по экономике нет: все формулы, коэффициенты и правила нормативно закреплены в `docs/ECONOMY.md`, `docs/SCORING.md`, `docs/ENGINE_CONTRACT.md` и подтверждены 30 эталонными числовыми сценариями.

---

## Предлагаемые изменения

### Модуль ядра экономики (`backend/app/engine/`)

Архитектура движка разделена на специализированные модули с чистыми функциями без сайд-эффектов:

#### [NEW] [types.py](file:///Users/kk0sta/Documents/Проекты/Свое/Симуляция%20"Убей%20стартап"/backend/app/engine/types.py)
- Enums: `Severity`, `Scale`, `Feasibility`, `WeaknessMatch`, `Duration`, `AttackType`, `DefenseType`, `SceneType`, `FinalStatus`.
- Структуры данных:
  - `RevenueStreamConfig`, `FinanceConfig`, `StartupTemplate`
  - `AttackInput`, `ValidatedAttack`, `ActiveEffect`
  - `StreamLedgerRow`, `MonthlyLedgerRow`
  - `GameState`, `DefenseDecision`, `EngineOutcome`
  - `FinalScore` (`damage`, `solvency`, `early_bankruptcy`, `score`, `status`)

#### [NEW] [constants.py](file:///Users/kk0sta/Documents/Проекты/Свое/Симуляция%20"Убей%20стартап"/backend/app/engine/constants.py)
- Нормативные базисные пункты (bps, 10 000 = 100%):
  - `SEVERITY_BPS`: weak=1200, medium=3000, strong=5500, critical=8000
  - `SCALE_BPS`: local=4000, regional=6500, company_wide=10000
  - `FEASIBILITY_BPS`: unsupported=5000, plausible=8000, established_in_state=10000
  - `WEAKNESS_MATCH_BPS`: indirect=8000, normal=10000, exact=12500
  - `DECAY_BPS`: temporary=6000 (до 3 месяцев), persistent=8500 (до 6 месяцев), structural=10000 (без decay, до 9 месяцев)
  - `INCIDENT_COST_BPS`: weak=1500, medium=3500, strong=7000, critical=12000 от базовых фиксированных расходов
  - `REPUTATION_DELTAS`: weak=-3, medium=-8, strong=-15, critical=-24
  - `DEFENSE_COSTS`: cost_cut=2500, pr=2500, supplier_switch=4500, pivot=7000 bps от фиксированных расходов

#### [NEW] [loader.py](file:///Users/kk0sta/Documents/Проекты/Свое/Симуляция%20"Убей%20стартап"/backend/app/engine/loader.py)
- Загрузка `data/startups.json` и валидация 10 неизменяемых авторских шаблонов.
- Вычисление и верификация `baseline_series` (месяцы 0..9) с точностью до копейки (`ROUND_HALF_UP`).
- Проверка уникальности slug, stream ID и fact ID.

#### [NEW] [scoring.py](file:///Users/kk0sta/Documents/Проекты/Свое/Симуляция%20"Убей%20стартап"/backend/app/engine/scoring.py)
- Расчёт компонентов рейтинга по `SCORING.md`:
  - Компонент A (0..700): дополнительный финансовый ущерб `700 * clamp((B - C) / B, 0, 1)`
  - Компонент K (0..200): ухудшение платёжеспособности `200 * clamp((risk_actual - risk_baseline) / (1 - risk_baseline), 0, 1)`
  - Компонент E (0..100): ускорение банкротства `100 * (9 - m) / 8` при банкротстве в месяц `m`, иначе 0
  - Финальный счёт: `ROUND_HALF_UP(A + K + E)`, clamp 0..1000
  - Определение статуса финала: `bankrupt`, `near_bankruptcy`, `deep_crisis`, `survived`

#### [NEW] [defense.py](file:///Users/kk0sta/Documents/Проекты/Свое/Симуляция%20"Убей%20стартап"/backend/app/engine/defense.py)
- Проверка доступности манёвров (`none`, `cost_cut`, `pr`, `supplier_switch`, `pivot`) по ресурсам, наличию кризиса, совместимым активам в `private_profile` и однократному использованию.
- Детерминированный 3-месячный прогноз текущего раунда для выбора манёвра с наибольшим `closing_cash_kopeks` (при равенстве — меньшие разовые расходы, далее порядок enum).

#### [NEW] [calculator.py](file:///Users/kk0sta/Documents/Проекты/Свое/Симуляция%20"Убей%20стартап"/backend/app/engine/calculator.py)
- `calculate_attack_impact`: расчёт результирующего шока в bps, разовых инцидентных затрат и изменения репутации.
- `simulate_month`: пошаговый расчёт одного месяца:
  - Базовая выручка потока с учётом ежемесячного роста
  - Применение активных шоков (мультипликативно для независимых, max для одного stack_group) и эффектов защиты
  - Переменные расходы от фактической выручки
  - Фиксированные расходы, разовые инциденты и защитные платежи
  - Расчёт прибыли и закрывающего остатка денег; при дефиците — `unpaid_obligations` и немедленный статус банкротства (без отрицательного баланса и без проводок в следующих месяцах)
  - Декремент таймеров decay/duration и обновление репутации (clamp 0..100)
- `simulate_round`: симуляция 3 месяцев раунда с учётом атаки и детерминированного выбора защиты.
- `simulate_game`: симуляция всей партии (до 3 раундов по 3 месяца).

---

### Тесты и верификация (`backend/tests/`)

#### [NEW] [test_baseline.py](file:///Users/kk0sta/Documents/Проекты/Свое/Симуляция%20"Убей%20стартап"/backend/tests/test_baseline.py)
- Проверка точного совпадения baseline-серий всех 10 авторских стартапов (все 90 месяцев до единой копейки).

#### [NEW] [test_golden_cases.py](file:///Users/kk0sta/Documents/Проекты/Свое/Симуляция%20"Убей%20стартап"/backend/tests/test_golden_cases.py)
- Запуск симулятора на всех **30 эталонных сценариях** из `data/economy_golden_cases.json`:
  - 10 сценариев `baseline`
  - 10 сценариев `weak_local_one_stream` (шок 384 -> 230 -> 138 -> 0 bps)
  - 10 сценариев `structural_95pct_all_streams` (банкротство до 9 месяца, непокрытые обязательства)
- Проверка идентичности каждой помесячной проводки, выручки, расходов, закрывающего баланса, месяца банкротства и каждого компонента очков (`damage`, `solvency`, `early_bankruptcy`, `score`).

#### [NEW] [test_invariants.py](file:///Users/kk0sta/Documents/Проекты/Свое/Симуляция%20"Убей%20стартап"/backend/tests/test_invariants.py)
- Граничные условия:
  - Стэкинг одинаковых эффектов (`max`)
  - Мультипликативное сложение независимых эффектов на один поток
  - Защита PR недоступна без репутационного кризиса
  - Защита `supplier_switch` требует альтернативного поставщика в паспорте
  - Однократность `cost_cut` и `pivot`
  - Запрет банкротства при наличии денег на счетах и запрет отрицательных остатков

---

## План верификации

### Автоматические тесты
1. Запуск тестового набора:
   ```bash
   pytest backend/tests/ -v
   ```
2. Запуск проверочных утилит проекта:
   ```bash
   python3 tools/contract_lint.py
   python3 -c "from backend.app.engine.loader import load_startups; print('Loaded', len(load_startups()), 'startups')"
   ```
3. Проверка всех 30 golden cases с подтверждением 100% совпадения результатов.

### Независимое код-ревью
- По завершении реализации вызов субагента-ревьюера (`requesting-code-review`) для проверки соответствия кодовой базы контрактам `docs/ECONOMY.md`, `docs/ENGINE_CONTRACT.md` и `docs/SCORING.md`.
