import pytest

from src.domain.enums.event_type import EventType


class TestEventType:

    def test_order_created_value(self):
        """Test ORDER_CREATED enum value"""
        assert EventType.ORDER_CREATED.value == "ORDER_CREATED"
        assert isinstance(EventType.ORDER_CREATED, str)

    def test_order_paid_value(self):
        """Test ORDER_PAID enum value"""
        assert EventType.ORDER_PAID.value == "ORDER_PAID"
        assert isinstance(EventType.ORDER_PAID, str)

    def test_order_cancelled_value(self):
        """Test ORDER_CANCELLED enum value"""
        assert EventType.ORDER_CANCELLED.value == "ORDER_CANCELLED"
        assert isinstance(EventType.ORDER_CANCELLED, str)

    def test_order_shipped_value(self):
        """Test ORDER_SHIPPED enum value"""
        assert EventType.ORDER_SHIPPED.value == "ORDER_SHIPPED"
        assert isinstance(EventType.ORDER_SHIPPED, str)

    def test_order_delivered_value(self):
        """Test ORDER_DELIVERED enum value"""
        assert EventType.ORDER_DELIVERED.value == "ORDER_DELIVERED"
        assert isinstance(EventType.ORDER_DELIVERED, str)

    def test_enum_is_string_enum(self):
        """Test that EventType is a string enum"""
        assert issubclass(EventType, str)
        assert issubclass(EventType, type(EventType.ORDER_CREATED))

    def test_all_enum_values(self):
        """Test that all enum values are accessible"""
        expected_values = {
            "ORDER_CREATED",
            "ORDER_PAID",
            "ORDER_CANCELLED",
            "ORDER_SHIPPED",
            "ORDER_DELIVERED"
        }
        actual_values = {member.value for member in EventType}
        assert actual_values == expected_values

    def test_enum_iteration(self):
        """Test that we can iterate over all EventType members"""
        members = list(EventType)
        assert len(members) == 5
        assert EventType.ORDER_CREATED in members
        assert EventType.ORDER_PAID in members
        assert EventType.ORDER_CANCELLED in members
        assert EventType.ORDER_SHIPPED in members
        assert EventType.ORDER_DELIVERED in members

    def test_enum_comparison(self):
        """Test enum comparison by value"""
        assert EventType.ORDER_CREATED == "ORDER_CREATED"
        assert EventType.ORDER_PAID == "ORDER_PAID"
        assert EventType.ORDER_CANCELLED == "ORDER_CANCELLED"
        assert EventType.ORDER_SHIPPED == "ORDER_SHIPPED"
        assert EventType.ORDER_DELIVERED == "ORDER_DELIVERED"

    def test_enum_inequality(self):
        """Test enum inequality"""
        assert EventType.ORDER_CREATED != EventType.ORDER_PAID
        assert EventType.ORDER_CANCELLED != "ORDER_CREATED"

    def test_enum_name(self):
        """Test enum member names"""
        assert EventType.ORDER_CREATED.name == "ORDER_CREATED"
        assert EventType.ORDER_PAID.name == "ORDER_PAID"
        assert EventType.ORDER_CANCELLED.name == "ORDER_CANCELLED"
        assert EventType.ORDER_SHIPPED.name == "ORDER_SHIPPED"
        assert EventType.ORDER_DELIVERED.name == "ORDER_DELIVERED"