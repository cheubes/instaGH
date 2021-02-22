import logging

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
    with smart_run(session):

        # general settings
        session.set_do_like(enabled=False, percentage=0)
        session.set_do_comment(enabled=False, percentage=0)
        session.set_do_follow(enabled=True, percentage=100, times=1)
        session.set_dont_include(parameters.dont_include)
        session.set_skip_users(skip_private=True, skip_no_profile_pic=True, skip_business=True)
