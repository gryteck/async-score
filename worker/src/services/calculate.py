import logging

import asyncio
import random

from worker.src.models.messages import Messages, Status
from worker.src.utils.kafka_client import KafkaAsyncClient


class CalculateService:
    def __init__(self):
        self.kafka_client = KafkaAsyncClient(external=True)

    async def process(self, msg: Messages):
        if msg.status == Status.scheduled.value:
            logging.warning(f"Recieved scheduled message run_id {msg.run_id}")
            await asyncio.sleep(random.randint(1, 16))

            result = round(random.uniform(-100, 100), 6)
            msg.result = result
            msg.status = Status.finished.value
            try:
                await self.kafka_client.get_producer()
                logging.warning(f"Sending message {msg}")
                await self.kafka_client.send_message("score", msg.run_id, msg.model_dump())
                logging.warning(f"Message {msg.run_id} sent successfully")
            except Exception as e:
                logging.exception(f"Failed to send message: {e}")
            finally:  # Завершаем работу продюсера
                await self.kafka_client.stop_producer()
        else:
            logging.warning(f"Recieved not scheduled message run_id {msg.run_id}")
