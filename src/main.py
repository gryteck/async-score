import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api import calculate
from src.utils.kafka_client import KafkaAsyncClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Настройка Kafka потребителя
    kafka_client = KafkaAsyncClient(external=False)
    consumer = await kafka_client.get_consumer("score", group_id="score_api")

    # Запуск задачи потребления сообщений
    consumer_task = asyncio.create_task(kafka_client.consume_messages())
    try:
        yield  # Приложение готово
    finally:
        # Завершение задач и ресурсов
        consumer_task.cancel()
        await consumer.stop()


app = FastAPI(
    title="score_api",
    docs_url="/docs",
    openapi_url="/src/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(calculate.router, prefix="", tags=["calculate"])

if __name__ == "__main__":
    import logging
    from core.logger import LOGGING

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
