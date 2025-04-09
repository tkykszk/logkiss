![LOGKISS](docs/logkiss-logo-tiny.png)

[![LOGKISS](https://img.shields.io/badge/LOGKISS-Keep%20It%20Simple%20and%20Stupid%20Logger-blue.svg)](https://github.com/takatosh/logkiss)

(README_JAPANEASE.mdのみ日本語です。english versionis in README.md)
LOGKISS（Keep It Simple and Stupid Logger）は、Pythonのシンプルで使いやすいロギングライブラリです。
標準のloggingモジュールをベースに、設定をデフォルトでやってくれるインターフェースを提供します。

## 特徴

- **デフォルトでカラフル**: LOGKISSは、デフォルトで`KissConsoleHandler`を使用し、ログレベルに応じて異なる色で出力します。
- **標準ロギングモジュールの代替**: `import logkiss as logging`とすることで、標準の`logging`モジュールの代わりとして使用できます。
- **柔軟な切り替え**: 必要に応じて、通常の`ConsoleHandler`に切り替えることができます。

## 新機軸

- どのloggerからどれぐらいの量が送られたか集計
- logger単位で抑制するconfigを案内してもらう
- handlerの共有
- console UI

## 環境変数の設定

LOGKISSは、クラウドサービス（GCP、AWS）への接続設定などを環境変数から読み込むことができます。以下の手順で設定してください：

1. リポジトリのルートディレクトリに `.env` ファイルを作成します（`.env.example` をコピーして使用できます）
2. 必要な環境変数を設定します

### Google Cloud Platform (GCP) の設定例

```
# Google Cloud 設定
GCP_PROJECT_ID=your-project-id
GCP_LOG_NAME=test-log
```

### AWS の設定例

```
# AWS 設定
AWS_REGION=us-east-1
AWS_LOG_GROUP_NAME=your-log-group
```

注意: `.env` ファイルは `.env.example` を参考に設定してください。

## インストール

```bash
pip install logkiss
```

## 使用例

```python
# 1. デフォルトでKissConsoleHandlerを使用:
import logkiss

logger1 = logkiss.getLogger("example1")
logger1.info("カラフルな出力")

# 2. loggingモジュールの代替として使用:
import logkiss as logging

logger2 = logging.getLogger("example2")
logger2.warning("これもカラフルな出力")

# 3. 通常のConsoleHandlerに切り替え:
import logging

logger3 = logging.getLogger("example3")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    fmt='%(asctime)s,%(msecs)03d %(levelname)-5s | %(filename)s:%(lineno)3d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
logger3.addHandler(handler)
logger3.error("通常の白黒出力")
```



## 環境変数

LOGKISSは以下の環境変数で設定を変更できます：

- `LOGKISS_DEBUG`: デバッグモードを有効にします。`1`、`true`、`yes`のいずれかを設定すると：
  - ルートロガーのレベルが`INFO`から`DEBUG`に変更されます
  - より詳細なログ情報が表示されます
- `LOGKISS_DISABLE_COLOR`: カラー出力を無効にします。`1`、`true`、`yes`のいずれかを設定します
- `NO_COLOR`: 業界標準の色付け無効化環境変数（値は任意）

使用例：
```bash
# デバッグモードを有効化
export LOGKISS_DEBUG=1

# Pythonスクリプトを実行
python your_script.py
```




### Q. 色の設定はどごて変更する?


### Q. レベル名を国際化したい


### Q. ログが出ない時デバッグしたい

案: ログトレースモード  checklogger(logger, logger.debug)  とかで調べられるようにする

### Q. スタックトレースからソースコードを開きたい



## 設定

詳細な設定方法については、[CONFIG.md](CONFIG.md)を参照してください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。
