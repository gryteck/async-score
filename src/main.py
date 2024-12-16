import asyncio
from contextlib import asynccontextmanager
import logging
from threading import Thread, Event

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api import calculate
from src.utils.kafka_client import KafkaAsyncClient

stop_event = Event()


def kafka_consumer_thread(stop_event: Event):
    """
    Функция для запуска Kafka-консьюмера в отдельном потоке.
    """
    logging.info("Starting Kafka consumer thread")

    async def consume():
        kafka_client = KafkaAsyncClient(external=True)
        consumer = await kafka_client.get_consumer(["score"], group_id="score_api")

        try:
            while not stop_event.is_set():
                # Обработка сообщений
                await kafka_client.consume_messages()
        except Exception as e:
            logging.error(f"Error in Kafka consumer: {e}")
        finally:
            logging.info("Stopping Kafka consumer")
            await consumer.stop()

    # Запуск асинхронной задачи
    asyncio.run(consume())


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Настройка Kafka потребителя
    global stop_event
    logging.info("Initializing lifespan")

    # Запуск Kafka-консьюмера в отдельном потоке
    kafka_thread = Thread(target=kafka_consumer_thread, args=(stop_event,))
    kafka_thread.start()
    logging.info("Kafka consumer thread started")

    # kafka_client = KafkaAsyncClient(external=True)
    # logging.info("Getting kafka consumer")
    # consumer = await kafka_client.get_consumer(["score", ], group_id="score_api")
    #
    # # Запуск задачи потребления сообщений
    # consumer_task = asyncio.create_task(kafka_client.consume_messages())
    try:
        yield  # Приложение готово
    finally:
        logging.info("Shutting down Kafka consumer thread")
        stop_event.set()  # Сигнализируем потоку завершить работу
        kafka_thread.join()  # Ждем завершения потока
        logging.info("Kafka consumer thread stopped")
        # Завершение задач и ресурсов
        # consumer_task.cancel()
        # await consumer.stop()


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
        port=81,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
