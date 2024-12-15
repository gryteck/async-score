import asyncio
import random

from worker.src.models.messages import Messages, Status
from worker.src.utils.kafka_client import KafkaAsyncClient


class CalculateService:
    def __init__(self):
        self.kafka_client = KafkaAsyncClient(external=True)

    async def process(self, msg: Messages):
        if msg.status == Status.scheduled.value:
            await asyncio.sleep(random.randint(1, 16))

            result = round(random.uniform(-100, 100), 6)
            msg.result = result
            msg.status = Status.finished.value
            try:
                await self.kafka_client.get_producer()
                await self.kafka_client.send_message("score", msg.run_id, msg.model_dump())
            except Exception as e:
                print(f"Failed to send message: {e}")
            finally:  # Завершаем работу продюсера
                await self.kafka_client.stop_producer()
