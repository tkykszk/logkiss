# LOGKISS Test Case Specification

This file contains test cases for the LOGKISS library examples.

## Basic Logging Test

### TestCases (basic_logging.py)

- ID: TC001
  Name: Basic Warning Log Output
  Desc: Test that warning logs are displayed in the console
  Pre-conditions: LOGKISS is installed
  Test Steps: |
    1. Import logkiss as logging
    2. Call logging.warning with a message
    3. Observe the console output
  Expected Result: Warning message is displayed in the console with proper formatting and color
  Test Data: "Watch out!"
  Priority: High
  Severity: Medium
  Status: Not implemented
  Environment: Python 3.12
  Comments/Notes: Default log level is WARNING, so this message should be displayed

- ID: TC002
  Name: Basic Info Log Filtering
  Desc: Test that info logs are not displayed with default log level
  Pre-conditions: LOGKISS is installed
  Test Steps: |
    1. Import logkiss as logging
    2. Call logging.info with a message
    3. Observe the console output
  Expected Result: No output in the console
  Test Data: "I told you so"
  Priority: Medium
  Severity: Low
  Status: Not implemented
  Environment: Python 3.12
  Comments/Notes: Default log level is WARNING, so INFO messages should be filtered out

## File Logging Test

### TestCases (sample_file_logging.py)

- ID: TC003
  Name: Configure File Logging
  Desc: Test configuration of logging to write to a file
  Pre-conditions: LOGKISS is installed
  Test Steps: |
    1. Import logkiss as logging
    2. Configure logging with basicConfig to write to a file
    3. Set the log level to DEBUG
    4. Create a logger with getLogger
    5. Log messages at different levels
    6. Check the log file
  Expected Result: All log messages (debug, info, warning, error, critical) are written to the file
  Test Data: Log messages at different levels
  Priority: High
  Severity: Medium
  Status: Not implemented
  Environment: Python 3.12
  Comments/Notes: File format should follow the specified format pattern

## Multi-Logger Test

### TestCases (sample_multi_logger.py)

- ID: TC004
  Name: Console-Only Logger Configuration
  Desc: Test creating a logger that only outputs to console
  Pre-conditions: LOGKISS is installed
  Test Steps: |
    1. Import logkiss as logging
    2. Create a logger with getLogger('console')
    3. Remove any existing handlers
    4. Set log level to DEBUG
    5. Add KissConsoleHandler
    6. Set propagate to False
    7. Log messages at different levels
  Expected Result: All messages appear in the console with proper formatting and color
  Test Data: Log messages at different levels
  Priority: High
  Severity: Medium
  Status: Not implemented
  Environment: Python 3.12
  Comments/Notes: Verify that console output is properly colored

- ID: TC005
  Name: Dual Output Logger Configuration
  Desc: Test creating a logger that outputs to both console and file
  Pre-conditions: LOGKISS is installed
  Test Steps: |
    1. Import logkiss as logging
    2. Create a logger with getLogger('both')
    3. Remove any existing handlers
    4. Set log level to DEBUG
    5. Add KissConsoleHandler for console output
    6. Add FileHandler with ColoredFormatter (no colors) for file output
    7. Set propagate to False
    8. Log messages at different levels
  Expected Result: Messages appear in both console (with color) and in the log file (without color)
  Test Data: Log messages at different levels
  Priority: High
  Severity: Medium
  Status: Not implemented
  Environment: Python 3.12
  Comments/Notes: Verify that console output is colored and file output has proper formatting

## Color Configuration Test

## Minimal Warning Method Test

### TestCases (minimal_warning.py)

- ID: TC008
  Name: Minimal Warning Method Compatibility
  Desc: Test that logkiss supports the same minimal usage as standard logging.warning
  Pre-conditions: LOGKISS is installed
  Test Steps: |
    1. Import logkiss as logging
    2. Call logging.warning with a message (省略メソッド)
    3. Observe the console output
  Expected Result: Warning message is displayed in the console with proper formatting and color
  Test Data: "初学者を惑わせがちな省略メソッド"
  Priority: High
  Severity: Medium
  Status: Not implemented
  Environment: Python 3.12
  Comments/Notes: Should behave identically to standard logging.warning


### TestCases (disable_color.py)

- ID: TC006
  Name: Disable Colors via Environment Variable
  Desc: Test that colors can be disabled using LOGKISS_DISABLE_COLOR environment variable
  Pre-conditions: LOGKISS is installed
  Test Steps: |
    1. Set the LOGKISS_DISABLE_COLOR environment variable to "1"
    2. Import logkiss
    3. Create a logger
    4. Log messages at different levels
    5. Observe console output
  Expected Result: Log messages are displayed without color formatting
  Test Data: Log messages at different levels
  Priority: Medium
  Severity: Low
  Status: Not implemented
  Environment: Python 3.12
  Comments/Notes: Color should be disabled when the environment variable is set

- ID: TC007
  Name: Enable Debug Mode via Environment Variable
  Desc: Test that debug mode can be enabled using LOGKISS_DEBUG environment variable
  Pre-conditions: LOGKISS is installed
  Test Steps: |
    1. Set the LOGKISS_DEBUG environment variable to "1"
    2. Import logkiss
    3. Create a logger
    4. Log debug message
    5. Observe console output
  Expected Result: Debug messages are displayed in the console
  Test Data: Debug log message
  Priority: Medium
  Severity: Low
  Status: Not implemented
  Environment: Python 3.12
  Comments/Notes: Debug level should be enabled when the environment variable is set
