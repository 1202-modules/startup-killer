# Локальный offline validation report

Это сводка локальных проверок; не доказывает production deployment, целевой host performance или PostgreSQL migration на production данных.

- `data/startups.json`: 10 заданных паспортов.
- `data/economy_golden_cases.json`: 30 числовых сценариев прежней экономики.
- `data/attack_choices.json`: 120 карточек, 4 на startup/round; strict JSON schema.
- `BALANCE_REPORT.md`: исчерпывающий перебор достижимых путей и локальный движок benchmark.
- Backend migration/API tests проверяют scrub/preservation на тестовой БД; web tests/build — локальную сборку.

В финальном acceptance report указать реальные команды, число тестов, build и asset checks. Production acceptance выполнять отдельно.
