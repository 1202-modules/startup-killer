# Развёртывание 02.10.2026

Игра доступна по http://104.171.139.202:8080. Каталог сервера: `/home/clubfest/startup-killer`.
Первая выкладка выполнена из checkout `feature/attack-model-v2` на базе `ddeef5c`, включая изменения восстановления завершённой партии и исправления PostgreSQL ниже.

## Хост и изоляция

- Linux x86_64, 2 vCPU, 3.8 GiB RAM; свободно около 30 GiB диска. Исходная load average около 8.2; CPU занят процессами пользователя timbqs.
- Уже работают Compose-проект `platypus_arena` (3001/3443), системные Nginx (80/443), PostgreSQL 14 (localhost:5432), PM2 (3000), PHP и несколько сайтов timbqs.ru.
- Новый Compose-проект `startup-killer`: собственные контейнеры, network `startup-killer_internal_net`, volume `startup-killer_postgres_data`. Наружу опубликован только web:8080; API/PostgreSQL доступны внутри сети.
- Docker inspect подтвердил лимиты: API 0.5 CPU/384 MiB, PostgreSQL 0.5 CPU/384 MiB, web 0.25 CPU/128 MiB; restart `unless-stopped`.
- `.env` создан на сервере с новыми случайными ключами, mode 600; каталог mode 700. Локальные env-файлы и базы не передавались.
- Образы собраны локально для linux/amd64 и загружены через SSH, сборка на сервере не выполнялась. Конфигурация остальных проектов не редактировалась.

## Исправления

- `backend/app/db/session.py`: глобальный listener выполнял SQLite PRAGMA на PostgreSQL, скрывая ошибку и оставляя аварийную транзакцию. Теперь он работает только с sync/async SQLite connections.
- `backend/alembic/versions/0002_deterministic_attack_choices.py`: revision ID не помещался в Alembic VARCHAR(32). Поле расширено до VARCHAR(64), прежние revision ID сохранены.
- Добавлены проверки SQLite listener и длины поля версии миграций.

## Выполненные проверки

- `python3 tools/spec_check.py`, `python3 tools/contract_lint.py`: PASS, 10 стартапов, 120 карточек, 30 fixtures.
- `python3 tools/verify_assets.py`: PASS, 30 WebP и 10 masters.
- `python3 -m pytest backend/tests -q`: 116 passed после исправления listener; после изменения миграции отдельно `python3 -m pytest backend/tests/test_alembic_migrations.py backend/tests/test_db_session.py -q`: 4 passed.
- `npm test -- --run`: 39 passed; `npm run build`: PASS.
- `docker build --platform linux/amd64` для API/web: PASS; `docker save --platform linux/amd64`, SCP и `docker load`: PASS.
- `docker compose config --quiet`: PASS; `docker compose up --no-build -d --wait --wait-timeout 90`: все три контейнера healthy.
- Реальная новая PostgreSQL 16 прошла upgrade от пустой схемы до `0003_multiple_browser_sessions`, загружены 10 стартапов.
- Внешний HTTP smoke: SPA/health/bootstrap, создание партии, три выбора и переходы, идемпотентный повтор выбора, восстановление результата раунда, финальный результат/рейтинг, новая партия после завершения — PASS. Проверочные партии удалены по созданной для проверки browser installation; после очистки 0 партий.
- Соседний `platypus` healthy, HTTP на localhost:3001 возвращает 200.
- `pg_dump -Fc` новой БД и `pg_restore --exit-on-error` в отдельную временную БД: PASS. В восстановленной копии revision 0003, 10 стартапов и 0 партий; временная БД удалена. Backup: `/home/clubfest/startup-killer/backups/initial-20261002.dump`, mode 600, 27 KiB.
- `git diff --check`: PASS.

## Измерения и ограничения

Три внешних запроса хода: 593.7 / 366.8 / 527.1 мс, включая сеть. Один снимок: Uvicorn RSS 93300 KiB; Docker memory API 70.44 MiB, PostgreSQL 41.91 MiB, web 3.133 MiB (RSS и cgroup memory являются разными метриками).

Это короткая функциональная проверка, не нагрузочный benchmark. Хост имеет 3.8 GiB, а не целевые 2 GiB, и уже загружен другими процессами; G4 не закрыт. Миграция старой production-БД не проводилась: создана новая отдельная БД. Визуальный browser acceptance и TLS/домен не выполнялись; адрес пока HTTP. npm ci сообщил 7 audit findings (5 moderate, 1 high, 1 critical), зависимости не обновлялись в этой задаче.

## Управление

```sh
ssh clubfest@104.171.139.202
cd /home/clubfest/startup-killer
docker compose ps
docker compose logs --tail 100 api
docker compose stop
docker compose up --no-build -d
```

`stop` относится только к этому Compose-проекту. Не удалять volume с БД; downgrade 0002 запрещён. Следующий этап: домен/TLS и bounded нагрузочная приёмка с учётом текущей загрузки хоста.

## Повторная выкладка и аудит 02.10.2026

- Перед обновлением создан `backups/pre-redeploy-20261002.dump` (mode 600, 554149 байт). `pg_restore --exit-on-error` во временную БД прошёл: revision `0003_multiple_browser_sessions`, 97 партий, 10 стартапов. Временная БД удалена; действующая БД не восстанавливалась.
- Локально пройдены `python3 tools/spec_check.py`, `python3 tools/contract_lint.py`, `python3 tools/verify_assets.py`, `python3 -m pytest backend/tests -q` (116 passed), `npm test -- --run` (41 passed), `npm run build` и `docker build --platform linux/amd64` для API и web. `tools/balance_simulation.py` прошёл 640 путей; локальный benchmark 1000 итераций: mean 0.3004 мс, p95 0.334 мс, peak RSS 31.73 MiB. Это измерение процесса на локальной машине, не хостовый benchmark.
- Образы переданы через SSH и загружены Docker, `docker compose up --no-build -d --wait --wait-timeout 90` завершился успешно. API, PostgreSQL и web имеют статус healthy. Внешние HTTP проверки SPA, API health, рейтинга и QR вернули 200; QR совпал с локальным файлом по SHA-256.
- В клиенте исправлены повторное использование ключа идемпотентности, сокрытие ошибки загрузки партии и отображение сообщения API при ошибке создания. Удалены неиспользуемые Axios, clsx, tailwind-merge, uuid, методы PATCH/DELETE и неработавший npm lint script.
- `npm audit --omit=dev`: 2 moderate по React Router; полный `npm audit`: 6 findings (4 moderate, 1 high, 1 critical), остальные связаны с инструментами сборки и тестов. Предлагаемые npm исправления требуют перехода на новые major-версии и не включены в эту выкладку.

Ограничения остаются: визуальная проверка браузером, TLS и нагрузочная проверка на целевых 2 vCPU/2 GiB не выполнялись; существующая БД не проходила миграцию 0002 в этой выкладке.
