#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import logkiss as logging

# Configure logger
logger = logging.getLogger(__name__)

# Suppress matplotlib logs
plt.set_loglevel('warning')

logger.error("Suppressing matplotlib logs")

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
        logger.info(f"Plot saved to: {output_file}")
        
        # Clean up
        plt.close()
        
    except Exception as e:
        logger.error(f"Error occurred while creating plot: {e}")
        raise

def main():
    """Main function"""
    logger.info("Starting matplotlib example")
    
    try:
        create_plot()
        logger.info("Example completed successfully")
    except Exception as e:
        logger.critical(f"Unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
