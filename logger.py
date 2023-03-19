import logging
import os
from datetime import datetime

class BotLogger:
    def __init__(self):
        log_directory = "./logs"
        os.makedirs(log_directory, exist_ok=True)

        current_month = datetime.now().strftime("%Y%m")
        log_filename = f"log{current_month}.txt"
        log_filepath = os.path.join(log_directory, log_filename)

        self.logger = logging.getLogger("BotLogger")
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # File handler
        file_handler = logging.FileHandler(log_filepath)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

logger = BotLogger().get_logger()
