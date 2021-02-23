import logging
from rich import inspect

class RichLogFilter(logging.Filter):

    rich_dashboard = None

    def __init__(self, rich_dashboard, loggers):
        self.rich_dashboard = rich_dashboard
        for logger in loggers:
            logger.setLevel(logging.DEBUG)
            logger.addFilter(self)

    def do_filter(self, msg):
        if msg.startswith('Ongoing Unfollow'):
            completed = int(msg.split('[')[1].split('/')[0])
            self.rich_dashboard.unfollow_progress.update(self.rich_dashboard.unfollow_job, completed=completed)

    def filter(self, record):
        self.rich_dashboard.console.log(record.levelname + '\t' + record.getMessage())
        self.rich_dashboard.console.log(record.filename + ':' + str(record.lineno) + ' (' + record.funcName + ')', style='italic #585858')
        self.do_filter(record.getMessage())
        return False
