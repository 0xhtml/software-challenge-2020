import logging

logger = logging.getLogger("socha")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
logger.addHandler(handler)

debug = logger.debug
info = logger.info
warn = logger.warning
error = logger.error
