import json

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from src.core.config import settings
from src.models.messages import Messages
from src.services.logs import LogsService
from src.services.runs import RunsService

BROKERS_EXTERNAL = [
    settings.KAFKA_BROKER_0,
    settings.KAFKA_BROKER_1,
    settings.KAFKA_BROKER_2,
]
BROKERS_INTERNAL = [
    settings.KAFKA_BROKER_0_LISTEN,
    settings.KAFKA_BROKER_1_LISTEN,
    settings.KAFKA_BROKER_2_LISTEN,
]


class KafkaAsyncClient:
    def __init__(self, external: bool = False):  # False for internal brokers
        self.servers = BROKERS_EXTERNAL if external else BROKERS_INTERNAL
        self.consumer = None
        self.producer = None
        self.logs_service = LogsService()
        self.run_service = RunsService()

    async def get_consumer(self, topic, offset: str = "earliest", group_id=None):
        """
        "earliest" - считывание с начала темы
        "latest" - с последнего сообщения
        Передаем group_id для сохранения смещений между перезапусками
        """
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=self.servers,
            auto_offset_reset=offset,
            consumer_timeout_ms=500,
            group_id=group_id,
            enable_auto_commit=True,  # Enable auto commit for simplicity
            heartbeat_interval_ms=30000,  # Adjust as needed
            session_timeout_ms=60000,  # Adjust as needed
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )
        await self.consumer.start()
        return self.consumer

    async def consume_messages(self):
        async for msg in self.consumer:
            msg = json.loads(msg.value)
            message = Messages(**msg)
            await self.logs_service.add_from_kafka(message)
            await self.run_service.add_from_kafka(message)
            print(f"Получено сообщение: {msg.value.decode('utf-8')}")

    async def stop_consumer(self):
        if self.consumer:
            await self.consumer.stop()

    async def get_producer(self):
        """
        Создание продюсера Kafka.
        """
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await self.producer.start()
        return self.producer

    async def send_message(self, topic: str, key, message: dict):
        """
        Отправка сообщения в Kafka.
        :param topic: Название топика
        :param key: Ключ сообщения
        :param message: Сообщение в формате dict
        """
        if not self.producer:
            raise RuntimeError("Producer is not initialized. Call get_producer first.")

        await self.producer.send_and_wait(
            topic,
            key=str(key).encode("utf-8"),
            value=message
        )

    async def stop_producer(self):
        if self.producer:
            await self.producer.stop()
