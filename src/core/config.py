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
    POSTGRES_USER: str = Field("user", alias='POSTGRES_USER')
    POSTGRES_PASSWORD: str = Field("password", alias='POSTGRES_PASSWORD')
    POSTGRES_DB: str = Field("database", alias='POSTGRES_DB')

    KAFKA_BROKER_0: str = Field("localhost:9094", alias="KAFKA_BROKER_0")
    KAFKA_BROKER_1: str = Field("localhost:9095", alias="KAFKA_BROKER_1")
    KAFKA_BROKER_2: str = Field("localhost:9096", alias="KAFKA_BROKER_2")
    KAFKA_BROKER_0_LISTEN: str = Field("score_kafka_0:9092", alias="KAFKA_BROKER_0_LISTEN")
    KAFKA_BROKER_1_LISTEN: str = Field("score_kafka_1:9092", alias="KAFKA_BROKER_1_LISTEN")
    KAFKA_BROKER_2_LISTEN: str = Field("score_kafka_2:9092", alias="KAFKA_BROKER_2_LISTEN")

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
