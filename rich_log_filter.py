import logging
from rich.logging import RichHandler

from const import Const

class RichLogFilter(logging.Filter):

    C = Const()
    rich_dashboard = None
    logger = None

    def __init__(self, rich_dashboard, loggers):
        self.rich_dashboard = rich_dashboard
        logging.basicConfig(level='INFO', format='%(message)s', datefmt='[%X]',handlers=[RichHandler(rich_tracebacks=True, console=rich_dashboard.console)])
        self.logger = logging.getLogger('rich')
        for logger in loggers:
            logger.setLevel(logging.DEBUG)
            logger.addFilter(self)

    def do_filter(self, msg):
        if msg.startswith('Ongoing Unfollow'):
            completed = int(msg.split('[')[1].split('/')[0])
            unfollow_progress = self.rich_dashboard.progress_bars[self.C.UNFOLLOW_STEP_KEY][self.C.PROGRESS_KEY]
            unfollow_job = self.rich_dashboard.progress_bars[self.C.UNFOLLOW_STEP_KEY][self.C.JOB_KEY]
            unfollow_progress.update(unfollow_job, completed=completed)

    def filter(self, record):
        self.logger.handle(record)
        self.do_filter(record.getMessage())
        return False
