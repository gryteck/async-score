import pathlib

from dotenv import dotenv_values
from pydantic import Field
from pydantic_settings import BaseSettings

env_path = pathlib.Path(__file__).cwd().parent.parent / '.env'
env_values = dotenv_values(env_path)

if not env_values:
    print(f"Warning: No environment variables loaded from {env_path}")


class Settings(BaseSettings):
    app_name: str = Field('API кинотеатра', alias='APP_NAME')

    POSTGRES_HOST: str = Field("127.0.0.1", alias='POSTGRES_HOST')
    POSTGRES_PORT: int = Field(5432, alias='POSTGRES_PORT')
    POSTGRES_USER: str = Field("olap", alias='POSTGRES_USER')
    POSTGRES_PASSWORD: str = Field("0LzyD7vnZ3", alias='POSTGRES_PASSWORD')
    POSTGRES_DB: str = Field("cup", alias='POSTGRES_DB')

    @property
    def POSTGRES_URL(self):
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


settings = Settings()
