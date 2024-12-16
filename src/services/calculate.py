import logging
import uuid

from starlette.exceptions import HTTPException

from src.models.cadastral import CadastralParams
from src.models.messages import Messages
from src.models.runs import Status, RunType
from src.utils.kafka_client import KafkaAsyncClient


class CalculateService:
    def __init__(self):
        self.kafka_client = KafkaAsyncClient(external=True)

    async def process(self, data: CadastralParams):
        run_id = uuid.uuid4()
        params = {
            "latitude": data.latitude,
            "longitude": data.longitude,
        }
        message = Messages(
            run_id=str(run_id),
            cadastral_number=data.cadastral_number,
            params=params,
            status=Status.scheduled.value,
            run_type=RunType.calculate.value,
        )
        await self.message_to_broker(message)
        return run_id

    async def message_to_broker(self, msg: Messages):
        await self.kafka_client.get_producer()
        try:
            # Отправляем сообщение
            await self.kafka_client.send_message("score", msg.run_id, msg.model_dump())
            logging.info(f"Message sent to topic 'score' with key '{msg.run_id}': {msg.model_dump()}")
        except Exception as e:
            logging.info(f"Failed to send message: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            # Завершаем работу продюсера
            await self.kafka_client.stop_producer()
