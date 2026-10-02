# Задачи реализации

- [x] T01 Предстартовые нормативные документы и baseline проверки.
- [x] T02 Каталог 120 карточек и schema/engine adapter.
- [x] T03 Race-safe synchronous API, session snapshots, idempotency и миграция очистки.
- [x] T04 UI выбора карточки и восстановления синхронного результата.
- [x] T05 Удалить runtime AI, очередь/worker, провайдеры, админку и свободный ввод.
- [x] T06 Exhaustive reachable path analysis, benchmark и `BALANCE_REPORT.md`.
- [x] T07 Обновить нормативную документацию и финальные статические acceptance checks: G0 и asset verification PASS.
- [x] T08 Выполнить полный локальный acceptance и residual audit: backend 100 passed, web 35 passed + build; независимый review запрошен.
- [ ] T09 Отдельно проверить развёртывание и миграцию на целевом хосте после подготовки backup и явной задачи на deployment.
  - 02.10.2026: новый отдельный экземпляр развёрнут, HTTP smoke и backup/restore прошли; целевой benchmark 2 vCPU/2 GiB и legacy production migration не закрыты. См. `DEPLOYMENT_2026-10-02.md`.
- [x] T10 V2 для всех десяти каталогов: явные эффекты, причинные комбо и защиты, 640 путей, локальные проверки и три независимые проверки GPT-6 Luna High. Баланс остаётся продуктовым решением владельца.

Команды и результаты отмечать только после исполнения; наличие документа не равно пройденному gate.
