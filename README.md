## Стуктура сервера
- `app/` — корневая директория FastAPI-сервера. Здесь храниться весь код cервера. Взял из документации [FastAPI](https://fastapi.tiangolo.com/tutorial/bigger-applications/?h=app)
- `app/__init__.py` — используется для импорта моделей SQLAlchemy в правильной последовательности
- `app/utils.py` — используется для `authx` (для работы с JWT)
- `app/redis.py` — файл для работы с `redis-клиентом`
- `app/main.py` — корневой файл сервера
- `app/dependencies.py` — зависимости сервера
- `app/database.py` — работа с сервером
- `app/config.py` — конфигурация и настройка переменных
- `app/users/` — слой для работы с пользователями. Содержит 3 файла:
  - `models.py` — SQLAlchemy-модели
  - `router.py` — роутер маршрута `/u` и обработчики для маршрутов
  - `schemas.py` — Pydantic-схемы для валидации данных
- `app/posts/` — слой для постов. Содержит 3 файла:
  - `models.py` — SQLAlchemy-модели
  - `router.py` — роутер маршрута `/u/{user_id}/p` и обработчики для маршрутов
  - `schemas.py` — Pydantic-схемы для валидации данных

Для запуска сервер используется `docker compose up --build`

## Инструкция запуска клиента
1. `cd frontend/`
2. `npm i` или `bun i`
3. Поменять в `src/App.vue` переменную `USER_ID` на созданного пользователя
4. `npm run dev` или `bun run dev`

_P.S. Нужно запустить сервер через `docker compose up --build`._
