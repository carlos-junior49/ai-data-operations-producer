# src/domain/generators/order_event_generator.py

from datetime import datetime, timezone
from decimal import Decimal
from random import choice, randint
from uuid import uuid4

from src.domain.entities.order_event import OrderEvent
from src.domain.enums.event_type import EventType


class OrderEventGenerator:
    _PRODUCTS = (
        ("PROD-001", Decimal("49.90")),
        ("PROD-002", Decimal("99.90")),
        ("PROD-003", Decimal("149.90")),
        ("PROD-004", Decimal("299.90"))
    )

    def generate(self) -> OrderEvent:
        product_id, unit_price = choice(self._PRODUCTS)
        quantity = randint(1, 10)

        return OrderEvent(
            event_id=str(uuid4()),
            event_type=EventType.ORDER_CREATED,
            event_version="1.0",
            timestamp=datetime.now(timezone.utc),
            order_id=self._generate_order_id(),
            customer_id=self._generate_customer_id(),
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            total_amount=unit_price * quantity
        )

    @staticmethod
    def _generate_order_id() -> str:
        return f"ORD-{str(uuid4().hex[:12].upper())}"

    @staticmethod
    def _generate_customer_id() -> str:
        return f"CUS-{randint(10000, 99999)}"
