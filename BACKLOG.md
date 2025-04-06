# スタックトレース付きログを簡単に出したい

```
try:
    # 何かのコード
    result = 1 / 0
except Exception as e:
    import traceback
    stack_trace = traceback.format_exc()
    logger.error("エラーが発生しました", extra={
        "json_fields": {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "stack_trace": stack_trace
        }
    })
```

```
import traceback

# 現在のスタックトレースを取得（例外なしでも）
stack_trace = ''.join(traceback.format_stack())

# ログにスタックトレースを追加
logger.info("処理を実行しました", extra={
    "json_fields": {
        "stack_trace": stack_trace
    }
}) 
```

もしすべてのログに自動的にスタックトレースを追加したい場合、カスタムフィルターやフォーマッター? ででてきる