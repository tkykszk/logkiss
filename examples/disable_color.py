import logkiss as logging

# Get logkiss logger
logger = logging.getLogger(__name__)

# Disable color output
for handler in logger.handlers:
    if isinstance(handler, logging.KissConsoleHandler):
        handler.use_color = False  # Disable color output

# Test log output
logger.warning('This warning message will be displayed without color')
logger.info('This information message will also be without color')
logger.error('This error message will be displayed without color')
