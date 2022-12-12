from logging import basicConfig, getLogger, Formatter, StreamHandler, INFO
import sys


logger = getLogger(__name__)
handler = StreamHandler(sys.stdout)
basicConfig(level=INFO, handlers=[handler])
handler.setLevel(INFO)
logger.setLevel(INFO)
formatter = Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False


def information_logger(
    description=None,
):
    message = f"{description if description else None} "
    logger.info(message)


def error_logger(
    description=None,
):
    """Exception logger."""
    message = f"{description if description else None} "
    logger.error(message)
