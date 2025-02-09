#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import logkiss as logging

# ロガーの設定
logger = logging.getLogger(__name__)

# matplotlibのログを抑制
plt.set_loglevel('warning')

logger.error("matplotlibのログを抑制")

def generate_sample_data():
    """サンプルデータを生成"""
    logger.info("サンプルデータを生成中...")
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    logger.debug(f"データポイント数: {len(x)}")
    return x, y

def create_plot():
    """プロットを作成"""
    logger.info("プロットを作成中...")
    
    try:
        # データ生成
        x, y = generate_sample_data()
        
        # プロット作成
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, label='sin(x)')
        plt.title('Sample Plot')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        plt.legend()
        
        # 保存
        output_file = 'sample_plot.png'
        plt.savefig(output_file)
        logger.info(f"プロットを保存しました: {output_file}")
        
        # クリーンアップ
        plt.close()
        
    except Exception as e:
        logger.error(f"プロット作成中にエラーが発生しました: {e}")
        raise

def main():
    """メイン関数"""
    logger.info("matplotlibサンプルを開始")
    
    try:
        create_plot()
        logger.info("正常に終了しました")
    except Exception as e:
        logger.critical(f"予期せぬエラーが発生しました: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
