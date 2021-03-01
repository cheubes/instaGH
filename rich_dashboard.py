"""
Rich dashboard for insta_gh InstaPy template.
"""

from contextlib import contextmanager
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table
from rich.text import Text

from const import Const


C = Const()


class ReportPanel:  # pylint: disable=R0903
    """Panel to display global report information in a Live context."""

    start_time = datetime.now()
    session_infos = {
        C.UNFOLLOWED_KEY: 0,
        C.ALREADY_UNFOLLOWED_KEY: 0,
        C.WHITE_LIST_USER_KEY: 0,
        C.UNFOLLOWED_ON_KEY: 0,
        C.FOLLOWED_KEY: 0,
        C.FOLLOWED_ON_KEY: 0,
        C.ALREADY_FOLLOWED_KEY: 0,
        C.NOT_VALID_USER_KEY: 0,
    }

    def __rich__(self) -> Panel:
        report_table = Table.grid()
        report_table.add_row(f'Started on [cyan]{self.start_time.ctime()}[/cyan]')

        elapsed_time = datetime.now() - self.start_time
        minutes = divmod(elapsed_time.seconds, 60)
        hours = divmod(minutes[0], 60)

        report_table.add_row(
            f'Time elapsed: [cyan]{hours[0]:02d}:{hours[1]:02d}:{minutes[1]:02d}[/cyan]'
        )
        report_table.add_row('')
        report_table.add_row(
            f'Unfollowed [bold cyan]{str(self.session_infos[C.UNFOLLOWED_KEY])}[/bold cyan]'
            + f' / [cyan]{str(self.session_infos[C.UNFOLLOWED_ON_KEY])}[/cyan] user(s)'
        )
        report_table.add_row(
            f'  - Already unfollowed: [bold cyan]{str(self.session_infos[C.ALREADY_UNFOLLOWED_KEY])}'
            + '[/bold cyan]'
        )
        report_table.add_row(
            f'  - White list user(s): [bold cyan]{str(self.session_infos[C.WHITE_LIST_USER_KEY])}'
            + '[/bold cyan]'
        )
        report_table.add_row('')
        report_table.add_row(
            f'Followed [bold cyan]{str(self.session_infos[C.FOLLOWED_KEY])}[/bold cyan]'
            + f' / [cyan]{str(self.session_infos[C.FOLLOWED_ON_KEY])}[/cyan] user(s)'
        )
        report_table.add_row(
            f'  - Already Followed: [bold cyan]{str(self.session_infos[C.ALREADY_FOLLOWED_KEY])}'
            + '[/bold cyan]'
        )
        report_table.add_row(
            f'  - Not valid user(s): [bold cyan]{str(self.session_infos[C.NOT_VALID_USER_KEY])}'
            + '[/bold cyan]'
        )
        return Panel(report_table, title='Report', border_style='blue', padding=(1, 1))


class RichDashboard:
    """Live rich dashboard for insta_gh InstaPy template logging."""

    console = None
    dashboard_table = None
    progress_table = None
    progress_bars = {}
    report_panel = ReportPanel()

    def __init__(self, parameters):
        self.report_panel.session_infos[C.UNFOLLOWED_ON_KEY] = parameters.unfollow_amount
        self.report_panel.session_infos[C.FOLLOWED_ON_KEY] = (
            parameters.photos_grab_amount
            * parameters.follow_likers_per_photo
            * len(parameters.targets)
        )

        self.console = Console()
        self.progress_table = Table.grid()
        self.dashboard_table = Table.grid(expand=True)
        self.dashboard_table.add_row(
            Panel(str(parameters), title='Parameters', border_style='blue', padding=(1, 1)),
            Panel(self.progress_table, title='Progress', border_style='blue', padding=(1, 1)),
            self.report_panel,
        )

    @contextmanager
    def log_step(self, step_name):
        """Context manager to log a step begin and completion."""
        step_text = Text(f'{step_name} ... ')
        self.progress_table.add_row(step_text)
        yield
        step_text.append(' ✅')

    @contextmanager
    def progress_step(self, step_key, step_name, total):
        """Context manager to show a progress bar during a step execution."""
        step_progress = Progress(
            '{task.description}',
            SpinnerColumn(spinner_name='earth'),
            BarColumn(),
            TextColumn('[progress.percentage]{task.percentage:>3.0f}%'),
        )
        step_job = step_progress.add_task(step_name, total=total)
        self.progress_bars[step_key] = {
            C.PROGRESS_KEY: step_progress,
            C.JOB_KEY: step_job,
        }
        self.progress_table.add_row(step_progress)
        yield
        step_progress.update(step_job, completed=step_progress.tasks[0].total)
