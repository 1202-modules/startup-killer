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
Пока не пройден. Требуется реальный benchmark 2 vCPU/2 GiB и фактическая миграция с заранее проверенным backup. Этот проект локально не развёртывался.

## Отчёт
Фиксировать статус и свидетельства каждого gate. Не переносить PASS из старых документов.
