# src/domain/entities/order_event.py

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from src.domain.enums.event_type import EventType


@dataclass(frozen=True)
class OrderEvent:
    event_id: str
    event_type: EventType
    event_version: str
    timestamp: datetime
    order_id: str
    customer_id: str
    product_id: str
    quantity: int
    unit_price: Decimal
    total_amount: Decimal

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "event_version": self.event_version,
            "timestamp": self.timestamp.isoformat(),
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": float(self.unit_price),
            "total_amount": float(self.total_amount)
        }
