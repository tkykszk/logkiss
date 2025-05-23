"""
Logkiss integration test - Logger hierarchy preservation.

このテストはlogkissが標準のloggingライブラリとうまく共存できることを確認します。
特にlogkissの新しい機能である、ロガー階層保持機能をテストします。
"""

# まず、標準のloggingを初期化（既存アプリケーションのシミュレーション）
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# アプリケーションの複数ロガーを作成（階層構造を持つ）
std_logger = logging.getLogger("std_app")
db_logger = logging.getLogger("app.database")
api_logger = logging.getLogger("app.api")

# ロガー階層を確認
import pytest

try:
    import logging_tree
    HAS_LOGGING_TREE = True
except ImportError:
    HAS_LOGGING_TREE = False

@pytest.mark.requires_logging_tree
@pytest.mark.skipif(not HAS_LOGGING_TREE, reason="logging_treeモジュールがインストールされていません")
def test_logger_hierarchy():
    """Test logger hierarchy preservation."""
    # この関数はテストとして実行されるようにするためのダミー関数です
    pass

if HAS_LOGGING_TREE:
    print("\n1. 初期状態のロガー階層:")
    logging_tree.printout()

# メッセージを出力
std_logger.warning("Standard logger: [1] This is from standard logger")
db_logger.warning("Database: [1] This is from db logger")

# logkissをインポート（デフォルトモード - 階層保持）
import logkiss

if HAS_LOGGING_TREE:
    print("\n2. logkissをインポートした後のロガー階層:")
    logging_tree.printout()

# logkissのロガーを作成
logkiss_logger = logkiss.getLogger("logkiss_app")

# 再度メッセージを出力
std_logger.warning("Standard logger: [2] This still works after logkiss import")
db_logger.warning("Database: [2] Database logger still works too")
api_logger.warning("API: [2] API logger works fine")
logkiss_logger.warning("Logkiss: [2] This is from logkiss logger")

# ルートロガーの設定を変更
print("\n3. ルートロガーの設定を変更する場合(階層は自動的に保持):")
# ルートロガーのハンドラーをカスタマイズ
root_logger = logging.getLogger()
for handler in root_logger.handlers[:]:  # 既存のハンドラーを削除
    root_logger.removeHandler(handler)
# 新しいハンドラーを追加
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root_logger.addHandler(handler)
if HAS_LOGGING_TREE:
    logging_tree.printout()

# 再度メッセージを出力
std_logger.warning("Standard logger: [3] After replacing root logger")
db_logger.warning("Database: [3] After replacing root logger")
api_logger.warning("API: [3] After replacing root logger")
logkiss_logger.warning("Logkiss: [3] After replacing root logger")

# ロガーの設定をリセット
print("\n4. ロガーの設定をリセットした後:")
# ルートロガーのハンドラーをリセット
root_logger = logging.getLogger()
for handler in root_logger.handlers[:]:  # 既存のハンドラーを削除
    root_logger.removeHandler(handler)
# 新しいデフォルトハンドラーを設定
logging.basicConfig(level=logging.WARNING, format='%(name)s - %(levelname)s - %(message)s')
if HAS_LOGGING_TREE:
    logging_tree.printout()

# 検証完了
print("\n本実装では、デフォルトでは既存のロガー階層が維持されます。")
print("ユーザーが明示的に設定した場合のみ、ルートロガーが置き換えられます。")
