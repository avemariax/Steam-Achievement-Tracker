from pydantic import BaseModel
from typing import List, Optional

class Game(BaseModel):
    appid: int
    name: str
    playtime_forever_minutes: int
    playtime_2weeks_minutes: Optional[int] = None 
    img_icon_url: Optional[str] = None

    @property 
    def playtime_forever_hours(self) -> float:
        return round (self.playtime_forever_minutes / 60, 1)

class GamesResponse(BaseModel):
    steam_id: str
    game_count : int
    games: List[Game]