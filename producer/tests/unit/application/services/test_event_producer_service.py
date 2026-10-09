import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime
from decimal import Decimal

from src.application.services.event_producer_service import EventProducerService
from src.application.ports.event_publisher import EventPublisher
from src.domain.entities.order_event import OrderEvent
from src.domain.enums.event_type import EventType


class TestEventProducerService:

    def test_init(self):
        """Test service initialization with publisher"""
        mock_publisher = Mock(spec=EventPublisher)
        service = EventProducerService(mock_publisher)
        assert service._publisher == mock_publisher

    def test_publish(self):
        """Test publishing a single event"""
        mock_publisher = Mock(spec=EventPublisher)
        service = EventProducerService(mock_publisher)

        event = OrderEvent(
            event_id="evt-123",
            event_type=EventType.ORDER_CREATED,
            event_version="1.0",
            timestamp=datetime.now(),
            order_id="ord-456",
            customer_id="cust-789",
            product_id="prod-101",
            quantity=2,
            unit_price=Decimal("10.50"),
            total_amount=Decimal("21.00")
        )

        service.publish(event)

        mock_publisher.publish.assert_called_once_with(event)

    def test_publish_batch_with_empty_list(self):
        """Test publishing batch with empty list returns early"""
        mock_publisher = Mock(spec=EventPublisher)
        service = EventProducerService(mock_publisher)

        service.publish_batch([])

        mock_publisher.publish_batch.assert_not_called()

    def test_publish_batch_with_events(self):
        """Test publishing batch with events"""
        mock_publisher = Mock(spec=EventPublisher)
        service = EventProducerService(mock_publisher)

        events = [
            OrderEvent(
                event_id="evt-1",
                event_type=EventType.ORDER_CREATED,
                event_version="1.0",
                timestamp=datetime.now(),
                order_id="ord-1",
                customer_id="cust-1",
                product_id="prod-1",
                quantity=1,
                unit_price=Decimal("10.00"),
                total_amount=Decimal("10.00")
            ),
            OrderEvent(
                event_id="evt-2",
                event_type=EventType.ORDER_DELIVERED,
                event_version="1.0",
                timestamp=datetime.now(),
                order_id="ord-2",
                customer_id="cust-2",
                product_id="prod-2",
                quantity=3,
                unit_price=Decimal("20.00"),
                total_amount=Decimal("60.00")
            )
        ]

        service.publish_batch(events)

        mock_publisher.publish_batch.assert_called_once_with(events)

    def test_publish_batch_with_none(self):
        """Test publishing batch with None returns early"""
        mock_publisher = Mock(spec=EventPublisher)
        service = EventProducerService(mock_publisher)

        service.publish_batch(None)

        mock_publisher.publish_batch.assert_not_called()