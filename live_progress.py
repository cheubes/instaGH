import logging
from time import sleep
from sys import exit as clean_exit

from rich.console import Console
from rich.live import Live
from rich.text import Text

from instapy import InstaPy
from utils import *
from rich_dashboard import RichDashboard
from rich_log_filter import RichLogFilter

unfollow_amount = 2
photos_grab_amount = 1
follow_likers_per_photo = 2
follow_likers_amount = photos_grab_amount * follow_likers_per_photo

parameters = load_parameters()
sleep_delay = 600

rich_dashboard = RichDashboard(Console(), parameters, unfollow_amount)
rich_filter = RichLogFilter(rich_dashboard, [logging.getLogger('__main__'), logging.getLogger(parameters.username)])


with Live(rich_dashboard.dashboard_table, console=rich_dashboard.console, refresh_per_second=10) as live:

    # get an InstaPy session!
    session = InstaPy(
        username=parameters.username,
        password=parameters.password,
        headless_browser=parameters.headless_browser,
        bypass_security_challenge_using='email',
        want_check_browser=True,
        show_logs=False)

    try:
        # general settings
        session.set_do_like(enabled=False, percentage=0)
        session.set_do_comment(enabled=False, percentage=0)
        session.set_do_follow(enabled=True, percentage=100, times=1)
        session.set_dont_include(parameters.dont_include)
        session.set_skip_users(skip_private=True, skip_no_profile_pic=True, skip_business=True)

        # Login
        login_text = Text('Login')
        rich_dashboard.overall_task.add_row(login_text)
        session.login()
        login_text.append(' ✅')

        # Unfollow
        rich_dashboard.overall_task.add_row(rich_dashboard.unfollow_progress)
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
