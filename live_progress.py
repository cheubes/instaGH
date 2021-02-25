import logging
from sys import exit as clean_exit
from datetime import datetime

from rich.live import Live
from instapy import InstaPy

from const import Const
from parameters import Parameters
from rich_dashboard import RichDashboard
from rich_log_filter import RichLogFilter

C = Const()
parameters = Parameters.load_from_args()
rich_dashboard = RichDashboard(parameters)
rich_filter = RichLogFilter(rich_dashboard, [logging.getLogger(parameters.username)])

with Live(
    rich_dashboard.dashboard_table,
    console=rich_dashboard.console,
    refresh_per_second=10,
):

    # get an InstaPy session
    with rich_dashboard.log_step("Begin session"):
        session = InstaPy(
            username=parameters.username,
            password=parameters.password,
            headless_browser=parameters.headless_browser,
            bypass_security_challenge_using="email",
            want_check_browser=True,
            show_logs=False,
        )
        # general settings
        session.set_do_like(enabled=False, percentage=0)
        session.set_do_comment(enabled=False, percentage=0)
        session.set_do_follow(enabled=True, percentage=100, times=1)
        session.set_dont_include(parameters.dont_include)
        session.set_skip_users(skip_private=True, skip_no_profile_pic=True, skip_business=True)

    try:

        # Login
        with rich_dashboard.log_step("Login"):
            session.login()

        # Unfollow
        if parameters.do_unfollow:
            with rich_dashboard.progress_step(
                C.UNFOLLOW_STEP_KEY, "Unfollow", parameters.unfollow_amount
            ):
                session.unfollow_users(
                    amount=parameters.unfollow_amount,
                    allFollowing=True,
                    style="FIFO",
                    unfollow_after=24 * 60 * 60,
                    sleep_delay=parameters.sleep_delay,
                )
        # Follow likers
        if parameters.do_follow_likers:
            with rich_dashboard.progress_step(
                C.FOLLOW_STEP_KEY,
                "Follow likers",
                parameters.photos_grab_amount
                * parameters.follow_likers_per_photo
                * len(parameters.targets),
            ):
                session.follow_likers(
                    parameters.targets,
                    photos_grab_amount=parameters.photos_grab_amount,
                    follow_likers_per_photo=parameters.follow_likers_per_photo,
                    randomize=True,
                    sleep_delay=parameters.sleep_delay,
                    interact=False,
                )

    except Exception:
        rich_filter.logger.exception("Exception catched")
    except KeyboardInterrupt:
        clean_exit("You have exited successfully.")
    finally:
        with rich_dashboard.log_step("End session"):
            session.end(threaded_session=False)
