import logging
from os import path, mkdir

class Logger:
    def __init__(self):
        self.logger = None

    def enable_logger(self, log_name: str, log_file: str=None, level=logging.INFO):
        self.logger = logging.getLogger(f'{log_name} =>')
        self.logger.setLevel(level)
        if not self.logger.handlers:
            log_fmt = logging.Formatter("%(asctime)s %(levelname)s: %(name)s %(message)s", "%Y-%m-%d %H:%M:%S")
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(log_fmt)
            self.logger.addHandler(console_handler)
            if log_file:
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(level)
                file_handler.setFormatter(log_fmt)
                self.logger.addHandler(file_handler)