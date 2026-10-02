# Матрица соответствия

## Промежуточный v2 этап 02.10.2026

| Gate | Свидетельство | Статус |
|---|---|---|
| G0 | `python3 tools/spec_check.py`, `python3 tools/contract_lint.py`: 10 паспортов, 120 карточек, 30 golden cases | PASS локально |
| G1 | `python3 -m pytest backend/tests -q`; `python3 tools/balance_simulation.py`: 64 пути каждого из четырёх v2 стартапов, подробные `BALANCE_REPORT.md` и `BALANCE_AUDIT.json` | PASS локально; баланс не утверждён |
| G2 | Тест API проверяет снимок v2, combo badge и baseline damage; схема БД не менялась, локальный seed создаёт версии 2 только для четырёх паспортов | PASS в тестовой БД; production миграция не запускалась |
| G3 | `npm test -- --run`, `npm run build`: результат показывает атаку, combo, причину защиты, фактические деньги и ущерб игрока | PASS локально |
| Independent logic/math/balance | Две волны трёх GPT-6 Luna High рецензентов получили правила и нормализованные симуляции без исходного кода | PASS с открытыми рекомендациями по балансу; математическая проверка forecast ограничена отсутствием списка всех кандидатов в отчёте |
| G4/G5 | Целевой host benchmark, production backup и migration | NOT RUN |

Шесть остальных стартапов сохранили исходные 72 карточки и v1 движок. Коэффициенты v2 не корректировались после симуляции. Этот этап не является окончательной приёмкой общего баланса.

## Локальная приёмка 29.09.2026

| Gate | Критерий | Результат |
|---|---|---|
| G0 | JSON/schema, 10 seeds, 30 golden cases, 120 карточек и API контракт | PASS: `python3 tools/spec_check.py`, `python3 tools/contract_lint.py` |
| G1 | Экономический движок и достижимые пути | PASS локально: backend suite 100 passed; `BALANCE_REPORT.md` перечисляет 640 terminal paths |
| G2 | API, идемпотентность, session snapshots, migration scrub/history | PASS в тестовой среде: API/migration covered in backend suite; production migration не запускалась |
| G3 | UI выбора, клавиатура, синхронный результат/recovery | PASS локально: 35 Vitest tests и production frontend build |
| Assets | Утверждённые пути, checksums и физические изображения | PASS: `python3 tools/verify_assets.py`, 30 WebP + 10 masters |
| G4 | Целевой production host 2 vCPU/2 GiB | NOT RUN; локальный engine benchmark не заменяет host benchmark |
| G5 | Backup/restore и migration на production данных | NOT RUN; migration downgrade намеренно не поддержан |

Backend pytest выдал одно предупреждение Starlette/httpx deprecation. Compose/deployment readiness и production данные не проверялись. Benchmark численные результаты и RSS указаны в `BALANCE_REPORT.md`.

Старые AI/provider/admin acceptance gates удалены вместе с runtime системой.
