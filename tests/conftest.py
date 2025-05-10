"""
Test configuration for Pytest.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.
"""

import os
import pytest


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "e2e: mark test as end-to-end test requiring cloud credentials")
    config.addinivalue_line("markers", "aws: mark test as requiring AWS credentials")
    config.addinivalue_line("markers", "gcp: mark test as requiring GCP credentials")
    config.addinivalue_line("markers", "timeout: mark test with timeout in seconds")
    
    # モジュール依存関係のマーカー
    config.addinivalue_line("markers", "requires_logging_tree: logging_treeモジュールが必要なテスト")
    config.addinivalue_line("markers", "requires_boto3: boto3モジュールが必要なテスト")
    config.addinivalue_line("markers", "requires_gcp_logging: Google Cloud Loggingモジュールが必要なテスト")
    config.addinivalue_line("markers", "env_vars: 環境変数のテスト")
    config.addinivalue_line("markers", "config: 設定ファイルのテスト")


def is_ci_environment():
    """Check if we're running in a CI environment."""
    # GitHub Actions sets this environment variable
    return os.environ.get("GITHUB_ACTIONS") == "true"


def pytest_collection_modifyitems(config, items):
    """Skip e2e tests in CI environment by default."""
    # If running in CI and the specific flags to enable cloud tests are not set,
    # skip these tests
    if is_ci_environment():
        run_aws_tests = os.environ.get("RUN_AWS_TESTS", "").lower() in ("1", "true", "yes")
        run_gcp_tests = os.environ.get("RUN_GCP_TESTS", "").lower() in ("1", "true", "yes")
        run_e2e_tests = os.environ.get("RUN_E2E_TESTS", "").lower() in ("1", "true", "yes")

        for item in items:
            # Skip e2e tests unless specifically enabled
            if "e2e" in item.keywords and not run_e2e_tests:
                item.add_marker(pytest.mark.skip(reason="E2E tests are disabled in CI"))
            # Skip AWS tests unless specifically enabled
            elif "aws" in item.keywords and not run_aws_tests:
                item.add_marker(pytest.mark.skip(reason="AWS tests are disabled in CI"))
            # Skip GCP tests unless specifically enabled
            elif "gcp" in item.keywords and not run_gcp_tests:
                item.add_marker(pytest.mark.skip(reason="GCP tests are disabled in CI"))
