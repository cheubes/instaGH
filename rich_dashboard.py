from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table

class RichDashboard:
    console = None
    dashboard_table = None
    unfollow_progress = None
    unfollow_job = None
    overall_task_table = None

    def __init__(self, console, parameters):
        self.console = console

        self.unfollow_progress = Progress(
            "{task.description}",
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        self.unfollow_job = self.unfollow_progress.add_task("Unfollow", total=parameters.unfollow_amount)
        # follow_likers_job = job_progress.add_task("Follow likers", total=follow_likers_amount)

        self.overall_task = Table.grid()

        self.dashboard_table = Table.grid()
        self.dashboard_table.add_row(
            Panel.fit(str(parameters), title="Parameters", border_style="green", padding=(1, 1)),
            Panel.fit(self.overall_task, title="Overall Progress", border_style="green", padding=(1, 1)),
            # Panel.fit(job_progress, title="[b]Jobs", border_style="red", padding=(1, 1)),
        )
