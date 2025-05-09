import logkiss 

logger = logkiss.getLogger("test")
logger.setLevel(logkiss.DEBUG)

logger.critical("critical: Hello, World!")
logger.error("error: Hello, World!")
logger.warning("warning: Hello, World!")
logger.info("info: Hello, World!")
logger.debug("debug: Hello, World!")

