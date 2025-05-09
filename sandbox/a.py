from logkiss.logkiss import setup
import logging

# 設定ファイルを指定してセットアップ
logger = setup('test.yaml')
logger.setLevel(logging.DEBUG)

# ログ出力
logger.warning("これは黄色地に黒字で表示されます")

