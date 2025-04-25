#!/usr/bin/env python
"""
例外処理のサンプル（AWS CloudWatch）

このサンプルでは、logkissモジュールを使用してAWS CloudWatchに例外情報を出力する方法を示します。
"""

import os
import sys
import traceback
import webbrowser
from datetime import datetime

# logkissモジュールをインポート
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import logkiss
from logkiss.handlers import AWSCloudWatchHandler


def configure_logging():
    """ロギングの設定"""
    # ロガーの設定
    logger = logkiss.getLogger("exception_aws_sample")
    logger.setLevel(logkiss.DEBUG)

    # AWS regionの取得
    region = os.environ.get("AWS_REGION")
    if not region:
        print("環境変数 AWS_REGION が設定されていません。")
        print("例: export AWS_REGION=ap-northeast-1")
        sys.exit(1)

    # ロググループとログストリームの設定
    log_group_name = f"/logkiss/exception_test_{datetime.now().strftime('%Y%m%d')}"
    log_stream_name = f"exception_test_{datetime.now().strftime('%H%M%S')}"

    # AWS CloudWatchハンドラーを追加
    aws_handler = AWSCloudWatchHandler(region_name=region, log_group_name=log_group_name, log_stream_name=log_stream_name)
    logger.addHandler(aws_handler)

    print(f"AWS CloudWatch ハンドラーを追加しました (リージョン: {region}, ロググループ: {log_group_name}, ログストリーム: {log_stream_name})")
    return logger, region, log_group_name, log_stream_name


def simulate_error():
    """エラーをシミュレート"""

    # いくつかのネストされた関数呼び出し
    def level1():
        def level2():
            def level3():
                # 0除算エラーを発生させる
                return 1 / 0

            return level3()

        return level2()

    return level1()


def demonstrate_exception_logging(logger):
    """例外のログ出力方法をデモンストレーション"""
    print("\n=== 例外のログ出力方法 ===")

    # 方法1: exc_info=True を使用
    try:
        print("\n方法1: exc_info=True を使用")
        result = simulate_error()
    except Exception as e:
        logger.error("エラーが発生しました: %s", str(e), exc_info=True)

    # 方法2: 例外オブジェクトを直接渡す
    try:
        print("\n方法2: 例外オブジェクトを直接渡す")
        result = simulate_error()
    except Exception as e:
        logger.error("エラーが発生しました: %s", str(e), exc_info=e)

    # 方法3: logger.exception() を使用（常にexc_info=Trueと同じ）
    try:
        print("\n方法3: logger.exception() を使用")
        result = simulate_error()
    except Exception as e:
        logger.exception("エラーが発生しました: %s", str(e))

    # 方法4: スタックトレースを手動で取得して出力
    try:
        print("\n方法4: スタックトレースを手動で取得")
        result = simulate_error()
    except Exception as e:
        stack_trace = traceback.format_exc()
        logger.error("エラーが発生しました: %s\n%s", str(e), stack_trace)

    # 方法5: 構造化ログとして出力
    try:
        print("\n方法5: 構造化ログとして出力")
        result = simulate_error()
    except Exception as e:
        logger.error("エラーが発生しました", extra={"error_type": type(e).__name__, "error_message": str(e), "stack_trace": traceback.format_exc()})


def open_aws_console(region, log_group_name, log_stream_name):
    """AWS CloudWatchコンソールを開く"""
    # AWS CloudWatchコンソールを開く
    url = (
        f"https://{region}.console.aws.amazon.com/cloudwatch/home"
        f"?region={region}#logsV2:log-groups/log-group/{log_group_name.replace('/', '%2F')}"
        f"/log-events/{log_stream_name.replace('/', '%2F')}"
    )
    print(f"\nAWS CloudWatchコンソールを開きます: {url}")
    webbrowser.open(url)


def main():
    """メイン関数"""
    print("=== AWS CloudWatchでの例外処理サンプル ===")

    # ロギングを設定
    logger, region, log_group_name, log_stream_name = configure_logging()

    # 例外のログ出力方法をデモンストレーション
    demonstrate_exception_logging(logger)

    # ログを確実に送信するために少し待機
    import time

    print("\nログを送信中...")
    time.sleep(3)

    # AWS CloudWatchコンソールを開く
    open_aws_console(region, log_group_name, log_stream_name)


if __name__ == "__main__":
    main()
