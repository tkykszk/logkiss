# LOGKISS Configuration Guide

LOGKISSは、YAMLファイルを使用してログの色とスタイルをカスタマイズできます。この設定ファイルでは、ログレベル、メッセージ、およびその他の要素の色やスタイルを詳細に制御できます。

## 設定ファイルの構造

設定ファイルは以下の3つの主要なセクションで構成されています：

1. `levels`: ログレベル名の色設定
2. `messages`: ログメッセージの色設定
3. `elements`: タイムスタンプやファイル名などの要素の色設定

### 基本構造

```yaml
levels:
  debug:
    color: cyan
    style: bold
  info:
    color: white
    style: bold
  warning:
    color: yellow
    style: bold
  error:
    color: black
    background: red
    style: bold
  critical:
    color: black
    background: bright_red
    style: bold

messages:
  debug:
    color: cyan
  info:
    color: white
  warning:
    color: yellow
  error:
    color: black
    background: red
  critical:
    color: black
    background: bright_red

elements:
  timestamp:
    color: blue
    style: dim
  filename:
    color: green
    style: bold
```

## 設定オプション

### 利用可能な色

#### 前景色（文字色）
- black
- red
- green
- yellow
- blue
- magenta
- cyan
- white
- bright_black
- bright_red
- bright_green
- bright_yellow
- bright_blue
- bright_magenta
- bright_cyan
- bright_white

#### 背景色
- black
- red
- green
- yellow
- blue
- magenta
- cyan
- white
- bright_black
- bright_red
- bright_green
- bright_yellow
- bright_blue
- bright_magenta
- bright_cyan
- bright_white

### スタイル
- bold: 太字
- dim: 暗い
- italic: イタリック
- underline: 下線
- blink: 点滅
- reverse: 反転
- hidden: 非表示
- strike: 取り消し線

## 設定の使用方法

1. 設定ファイルの作成:
```python
# logkiss.yaml
levels:
  debug:
    color: cyan
    style: bold
  error:
    color: red
    style: bold
    background: black
```

2. ロガーの初期化時に設定ファイルを指定:
```python
import logkiss
from pathlib import Path

config_path = Path('logkiss.yaml')
logger = logkiss.getLogger(__name__, color_config=config_path)
```

## デフォルト設定

設定ファイルを指定しない場合、以下のデフォルト設定が使用されます：

```yaml
levels:
  debug:
    color: cyan
    style: bold
  info:
    color: white
    style: bold
  warning:
    color: yellow
    style: bold
  error:
    color: black
    background: red
    style: bold
  critical:
    color: black
    background: bright_red
    style: bold
```

## 環境変数

ログの色付けは以下の環境変数で制御できます：

- `LOGKISS_FORCE_COLOR`: 色付けを強制的に有効にする（値: 1, true, yes）
- `LOGKISS_NO_COLOR`: 色付けを無効にする（値: 任意）
- `LOGKISS_LEVEL_FORMAT`: ログレベル名の表示長を指定する（値: 数値、デフォルト: 5）
  - 例: `LOGKISS_LEVEL_FORMAT=5` とすると、全てのログレベル名が5文字に調整されます
  - WARNINGは特別に「WARN」に短縮されます
  - 指定した長さより長いレベル名は切り詰められ、短いレベル名は空白で埋められます

## 注意事項

1. 設定ファイルの読み込みに失敗した場合は、デフォルト設定が使用されます
2. 未定義の色やスタイルは無視されます
3. 各セクション（levels, messages, elements）は独立して設定可能です
4. 特定のログレベルや要素の設定を省略した場合、その部分はデフォルト設定が使用されます
