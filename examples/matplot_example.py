#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example of using logkiss with matplotlib.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import logkiss as logging

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # DEBUGレベル以上のログを表示
logger.propagate = False  # ルートロガーへの伝播を無効化

# ハンドラーがない場合は追加
if not logger.handlers:
    handler = logging.KissConsoleHandler()
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

# Suppress matplotlib logs
plt.set_loglevel('warning')

logger.error("Suppressing matplotlib debug logs")

def generate_sample_data():
    """Generate sample data"""
    logger.info("Generating sample data...")
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    logger.debug(f"Number of data points: {len(x)}")
    return x, y

def create_plot():
    """Create plot"""
    logger.info("Creating plot...")
    
    try:
        # Generate data
        x, y = generate_sample_data()
        
        # Create plot
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, label='sin(x)')
        plt.title('Sample Plot')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        plt.legend()
        
        # Save plot
        output_file = 'sample_plot.png'
        plt.savefig(output_file)
        logger.debug(f"Plot saved to: {output_file}")
        
        # Clean up
        plt.close()
        
    except Exception as e:
        logger.error(f"Error occurred while creating plot: {e}")
        raise

def main():
    """Main function"""
    logger.debug("Starting matplotlib example")
    
    try:
        create_plot()
        logger.debug("Example completed successfully")
    except Exception as e:
        logger.critical(f"Unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
