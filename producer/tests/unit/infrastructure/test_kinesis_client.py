import pytest
from unittest.mock import Mock, patch

from src.infrastructure.kinesis.kinesis_client import KinesisClient


class TestKinesisClient:

    @patch('src.infrastructure.kinesis.kinesis_client.boto3.client')
    def test_init(self, mock_boto3_client):
        """Test KinesisClient initialization with region"""
        mock_client = Mock()
        mock_boto3_client.return_value = mock_client

        client = KinesisClient("us-east-1")

        assert client._client == mock_client
        mock_boto3_client.assert_called_once_with("kinesis", region_name="us-east-1")

    @patch('src.infrastructure.kinesis.kinesis_client.boto3.client')
    def test_init_with_different_region(self, mock_boto3_client):
        """Test initialization with different region"""
        mock_client = Mock()
        mock_boto3_client.return_value = mock_client

        client = KinesisClient("eu-west-1")

        mock_boto3_client.assert_called_once_with("kinesis", region_name="eu-west-1")

    @patch('src.infrastructure.kinesis.kinesis_client.boto3.client')
    def test_put_record(self, mock_boto3_client):
        """Test put_record calls boto3 client correctly"""
        mock_client = Mock()
        mock_client.put_record.return_value = {"SequenceNumber": "123"}
        mock_boto3_client.return_value = mock_client

        client = KinesisClient("us-east-1")
        result = client.put_record("test-stream", b"test-data", "partition-1")

        mock_client.put_record.assert_called_once_with(
            StreamName="test-stream",
            Data=b"test-data",
            PartitionKey="partition-1"
        )
        assert result == {"SequenceNumber": "123"}

    @patch('src.infrastructure.kinesis.kinesis_client.boto3.client')
    def test_put_record_with_empty_data(self, mock_boto3_client):
        """Test put_record with empty data"""
        mock_client = Mock()
        mock_boto3_client.return_value = mock_client

        client = KinesisClient("us-east-1")
        client.put_record("test-stream", b"", "partition-1")

        mock_client.put_record.assert_called_once_with(
            StreamName="test-stream",
            Data=b"",
            PartitionKey="partition-1"
        )

    @patch('src.infrastructure.kinesis.kinesis_client.boto3.client')
    def test_put_records(self, mock_boto3_client):
        """Test put_records calls boto3 client correctly"""
        mock_client = Mock()
        mock_client.put_records.return_value = {"FailedRecordCount": 0}
        mock_boto3_client.return_value = mock_client

        client = KinesisClient("us-east-1")
        records = [{"Data": b"data1", "PartitionKey": "key1"}, {"Data": b"data2", "PartitionKey": "key2"}]
        result = client.put_records("test-stream", records)

        mock_client.put_records.assert_called_once_with(
            StreamName="test-stream",
            Records=list(records)
        )
        assert result == {"FailedRecordCount": 0}

    @patch('src.infrastructure.kinesis.kinesis_client.boto3.client')
    def test_put_records_with_generator(self, mock_boto3_client):
        """Test put_records converts generator to list"""
        mock_client = Mock()
        mock_boto3_client.return_value = mock_client

        client = KinesisClient("us-east-1")

        def record_generator():
            yield {"Data": b"data1", "PartitionKey": "key1"}
            yield {"Data": b"data2", "PartitionKey": "key2"}

        client.put_records("test-stream", record_generator())

        # Verify that Records was called with a list (not generator)
        call_args = mock_client.put_records.call_args
        assert isinstance(call_args[1]["Records"], list)

    @patch('src.infrastructure.kinesis.kinesis_client.boto3.client')
    def test_put_records_with_empty_list(self, mock_boto3_client):
        """Test put_records with empty list"""
        mock_client = Mock()
        mock_boto3_client.return_value = mock_client

        client = KinesisClient("us-east-1")
        client.put_records("test-stream", [])

        mock_client.put_records.assert_called_once_with(
            StreamName="test-stream",
            Records=[]
        )

    @patch('src.infrastructure.kinesis.kinesis_client.boto3.client')
    def test_put_records_with_tuple(self, mock_boto3_client):
        """Test put_records converts tuple to list"""
        mock_client = Mock()
        mock_boto3_client.return_value = mock_client

        client = KinesisClient("us-east-1")
        records = ({"Data": b"data1", "PartitionKey": "key1"}, {"Data": b"data2", "PartitionKey": "key2"})
        client.put_records("test-stream", records)

        call_args = mock_client.put_records.call_args
        assert isinstance(call_args[1]["Records"], list)
        assert len(call_args[1]["Records"]) == 2