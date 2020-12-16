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

    ## Follow likers
    session.set_do_follow(enabled=True, percentage=100, times=1)
    session.follow_likers(
                        parameters.targets,
                        photos_grab_amount=3,
                        follow_likers_per_photo=100,
                        randomize=True,
                        sleep_delay=600,
                        interact=False)
