import asyncio
import logging

from worker.src.utils.kafka_client import KafkaAsyncClient
from worker.src.services.calculate import CalculateService
from worker.src.models.messages import Messages

calculate_service = CalculateService()


async def main():
    logging.warning("Connecting to Kafka server...")
    kafka_client = KafkaAsyncClient(external=True)

    logging.warning("Getting consumer...")
    consumer = await kafka_client.get_consumer(["score", ], group_id="score_worker")
    try:
        logging.warning("Program successfully started.")
        async for msg in consumer:
            logging.warning(f"Recieved message on topic {msg.topic}, {msg}")

            if msg:
                msg = Messages(**msg.value)
                logging.warning(f"Started processing message {msg.run_id}")
                await calculate_service.process(msg)
            await asyncio.sleep(1)

        logging.warning("Closing Kafka server...")
    except Exception:
        consumer.close()


if __name__ == "__main__":
    asyncio.run(main())
