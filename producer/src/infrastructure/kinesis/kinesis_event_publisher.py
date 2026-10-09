# src/infrastructure/kinesis/kinesis_event_publisher.py

import json
from typing import Any, Dict, Sequence

from src.application.ports.event_publisher import EventPublisher
from src.domain.entities.order_event import OrderEvent
from src.infrastructure.kinesis.kinesis_client import KinesisClient


class KinesisEventPublisher(EventPublisher):
    def __init__(self, client: KinesisClient, stream_name: str):
        self._client = client
        self._stream_name = stream_name

    def publish(self, event: OrderEvent) -> None:
        record = self._to_kinesis_record(event)

        self._client.put_record(
            stream_name=self._stream_name,
            data=record["Data"],
            partition_key=record["PartitionKey"]
        )

    def publish_batch(self, events: Sequence[OrderEvent]) -> None:
        records = [
            self._to_kinesis_record(event)
            for event in events
        ]

        if not events:
            return

        self._client.put_records(
            stream_name=self._stream_name,
            records=records
        )

    @staticmethod
    def _to_kinesis_record(event: OrderEvent) -> Dict[str, Any]:
        data = json.dumps(event.to_dict(), ensure_ascii=False).encode("utf-8")

        return {
            "Data": data,
            "PartitionKey": event.order_id
        }
