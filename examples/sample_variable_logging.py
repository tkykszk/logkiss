import logkiss as logging

# Basic logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

# %-style formatting (traditional way)
logger.warning("%s before you %s", "Look", "leap")

# str.format() style
logger.info("User {user} performed {action}".format(user="John", action="login"))

# f-string style (Python 3.6+)
user_id = 123
action = "data update"
logger.debug(f"User ID {user_id} is attempting {action}")
