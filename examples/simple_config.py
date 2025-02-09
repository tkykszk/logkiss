#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logkiss as logging

# Get the root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  

print("Success if 4 lines are output")
# Output logs
logger.debug("Debug message")  
logger.info("Info message")    
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
