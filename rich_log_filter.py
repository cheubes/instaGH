"""
Log filter for insta_gh InstaPy template.
"""

import logging
from rich.logging import RichHandler

from const import Const

C = Const()


class RichLogFilter(logging.Filter):
    """
    This log filter:
        - Reemit logs on rich handler in a live console
        - Update steps progress bars based on log content
    """

    rich_dashboard = None
    logger = None

    def __init__(self, rich_dashboard, loggers):  # pylint: disable=W0231
        self.rich_dashboard = rich_dashboard
        logging.basicConfig(
            level='INFO',
            format='%(message)s',
            datefmt='[%X]',
            handlers=[RichHandler(rich_tracebacks=True, console=rich_dashboard.console)],
        )
        self.logger = logging.getLogger('rich')
        for logger in loggers:
            logger.setLevel(logging.DEBUG)
            logger.addFilter(self)

    def update_unfollow_job(self, completed):
        """Update the unfollow job progress bar completion."""
        unfollow_progress = self.rich_dashboard.progress_bars[C.UNFOLLOW_STEP_KEY][C.PROGRESS_KEY]
        unfollow_job = self.rich_dashboard.progress_bars[C.UNFOLLOW_STEP_KEY][C.JOB_KEY]
        unfollow_progress.update(unfollow_job, completed=completed)
        self.rich_dashboard.report_panel.session_infos[C.UNFOLLOWED_KEY] = completed

    def update_follow_job(self, info_key):
        """Update the follow job progress bar completion."""
        follow_progress = self.rich_dashboard.progress_bars[C.FOLLOW_STEP_KEY][C.PROGRESS_KEY]
        follow_job = self.rich_dashboard.progress_bars[C.FOLLOW_STEP_KEY][C.JOB_KEY]
        follow_progress.advance(follow_job)
        self.rich_dashboard.report_panel.session_infos[info_key] += 1

    def do_filter(self, msg):
        """Update steps progress bars based on log content."""
        if msg.startswith('Ongoing Unfollow'):
            completed = int(msg.split('[')[1].split('/')[0]) - 1
            self.update_unfollow_job(completed)
        if msg.find('Total people unfollowed') >= 0:
            completed = int(msg.split(':')[1].strip())
            self.update_unfollow_job(completed)
        if msg.startswith('Total Follow'):
            self.update_follow_job(C.FOLLOWED_KEY)
        if msg.find('Not a valid user') >= 0:
            self.update_follow_job(C.NOT_VALID_USER_KEY)
        if msg.find('has already been followed') >= 0:
            self.update_follow_job(C.ALREADY_FOLLOWED_KEY)

    def filter(self, record):
        self.logger.handle(record)
        self.do_filter(record.getMessage())
        return False
