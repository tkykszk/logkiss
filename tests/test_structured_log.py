"""Test structured logging functionality.

This module tests the structured logging capabilities,
particularly focusing on cloud logging integration.
"""

import json
import logging
from unittest import mock

import pytest

from logkiss.handler_aws import AWSCloudWatchHandler
from logkiss.handler_gcp import GCloudLoggingHandler


@pytest.fixture
def mock_gcp_handler():
    """Create a mocked GCP logging handler."""
    mock_client = mock.MagicMock()
    handler = GCloudLoggingHandler(project_id="test-project")
    handler.handler.transport = mock_client
    return handler, mock_client


@pytest.fixture
def mock_aws_handler():
    """Create a mocked AWS CloudWatch handler."""
    mock_client = mock.MagicMock()
    handler = AWSCloudWatchHandler(
        log_group="test-group",
        log_stream="test-stream"
    )
    handler.client = mock_client
    return handler, mock_client


@pytest.mark.gcp
def test_gcp_structured_logging(mock_gcp_handler):
    """Test structured logging with Google Cloud Logging."""
    handler, mock_client = mock_gcp_handler
    
    logger = logging.getLogger("test_gcp")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    # Test structured logging with json_fields
    structured_data = {
        "user_id": "123",
        "action": "login",
        "status": "success"
    }
    
    logger.info(
        "Test message",
        extra={"json_fields": structured_data}
    )
    
    # Verify the structured data was properly formatted
    last_call = mock_client.send.call_args[0][0]
    assert hasattr(last_call, "json_fields")
    assert last_call.json_fields == structured_data
    
    # Test nested structured data
    nested_data = {
        "error": {
            "type": "ValueError",
            "message": "Invalid input",
            "stack_trace": "..."
        },
        "context": {
            "user_id": "123",
            "request_id": "abc"
        }
    }
    
    logger.error(
        "Error occurred",
        extra={"json_fields": nested_data}
    )
    
    # Verify nested data handling
    last_call = mock_client.send.call_args[0][0]
    assert last_call.json_fields["error"]["type"] == "ValueError"


@pytest.mark.aws
def test_aws_structured_logging(mock_aws_handler):
    """Test structured logging with AWS CloudWatch Logs."""
    handler, mock_client = mock_aws_handler
    
    logger = logging.getLogger("test_aws")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    # Test structured logging
    structured_data = {
        "user_id": "123",
        "action": "login"
    }
    
    logger.info(
        "Test message",
        extra=structured_data
    )
    
    # Verify the structured data was properly formatted
    last_call = mock_client.put_log_events.call_args.kwargs
    log_event = json.loads(last_call["logEvents"][0]["message"])
    assert log_event["extra"] == structured_data
    
    # Test with complex data types
    complex_data = {
        "error": {
            "code": 500,
            "message": "Internal error",
            "details": ["detail1", "detail2"]
        },
        "metadata": {
            "version": "1.0",
            "timestamp": 12345
        }
    }
    
    logger.error(
        "Error occurred",
        extra=complex_data
    )
    
    # Verify complex data handling
    last_call = mock_client.put_log_events.call_args.kwargs
    log_event = json.loads(last_call["logEvents"][0]["message"])
    assert log_event["extra"] == complex_data


@pytest.mark.gcp
def test_invalid_structured_data(mock_gcp_handler):
    """Test handling of invalid structured data."""
    handler, mock_client = mock_gcp_handler
    
    logger = logging.getLogger("test_invalid")
    logger.addHandler(handler)
    
    class NonSerializable:
        def __str__(self):
            return "<NonSerializable object>"
    
    logger.info(
        "Test message",
        extra={"json_fields": {"obj": NonSerializable()}}
    )
    
    # Verify fallback to string representation
    last_call = mock_client.send.call_args[0][0]
    assert last_call.json_fields["obj"] == "<NonSerializable object>"
