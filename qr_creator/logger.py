import logging as _logging
import platform as _platform

logger = None

def _log_environment():
    logger.debug(f"System: {_platform.system()}")
    logger.debug(f"Python: v{_platform.python_version()}")


def get_logger(ns):
    global logger
    logger = _logging.getLogger("qr-creator")
    logger.setLevel("DEBUG")
    file_handler = _logging.FileHandler("qr-creator.log", mode="w")
    file_handler.setLevel("DEBUG")
    file_handler.setFormatter(_logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(file_handler)
    err_handler = _logging.StreamHandler()
    err_handler.setFormatter(_logging.Formatter("qr-creator:%(levelname)s: %(message)s "))
    try:
        err_handler.setLevel(ns.log_level)
    except ValueError:
        err_handler.setLevel("WARNING")
        logger.warning(f"'{ns.log_level} is not valid, Back to WARNING'")
    logger.addHandler(err_handler)
    logger.info("Instance started")
    _log_environment()
    return logger