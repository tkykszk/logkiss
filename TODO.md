# logkiss TODO リスト

## 疑惑

色の設定が変えられない.

### テストケース1
- DEBUGを赤地に黒字にする設定だけを反映させたい

### テストケース2
- formatをデフォルトでなくて すっぴんにしたい









- logger.exception の対応
    logger.exception は どのように処理されるべきか?
    logger.exception は、例外が発生したときにスタックトレースを出力するために使用されます。
    スタックトレースを出力する
    

- logger.error("", exc_info=True)
    クラウドのハンドラーはexc_infoを送った場合、スタックトレースの内容を
    gcp cloud loggingに送るが標準の実装を調べて良いやり方を検討して

# logkiss TODO リスト

## 機能改善

- **exc_info処理の改善** ✅
  - `logger.error("", exc_info=True)` を使用した場合のスタックトレース処理の改善
  - GCP Cloud LoggingとAWS CloudWatchにスタックトレース情報を適切に送信する方法の実装
  - 標準のロギング実装を参考にして最適な方法を検討する
  - 実装完了: 2025-03-02
    - GCPハンドラー: スタックトレース情報をlabelsの`stack_trace`フィールドに追加
    - AWSハンドラー: スタックトレース情報をJSON形式でメッセージに追加

## バグ修正

## ドキュメント

- **exc_info処理のドキュメント追加**
  - `exc_info=True`を使用した場合のスタックトレース情報の処理方法をドキュメントに追加する