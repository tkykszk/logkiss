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


def test_gcp_structured_logging():
    """Test structured logging with Google Cloud Logging."""
    mock_client = mock.MagicMock()
    handler = GCloudLoggingHandler(project_id="test-project")
    handler.handler.transport = mock_client
    
    logger = logging.getLogger("test_gcp")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    # Test structured logging with json_fields
    logger.info(
        "Test message",
        extra={
            "json_fields": {
                "user_id": "123",
                "action": "login",
                "status": "success"
            }
        }
    )
    
    # Verify the structured data was properly formatted
    last_call = mock_client.send.call_args[0][0]
    assert "json_fields" in last_call.labels
    assert last_call.labels["json_fields"]["user_id"] == "123"
    
    # Test nested structured data
    logger.error(
        "Error occurred",
        extra={
            "json_fields": {
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
        }
    )
    
    # Verify nested data handling
    last_call = mock_client.send.call_args[0][0]
    assert last_call.labels["json_fields"]["error"]["type"] == "ValueError"


def test_aws_structured_logging():
    """Test structured logging with AWS CloudWatch Logs."""
    mock_client = mock.MagicMock()
    handler = AWSCloudWatchHandler(
        log_group="test-group",
        log_stream="test-stream"
    )
    handler.client = mock_client
    
    logger = logging.getLogger("test_aws")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    # Test structured logging
    logger.info(
        "Test message",
        extra={
            "user_id": "123",
            "action": "login"
        }
    )
    
    # Verify the structured data was properly formatted
    last_call = mock_client.put_log_events.call_args[1]
    log_event = json.loads(last_call["logEvents"][0]["message"])
    assert log_event["extra"]["user_id"] == "123"
    
    # Test with complex data types
    logger.error(
        "Error occurred",
        extra={
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
    )
    
    # Verify complex data handling
    last_call = mock_client.put_log_events.call_args[1]
    log_event = json.loads(last_call["logEvents"][0]["message"])
    assert log_event["extra"]["error"]["code"] == 500
    assert isinstance(log_event["extra"]["error"]["details"], list)


def test_invalid_structured_data():
    """Test handling of invalid structured data."""
    mock_client = mock.MagicMock()
    handler = GCloudLoggingHandler(project_id="test-project")
    handler.handler.transport = mock_client
    
    logger = logging.getLogger("test_invalid")
    logger.addHandler(handler)
    
    # Test with non-serializable object
    class NonSerializable:
        pass
    
    logger.info(
        "Test message",
        extra={
            "json_fields": {
                "obj": NonSerializable()
            }
        }
    )
    
    # Verify fallback to string representation
    last_call = mock_client.send.call_args[0][0]
    assert isinstance(last_call.labels["json_fields"]["obj"], str)
