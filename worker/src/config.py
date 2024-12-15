from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    KAFKA_BROKER_0: str = Field("localhost:9094", alias="KAFKA_BROKER_0")
    KAFKA_BROKER_1: str = Field("localhost:9095", alias="KAFKA_BROKER_1")
    KAFKA_BROKER_2: str = Field("localhost:9096", alias="KAFKA_BROKER_2")
    KAFKA_BROKER_0_LISTEN: str = Field("kafka-0:9092", alias="KAFKA_BROKER_0_LISTEN")
    KAFKA_BROKER_1_LISTEN: str = Field("kafka-1:9092", alias="KAFKA_BROKER_1_LISTEN")
    KAFKA_BROKER_2_LISTEN: str = Field("kafka-2:9092", alias="KAFKA_BROKER_2_LISTEN")


settings = Settings()
