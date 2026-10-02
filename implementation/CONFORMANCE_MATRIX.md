# Матрица соответствия

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
