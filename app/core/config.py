import os
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum
from dotenv import load_dotenv


class ModeEnum(str, Enum):
    development = "development"
    production = "production"
    testing = "testing"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    PROJECT_NAME: str = "app"
    BACKEND_CORS_ORIGINS: list[str] | list[AnyHttpUrl]
    MODE: ModeEnum = ModeEnum.development
    API_VERSION: str = "v1"
    API_PREFIX: str = "/api"
    OPENAI_API_KEY: str
    UNSPLASH_API_KEY: str
    SERP_API_KEY: str
    AZURE_OPENAI_API_KEY: str
    APP_AK: str
    APP_SK: str
    APP_APP_ID: str
    ZHIPUAI_API_KEY: str

    # class Config:
    #     case_sensitive = True
    #     env_file = os.path.expanduser(".env")


load_dotenv(os.path.expanduser(".env"))
load_dotenv() #Pycharm2022
settings = Settings()
