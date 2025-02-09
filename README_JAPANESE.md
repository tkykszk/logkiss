# LOGKISS

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

使用例：
```bash
# デバッグモードを有効化
export LOGKISS_DEBUG=1

# Pythonスクリプトを実行
python your_script.py
```

## 設定

詳細な設定方法については、[CONFIG.md](CONFIG.md)を参照してください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。
