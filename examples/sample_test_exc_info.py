#!/usr/bin/env python
"""
exc_info=True の動作テスト
"""

import logging
import traceback
import sys


# 標準のロギング
def test_standard_logging():
    print("\n=== 標準のロギング ===")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger = logging.getLogger("test_standard")

    try:
        1 / 0
    except Exception as e:
        # exc_info=True を使用
        logger.error("エラーが発生しました (exc_info=True)", exc_info=True)

        # 例外オブジェクトを直接渡す
        logger.error("エラーが発生しました (exc_info=e)", exc_info=e)

        # スタックトレースを文字列として渡す
        stack_trace = traceback.format_exc()
        logger.error(f"エラーが発生しました (traceback文字列)\n{stack_trace}")


# logkissを使用
def test_logkiss():
    print("\n=== logkissのロギング ===")
    import logkiss

    logkiss.basicConfig(level=logkiss.DEBUG)
    logger = logkiss.getLogger("test_logkiss")

    try:
        1 / 0
    except Exception as e:
        # exc_info=True を使用
        logger.error("エラーが発生しました (exc_info=True)", exc_info=True)

        # 例外オブジェクトを直接渡す
        logger.error("エラーが発生しました (exc_info=e)", exc_info=e)

        # スタックトレースを文字列として渡す
        stack_trace = traceback.format_exc()
        logger.error(f"エラーが発生しました (traceback文字列)\n{stack_trace}")


# GCP Cloud Loggingを使用
def test_gcp_logging():
    print("\n=== GCP Cloud Loggingのテスト ===")
    import logging
    from logkiss import getLogger
    from logkiss.handlers import GCPCloudLoggingHandler

    # ロガーの設定
    logger = getLogger("test_gcp")
    logger.setLevel(logging.DEBUG)

    # 既存のハンドラーをクリア
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # GCP Cloud Loggingハンドラーを追加
    try:
        gcp_handler = GCPCloudLoggingHandler()
        logger.addHandler(gcp_handler)
        print("GCP Cloud Logging ハンドラーを追加しました")
    except ImportError as e:
        print(f"エラー: {e}")
        print("google-cloud-logging パッケージをインストールしてください: pip install 'logkiss[cloud]'")
        return

    try:
        1 / 0
    except Exception as e:
        # exc_info=True を使用
        logger.error("エラーが発生しました (exc_info=True)", exc_info=True)

        # 例外オブジェクトを直接渡す
        logger.error("エラーが発生しました (exc_info=e)", exc_info=e)

        # スタックトレースを文字列として渡す
        stack_trace = traceback.format_exc()
        logger.error(f"エラーが発生しました (traceback文字列)\n{stack_trace}")

    # ハンドラーをクローズ
    gcp_handler.close()


# AWS CloudWatchを使用
def test_aws_logging():
    print("\n=== AWS CloudWatchのテスト ===")
    import logging
    from logkiss import getLogger
    from logkiss.handlers import AWSCloudWatchHandler

    # ロガーの設定
    logger = getLogger("test_aws")
    logger.setLevel(logging.DEBUG)

    # 既存のハンドラーをクリア
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # AWS CloudWatchハンドラーを追加
    try:
        aws_handler = AWSCloudWatchHandler("logkiss-test-excinfo", "test-stream")
        logger.addHandler(aws_handler)
        print("AWS CloudWatch ハンドラーを追加しました")
    except ImportError as e:
        print(f"エラー: {e}")
        print("boto3 パッケージをインストールしてください: pip install 'logkiss[cloud]'")
        return

    try:
        1 / 0
    except Exception as e:
        # exc_info=True を使用
        logger.error("エラーが発生しました (exc_info=True)", exc_info=True)

        # 例外オブジェクトを直接渡す
        logger.error("エラーが発生しました (exc_info=e)", exc_info=e)

        # スタックトレースを文字列として渡す
        stack_trace = traceback.format_exc()
        logger.error(f"エラーが発生しました (traceback文字列)\n{stack_trace}")

    # ハンドラーをクローズ
    aws_handler.close()


if __name__ == "__main__":
    test_standard_logging()
    test_logkiss()

    # クラウドロギングのテスト
    test_gcp_logging()
    test_aws_logging()
