import sys
import logging


class Logger(logging.Logger):
    COLORS = {
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "RESET": "\033[0m",  # Reset
    }

    def __init__(self, name="Logger"):
        super().__init__(name)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(self.Formatter())
        self.addHandler(handler)
        self.setLevel(logging.DEBUG)

    class Formatter(logging.Formatter):
        def format(self, record):
            color = Logger.COLORS.get(record.levelname, Logger.COLORS["RESET"])
            reset = Logger.COLORS["RESET"]
            log_format = f"{color}[%(levelname)s] %(asctime)s - %(message)s{reset}"
            formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
            return formatter.format(record)

