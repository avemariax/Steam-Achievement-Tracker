import httpx 
from fastapi import HTTPException
from app.config import settings

class SteamClient:
    def __init__(self):
        self.base = settings.steam_api_base
        self.key = settings.steam_api_key

    async def get_owned_games(self, steam_id: str) -> dict:
        url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
        params = {
            "key": self.key,
            "steamid": steam_id,
            "include_appinfo": True,
            "include_played_free_games": True,
            "format": "json"
        }


        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params)

        print("FULL URL:", resp.url)
        print("STATUS: ", resp.status_code)
        print("BODY: ", resp.text)

        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail="STEAM API Недоступен")

        data = resp.json().get("response", {})
        if not data: 
            # If the response is empty, return an empty dictionary
            raise HTTPException( 
                status_code=404, 
                detail="Профиль приватный или Steam ID не найден"
            )
        return data


steam_client = SteamClient()
        