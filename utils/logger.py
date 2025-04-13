import logging

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'INFO': '\033[97m',  # White
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',  # Red
        'DEBUG': '\033[94m',  # Blue
        'RESET': '\033[0m',  # Reset to default
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        return f"{color}{super().format(record)}{reset}"


def get_logger(logger_name: str) -> logging:
    logger = logging.getLogger(logger_name)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()

        formatter = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
    return logger