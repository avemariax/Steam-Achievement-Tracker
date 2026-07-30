from fastapi import FastAPI
from app.services.steam_client import steam_client
from app.schemas import GamesResponse, Game, AchievementsResponse, Achievement

app = FastAPI(title="Steam Achievement Tracker")

@app.get("/games/{steam_id}", response_model=GamesResponse)
async def get_user_games(steam_id: str):
    raw = await steam_client.get_owned_games(steam_id)

    games = [
        Game(
            appid=game["appid"],
            name=game["name"],
            playtime_forever_minutes=game.get("playtime_forever", 0),
            playtime_2weeks_minutes=game.get("playtime_2weeks"),
            img_icon_url=game.get("img_icon_url")
        )
        for game in raw.get("games", [])
    ]

    return GamesResponse(
        steam_id=steam_id,
        game_count=raw.get("game_count", 0),
        games=games
    )

@app.get("/games/{app_id}/achievements", response_model=AchievementsResponse)
async def get_game_achievements(app_id: int, steam_id: str):
    player_data = await steam_client.get_player_achievements(steam_id, app_id)
    schema_data = await steam_client.get_game_schema(app_id)

    # Собираем "справочник" ачивок из схемы игры: apiname -> детали
    schema_lookup = {
        item["name"]: item
        for item in schema_data.get("availableGameStats", {}).get("achievements", [])
    }

    achievements = []
    for ach in player_data.get("achievements", []):
        details = schema_lookup.get(ach["apiname"], {})
        achievements.append(
            Achievement(
                api_name=ach["apiname"],
                name=details.get("displayName", ach["apiname"]),
                description=details.get("description"),
                achieved=bool(ach["achieved"]),
                unlock_time=ach.get("unlocktime"),
                icon=details.get("icon"),
                icon_gray=details.get("icongray"),
            )
        )

    completed = sum(1 for a in achievements if a.achieved)
    total = len(achievements)
    percent = round((completed / total) * 100, 1) if total > 0 else 0.0

    return AchievementsResponse(
        steam_id=steam_id,
        app_id=app_id,
        total_achievements=total,
        completed_achievements=completed,
        completion_percentage=percent,
        achievements=achievements,
    )