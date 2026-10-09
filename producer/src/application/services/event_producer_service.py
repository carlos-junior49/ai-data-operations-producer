# src.application/services/event_producer_service.py

from typing import Sequence

from src.application.ports.event_publisher import EventPublisher
from src.domain.entities.order_event import OrderEvent


class EventProducerService:
    def __init__(self, publisher: EventPublisher):
        self._publisher = publisher

    def publish(self, event: OrderEvent):
        self._publisher.publish(event)

    def publish_batch(self, events: Sequence[OrderEvent]):
        if not events:
            return
        self._publisher.publish_batch(events)
