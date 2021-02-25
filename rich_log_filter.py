import logging
from rich.logging import RichHandler

from const import Const

C = Const()


class RichLogFilter(logging.Filter):

    rich_dashboard = None
    logger = None

    def __init__(self, rich_dashboard, loggers):
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

    def do_filter(self, msg):
        if msg.startswith('Ongoing Unfollow'):
            completed = int(msg.split('[')[1].split('/')[0]) - 1
            unfollow_progress = self.rich_dashboard.progress_bars[C.UNFOLLOW_STEP_KEY][
                C.PROGRESS_KEY
            ]
            unfollow_job = self.rich_dashboard.progress_bars[C.UNFOLLOW_STEP_KEY][C.JOB_KEY]
            unfollow_progress.update(unfollow_job, completed=completed)
            self.rich_dashboard.report_panel.session_infos[C.UNFOLLOWED_KEY] = completed
        if msg.find('Total people unfollowed') >= 0:
            completed = int(msg.split(':')[1].strip())
            unfollow_progress = self.rich_dashboard.progress_bars[C.UNFOLLOW_STEP_KEY][
                C.PROGRESS_KEY
            ]
            unfollow_job = self.rich_dashboard.progress_bars[C.UNFOLLOW_STEP_KEY][C.JOB_KEY]
            unfollow_progress.update(unfollow_job, completed=completed)
            self.rich_dashboard.report_panel.session_infos[C.UNFOLLOWED_KEY] = completed
        if msg.startswith('Total Follow'):
            follow_progress = self.rich_dashboard.progress_bars[C.FOLLOW_STEP_KEY][C.PROGRESS_KEY]
            follow_job = self.rich_dashboard.progress_bars[C.FOLLOW_STEP_KEY][C.JOB_KEY]
            follow_progress.advance(follow_job)
            self.rich_dashboard.report_panel.session_infos[C.FOLLOWED_KEY] += 1
        if msg.find('Not a valid user') >= 0:
            follow_progress = self.rich_dashboard.progress_bars[C.FOLLOW_STEP_KEY][C.PROGRESS_KEY]
            follow_job = self.rich_dashboard.progress_bars[C.FOLLOW_STEP_KEY][C.JOB_KEY]
            follow_progress.advance(follow_job)
            self.rich_dashboard.report_panel.session_infos[C.NOT_VALID_USER_KEY] += 1
        if msg.find('has already been followed') >= 0:
            follow_progress = self.rich_dashboard.progress_bars[C.FOLLOW_STEP_KEY][C.PROGRESS_KEY]
            follow_job = self.rich_dashboard.progress_bars[C.FOLLOW_STEP_KEY][C.JOB_KEY]
            follow_progress.advance(follow_job)
            self.rich_dashboard.report_panel.session_infos[C.ALREADY_FOLLOWED_KEY] += 1

    def filter(self, record):
        self.logger.handle(record)
        self.do_filter(record.getMessage())
        return False
