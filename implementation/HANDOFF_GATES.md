# Handoff gates

## G0 — контракты
Запустить `python3 tools/spec_check.py`, `python3 tools/contract_lint.py`; проверить 10 стартапов, 30 economy fixtures, schema каталога и 120 выборов. Это статический preflight, не runtime acceptance.

## G1 — движок и баланс
Прогнать golden cases и unit suite. `tools/balance_simulation.py` должен перечислить все достижимые терминальные пути существующим движком, остановить каждый путь на банкротстве, вывести диапазон результатов и bounded round benchmark в `BALANCE_REPORT.md`.

## G2 — база/API
Проверить миграцию и API: только `choice_id`, extra fields запрещены, session snapshot, idempotency, ownership, восстановление round result; завершённые ledger сохраняются, свободный текст/AI-сущности удаляются.

## G3 — frontend/deployment contract
Frontend отображает только публичные варианты, принимает клавиатурный выбор, получает синхронный результат и восстанавливается после обновления. Compose не содержит AI worker. Локальные build/tests не означают production acceptance.

## G4 — целевой хост
Пока не пройден. Отдельный новый экземпляр развёрнут на хосте 2 vCPU/3.8 GiB; см. `DEPLOYMENT_2026-10-02.md`. Требуется реальный benchmark 2 vCPU/2 GiB и фактическая миграция существующей БД с заранее проверенным backup.

## Отчёт
Фиксировать статус и свидетельства каждого gate. Не переносить PASS из старых документов.
