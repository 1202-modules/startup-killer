# Архитектура

React + TypeScript + Vite SPA получает данные через FastAPI `/api/v1`. TanStack Query хранит server state; Zustand ограничен локальными UI-настройками. Tailwind задаёт стили; Framer Motion отвечает за необязательное движение и учитывает reduced motion.

FastAPI проверяет cookie, CSRF, Origin, idempotency и право на сессию. Для действия он разрешает ID карточки из session snapshot, запускает общий Python engine, записывает результат/ledger и рейтинг в SQLAlchemy-транзакции. PostgreSQL хранит игровые и финансовые данные. Runtime AI, provider adapters, фоновые jobs и административная подсистема отсутствуют.

В production раздаётся статическая сборка SPA и API через Nginx. У изображений и сцен browser-only исполнение; сервер не создаёт медиа.
