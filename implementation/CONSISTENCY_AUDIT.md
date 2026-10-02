# Consistency audit — deterministic catalog

Проверяемые инварианты: десять startup seeds; 4 карточки на раунд на startup; каталог версии фиксируется в session snapshot; клиент передаёт только choice ID; вся экономика проходит `simulate_round`; рейтинг использует сохранённые server ledger. Database migration scrubs прежние raw attack/model outputs, сохраняя resolved ledger. Провайдерские, очередные и админские контракты удалены.

Аудит артефактов и локальные результаты фиксируются в `OFFLINE_VALIDATION_REPORT.md`; не переносить статический PASS на production readiness.
