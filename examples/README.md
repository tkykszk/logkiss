# logkiss Sample Code Collection

This directory contains sample code demonstrating how to use Python's logging module in combination with logkiss.

## ⚠️ This is an Alpha Release

This package is currently in alpha. Interfaces and behaviors may change without notice. Use at your own risk.

## Sample List

### console_handler_example.py

A sample demonstrating how to output logs to the console by combining the standard Python logging module with logkiss.

**Main Features**:
- Setting up a colored console handler using `logkiss.logkiss.KissConsoleHandler`
- Outputting normal log messages
- Outputting structured logs
- Outputting nested structured logs
- Example of using the root logger

**How to Install**:

```bash
# install from github
pip install 'git+https://github.com/tkykszk/logkiss.git'

```


**How to Run**:
```bash
python examples/console_handler_example.py
```

### file_handler_example.py

A sample demonstrating how to output logs to a file using logkiss.

**Main Features**:
- Setting up a file handler
- Log rotation
- Log filtering
- Specifying log formats

**How to Run**:
```bash
python examples/file_handler_example.py
```

### Cloud Logging Examples

#### sample_aws_fixed.py

Example of sending logs to AWS CloudWatch Logs.

**Main Features**:
- Setting up an AWS CloudWatch Logs handler
- Sending logs to CloudWatch Logs
- Managing log groups and streams
- Error handling for cloud logging

**How to Run** (AWS credentials required):
```bash
AWS_DEFAULT_REGION=us-west-2 python examples/sample_aws_fixed.py
```

#### sample_gcp_fixed.py

Example of sending logs to Google Cloud Logging.

**Main Features**:
- Setting up a Google Cloud Logging handler
- Sending logs to Cloud Logging
- Managing log names and resources
- Error handling for cloud logging

**How to Run** (GCP credentials required):
```bash
GCP_PROJECT_ID=your-project-id python examples/sample_gcp_fixed.py
```

### Proof of Concept Examples

The `poc` directory contains various proof-of-concept examples demonstrating specific features:

- **poc1_sandbox.py**: Basic usage pattern of logkiss
- **poc2_integration.py**: Integration with existing loggers
- **poc2_integration_B.py**: Another integration example
- **poc3_hierarchy_test.py**: Logger hierarchy preservation

These examples are designed to show how logkiss can be used in different scenarios while maintaining the KISS (Keep It Simple, Stupid) principle.
