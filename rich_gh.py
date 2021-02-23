import logging

from sys import exit as clean_exit

from utils import *

from instapy import InstaPy
from instapy import smart_run

from rich import inspect

from rich_logging import RichLogging


parameters = load_parameters()

sleep_delay = 600

# get an InstaPy session!
session = InstaPy(
                username=parameters.username,
                password=parameters.password,
                headless_browser=parameters.headless_browser,
                bypass_security_challenge_using='email',
	            want_check_browser=True,
                show_logs=False)

with RichLogging([logging.getLogger('__main__'), logging.getLogger(parameters.username)]) as rl:
    try:
        # general settings
        session.set_do_like(enabled=False, percentage=0)
        session.set_do_comment(enabled=False, percentage=0)
        session.set_do_follow(enabled=True, percentage=100, times=1)
        session.set_dont_include(parameters.dont_include)
        session.set_skip_users(skip_private=True, skip_no_profile_pic=True, skip_business=True)

        # Login
        # with rl.console.status('Login...', spinner='earth'):
        session.login()

        with rl.console.status('Unfollowing...', spinner='earth'):
            if parameters.do_unfollow :
                rl.console.log('Start unfollow')
                session.unfollow_users(amount=5,
                                        allFollowing=True,
                                        style="FIFO",
                                        unfollow_after=24*60*60,
                                        sleep_delay=sleep_delay)


        # rl.console.log('Login done')
        # with Progress() as progress:
        #     rl.console.log('Start progress')
        #     task1 = progress.add_task("[red]Unfollowing...", total=5)
        #     # Unfollow
        #     rl.console.log('do_unfollow: ', parameters.do_unfollow)
        #     if parameters.do_unfollow :
        #         rl.console.log('Start unfollow')
        #         session.unfollow_users(amount=5,
        #                                 allFollowing=True,
        #                                 style="FIFO",
        #                                 unfollow_after=24*60*60,
        #                                 sleep_delay=sleep_delay)


    except NoSuchElementException:
        # The problem is with a change in IG page layout
        log_file = "{}.html".format(time.strftime("%Y%m%d-%H%M%S"))
        file_path = os.path.join(gettempdir(), log_file)

        with open(file_path, "wb") as fp:
            fp.write(session.browser.page_source.encode("utf-8"))

        print(
            "{0}\nIf raising an issue, "
            "please also upload the file located at:\n{1}\n{0}".format(
                "*" * 70, file_path
            )
        )
    except KeyboardInterrupt:
        clean_exit("You have exited successfully.")
    finally:
        session.end(threaded_session=False)
