from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Steam API key 
    steam_api_key: str
    steam_api_base: str = "https://api.steampowered.com"

    class Config:
        env_file = ".env"

settings = Settings()

