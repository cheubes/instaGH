from contextlib import contextmanager

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table
from rich.text import Text

from const import Const

class RichDashboard:

    C = Const()
    console = None
    dashboard_table = None
    progress_table = None
    progress_bars = {}

    def __init__(self, parameters):
        self.console = Console()
        self.progress_table = Table.grid()
        self.dashboard_table = Table.grid()
        self.dashboard_table.add_row(
            Panel.fit(str(parameters), title='Parameters', border_style='blue', padding=(1, 1)),
            Panel.fit(self.progress_table, title='Progress', border_style='blue', padding=(1, 1))
        )

    @contextmanager
    def log_step(self, step_name):
        step_text = Text(step_name + ' ... ')
        self.progress_table.add_row(step_text)
        yield
        step_text.append(' ✅')

    @contextmanager
    def progress_step(self, step_key, step_name, total):
        step_progress = Progress('{task.description}', SpinnerColumn(), BarColumn(), TextColumn('[progress.percentage]{task.percentage:>3.0f}%'))
        step_job = step_progress.add_task(step_name, total=total)
        self.progress_bars[step_key] = {self.C.PROGRESS_KEY:step_progress, self.C.JOB_KEY:step_job}
        self.progress_table.add_row(step_progress)
        yield
