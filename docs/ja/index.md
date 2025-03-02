# logkiss

![logkiss logo](https://via.placeholder.com/200x100?text=logkiss)

**logkiss**は、シンプルで美しいPythonロギングライブラリです。

## 特徴

- **カラフルなログ出力** - ログレベルに応じた色分けで視認性向上
- **シンプルなAPI** - 標準のPythonロギングと互換性のある使いやすいAPI
- **クラウド対応** - AWS CloudWatchとGoogle Cloud Loggingをサポート
- **カスタマイズ可能** - 色やフォーマットを簡単にカスタマイズ

## クイックスタート

```python
import logkiss as logging

# ロガーの取得
logger = logging.getLogger(__name__)

# ログの出力
logger.debug("デバッグメッセージ")
logger.info("情報メッセージ")
logger.warning("警告メッセージ")
logger.error("エラーメッセージ")
logger.critical("致命的エラーメッセージ")
```

## インストール

```bash
pip install logkiss
```

クラウドロギング機能を使用する場合：

```bash
pip install "logkiss[cloud]"
```

## ライセンス

MITライセンスの下で配布されています。詳細は[LICENSE](https://github.com/yourusername/logkiss/blob/main/LICENSE)ファイルを参照してください。
