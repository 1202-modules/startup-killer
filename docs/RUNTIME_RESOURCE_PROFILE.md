# Runtime resource profile

Игра не использует AI/LLM API, модели, provider keys или AI worker. Операция раунда — локальный расчёт детерминированного Python engine и запись транзакции БД. Остальная production схема: статическая SPA, один API-процесс и PostgreSQL.

Проектный ориентир — 2 vCPU / 2 GiB RAM. Документ не является измерением: целевой host benchmark и проверка соседней нагрузки остаются release gate.
