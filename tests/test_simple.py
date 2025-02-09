#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import sys
import logkiss as logging

def capture_output():
    """出力をキャプチャする"""
    output = io.StringIO()
    sys.stderr = output
    # ロガーのハンドラーを更新
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        if isinstance(handler, logging.KissConsoleHandler):
            handler.stream = output
    return output

def restore_output(output):
    """出力を元に戻す"""
    sys.stderr = sys.__stderr__
    return output.getvalue()

def reset_logger():
    """ロガーをリセットする"""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # デフォルトレベルをDEBUGに設定
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    handler = logging.KissConsoleHandler()
    handler.setLevel(logging.DEBUG)  # ハンドラーのレベルもDEBUGに設定
    logger.addHandler(handler)

def test_simplest():
    """simplest.pyのテスト"""
    reset_logger()  # ロガーをリセット
    output = capture_output()

    # ログを出力
    logging.debug("デバッグメッセージ")
    logging.info("情報メッセージ")
    logging.warning("警告メッセージ")
    logging.error("エラーメッセージ")
    logging.critical("重大なエラーメッセージ")

    result = restore_output(output)
    lines = [line for line in result.split('\n') if line]

    # 5行出力されることを確認（全レベル）
    assert len(lines) == 5, f"Expected 5 lines, got {len(lines)}"
    assert "DEBUG" in lines[0]
    assert "INFO" in lines[1]
    assert "WARNING" in lines[2]
    assert "ERROR" in lines[3]
    assert "CRITICAL" in lines[4]

def test_simple():
    """simple.pyのテスト"""
    reset_logger()  # ロガーをリセット
    output = capture_output()

    # ロガーを取得
    logger = logging.getLogger()

    # ログを出力
    logger.debug("デバッグメッセージ")
    logger.info("情報メッセージ")
    logger.warning("警告メッセージ")
    logger.error("エラーメッセージ")
    logger.critical("重大なエラーメッセージ")

    result = restore_output(output)
    lines = [line for line in result.split('\n') if line]

    # 5行出力されることを確認（全レベル）
    assert len(lines) == 5, f"Expected 5 lines, got {len(lines)}"
    assert "DEBUG" in lines[0]
    assert "INFO" in lines[1]
    assert "WARNING" in lines[2]
    assert "ERROR" in lines[3]
    assert "CRITICAL" in lines[4]

def test_simple_config():
    """simple_config.pyのテスト"""
    reset_logger()  # ロガーをリセット
    output = capture_output()

    # ロガーとハンドラーをDEBUGレベルに設定
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    for handler in logger.handlers:
        handler.setLevel(logging.DEBUG)

    # ログを出力
    logger.debug("デバッグメッセージ")
    logger.info("情報メッセージ")
    logger.warning("警告メッセージ")
    logger.error("エラーメッセージ")
    logger.critical("重大なエラーメッセージ")

    result = restore_output(output)
    lines = [line for line in result.split('\n') if line]

    # 5行出力されることを確認（全レベル）
    assert len(lines) == 5, f"Expected 5 lines, got {len(lines)}"
    assert "DEBUG" in lines[0]
    assert "INFO" in lines[1]
    assert "WARNING" in lines[2]
    assert "ERROR" in lines[3]
    assert "CRITICAL" in lines[4]

def test_simple_config_2():
    """simple_config_2.pyのテスト"""
    reset_logger()  # ロガーをリセット
    output = capture_output()

    # ロガーを取得してERRORレベルに設定
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)

    # ログを出力
    logger.debug("デバッグメッセージ")
    logger.info("情報メッセージ")
    logger.warning("警告メッセージ")
    logger.error("エラーメッセージ")
    logger.critical("重大なエラーメッセージ")

    result = restore_output(output)
    lines = [line for line in result.split('\n') if line]

    # 2行出力されることを確認（ERROR以上）
    assert len(lines) == 2, f"Expected 2 lines, got {len(lines)}"
    assert "ERROR" in lines[0]
    assert "CRITICAL" in lines[1]
