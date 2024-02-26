from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Config(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017/"
    secret_key: str = "default_secret_key"
    algorithm: str = "default_algorithm"
    salt: str = "default_salt"
    db_name: str = "default_db_name"
    env_loaded: bool = False,
    access_token_expire_minutes: int = 10

    # class Config:
    #     env_file = ".env"
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_config():
    return Config()