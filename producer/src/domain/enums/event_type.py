# src/domain/enums/event_type.py

from enum import Enum


class EventType(str, Enum):
    ORDER_CREATED = "ORDER_CREATED"
    ORDER_PAID = "ORDER_PAID"
    ORDER_CANCELLED = "ORDER_CANCELLED"
    ORDER_SHIPPED = "ORDER_SHIPPED"
    ORDER_DELIVERED = "ORDER_DELIVERED"
