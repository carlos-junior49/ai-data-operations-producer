import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    aws_region: str
    kinesis_stream_name: str
    event_rate: int
    batch_size: int

    @classmethod
    def from_environment(cls):
        settings = cls(
            aws_region=os.getenv("AWS_REGION", "us-east-2"),
            kinesis_stream_name=os.getenv("KINESIS_STREAM_NAME", "ai-data-operations-events"),
            event_rate=int(os.getenv("EVENT_RATE", 10)),
            batch_size=int(os.getenv("BATCH_SIZE", 10))
        )

        settings._validate()

        return settings

    def _validate(self):
        if not self.aws_region:
            raise ValueError("AWS_REGION environment variable é obrigatorio.")
        if not self.kinesis_stream_name:
            raise ValueError("KINESIS_STREAM_NAME environment variable é obrigatorio.")
        if self.event_rate <= 0:
            raise ValueError("EVENT_RATE environment variable é obrigatorio.")
        if self.batch_size <= 0:
            raise ValueError("BATCH_SIZE environment variable é obrigatorio.")
        if self.event_rate < self.batch_size:
            raise ValueError("EVENT_RATE deve ser maior que BATCH_SIZE.")
