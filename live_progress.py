import logging
from time import sleep
from sys import exit as clean_exit

from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table
from rich.text import Text

from instapy import InstaPy
from utils import *
from rich_logging import RichLogging

unfollow_amount = 2
photos_grab_amount = 1
follow_likers_per_photo = 100
follow_likers_amount = photos_grab_amount * follow_likers_per_photo

parameters = load_parameters()

sleep_delay = 600


unfollow_progress = Progress(
    "{task.description}",
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
)
unfollow_job = unfollow_progress.add_task("Unfollow", total=unfollow_amount)
# follow_likers_job = job_progress.add_task("Follow likers", total=follow_likers_amount)

overall_task = Table.grid()

dashboard_table = Table.grid()
dashboard_table.add_row(
    Panel.fit(str(parameters), title="Parameters", border_style="green", padding=(1, 1)),
    Panel.fit(overall_task, title="Overall Progress", border_style="green", padding=(1, 1)),
    # Panel.fit(job_progress, title="[b]Jobs", border_style="red", padding=(1, 1)),
)

# get an InstaPy session!
session = InstaPy(
                username=parameters.username,
                password=parameters.password,
                headless_browser=parameters.headless_browser,
                bypass_security_challenge_using='email',
	            want_check_browser=True,
                show_logs=False)



with Live(dashboard_table, refresh_per_second=10) as live:

    class LogFilter(logging.Filter):
        console = None
        def __init__(self, console):
            self.console = console
        def do_filter(self, msg):
            if msg.startswith('Ongoing Unfollow'):
                completed = int(msg.split('[')[1].split('/')[0])
                unfollow_progress.update(unfollow_job, completed=completed)
        def filter(self, record):
            self.console.log('Filtered: ', record.getMessage())
            self.do_filter(record.getMessage())
            return False
    filter_ = LogFilter(live.console)

    mainLogger = logging.getLogger('__main__')
    mainLogger.setLevel(logging.DEBUG)
    mainLogger.addFilter(filter_)

    instaPyLogger = logging.getLogger(parameters.username)
    instaPyLogger.setLevel(logging.DEBUG)
    instaPyLogger.addFilter(filter_)

    try:
        # general settings
        session.set_do_like(enabled=False, percentage=0)
        session.set_do_comment(enabled=False, percentage=0)
        session.set_do_follow(enabled=True, percentage=100, times=1)
        session.set_dont_include(parameters.dont_include)
        session.set_skip_users(skip_private=True, skip_no_profile_pic=True, skip_business=True)

        # Login
        login_text = Text('Login')
        overall_task.add_row(login_text)
        session.login()
        login_text.append(' ✅')

        # Unfollow
        overall_task.add_row(unfollow_progress)
        if parameters.do_unfollow :
            session.unfollow_users(amount=unfollow_amount,
                                allFollowing=True,
                                style="FIFO",
                                unfollow_after=24*60*60,
                                sleep_delay=sleep_delay)


    except Exception as e:
        mainLogger.exception('', e)
    except KeyboardInterrupt:
        clean_exit("You have exited successfully.")
    finally:
        session.end(threaded_session=False)
