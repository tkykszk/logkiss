#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple test cases for logkiss.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.
"""

import io
import sys
import logkiss as logging


def capture_output():
    """Capture the output to a string buffer"""
    output = io.StringIO()
    sys.stderr = output
    # Update logger handlers
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        if isinstance(handler, logging.KissConsoleHandler):
            handler.stream = output
    return output


def restore_output(output):
    """Restore the output and get the captured content"""
    sys.stderr = sys.__stderr__
    return output.getvalue()


def reset_logger():
    """Reset the logger to its default state"""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set default level to DEBUG
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    handler = logging.KissConsoleHandler()
    handler.setLevel(logging.DEBUG)  # Set handler level to DEBUG
    logger.addHandler(handler)


def test_simplest():
    """Test simplest.py"""
    reset_logger()  # Reset logger
    output = capture_output()

    # Output logs
    logging.debug("Debug message")
    logging.info("Info message")
    logging.warning("Warning message")
    logging.error("Error message")
    logging.critical("Critical message")

    result = restore_output(output)
    lines = [line for line in result.split("\n") if line]

    # Verify all 5 levels are output
    assert len(lines) == 5, f"Expected 5 lines, got {len(lines)}"
    assert "DEBUG" in lines[0]
    assert "INFO" in lines[1]
    assert "WARN" in lines[2]
    assert "ERROR" in lines[3]
    assert "CRITI" in lines[4]


def test_simple():
    """Test simple.py"""
    reset_logger()  # Reset logger
    output = capture_output()

    # Get logger
    logger = logging.getLogger()

    # Output logs
    logging.getLogger().debug("Debug message")
    logging.getLogger().info("Info message")
    logging.getLogger().warning("Warning message")
    logging.getLogger().error("Error message")
    logging.getLogger().critical("Critical message")

    result = restore_output(output)
    lines = [line for line in result.split("\n") if line]

    # Verify all 5 levels are output
    assert len(lines) == 5, f"Expected 5 lines, got {len(lines)}"
    assert "DEBUG" in lines[0]
    assert "INFO" in lines[1]
    assert "WARN" in lines[2]
    assert "ERROR" in lines[3]
    assert "CRITI" in lines[4]


def test_simple_config():
    """Test simple_config.py"""
    reset_logger()  # Reset logger
    output = capture_output()

    # Set logger and handler to DEBUG level
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    for handler in logger.handlers:
        handler.setLevel(logging.DEBUG)

    # Output logs
    logging.getLogger().debug("Debug message")
    logging.getLogger().info("Info message")
    logging.getLogger().warning("Warning message")
    logging.getLogger().error("Error message")
    logging.getLogger().critical("Critical message")

    result = restore_output(output)
    lines = [line for line in result.split("\n") if line]

    # Verify all 5 levels are output
    assert len(lines) == 5, f"Expected 5 lines, got {len(lines)}"
    assert "DEBUG" in lines[0]
    assert "INFO" in lines[1]
    assert "WARN" in lines[2]
    assert "ERROR" in lines[3]
    assert "CRITI" in lines[4]


def test_simple_config_2():
    """Test simple_config_2.py"""
    reset_logger()  # Reset logger
    output = capture_output()

    # Set logger to ERROR level
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)

    # Output logs
    logging.getLogger().debug("Debug message")
    logging.getLogger().info("Info message")
    logging.getLogger().warning("Warning message")
    logging.getLogger().error("Error message")
    logging.getLogger().critical("Critical message")

    result = restore_output(output)
    lines = [line for line in result.split("\n") if line]

    # Verify only ERROR and CRITICAL are output
    assert len(lines) == 2, f"Expected 2 lines, got {len(lines)}"
    assert "ERROR" in lines[0]
    assert "CRITI" in lines[1]
