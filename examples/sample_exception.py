#!/usr/bin/env python
"""
例外処理のサンプル（標準ロギング）

このサンプルでは、標準のloggingモジュールを使用して例外情報をログに出力する方法を示します。
"""

import logkiss as logging
import traceback
import sys
from datetime import datetime


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

    # # 方法4: スタックトレースを手動で取得して出力
    # try:
    #     print("\n方法4: スタックトレースを手動で取得")
    #     result = simulate_error()
    # except Exception as e:
    #     stack_trace = traceback.format_exc()
    #     logger.error("エラーが発生しました: %s\n%s", str(e), stack_trace)

    # 方法5: 構造化ログとして出力
    try:
        print("\n方法5: 構造化ログとして出力")
        result = simulate_error()
    except Exception as e:
        logger.error("エラーが発生しました", extra={"error_type": type(e).__name__, "error_message": str(e), "stack_trace": traceback.format_exc()})


def main():
    """メイン関数"""
    print("=== 標準ロギングでの例外処理サンプル ===")

    # ロガーの設定
    logger = logging.getLogger("exception_sample")
    logger.setLevel(logging.DEBUG)

    # ファイルハンドラーを追加
    file_handler = logging.FileHandler(f"exception_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    # 例外のログ出力方法をデモンストレーション
    demonstrate_exception_logging(logger)

    print("\n=== ログファイルを確認してください ===")


if __name__ == "__main__":
    main()
