import pytest
from unittest.mock import Mock
from datetime import datetime
from decimal import Decimal

from src.infrastructure.kinesis.kinesis_event_publisher import KinesisEventPublisher
from src.infrastructure.kinesis.kinesis_client import KinesisClient
from src.domain.entities.order_event import OrderEvent
from src.domain.enums.event_type import EventType


class TestKinesisEventPublisher:

    def test_init(self):
        """Test KinesisEventPublisher initialization"""
        mock_client = Mock(spec=KinesisClient)
        publisher = KinesisEventPublisher(mock_client, "test-stream")

        assert publisher._client == mock_client
        assert publisher._stream_name == "test-stream"

    def test_publish(self):
        """Test publish converts event and calls client.put_record"""
        mock_client = Mock(spec=KinesisClient)
        publisher = KinesisEventPublisher(mock_client, "test-stream")

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

        publisher.publish(event)

        mock_client.put_record.assert_called_once()
        call_args = mock_client.put_record.call_args
        assert call_args[1]["stream_name"] == "test-stream"
        assert isinstance(call_args[1]["data"], bytes)
        assert call_args[1]["partition_key"] == "ord-456"

    def test_publish_with_unicode_characters(self):
        """Test publish handles unicode characters in event data"""
        mock_client = Mock(spec=KinesisClient)
        publisher = KinesisEventPublisher(mock_client, "test-stream")

        timestamp = datetime.now()
        event = OrderEvent(
            event_id="evt-123",
            event_type=EventType.ORDER_CREATED,
            event_version="1.0",
            timestamp=timestamp,
            order_id="ord-456",
            customer_id="cust-café",
            product_id="prod-101",
            quantity=2,
            unit_price=Decimal("10.50"),
            total_amount=Decimal("21.00")
        )

        publisher.publish(event)

        mock_client.put_record.assert_called_once()
        call_args = mock_client.put_record.call_args
        assert call_args[1]["partition_key"] == "ord-456"

    def test_publish_batch_with_events(self):
        """Test publish_batch converts events and calls client.put_records"""
        mock_client = Mock(spec=KinesisClient)
        publisher = KinesisEventPublisher(mock_client, "test-stream")

        timestamp = datetime.now()
        events = [
            OrderEvent(
                event_id="evt-1",
                event_type=EventType.ORDER_CREATED,
                event_version="1.0",
                timestamp=timestamp,
                order_id="ord-1",
                customer_id="cust-1",
                product_id="prod-1",
                quantity=1,
                unit_price=Decimal("10.00"),
                total_amount=Decimal("10.00")
            ),
            OrderEvent(
                event_id="evt-2",
                event_type=EventType.ORDER_PAID,
                event_version="1.0",
                timestamp=timestamp,
                order_id="ord-2",
                customer_id="cust-2",
                product_id="prod-2",
                quantity=2,
                unit_price=Decimal("20.00"),
                total_amount=Decimal("40.00")
            )
        ]

        publisher.publish_batch(events)

        mock_client.put_records.assert_called_once()
        call_args = mock_client.put_records.call_args
        assert call_args[1]["stream_name"] == "test-stream"
        assert len(call_args[1]["records"]) == 2

    def test_publish_batch_with_empty_list(self):
        """Test publish_batch returns early with empty list"""
        mock_client = Mock(spec=KinesisClient)
        publisher = KinesisEventPublisher(mock_client, "test-stream")

        publisher.publish_batch([])

        mock_client.put_records.assert_not_called()

    def test_to_kinesis_record(self):
        """Test _to_kinesis_record static method"""
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

        record = KinesisEventPublisher._to_kinesis_record(event)

        assert "Data" in record
        assert "PartitionKey" in record
        assert record["PartitionKey"] == "ord-456"
        assert isinstance(record["Data"], bytes)

    def test_to_kinesis_record_json_encoding(self):
        """Test _to_kinesis_record encodes event to JSON"""
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

        record = KinesisEventPublisher._to_kinesis_record(event)

        import json
        decoded = json.loads(record["Data"].decode("utf-8"))
        assert decoded["event_id"] == "evt-123"
        assert decoded["order_id"] == "ord-456"
        assert decoded["quantity"] == 2

    def test_to_kinesis_record_ensure_ascii_false(self):
        """Test _to_kinesis_record preserves unicode characters"""
        timestamp = datetime.now()
        event = OrderEvent(
            event_id="evt-123",
            event_type=EventType.ORDER_CREATED,
            event_version="1.0",
            timestamp=timestamp,
            order_id="ord-456",
            customer_id="cust-café",
            product_id="prod-101",
            quantity=1,
            unit_price=Decimal("10.00"),
            total_amount=Decimal("10.00")
        )

        record = KinesisEventPublisher._to_kinesis_record(event)

        import json
        decoded = json.loads(record["Data"].decode("utf-8"))
        assert decoded["customer_id"] == "cust-café"

    def test_publish_batch_single_event(self):
        """Test publish_batch with single event"""
        mock_client = Mock(spec=KinesisClient)
        publisher = KinesisEventPublisher(mock_client, "test-stream")

        timestamp = datetime.now()
        event = OrderEvent(
            event_id="evt-1",
            event_type=EventType.ORDER_CREATED,
            event_version="1.0",
            timestamp=timestamp,
            order_id="ord-1",
            customer_id="cust-1",
            product_id="prod-1",
            quantity=1,
            unit_price=Decimal("10.00"),
            total_amount=Decimal("10.00")
        )

        publisher.publish_batch([event])

        mock_client.put_records.assert_called_once()
        call_args = mock_client.put_records.call_args
        assert len(call_args[1]["records"]) == 1