# Testing LOGKISS

This document explains how testing is organized for the LOGKISS project.

## Test Organization

Tests are organized into two main categories:

1. **Unit Tests**: These tests run without external dependencies and can run in any environment, including CI pipelines.
2. **E2E Tests**: End-to-end tests that require real cloud service credentials (AWS, GCP) and are skipped in CI environments by default.

## Mock Tests vs E2E Tests

- **Mock Tests**: `test_aws_handler_mock.py` and `test_gcp_handler_mock.py` use mocked cloud services and can run without credentials.
- **E2E Tests**: `test_aws_log.py` and `test_gcp_logging.py` connect to actual cloud services and require proper credentials.

## Running Tests

### Running All Unit Tests (No Cloud Services)

There are several ways to run tests while excluding cloud-related tests:

```bash
# Method 1: Run all tests except those marked with e2e, aws, or gcp
pytest tests/ -v -k "not aws and not gcp and not e2e"

# Method 2: Exclude specific test files
pytest tests/ --ignore=tests/test_aws_log.py --ignore=tests/test_gcp_logging.py --ignore=tests/test_structured_log.py -v

# Method 3: Run specific test files only
pytest tests/test_basic.py tests/test_config.py tests/test_console_handler.py -v

# Method 4: Simulate CI environment to automatically skip cloud tests
GITHUB_ACTIONS=true pytest tests/ -v
```

### Configuring Cloud Credentials

#### AWS Credentials Setup

```bash
# Option 1: Using AWS profile
export AWS_PROFILE=your-aws-profile-name

# Option 2: Using explicit credentials
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_REGION=your-region  # e.g., us-west-2, ap-northeast-1
```

#### GCP Credentials Setup

```bash
# Option 1: Using service account key file
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-service-account-key.json
export GCP_PROJECT_ID=your-gcp-project-id

# Option 2: Using gcloud CLI authentication
gcloud auth application-default login
export GCP_PROJECT_ID=your-gcp-project-id
```

### Running AWS Tests

```bash
# Run only AWS mock tests (no credentials needed)
pytest tests/test_aws_handler_mock.py -v

# Run AWS E2E tests (requires credentials)
pytest tests/test_aws_log.py -v

# Run only tests marked with aws
pytest tests/ -v -m aws

# Or run all tests including AWS tests
RUN_AWS_TESTS=1 pytest tests/ -v
```

### Running GCP Tests

```bash
# Run only GCP mock tests (no credentials needed)
pytest tests/test_gcp_handler_mock.py -v

# Run GCP E2E tests (requires credentials)
pytest tests/test_gcp_logging.py -v

# Run only tests marked with gcp
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

### How Cloud Tests Are Skipped in CI

The automatic skipping of cloud tests in CI environments is implemented in `conftest.py`. Here's how it works:

1. The `is_ci_environment()` function checks if the `GITHUB_ACTIONS` environment variable is set to `"true"`.

2. The `pytest_collection_modifyitems()` function adds skip markers to tests with `aws`, `gcp`, or `e2e` markers when running in a CI environment, unless the corresponding environment variables (`RUN_AWS_TESTS`, `RUN_GCP_TESTS`, or `RUN_E2E_TESTS`) are explicitly set.

3. In the GitHub Actions workflow (`.github/workflows/test.yml`), the `GITHUB_ACTIONS` environment variable is automatically set to `"true"`, which triggers this skipping mechanism.

### Simulating CI Environment Locally

You can simulate the CI environment locally to automatically skip cloud tests:

```bash
# Set GITHUB_ACTIONS environment variable to skip cloud tests
GITHUB_ACTIONS=true pytest tests/ -v
```

This will run the tests as if they were running in GitHub Actions, automatically skipping all cloud-related tests.

## テスト実行方法 (日本語)

### テスト構成

- **単体テスト**: クラウド接続を必要としないモックテスト
- **E2Eテスト**: 実際のクラウドサービスに接続するテスト

### クラウド認証情報の設定

#### AWS認証情報

```bash
# 方法1: AWSプロファイルを使用
export AWS_PROFILE=プロファイル名

# 方法2: 直接認証情報を設定
export AWS_ACCESS_KEY_ID=アクセスキーID
export AWS_SECRET_ACCESS_KEY=シークレットアクセスキー
export AWS_REGION=リージョン名  # 例: ap-northeast-1
```

#### GCP認証情報

```bash
# 方法1: サービスアカウントキーファイルを使用
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/サービスアカウントキー.json
export GCP_PROJECT_ID=プロジェクトID

# 方法2: gcloudコマンドで認証
gcloud auth application-default login
export GCP_PROJECT_ID=プロジェクトID
```

### テスト実行コマンド

```bash
# モックテストのみ実行（認証情報不要）
pytest tests/test_aws_handler_mock.py tests/test_gcp_handler_mock.py -v

# クラウドテストを除外して実行
pytest tests/ -v -k "not aws and not gcp and not e2e"

# CI環境をシミュレートしてクラウドテストを自動スキップ
GITHUB_ACTIONS=true pytest tests/ -v

# AWSのE2Eテスト実行（認証情報必要）
pytest tests/test_aws_log.py -v

# GCPのE2Eテスト実行（認証情報必要）
pytest tests/test_gcp_logging.py -v

# 全テスト実行（E2E含む）
RUN_E2E_TESTS=1 RUN_AWS_TESTS=1 RUN_GCP_TESTS=1 pytest tests/ -v
```
