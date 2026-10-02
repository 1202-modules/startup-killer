# План ресурсных измерений

Production ориентир: 2 vCPU / 2 GiB RAM. Локальный `tools/load_test_benchmark.py` измеряет только синхронную детерминированную операцию движка; он не моделирует БД, сеть, соседние процессы или production SPA.

На целевом host снять базовый RSS/CPU и системный запас; затем ограниченным параллелизмом измерить реальный API round latency, RSS процесса API и PostgreSQL, ошибки/таймауты. Записать число итераций, hardware/container limits, p50/p95/max и RSS. Повторить после миграции с representative DB snapshot. Не выводить 100-пользовательскую capacity из локального engine microbenchmark.
