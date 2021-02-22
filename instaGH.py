import logging

from utils import *

from instapy import InstaPy
from instapy import smart_run

from rich.logging import RichHandler

parameters = load_parameters()

sleep_delay = 600

# get an InstaPy session!
session = InstaPy(
                username=parameters.username,
                password=parameters.password,
                headless_browser=parameters.headless_browser,
                bypass_security_challenge_using='email',
	            want_check_browser=True,
                log_handler=RichHandler(rich_tracebacks=True),
                show_logs=False)


with smart_run(session):

    # general settings
    session.set_do_like(enabled=False, percentage=0)
    session.set_do_comment(enabled=False, percentage=0)
    session.set_do_follow(enabled=True, percentage=100, times=1)
    session.set_dont_include(parameters.dont_include)
    session.set_skip_users(skip_private=True, skip_no_profile_pic=True, skip_business=True)

    # Unfollow
    if parameters.do_unfollow :
        session.unfollow_users(amount=200,
                            allFollowing=True,
                            style="FIFO",
                            unfollow_after=24*60*60,
                            sleep_delay=sleep_delay)
    # Follow likers
    if parameters.do_follow_likers :
        session.follow_likers(
                            parameters.targets,
                            photos_grab_amount=3,
                            follow_likers_per_photo=100,
                            randomize=True,
                            sleep_delay=sleep_delay,
                            interact=False)



    # # Follow followers
    # if parameters.do_follow_followers :
    #     session.follow_user_followers(
    #                         parameters.targets,
    #                         amount=200,
    #                         randomize=True,
    #                         sleep_delay=sleep_delay,
    #                         interact=False)
    #
    # # Follow following
    # if parameters.do_follow_following :
    #     session.follow_user_following(
    #                         parameters.targets,
    #                         amount=200,
    #                         randomize=True,
    #                         sleep_delay=sleep_delay,
    #                         interact=False)
