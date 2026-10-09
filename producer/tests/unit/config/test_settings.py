import pytest
import os
from unittest.mock import patch
from src.config.settings import Settings


class TestSettings:

    def test_init(self):
        """Test Settings initialization"""
        settings = Settings(
            aws_region="us-east-1",
            kinesis_stream_name="test-stream",
            event_rate=10,
            batch_size=5
        )
        assert settings.aws_region == "us-east-1"
        assert settings.kinesis_stream_name == "test-stream"
        assert settings.event_rate == 10
        assert settings.batch_size == 5

    @patch.dict(os.environ, {}, clear=True)
    def test_from_environment_with_defaults(self):
        """Test from_environment with default values"""
        settings = Settings.from_environment()
        assert settings.aws_region == "us-east-2"
        assert settings.kinesis_stream_name == "ia-data-operations-events"
        assert settings.event_rate == 10
        assert settings.batch_size == 10

    @patch.dict(os.environ, {
        "AWS_REGION": "us-west-1",
        "KINESIS_STREAM_NAME": "custom-stream",
        "EVENT_RATE": "20",
        "BATCH_SIZE": "5"
    })
    def test_from_environment_with_custom_values(self):
        """Test from_environment with custom environment variables"""
        settings = Settings.from_environment()
        assert settings.aws_region == "us-west-1"
        assert settings.kinesis_stream_name == "custom-stream"
        assert settings.event_rate == 20
        assert settings.batch_size == 5

    @patch.dict(os.environ, {
        "AWS_REGION": "",
        "KINESIS_STREAM_NAME": "test-stream",
        "EVENT_RATE": "10",
        "BATCH_SIZE": "5"
    })
    def test_validate_empty_aws_region(self):
        """Test validation fails with empty AWS_REGION"""
        with pytest.raises(ValueError, match="AWS_REGION environment variable é obrigatorio"):
            Settings.from_environment()

    @patch.dict(os.environ, {
        "AWS_REGION": "us-east-1",
        "KINESIS_STREAM_NAME": "",
        "EVENT_RATE": "10",
        "BATCH_SIZE": "5"
    })
    def test_validate_empty_kinesis_stream_name(self):
        """Test validation fails with empty KINESIS_STREAM_NAME"""
        with pytest.raises(ValueError, match="KINESIS_STREAM_NAME environment variable é obrigatorio"):
            Settings.from_environment()

    @patch.dict(os.environ, {
        "AWS_REGION": "us-east-1",
        "KINESIS_STREAM_NAME": "test-stream",
        "EVENT_RATE": "0",
        "BATCH_SIZE": "5"
    })
    def test_validate_event_rate_zero(self):
        """Test validation fails with EVENT_RATE <= 0"""
        with pytest.raises(ValueError, match="EVENT_RATE environment variable é obrigatorio"):
            Settings.from_environment()

    @patch.dict(os.environ, {
        "AWS_REGION": "us-east-1",
        "KINESIS_STREAM_NAME": "test-stream",
        "EVENT_RATE": "-5",
        "BATCH_SIZE": "5"
    })
    def test_validate_event_rate_negative(self):
        """Test validation fails with negative EVENT_RATE"""
        with pytest.raises(ValueError, match="EVENT_RATE environment variable é obrigatorio"):
            Settings.from_environment()

    @patch.dict(os.environ, {
        "AWS_REGION": "us-east-1",
        "KINESIS_STREAM_NAME": "test-stream",
        "EVENT_RATE": "10",
        "BATCH_SIZE": "0"
    })
    def test_validate_batch_size_zero(self):
        """Test validation fails with BATCH_SIZE <= 0"""
        with pytest.raises(ValueError, match="BATCH_SIZE environment variable é obrigatorio"):
            Settings.from_environment()

    @patch.dict(os.environ, {
        "AWS_REGION": "us-east-1",
        "KINESIS_STREAM_NAME": "test-stream",
        "EVENT_RATE": "10",
        "BATCH_SIZE": "-3"
    })
    def test_validate_batch_size_negative(self):
        """Test validation fails with negative BATCH_SIZE"""
        with pytest.raises(ValueError, match="BATCH_SIZE environment variable é obrigatorio"):
            Settings.from_environment()

    @patch.dict(os.environ, {
        "AWS_REGION": "us-east-1",
        "KINESIS_STREAM_NAME": "test-stream",
        "EVENT_RATE": "5",
        "BATCH_SIZE": "10"
    })
    def test_validate_event_rate_less_than_batch_size(self):
        """Test validation fails when EVENT_RATE < BATCH_SIZE"""
        with pytest.raises(ValueError, match="EVENT_RATE deve ser maior que BATCH_SIZE"):
            Settings.from_environment()

    @patch.dict(os.environ, {
        "AWS_REGION": "us-east-1",
        "KINESIS_STREAM_NAME": "test-stream",
        "EVENT_RATE": "10",
        "BATCH_SIZE": "11"
    })
    def test_validate_event_rate_equal_to_batch_size(self):
        """Test validation fails when EVENT_RATE == BATCH_SIZE"""
        with pytest.raises(ValueError, match="EVENT_RATE deve ser maior que BATCH_SIZE"):
            Settings.from_environment()

    @patch.dict(os.environ, {
        "AWS_REGION": "us-east-1",
        "KINESIS_STREAM_NAME": "test-stream",
        "EVENT_RATE": "20",
        "BATCH_SIZE": "10"
    })
    def test_validate_valid_settings(self):
        """Test validation passes with valid settings"""
        settings = Settings.from_environment()
        assert settings.aws_region == "us-east-1"
        assert settings.kinesis_stream_name == "test-stream"
        assert settings.event_rate == 20
        assert settings.batch_size == 10