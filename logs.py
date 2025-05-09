import logging
import logging.handlers
import os
import sys

LOG_FILENAME = "admin.log"
MAX_LOG_SIZE = 10 * 1024 * 1024

def get_log_path():
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, LOG_FILENAME)

def setup_logger():
    log_path = get_log_path()
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    handler = logging.handlers.RotatingFileHandler(
        log_path, maxBytes=MAX_LOG_SIZE, backupCount=1, encoding="utf-8"
    )
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    handler.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(handler)
    sys.stdout = StreamToLogger(logger, logging.WARNING)
    sys.stderr = StreamToLogger(logger, logging.ERROR)

class StreamToLogger:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self.linebuf = ""

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass