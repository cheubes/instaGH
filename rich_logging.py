import logging
from rich.console import Console

console = Console()

class RichLogging:
    def __init__(self, loggers):
        self.console = console
        filter_ = ListenFilter()
        for logger in loggers:
            logger.setLevel(logging.DEBUG)
            logger.addFilter(filter_)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True

    def __enter__(self):
        return self


class ListenFilter(logging.Filter):
    def filter(self, record):
        console.log('Filtered: ', record.getMessage())
        return False
