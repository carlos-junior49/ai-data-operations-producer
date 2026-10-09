import pytest
from unittest.mock import Mock, patch

from src.entrypoint.main import create_producer_service, main
from src.config.settings import Settings
from src.application.services.event_producer_service import EventProducerService
from src.domain.generators.order_event_generator import OrderEventGenerator
from src.infrastructure.kinesis.kinesis_client import KinesisClient
from src.infrastructure.kinesis.kinesis_event_publisher import KinesisEventPublisher


class TestMain:

    @patch('src.entrypoint.main.KinesisClient')
    @patch('src.entrypoint.main.KinesisEventPublisher')
    def test_create_producer_service(self, mock_publisher_class, mock_client_class):
        """Test create_producer_service creates service correctly"""
        mock_settings = Mock(spec=Settings)
        mock_settings.aws_region = "us-east-1"
        mock_settings.kinesis_stream_name = "test-stream"

        mock_client = Mock(spec=KinesisClient)
        mock_client_class.return_value = mock_client

        mock_publisher = Mock(spec=KinesisEventPublisher)
        mock_publisher_class.return_value = mock_publisher

        service = create_producer_service(mock_settings)

        assert isinstance(service, EventProducerService)
        mock_client_class.assert_called_once_with("us-east-1")
        mock_publisher_class.assert_called_once_with(mock_client, "test-stream")

    @patch('src.entrypoint.main.time.sleep')
    @patch('src.entrypoint.main.OrderEventGenerator')
    @patch('src.entrypoint.main.create_producer_service')
    @patch('src.entrypoint.main.Settings')
    @patch('src.entrypoint.main.logger')
    def test_main_startup_logging(self, mock_logger, mock_settings_class, mock_create_service,
                                  mock_generator_class, mock_sleep):
        """Test main logs startup information correctly"""
        mock_settings = Mock(spec=Settings)
        mock_settings.aws_region = "us-east-1"
        mock_settings.kinesis_stream_name = "test-stream"
        mock_settings.event_rate = 10
        mock_settings.batch_size = 5
        mock_settings_class.from_environment.return_value = mock_settings

        mock_generator = Mock(spec=OrderEventGenerator)
        mock_event = Mock()
        mock_generator.generate.return_value = mock_event
        mock_generator_class.return_value = mock_generator

        mock_service = Mock(spec=EventProducerService)
        mock_create_service.return_value = mock_service

        mock_sleep.side_effect = [None, KeyboardInterrupt()]

        with pytest.raises(KeyboardInterrupt):
            main()

        mock_logger.info.assert_called()
        startup_call = mock_logger.info.call_args_list[0]
        assert "Producer started" in startup_call[0][0]

    @patch('src.entrypoint.main.time.sleep')
    @patch('src.entrypoint.main.OrderEventGenerator')
    @patch('src.entrypoint.main.create_producer_service')
    @patch('src.entrypoint.main.Settings')
    @patch('src.entrypoint.main.logger')
    def test_main_generates_events(self, mock_logger, mock_settings_class, mock_create_service,
                                   mock_generator_class, mock_sleep):
        """Test main generates events using generator"""
        mock_settings = Mock(spec=Settings)
        mock_settings.aws_region = "us-east-1"
        mock_settings.kinesis_stream_name = "test-stream"
        mock_settings.event_rate = 10
        mock_settings.batch_size = 2
        mock_settings_class.from_environment.return_value = mock_settings

        mock_generator = Mock(spec=OrderEventGenerator)
        mock_generator.generate.return_value = Mock()  # Use return_value instead of side_effect
        mock_generator_class.return_value = mock_generator

        mock_service = Mock(spec=EventProducerService)
        mock_create_service.return_value = mock_service

        mock_sleep.side_effect = [None, KeyboardInterrupt()]

        with pytest.raises(KeyboardInterrupt):
            main()

        assert mock_generator.generate.call_count == 4

    @patch('src.entrypoint.main.time.sleep')
    @patch('src.entrypoint.main.OrderEventGenerator')
    @patch('src.entrypoint.main.create_producer_service')
    @patch('src.entrypoint.main.Settings')
    @patch('src.entrypoint.main.logger')
    def test_main_publishes_batch(self, mock_logger, mock_settings_class, mock_create_service,
                                  mock_generator_class, mock_sleep):
        """Test main publishes batch of events"""
        mock_settings = Mock(spec=Settings)
        mock_settings.aws_region = "us-east-1"
        mock_settings.kinesis_stream_name = "test-stream"
        mock_settings.event_rate = 10
        mock_settings.batch_size = 3
        mock_settings_class.from_environment.return_value = mock_settings

        mock_generator = Mock(spec=OrderEventGenerator)
        mock_generator.generate.return_value = Mock()
        mock_generator_class.return_value = mock_generator

        mock_service = Mock(spec=EventProducerService)
        mock_create_service.return_value = mock_service

        mock_sleep.side_effect = [None, KeyboardInterrupt()]

        with pytest.raises(KeyboardInterrupt):
            main()

        # Verifica que publish_batch foi chamado (pode ser mais de 1 vez)
        assert mock_service.publish_batch.call_count >= 1
        published_events = mock_service.publish_batch.call_args[0][0]
        assert len(published_events) == 3

    @patch('src.entrypoint.main.time.sleep')
    @patch('src.entrypoint.main.OrderEventGenerator')
    @patch('src.entrypoint.main.create_producer_service')
    @patch('src.entrypoint.main.Settings')
    @patch('src.entrypoint.main.logger')
    def test_main_logs_published_events(self, mock_logger, mock_settings_class, mock_create_service,
                                        mock_generator_class, mock_sleep):
        """Test main logs number of published events"""
        mock_settings = Mock(spec=Settings)
        mock_settings.aws_region = "us-east-1"
        mock_settings.kinesis_stream_name = "test-stream"
        mock_settings.event_rate = 10
        mock_settings.batch_size = 5
        mock_settings_class.from_environment.return_value = mock_settings

        mock_generator = Mock(spec=OrderEventGenerator)
        mock_generator.generate.return_value = Mock()  # Trocar side_effect por return_value
        mock_generator_class.return_value = mock_generator

        mock_service = Mock(spec=EventProducerService)
        mock_create_service.return_value = mock_service

        mock_sleep.side_effect = [None, KeyboardInterrupt()]

        with pytest.raises(KeyboardInterrupt):
            main()

        published_log_calls = [call for call in mock_logger.info.call_args_list
                               if "Published" in str(call[0][0])]
        assert len(published_log_calls) > 0

    @patch('src.entrypoint.main.time.sleep')
    @patch('src.entrypoint.main.OrderEventGenerator')
    @patch('src.entrypoint.main.create_producer_service')
    @patch('src.entrypoint.main.Settings')
    @patch('src.entrypoint.main.logger')
    def test_main_sleeps_correct_duration(self, mock_logger, mock_settings_class, mock_create_service,
                                          mock_generator_class, mock_sleep):
        """Test main sleeps for correct duration based on rate and batch size"""
        mock_settings = Mock(spec=Settings)
        mock_settings.aws_region = "us-east-1"
        mock_settings.kinesis_stream_name = "test-stream"
        mock_settings.event_rate = 20
        mock_settings.batch_size = 10
        mock_settings_class.from_environment.return_value = mock_settings

        mock_generator = Mock(spec=OrderEventGenerator)
        mock_generator.generate.return_value = Mock()
        mock_generator_class.return_value = mock_generator

        mock_service = Mock(spec=EventProducerService)
        mock_create_service.return_value = mock_service

        mock_sleep.side_effect = [None, KeyboardInterrupt()]

        with pytest.raises(KeyboardInterrupt):
            main()

        # Sleep duration should be batch_size / event_rate = 10 / 20 = 0.5
        mock_sleep.assert_called_with(0.5)

    @patch('src.entrypoint.main.time.sleep')
    @patch('src.entrypoint.main.OrderEventGenerator')
    @patch('src.entrypoint.main.create_producer_service')
    @patch('src.entrypoint.main.Settings')
    @patch('src.entrypoint.main.logger')
    def test_main_loads_settings_from_environment(self, mock_logger, mock_settings_class,
                                                  mock_create_service, mock_generator_class, mock_sleep):
        """Test main loads settings from environment"""
        mock_settings = Mock(spec=Settings)
        mock_settings.aws_region = "us-east-1"
        mock_settings.kinesis_stream_name = "test-stream"
        mock_settings.event_rate = 10
        mock_settings.batch_size = 5
        mock_settings_class.from_environment.return_value = mock_settings

        mock_generator = Mock(spec=OrderEventGenerator)
        mock_generator.generate.return_value = Mock()
        mock_generator_class.return_value = mock_generator

        mock_service = Mock(spec=EventProducerService)
        mock_create_service.return_value = mock_service

        mock_sleep.side_effect = [None, KeyboardInterrupt()]

        with pytest.raises(KeyboardInterrupt):
            main()

        mock_settings_class.from_environment.assert_called_once()

    @patch('src.entrypoint.main.time.sleep')
    @patch('src.entrypoint.main.OrderEventGenerator')
    @patch('src.entrypoint.main.create_producer_service')
    @patch('src.entrypoint.main.Settings')
    @patch('src.entrypoint.main.logger')
    def test_main_creates_producer_service(self, mock_logger, mock_settings_class,
                                           mock_create_service, mock_generator_class, mock_sleep):
        """Test main creates producer service with settings"""
        mock_settings = Mock(spec=Settings)
        mock_settings.aws_region = "us-east-1"
        mock_settings.kinesis_stream_name = "test-stream"
        mock_settings.event_rate = 10
        mock_settings.batch_size = 5
        mock_settings_class.from_environment.return_value = mock_settings

        mock_generator = Mock(spec=OrderEventGenerator)
        mock_generator.generate.return_value = Mock()
        mock_generator_class.return_value = mock_generator

        mock_service = Mock(spec=EventProducerService)
        mock_create_service.return_value = mock_service

        mock_sleep.side_effect = [None, KeyboardInterrupt()]

        with pytest.raises(KeyboardInterrupt):
            main()

        mock_create_service.assert_called_once_with(mock_settings)

    @patch('src.entrypoint.main.time.sleep')
    @patch('src.entrypoint.main.OrderEventGenerator')
    @patch('src.entrypoint.main.create_producer_service')
    @patch('src.entrypoint.main.Settings')
    @patch('src.entrypoint.main.logger')
    def test_main_infinite_loop(self, mock_logger, mock_settings_class, mock_create_service,
                                mock_generator_class, mock_sleep):
        """Test main runs in infinite loop until interrupted"""
        mock_settings = Mock(spec=Settings)
        mock_settings.aws_region = "us-east-1"
        mock_settings.kinesis_stream_name = "test-stream"
        mock_settings.event_rate = 10
        mock_settings.batch_size = 1
        mock_settings_class.from_environment.return_value = mock_settings

        mock_generator = Mock(spec=OrderEventGenerator)
        mock_generator.generate.return_value = Mock()
        mock_generator_class.return_value = mock_generator

        mock_service = Mock(spec=EventProducerService)
        mock_create_service.return_value = mock_service

        # Simulate 3 iterations then stop
        mock_sleep.side_effect = [None, None, None, KeyboardInterrupt()]

        with pytest.raises(KeyboardInterrupt):
            main()

        # Should have published 3 batches
        assert mock_service.publish_batch.call_count == 4  # 4 iterations total
        assert mock_sleep.call_count == 4  # 3 iterations + 1 final check