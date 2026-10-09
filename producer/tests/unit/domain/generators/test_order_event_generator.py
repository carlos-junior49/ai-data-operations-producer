import pytest
from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import patch, MagicMock

from src.domain.generators.order_event_generator import OrderEventGenerator
from src.domain.entities.order_event import OrderEvent
from src.domain.enums.event_type import EventType


class TestOrderEventGenerator:

    def test_generate_returns_order_event(self):
        """Test that generate returns an OrderEvent instance"""
        generator = OrderEventGenerator()
        event = generator.generate()

        assert isinstance(event, OrderEvent)

    def test_generate_event_type(self):
        """Test that generated event has ORDER_CREATED type"""
        generator = OrderEventGenerator()
        event = generator.generate()

        assert event.event_type == EventType.ORDER_CREATED

    def test_generate_event_version(self):
        """Test that generated event has version 1.0"""
        generator = OrderEventGenerator()
        event = generator.generate()

        assert event.event_version == "1.0"

    def test_generate_timestamp_is_utc(self):
        """Test that generated timestamp is in UTC timezone"""
        generator = OrderEventGenerator()
        event = generator.generate()

        assert event.timestamp.tzinfo == timezone.utc

    def test_generate_event_id_is_uuid(self):
        """Test that event_id is a valid UUID string"""
        generator = OrderEventGenerator()
        event = generator.generate()

        assert len(event.event_id) == 36  # UUID4 format
        assert event.event_id.count('-') == 4

    @patch('src.domain.generators.order_event_generator.choice')
    def test_generate_uses_product_from_list(self, mock_choice):
        """Test that generate selects a product from the predefined list"""
        mock_choice.return_value = ("PROD-001", Decimal("49.90"))
        generator = OrderEventGenerator()
        event = generator.generate()

        assert event.product_id == "PROD-001"
        assert event.unit_price == Decimal("49.90")

    @patch('src.domain.generators.order_event_generator.randint')
    def test_generate_quantity_range(self, mock_randint):
        """Test that quantity is generated using randint(1, 10)"""
        mock_randint.side_effect = [5, 12345]
        generator = OrderEventGenerator()
        event = generator.generate()

        assert event.quantity == 5
        assert mock_randint.call_count == 2
        assert mock_randint.call_args_list[0] == ((1, 10),)

    def test_generate_total_amount_calculation(self):
        """Test that total_amount is calculated correctly"""
        generator = OrderEventGenerator()

        with patch('src.domain.generators.order_event_generator.choice') as mock_choice, \
                patch('src.domain.generators.order_event_generator.randint') as mock_randint:
            mock_choice.return_value = ("PROD-002", Decimal("99.90"))
            mock_randint.return_value = 3

            event = generator.generate()

            assert event.total_amount == Decimal("99.90") * 3

    def test_generate_order_id_format(self):
        """Test that order_id follows the ORD-{hex} format"""
        generator = OrderEventGenerator()
        event = generator.generate()

        assert event.order_id.startswith("ORD-")
        assert len(event.order_id) == 16  # ORD- + 12 hex chars
        assert event.order_id[4:].isalnum()

    def test_generate_customer_id_format(self):
        """Test that customer_id follows the CUS-{number} format"""
        generator = OrderEventGenerator()
        event = generator.generate()

        assert event.customer_id.startswith("CUS-")
        assert len(event.customer_id) == 9  # CUS- + 5 digits
        assert event.customer_id[4:].isdigit()

    def test_generate_customer_id_range(self):
        """Test that customer_id number is between 10000 and 99999"""
        generator = OrderEventGenerator()

        for _ in range(10):
            event = generator.generate()
            customer_num = int(event.customer_id[4:])
            assert 10000 <= customer_num <= 99999

    @patch('src.domain.generators.order_event_generator.choice')
    def test_generate_with_different_products(self, mock_choice):
        """Test that different products can be selected"""
        generator = OrderEventGenerator()

        products = [
            ("PROD-001", Decimal("49.90")),
            ("PROD-002", Decimal("99.90")),
            ("PROD-003", Decimal("149.90")),
            ("PROD-004", Decimal("299.90"))
        ]

        for product in products:
            mock_choice.return_value = product
            event = generator.generate()
            assert event.product_id == product[0]
            assert event.unit_price == product[1]

    def test_generate_order_id_static_method(self):
        """Test _generate_order_id static method directly"""
        order_id = OrderEventGenerator._generate_order_id()

        assert order_id.startswith("ORD-")
        assert len(order_id) == 16
        assert order_id[4:].isupper()

    def test_generate_customer_id_static_method(self):
        """Test _generate_customer_id static method directly"""
        customer_id = OrderEventGenerator._generate_customer_id()

        assert customer_id.startswith("CUS-")
        assert len(customer_id) == 9
        assert customer_id[4:].isdigit()

    def test_generate_order_id_uniqueness(self):
        """Test that generated order_ids are unique"""
        generator = OrderEventGenerator()
        order_ids = set()

        for _ in range(100):
            event = generator.generate()
            order_ids.add(event.order_id)

        assert len(order_ids) == 100

    def test_generate_customer_id_not_necessarily_unique(self):
        """Test that customer_ids can repeat (random range)"""
        generator = OrderEventGenerator()
        customer_ids = [generator.generate().customer_id for _ in range(100)]

        # With 100 samples from 90000 possible values, duplicates are unlikely but possible
        # This test just verifies the mechanism works
        assert all(cid.startswith("CUS-") for cid in customer_ids)

    def test_products_constant(self):
        """Test that _PRODUCTS constant contains expected tuples"""
        assert len(OrderEventGenerator._PRODUCTS) == 4
        assert OrderEventGenerator._PRODUCTS[0] == ("PROD-001", Decimal("49.90"))
        assert OrderEventGenerator._PRODUCTS[1] == ("PROD-002", Decimal("99.90"))
        assert OrderEventGenerator._PRODUCTS[2] == ("PROD-003", Decimal("149.90"))
        assert OrderEventGenerator._PRODUCTS[3] == ("PROD-004", Decimal("299.90"))