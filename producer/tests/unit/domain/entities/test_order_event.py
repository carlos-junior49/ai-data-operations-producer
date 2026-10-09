import pytest
from datetime import datetime
from decimal import Decimal

from src.domain.entities.order_event import OrderEvent
from src.domain.enums.event_type import EventType


class TestOrderEvent:

    def test_init(self):
        """Test OrderEvent initialization"""
        timestamp = datetime.now()
        event = OrderEvent(
            event_id="evt-123",
            event_type=EventType.ORDER_CREATED,
            event_version="1.0",
            timestamp=timestamp,
            order_id="ord-456",
            customer_id="cust-789",
            product_id="prod-101",
            quantity=2,
            unit_price=Decimal("10.50"),
            total_amount=Decimal("21.00")
        )
        assert event.event_id == "evt-123"
        assert event.event_type == EventType.ORDER_CREATED
        assert event.event_version == "1.0"
        assert event.timestamp == timestamp
        assert event.order_id == "ord-456"
        assert event.customer_id == "cust-789"
        assert event.product_id == "prod-101"
        assert event.quantity == 2
        assert event.unit_price == Decimal("10.50")
        assert event.total_amount == Decimal("21.00")

    def test_to_dict(self):
        """Test to_dict method converts all fields correctly"""
        timestamp = datetime(2024, 1, 15, 10, 30, 45)
        event = OrderEvent(
            event_id="evt-123",
            event_type=EventType.ORDER_CREATED,
            event_version="1.0",
            timestamp=timestamp,
            order_id="ord-456",
            customer_id="cust-789",
            product_id="prod-101",
            quantity=2,
            unit_price=Decimal("10.50"),
            total_amount=Decimal("21.00")
        )

        result = event.to_dict()

        assert result == {
            "event_id": "evt-123",
            "event_type": "ORDER_CREATED",
            "event_version": "1.0",
            "timestamp": "2024-01-15T10:30:45",
            "order_id": "ord-456",
            "customer_id": "cust-789",
            "product_id": "prod-101",
            "quantity": 2,
            "unit_price": 10.50,
            "total_amount": 21.00
        }

    def test_to_dict_with_order_paid(self):
        """Test to_dict with ORDER_PAID event type"""
        timestamp = datetime.now()
        event = OrderEvent(
            event_id="evt-456",
            event_type=EventType.ORDER_PAID,
            event_version="2.0",
            timestamp=timestamp,
            order_id="ord-789",
            customer_id="cust-123",
            product_id="prod-456",
            quantity=1,
            unit_price=Decimal("100.00"),
            total_amount=Decimal("100.00")
        )

        result = event.to_dict()

        assert result["event_type"] == "ORDER_PAID"
        assert result["event_id"] == "evt-456"

    def test_to_dict_with_order_cancelled(self):
        """Test to_dict with ORDER_CANCELLED event type"""
        timestamp = datetime.now()
        event = OrderEvent(
            event_id="evt-789",
            event_type=EventType.ORDER_CANCELLED,
            event_version="1.0",
            timestamp=timestamp,
            order_id="ord-123",
            customer_id="cust-456",
            product_id="prod-789",
            quantity=5,
            unit_price=Decimal("25.00"),
            total_amount=Decimal("125.00")
        )

        result = event.to_dict()

        assert result["event_type"] == "ORDER_CANCELLED"

    def test_to_dict_with_order_shipped(self):
        """Test to_dict with ORDER_SHIPPED event type"""
        timestamp = datetime.now()
        event = OrderEvent(
            event_id="evt-101",
            event_type=EventType.ORDER_SHIPPED,
            event_version="1.0",
            timestamp=timestamp,
            order_id="ord-202",
            customer_id="cust-303",
            product_id="prod-404",
            quantity=3,
            unit_price=Decimal("50.00"),
            total_amount=Decimal("150.00")
        )

        result = event.to_dict()

        assert result["event_type"] == "ORDER_SHIPPED"

    def test_to_dict_with_order_delivered(self):
        """Test to_dict with ORDER_DELIVERED event type"""
        timestamp = datetime.now()
        event = OrderEvent(
            event_id="evt-202",
            event_type=EventType.ORDER_DELIVERED,
            event_version="1.0",
            timestamp=timestamp,
            order_id="ord-303",
            customer_id="cust-404",
            product_id="prod-505",
            quantity=1,
            unit_price=Decimal("75.00"),
            total_amount=Decimal("75.00")
        )

        result = event.to_dict()

        assert result["event_type"] == "ORDER_DELIVERED"

    def test_frozen_dataclass_cannot_modify(self):
        """Test that frozen dataclass cannot be modified after creation"""
        timestamp = datetime.now()
        event = OrderEvent(
            event_id="evt-123",
            event_type=EventType.ORDER_CREATED,
            event_version="1.0",
            timestamp=timestamp,
            order_id="ord-456",
            customer_id="cust-789",
            product_id="prod-101",
            quantity=2,
            unit_price=Decimal("10.50"),
            total_amount=Decimal("21.00")
        )

        with pytest.raises(Exception):  # FrozenInstanceError
            event.event_id = "new-id"

    def test_decimal_conversion_to_float(self):
        """Test that Decimal values are converted to float in to_dict"""
        timestamp = datetime.now()
        event = OrderEvent(
            event_id="evt-123",
            event_type=EventType.ORDER_CREATED,
            event_version="1.0",
            timestamp=timestamp,
            order_id="ord-456",
            customer_id="cust-789",
            product_id="prod-101",
            quantity=2,
            unit_price=Decimal("99.99"),
            total_amount=Decimal("199.98")
        )

        result = event.to_dict()

        assert isinstance(result["unit_price"], float)
        assert isinstance(result["total_amount"], float)
        assert result["unit_price"] == 99.99
        assert result["total_amount"] == 199.98

    def test_timestamp_iso_format(self):
        """Test that timestamp is converted to ISO format string"""
        timestamp = datetime(2024, 12, 25, 23, 59, 59)
        event = OrderEvent(
            event_id="evt-123",
            event_type=EventType.ORDER_CREATED,
            event_version="1.0",
            timestamp=timestamp,
            order_id="ord-456",
            customer_id="cust-789",
            product_id="prod-101",
            quantity=1,
            unit_price=Decimal("10.00"),
            total_amount=Decimal("10.00")
        )

        result = event.to_dict()

        assert result["timestamp"] == "2024-12-25T23:59:59"
        assert isinstance(result["timestamp"], str)