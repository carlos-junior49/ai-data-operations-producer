import datetime
import json
from typing import Any, Dict, List
from pathlib import Path

import boto3

from src.config.settings import Settings

settings = Settings.from_environment()
from src.infrastructure.kinesis.kinesis_client import KinesisClient


class ExportKinesisEvents:
    def __init__(self, client_kinesis, stream_name: str, output_path: str = "events.json"):
        self._client = client_kinesis
        self._stream_name = stream_name
        self._output_path = Path(output_path)

    def list_shards(self) -> List[Dict[str, Any]]:
        """List all open shards in the Kinesis stream"""
        response = self._client.list_shards(
            StreamName=self._stream_name,
            MaxResults=1000
        )
        return response.get("Shards", [])

    def get_shard_iterator(self, shard_id: str) -> str:
        """Get shard iterator for a specific shard"""
        response = self._client.get_shard_iterator(
            StreamName=self._stream_name,
            ShardId=shard_id,
            ShardIteratorType="TRIM_HORIZON"
        )
        return response["ShardIterator"]

    def get_records(self, shard_iterator: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get records from a shard using shard iterator"""
        response = self._client.get_records(
            ShardIterator=shard_iterator,
            Limit=limit
        )
        return response.get("Records", [])

    def read_and_save(self, limit: int = 100) -> None:
        """Read events from all open shards and save to local file"""
        all_records = []

        shards = self.list_shards()

        for shard in shards:
            shard_id = shard["ShardId"]
            shard_iterator = self.get_shard_iterator(shard_id)

            records = self.get_records(shard_iterator, limit)

            for record in records:
                data = record.get("Data", b"")
                if data:
                    try:
                        decoded_data = json.loads(data.decode("utf-8"))
                        all_records.append(decoded_data)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        all_records.append({"raw_data": data.decode("utf-8", errors="ignore")})

        self._save_to_file(all_records)

    def _save_to_file(self, records: List[Dict[str, Any]]) -> None:
        """Save records to local JSON file"""
        self._output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self._output_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)

    def get_open_shards_count(self) -> int:
        """Get the count of open shards"""
        shards = self.list_shards()
        return len(shards)


def main():
    from src.config.settings import Settings

    settings = Settings.from_environment()

    client_kinesis = boto3.client("kinesis", region_name=settings.aws_region)
    exporter = ExportKinesisEvents(
        client_kinesis=client_kinesis,
        stream_name=settings.kinesis_stream_name,
        output_path=datetime.datetime.now().strftime("events_%Y%m%d_%H%M%S.json")
    )

    print(f"Reading events from stream: {settings.kinesis_stream_name}")
    print(f"Open shards: {exporter.get_open_shards_count()}")

    exporter.read_and_save(limit=100)

    print(f"Events saved to: {exporter._output_path}")


if __name__ == "__main__":
    main()
