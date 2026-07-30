import httpx
from fastapi import HTTPException
from app.config import settings


class SteamClient:
    def __init__(self):
        self.base = settings.steam_api_base
        self.key = settings.steam_api_key
        self.headers = {"User-Agent": "Mozilla/5.0"}\

    async def get_owned_games(self, steam_id: str) -> dict:
        url = f"{self.base}/IPlayerService/GetOwnedGames/v0001/"
        params = {
            "key": self.key,
            "steamid": steam_id,
            "include_appinfo": True,
            "include_played_free_games": True,
            "format": "json",
        }

        async with httpx.AsyncClient(timeout=10.0, headers=self.headers) as client:
            resp = await client.get(url, params=params)

        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail="Steam API недоступен")

        data = resp.json().get("response", {})
        if not data:
            raise HTTPException(
                status_code=404,
                detail="Профиль приватный или Steam ID не найден"
            )
        return data

    async def get_player_achievements(self, steam_id: str, appid: int) -> dict:
        url = f"{self.base}/ISteamUserStats/GetPlayerAchievements/v0001/"
        params = {
            "key": self.key,
            "steamid": steam_id,
            "appid": appid,
            "format": "json",
        }

        async with httpx.AsyncClient(timeout=10.0, headers=self.headers) as client:
            resp = await client.get(url, params=params)

        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail="Steam API недоступен")

        data = resp.json().get("playerstats", {})
        if not data.get("success", False):
            raise HTTPException(
                status_code=404,
                detail="Достижения не найдены (игра без ачивок или приватный профиль)"
            )
        return data

    async def get_global_achievements(self, appid: int) -> dict:
        url = f"{self.base}/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/"
        params = {
            "gameid": appid,
            "format": "json",
        }

        async with httpx.AsyncClient(timeout=10.0, headers=self.headers) as client:
            resp = await client.get(url, params=params)

        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail="Steam API недоступен")

        data = resp.json().get("achievementpercentages", {})
        return data

    async def get_game_schema(self, appid: int) -> dict:
        url = f"{self.base}/ISteamUserStats/GetSchemaForGame/v0002/"
        params = {
            "key": self.key,
            "appid": appid,
            "format": "json",
        }

        async with httpx.AsyncClient(timeout=10.0, headers=self.headers) as client:
            resp = await client.get(url, params=params)

        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail="Steam API недоступен")

        data = resp.json().get("game", {})
        return data


steam_client = SteamClient()