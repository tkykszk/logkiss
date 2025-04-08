# Testing LOGKISS

This document explains how testing is organized for the LOGKISS project.

## Test Organization

Tests are organized into two main categories:

1. **Unit Tests**: These tests run without external dependencies and can run in any environment, including CI pipelines.
2. **E2E Tests**: End-to-end tests that require real cloud service credentials (AWS, GCP) and are skipped in CI environments by default.

## Running Tests

### Running All Unit Tests (No Cloud Services)

```bash
# Run all tests except those marked with e2e, aws, or gcp
pytest tests/ -v
```

### Running AWS Tests

```bash
# Make sure you have AWS credentials configured
# Either set AWS_PROFILE or AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY

# Run only AWS tests
pytest tests/ -v -m aws

# Or run all tests including AWS tests
RUN_AWS_TESTS=1 pytest tests/ -v
```

### Running GCP Tests

```bash
# Make sure you have GCP credentials configured
# Either authenticate with gcloud auth or set GOOGLE_APPLICATION_CREDENTIALS

# Run only GCP tests
pytest tests/ -v -m gcp

# Or run all tests including GCP tests
RUN_GCP_TESTS=1 pytest tests/ -v
```

### Running All Tests Including E2E Tests

```bash
# Run everything
RUN_E2E_TESTS=1 RUN_AWS_TESTS=1 RUN_GCP_TESTS=1 pytest tests/ -v
```

## Test Markers

The following pytest markers are used:

- `@pytest.mark.e2e`: End-to-end tests that may interact with external services
- `@pytest.mark.aws`: Tests that require AWS credentials
- `@pytest.mark.gcp`: Tests that require GCP credentials

## CI Environment

In CI environments (GitHub Actions), tests with the above markers are automatically skipped unless explicitly enabled with environment variables:

- `RUN_E2E_TESTS=1`
- `RUN_AWS_TESTS=1`
- `RUN_GCP_TESTS=1`

This ensures that CI builds don't fail due to missing credentials while still allowing thorough testing in development environments.
