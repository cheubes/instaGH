from utils import *

from instapy import InstaPy
from instapy import smart_run


parameters = load_parameters()

# get an InstaPy session!
session = InstaPy(
                username=parameters.username,
                password=parameters.password,
                headless_browser=parameters.headless_browser)


with smart_run(session):

    # general settings
    session.set_do_like(enabled=False, percentage=0)
    session.set_do_comment(enabled=False, percentage=0)
    session.set_do_follow(enabled=True, percentage=100, times=1)
    session.set_dont_include(parameters.dont_include)

    # Follow likers
    if parameters.do_follow_likers :
        session.follow_likers(
                            parameters.targets,
                            photos_grab_amount=3,
                            follow_likers_per_photo=100,
                            randomize=True,
                            sleep_delay=600,
                            interact=False)

    # Follow followers
    if parameters.do_follow_followers :
        session.follow_user_followers(
                            parameters.targets,
                            amount=200,
                            randomize=True,
                            sleep_delay=600,
                            interact=False)

    # Follow following
    if parameters.do_follow_following :
        session.follow_user_following(
                            parameters.targets,
                            amount=200,
                            randomize=True,
                            sleep_delay=600,
                            interact=False)

    # Unfollow
    if parameters.do_unfollow :
        session.unfollow_users(amount=200,
                            allFollowing=True,
                            style="FIFO",
                            unfollow_after=24*60*60,
                            sleep_delay=600)
