"""logkissモジュールのAPI機能テスト

このテストファイルでは、logkissモジュールが正しくAPIを公開しているかを確認します。
特に、標準のloggingモジュールと互換性のあるAPIが存在するかをテストします。
"""

import pytest
import logging
import inspect
import logkiss


def test_standard_logging_compatibility():
    """標準のloggingモジュールと互換性のあるAPIが存在するかをテストします"""
    # 必須の関数とクラス
    essential_apis = [
        "basicConfig",
        "getLogger",
        "debug",
        "info",
        "warning",
        "error",
        "critical",
        "exception",
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
        "Logger",
        "Handler",
        "Formatter",
        "Filter",
        "FileHandler",
        "StreamHandler",
    ]
    
    for api in essential_apis:
        assert hasattr(logkiss, api), f"logkissモジュールに{api}が存在しません"
        assert hasattr(logging, api), f"標準loggingモジュールに{api}が存在しません"


def test_logkiss_specific_apis():
    """logkiss固有のAPIが存在するかをテストします"""
    logkiss_specific_apis = [
        "KissLogger",
        "KissConsoleHandler",
        "ColoredFormatter",
        "setup_from_yaml",
        "setup_from_env",
        "setup",
    ]
    
    for api in logkiss_specific_apis:
        assert hasattr(logkiss, api), f"logkissモジュールに{api}が存在しません"


def test_basicconfig_functionality():
    """basicConfig関数が正しく動作するかをテストします"""
    # テスト前にrootロガーをリセット
    root = logging.getLogger()
    for handler in root.handlers[:]:
        root.removeHandler(handler)
    
    # logkiss.basicConfigを使用
    logkiss.basicConfig(level=logkiss.DEBUG, format="%(levelname)s - %(message)s")
    
    # ロガーを取得してログを出力
    logger = logkiss.getLogger("test_basic_config")
    
    # ハンドラーが追加されていることを確認
    assert len(root.handlers) > 0, "basicConfigがハンドラーを追加していません"
    
    # レベルが設定されていることを確認
    assert root.level == logkiss.DEBUG, "basicConfigがレベルを正しく設定していません"
    
    # フォーマットが設定されていることを確認
    handler = root.handlers[0]
    assert handler.formatter is not None, "basicConfigがフォーマッターを設定していません"


def test_method_signatures_compatibility():
    """主要なメソッドのシグネチャが標準loggingと互換性があるかをテストします"""
    methods_to_check = [
        "basicConfig",
        "getLogger",
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ]
    
    for method_name in methods_to_check:
        logkiss_method = getattr(logkiss, method_name)
        logging_method = getattr(logging, method_name)
        
        logkiss_sig = inspect.signature(logkiss_method)
        logging_sig = inspect.signature(logging_method)
        
        # パラメータ名のリストを比較
        logkiss_params = list(logkiss_sig.parameters.keys())
        logging_params = list(logging_sig.parameters.keys())
        
        # 必須パラメータが一致することを確認
        for param in logging_params:
            if logging_sig.parameters[param].default == inspect.Parameter.empty:
                assert param in logkiss_params, f"{method_name}の必須パラメータ{param}が一致しません"


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
