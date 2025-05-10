#!/usr/bin/env python
"""
AWS CloudWatch Logs Sample

This sample demonstrates how to send logs to AWS CloudWatch Logs using logkiss.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
"""

import json
import os
import socket
import uuid
import hashlib
import logging
from datetime import datetime

import boto3

# Get AWS settings from environment variables
AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

# Import logkiss
import logkiss
from logkiss.handlers import AWSCloudWatchHandler


# Generate unique log group name (for testing)
def generate_test_log_group_name():
    """Generate a unique log group name for testing (using short hash value)"""
    timestamp = datetime.now().strftime("%Y%m%d")
    unique_id = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:12]
    return f"logkiss-test-{timestamp}-{unique_id}"


# Cleanup flag (whether to delete resources after testing)
CLEAN_UP = True


def main():
    """Main function"""
    # Import necessary modules
    import time
    import logging
    from logkiss import getLogger
    from logkiss.handlers import AWSCloudWatchHandler

    # Set log group and stream names
    log_group_name = generate_test_log_group_name()
    log_stream_name = f"sample-{datetime.now().strftime('%H%M%S')}"
    print(f"Log group name: {log_group_name}")
    print(f"Log stream name: {log_stream_name}")

    # Configure logger
    logger = getLogger("aws_sample")
    logger.setLevel(logging.DEBUG)

    # Clear existing handlers (to avoid duplicate output)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Add AWSCloudWatchHandler
    try:
        aws_handler = AWSCloudWatchHandler(
            log_group_name=log_group_name,
            log_stream_name=log_stream_name,
            region_name=AWS_REGION,
            batch_size=10,  # Set small batch size (for sample)
            flush_interval=2.0,  # Set short flush interval (for sample)
        )
        logger.addHandler(aws_handler)
        print("Added AWS CloudWatch Logs handler")
    except ImportError as e:
        print(f"Error: {e}")
        print("Please install the boto3 package: pip install 'logkiss[cloud]'")
        return

    # Output logs
    print("\n=== Starting log output ===")
    logger.info("Starting AWS CloudWatch Logs sample")
    logger.debug("This is a debug message")

    # Output structured log
    logger.warning(
        "User failed to login", extra={"user_id": 12345, "ip_address": "192.168.1.100", "attempts": 3, "timestamp": time.time()}
    )

    # Output error log
    try:
        result = 10 / 0
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", extra={"error_type": type(e).__name__, "timestamp": time.time()})

    # Wait for the batch to be flushed
    print("Sending logs to CloudWatch Logs...")
    time.sleep(3)

    # Explicitly close the handler
    print("Closing handler...")
    aws_handler.close()

    # Display how to check logs
    print("\n=== How to check logs ===")
    print(f"1. Open AWS Management Console: https://console.aws.amazon.com/cloudwatch/")
    print(f"2. Select 'Log groups' from the left menu")
    print(f"3. Search for log group '{log_group_name}'")
    print(f"4. Click on log stream '{log_stream_name}'")
    print("\nOr run the following AWS CLI command:")
    print(f"aws logs get-log-events --log-group-name {log_group_name} " f"--log-stream-name {log_stream_name} --region {AWS_REGION}")

    # Cleanup (delete test resources)
    if CLEAN_UP:
        print("\n=== Cleanup ===")
        print(f"Deleting log group '{log_group_name}'...")
        try:
            import boto3

            logs_client = boto3.client("logs", region_name=AWS_REGION)

            # Open CloudWatch Logs console
            import webbrowser

            region = logs_client.meta.region_name
            # URL to directly access the specific log group
            console_url = f"https://{region}.console.aws.amazon.com/cloudwatch/home?region={region}#logsV2:log-groups/log-group/{log_group_name}"
            print(f"Opening CloudWatch Logs console: {console_url}")
            webbrowser.open(console_url)

            # Wait a bit before deleting the log group (wait for browser to open)
            import time

            time.sleep(2)

            # Delete log group
            logs_client.delete_log_group(logGroupName=log_group_name)
            print("Log group deleted")
        except Exception as e:
            print(f"Error occurred during cleanup: {e}")
    else:
        print("\n=== Cleanup was skipped ===")
        print("Resources will not be deleted because CLEAN_UP = False")


if __name__ == "__main__":
    main()
