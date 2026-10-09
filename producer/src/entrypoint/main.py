# src/entrypoint/main.py

import logging
import time
from src.application.services.event_producer_service import EventProducerService
from src.config.settings import Settings
from src.domain.generators.order_event_generator import OrderEventGenerator
from src.infrastructure.kinesis.kinesis_client import KinesisClient
from src.infrastructure.kinesis.kinesis_event_publisher import KinesisEventPublisher

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s | %(message)s')
logger = logging.getLogger(__name__)

def create_producer_service(settings: Settings) -> EventProducerService:
    kinesis_client = KinesisClient(settings.aws_region)
    event_publisher = KinesisEventPublisher(kinesis_client, settings.kinesis_stream_name)
    return EventProducerService(event_publisher)


def main() -> None:
    settings = Settings.from_environment()
    event_generator = OrderEventGenerator()
    producer_service = create_producer_service(settings)
    logger.info(
        "Producer started | stream=%s | rate=%s events/s | batch=%s",
        settings.kinesis_stream_name,
        settings.event_rate,
        settings.batch_size
    )

    while True:
        events = [
            event_generator.generate() for _ in range(settings.batch_size)
        ]

        producer_service.publish_batch(events)
        logger.info(
            "Published %s events",
            len(events)
        )

        time.sleep(settings.batch_size / settings.event_rate)


if __name__ == "__main__":
    main()
