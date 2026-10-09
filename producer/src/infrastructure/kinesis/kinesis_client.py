# src/infrastructure/kinesis/kinesis_client.py

from typing import Any, Sequence

import boto3
from botocore.client import BaseClient


class KinesisClient:
    def __init__(self, region_name: str):
        self._client = boto3.client("kinesis", region_name=region_name)

    def put_record(self, stream_name: str, data: bytes, partition_key: str) -> Any:
        return self._client.put_record(
            StreamName=stream_name,
            Data=data,
            PartitionKey=partition_key
        )

    def put_records(self, stream_name: str, records: Sequence[dict]) -> Any:
        return self._client.put_records(
            StreamName=stream_name,
            Records=list(records)
        )
