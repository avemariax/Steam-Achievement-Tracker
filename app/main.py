from fastapi import FastAPI
from app.services.steam_client import steam_client
from app.schemas import GamesResponse, Game

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
