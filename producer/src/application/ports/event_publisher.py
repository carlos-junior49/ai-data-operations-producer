# src/application/ports/event_publisher.py

from abc import ABC, abstractmethod
from typing import Sequence

from src.domain.entities.order_event import OrderEvent


class EventPublisher(ABC):
    @abstractmethod
    def publish(self, event: OrderEvent) -> None:
        ...  # pragma: no cover

    @abstractmethod
    def publish_batch(self, events: Sequence[OrderEvent]) -> None:
        ...  # pragma: no cover
