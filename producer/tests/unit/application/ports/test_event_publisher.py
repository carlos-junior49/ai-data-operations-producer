import pytest
from datetime import datetime
from decimal import Decimal
from typing import Sequence

from src.application.ports.event_publisher import EventPublisher
from src.domain.entities.order_event import OrderEvent
from src.domain.enums.event_type import EventType


class ConcreteEventPublisher(EventPublisher):
    """Concrete implementation of EventPublisher for testing purposes."""
    
    def __init__(self):
        self.published_events = []
        self.batch_published_events = []
    
    def publish(self, event: OrderEvent) -> None:
        self.published_events.append(event)
    
    def publish_batch(self, events: Sequence[OrderEvent]) -> None:
        self.batch_published_events.extend(events)


class TestEventPublisher:
    """Test suite for EventPublisher abstract base class."""
    
    def test_event_publisher_is_abstract_cannot_be_instantiated(self):
        """Test that EventPublisher cannot be instantiated directly as it's abstract."""
        with pytest.raises(TypeError) as exc_info:
            EventPublisher()
        
        assert "Can't instantiate abstract class" in str(exc_info.value)
        assert "publish" in str(exc_info.value)
        assert "publish_batch" in str(exc_info.value)
    
    def test_concrete_implementation_can_be_instantiated(self):
        """Test that a concrete implementation of EventPublisher can be instantiated."""
        publisher = ConcreteEventPublisher()
        assert isinstance(publisher, EventPublisher)
        assert publisher.published_events == []
        assert publisher.batch_published_events == []
    
    def test_publish_method_with_single_event(self):
        """Test the publish method with a single OrderEvent."""
        publisher = ConcreteEventPublisher()
        
        event = OrderEvent(
            event_id="evt-001",
            event_type=EventType.ORDER_CREATED,
            event_version="1.0",
            timestamp=datetime(2024, 1, 1, 12, 0, 0),
            order_id="ord-001",
            customer_id="cust-001",
            product_id="prod-001",
            quantity=2,
            unit_price=Decimal("10.50"),
            total_amount=Decimal("21.00")
        )
        
        publisher.publish(event)
        
        assert len(publisher.published_events) == 1
        assert publisher.published_events[0] == event
        assert publisher.published_events[0].event_id == "evt-001"
        assert publisher.published_events[0].event_type == EventType.ORDER_CREATED
    
    def test_publish_method_with_multiple_sequential_calls(self):
        """Test the publish method with multiple sequential calls."""
        publisher = ConcreteEventPublisher()
        
        event1 = OrderEvent(
            event_id="evt-001",
            event_type=EventType.ORDER_CREATED,
            event_version="1.0",
            timestamp=datetime(2024, 1, 1, 12, 0, 0),
            order_id="ord-001",
            customer_id="cust-001",
            product_id="prod-001",
            quantity=2,
            unit_price=Decimal("10.50"),
            total_amount=Decimal("21.00")
        )
        
        event2 = OrderEvent(
            event_id="evt-002",
            event_type=EventType.ORDER_PAID,
            event_version="1.0",
            timestamp=datetime(2024, 1, 1, 12, 30, 0),
            order_id="ord-002",
            customer_id="cust-002",
            product_id="prod-002",
            quantity=1,
            unit_price=Decimal("25.00"),
            total_amount=Decimal("25.00")
        )
        
        publisher.publish(event1)
        publisher.publish(event2)
        
        assert len(publisher.published_events) == 2
        assert publisher.published_events[0] == event1
        assert publisher.published_events[1] == event2
    
    def test_publish_method_with_all_event_types(self):
        """Test the publish method with all possible EventType values."""
        publisher = ConcreteEventPublisher()
        
        event_types = [
            EventType.ORDER_CREATED,
            EventType.ORDER_PAID,
            EventType.ORDER_CANCELLED,
            EventType.ORDER_SHIPPED,
            EventType.ORDER_DELIVERED
        ]
        
        for idx, event_type in enumerate(event_types):
            event = OrderEvent(
                event_id=f"evt-{idx:03d}",
                event_type=event_type,
                event_version="1.0",
                timestamp=datetime(2024, 1, 1, 12, 0, 0),
                order_id=f"ord-{idx:03d}",
                customer_id=f"cust-{idx:03d}",
                product_id=f"prod-{idx:03d}",
                quantity=1,
                unit_price=Decimal("10.00"),
                total_amount=Decimal("10.00")
            )
            publisher.publish(event)
        
        assert len(publisher.published_events) == 5
        for idx, event_type in enumerate(event_types):
            assert publisher.published_events[idx].event_type == event_type
    
    def test_publish_batch_method_with_empty_sequence(self):
        """Test the publish_batch method with an empty sequence."""
        publisher = ConcreteEventPublisher()
        
        publisher.publish_batch([])
        
        assert len(publisher.batch_published_events) == 0
    
    def test_publish_batch_method_with_single_event(self):
        """Test the publish_batch method with a single event in sequence."""
        publisher = ConcreteEventPublisher()
        
        event = OrderEvent(
            event_id="evt-001",
            event_type=EventType.ORDER_CREATED,
            event_version="1.0",
            timestamp=datetime(2024, 1, 1, 12, 0, 0),
            order_id="ord-001",
            customer_id="cust-001",
            product_id="prod-001",
            quantity=2,
            unit_price=Decimal("10.50"),
            total_amount=Decimal("21.00")
        )
        
        publisher.publish_batch([event])
        
        assert len(publisher.batch_published_events) == 1
        assert publisher.batch_published_events[0] == event
    
    def test_publish_batch_method_with_multiple_events(self):
        """Test the publish_batch method with multiple events."""
        publisher = ConcreteEventPublisher()
        
        events = [
            OrderEvent(
                event_id="evt-001",
                event_type=EventType.ORDER_CREATED,
                event_version="1.0",
                timestamp=datetime(2024, 1, 1, 12, 0, 0),
                order_id="ord-001",
                customer_id="cust-001",
                product_id="prod-001",
                quantity=2,
                unit_price=Decimal("10.50"),
                total_amount=Decimal("21.00")
            ),
            OrderEvent(
                event_id="evt-002",
                event_type=EventType.ORDER_PAID,
                event_version="1.0",
                timestamp=datetime(2024, 1, 1, 12, 30, 0),
                order_id="ord-002",
                customer_id="cust-002",
                product_id="prod-002",
                quantity=1,
                unit_price=Decimal("25.00"),
                total_amount=Decimal("25.00")
            ),
            OrderEvent(
                event_id="evt-003",
                event_type=EventType.ORDER_SHIPPED,
                event_version="1.0",
                timestamp=datetime(2024, 1, 2, 9, 0, 0),
                order_id="ord-003",
                customer_id="cust-003",
                product_id="prod-003",
                quantity=3,
                unit_price=Decimal("15.00"),
                total_amount=Decimal("45.00")
            )
        ]
        
        publisher.publish_batch(events)
        
        assert len(publisher.batch_published_events) == 3
        assert publisher.batch_published_events == events
    
    def test_publish_batch_with_tuple_sequence(self):
        """Test the publish_batch method with a tuple instead of list."""
        publisher = ConcreteEventPublisher()
        
        events = (
            OrderEvent(
                event_id="evt-001",
                event_type=EventType.ORDER_CREATED,
                event_version="1.0",
                timestamp=datetime(2024, 1, 1, 12, 0, 0),
                order_id="ord-001",
                customer_id="cust-001",
                product_id="prod-001",
                quantity=1,
                unit_price=Decimal("10.00"),
                total_amount=Decimal("10.00")
            ),
        )
        
        publisher.publish_batch(events)
        
        assert len(publisher.batch_published_events) == 1
        assert publisher.batch_published_events[0] == events[0]
    
    def test_concrete_implementation_must_implement_publish(self):
        """Test that concrete implementation must implement publish method."""
        with pytest.raises(TypeError):
            class IncompletePublisher(EventPublisher):
                def publish_batch(self, events: Sequence[OrderEvent]) -> None:
                    pass
            
            IncompletePublisher()
    
    def test_concrete_implementation_must_implement_publish_batch(self):
        """Test that concrete implementation must implement publish_batch method."""
        with pytest.raises(TypeError):
            class IncompletePublisher(EventPublisher):
                def publish(self, event: OrderEvent) -> None:
                    pass
            
            IncompletePublisher()
    
    def test_publish_and_publish_batch_independence(self):
        """Test that publish and publish_batch methods work independently."""
        publisher = ConcreteEventPublisher()
        
        event1 = OrderEvent(
            event_id="evt-001",
            event_type=EventType.ORDER_CREATED,
            event_version="1.0",
            timestamp=datetime(2024, 1, 1, 12, 0, 0),
            order_id="ord-001",
            customer_id="cust-001",
            product_id="prod-001",
            quantity=1,
            unit_price=Decimal("10.00"),
            total_amount=Decimal("10.00")
        )
        
        event2 = OrderEvent(
            event_id="evt-002",
            event_type=EventType.ORDER_PAID,
            event_version="1.0",
            timestamp=datetime(2024, 1, 1, 12, 30, 0),
            order_id="ord-002",
            customer_id="cust-002",
            product_id="prod-002",
            quantity=2,
            unit_price=Decimal("20.00"),
            total_amount=Decimal("40.00")
        )
        
        publisher.publish(event1)
        publisher.publish_batch([event2])
        
        assert len(publisher.published_events) == 1
        assert len(publisher.batch_published_events) == 1
        assert publisher.published_events[0] == event1
        assert publisher.batch_published_events[0] == event2
