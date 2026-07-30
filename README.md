# Steam-Achievement-Tracker
Бэкенд-сервис для трекинга ачивок Steam.

Сервис стоит между Steam Web API и клиентом (будущим фронтендом/ботом), отдаёт нормализованные данные об играх и достижениях в удобном JSON.

## Стек

- **FastAPI** — веб-фреймворк, роутинг и валидация запросов
- **httpx (async)** — асинхронные запросы к Steam Web API
- **Pydantic** — схемы данных и валидация
- **PostgreSQL + SQLAlchemy** — планируется для кэширования (в разработке)

## Текущие эндпоинты

### `GET /games/{steam_id}`
Возвращает список игр пользователя с временем игры.
**Пример:**
GET /games/76561198378551634

### `GET /games/{app_id}/achievements?steam_id=XXX`
Возвращает список достижений пользователя в конкретной игре: какие получены, названия, описания, иконки, процент завершения.
**Пример:**
GET /games/105600/achievements?steam_id=76561198378551634

## Установка и запуск
1. Клонируй репозиторий:
git clone https://github.com/avemariax/Steam-Achievement-Tracker
cd Steam-Achievement-Tracker
2. Создай и активируй виртуальное окружение(не обязательно):
python -m venv venv
venv\Scripts\Activate.ps1 (Windows Powershell)
3. Установи зависимости:
pip install -r requirements.txt
4. Скопируй `.env.example` в `.env` и впиши свой Steam API ключ:
STEAM_API_KEY=твой_ключ
STEAM_API_BASE=https://api.steampowered.com
5. Запусти сервер:
uvicorn app.main:app --reload
6. Открой документацию API: http://127.0.0.1:8000/docs

## Как получить Steam API ключ

1. Зайди на https://steamcommunity.com/dev/apikey
2. Зарегистрируй домен (можно `localhost`)
3. Скопируй ключ в `.env`

**Важно:** профиль Steam, для которого делаешь запросы должен быть публичным (Настройки -> Приватность -> Игровые данные -> Публично), иначе Steam вернёт ошибку доступа.

## Планы развития

- [ ] Кэширование в PostgreSQL через SQLAlchemy
- [ ] Эндпоинт `GET /users/{steam_id}/rarest` — самые редкие ачивки в библиотеке
- [ ] Эндпоинт `GET /users/{steam_id}/summary` — сводка по всем играм
- [ ] Фоновая синхронизация (APScheduler / Celery)
- [ ] Деплой на Railway

# Steam-Achievement-Tracker
A backend service for tracking Steam achievements.

The service stay between the Steam Web API and a client (future frontend/bot), serving normalized data about games and achievements as clean JSON.

## Tech Stack

- **FastAPI** — web framework, routing and request validation
- **httpx (async)** — asynchronous requests to the Steam Web API
- **Pydantic** — data schemas and validation
- **PostgreSQL + SQLAlchemy** — planned for caching (in progress)

## Current Endpoints

### `GET /games/{steam_id}`
Returns a list of the user's owned games with playtime.
**Example:**
GET /games/76561198378551634

### `GET /games/{app_id}/achievements?steam_id=XXX`
Returns the user's achievements for a specific game: unlocked status, names, descriptions, icons, and completion percentage.
**Example:**
GET /games/105600/achievements?steam_id=76561198378551634
## Setup & Running

1. Clone the repository:
git clone https://github.com/avemariax/Steam-Achievement-Tracker
cd Steam-Achievement-Tracker
2. Create and activate a virtual environment:
python -m venv venv
venv\Scripts\Activate.ps1 (Windows PowerShell)
3. Install dependencies:
pip install -r requirements.txt
4. Copy `.env.example` to `.env` and add your Steam API key:
STEAM_API_KEY=your_key_here
STEAM_API_BASE=https://api.steampowered.com
5. Run the server:
uvicorn app.main:app --reload
6. Open the API docs: http://127.0.0.1:8000/docs

## Getting a Steam API Key

1. Go to https://steamcommunity.com/dev/apikey
2. Register a domain (`localhost` works fine)
3. Copy the key into `.env`

**Note:** the Steam profile you're querying must have its game details set to public (Settings -> Privacy -> Game details -> Public), otherwise Steam will return an access error.

## Roadmap

- [ ] PostgreSQL caching via SQLAlchemy
- [ ] `GET /users/{steam_id}/rarest` — rarest achievements in the library
- [ ] `GET /users/{steam_id}/summary` — summary across all games
- [ ] Background sync (APScheduler / Celery)
- [ ] Deployment on Railway
