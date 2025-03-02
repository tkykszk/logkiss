#!/usr/bin/env python
"""
例外処理のサンプル（GCP Cloud Logging）

このサンプルでは、logkissモジュールを使用してGCP Cloud Loggingに例外情報を出力する方法を示します。
"""

import os
import sys
import traceback
import webbrowser
from datetime import datetime

# logkissモジュールをインポート
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logkiss
from logkiss.handlers import GCPCloudLoggingHandler


def configure_logging():
    """ロギングの設定"""
    # ロガーの設定
    logger = logkiss.getLogger("exception_gcp_sample")
    logger.setLevel(logkiss.DEBUG)
    
    # GCPプロジェクトIDの取得
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        print("環境変数 GCP_PROJECT_ID が設定されていません。")
        print("例: export GCP_PROJECT_ID=your-project-id")
        sys.exit(1)
    
    # ログ名の設定
    log_name = f"exception_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # GCP Cloud Loggingハンドラーを追加
    gcp_handler = GCPCloudLoggingHandler(
        project_id=project_id,
        log_name=log_name,
        labels={
            "application": "exception_sample",
            "environment": "development"
        }
    )
    logger.addHandler(gcp_handler)
    
    print(f"GCP Cloud Logging ハンドラーを追加しました (プロジェクトID: {project_id}, ログ名: {log_name})")
    return logger, project_id, log_name


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
        logger.error(
            "エラーが発生しました: %s", str(e), 
            exc_info=True
        )
    
    # 方法2: 例外オブジェクトを直接渡す
    try:
        print("\n方法2: 例外オブジェクトを直接渡す")
        result = simulate_error()
    except Exception as e:
        logger.error(
            "エラーが発生しました: %s", str(e), 
            exc_info=e
        )
    
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
        logger.error(
            "エラーが発生しました", 
            extra={
                "error_type": type(e).__name__,
                "error_message": str(e),
                "stack_trace": traceback.format_exc()
            }
        )


def open_gcp_console(project_id, log_name):
    """GCP Loggingコンソールを開く"""
    # GCP Loggingコンソールを開く
    url = (
        f"https://console.cloud.google.com/logs/query"
        f"?project={project_id}"
        f"&query=logName%3D%22projects%2F{project_id}%2Flogs%2F{log_name}%22"
    )
    print(f"\nGCP Loggingコンソールを開く: {url}")
    # webbrowser.open(url)


def main():
    """メイン関数"""
    print("=== GCP Cloud Loggingでの例外処理サンプル ===")
    
    # ロギングを設定
    logger, project_id, log_name = configure_logging()
    
    # 例外のログ出力方法をデモンストレーション
    demonstrate_exception_logging(logger)
    
    # ログを確実に送信するために少し待機
    import time
    print("\nログを送信中...")
    time.sleep(3)
    
    # GCP Loggingコンソールを開く
    open_gcp_console(project_id, log_name)


if __name__ == "__main__":
    main()
