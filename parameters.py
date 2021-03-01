"""
insta_gh parameters utility
"""
import argparse
import os
import random
from typing import NamedTuple
import yaml


def load_from_args():
    """Load parameters from the yaml file passed in args."""
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', help='Yaml file to get parameters from.')
    args = parser.parse_args()
    # Loading data
    current_path = os.path.abspath(os.path.dirname(__file__))
    data = yaml.safe_load(open('%s/%s' % (current_path, args.data_file)))
    parameters = Parameters(
        data['username'],
        data['password'],
        random.sample(data['target_list'], data['target_size']),
        data['do_follow_likers'],
        data['do_follow_followers'],
        data['do_follow_following'],
        data['do_unfollow'],
        data['dont_include_list'],
        data['unfollow_after'],
        data['headless_browser'],
        data['unfollow_amount'],
        data['photos_grab_amount'],
        data['follow_likers_per_photo'],
        data['sleep_delay'],
    )
    return parameters


def eval_param(param):
    """Returns emoji representation of a boolean param for display purpose."""
    if param:
        return '✅'
    return '❌'


class Parameters(NamedTuple):
    """insta_gh parameters tuple."""

    username: str
    password: str
    targets: list
    do_follow_likers: bool
    do_follow_followers: bool
    do_follow_following: bool
    do_unfollow: bool
    dont_include: list
    unfollow_after: int
    headless_browser: bool
    unfollow_amount: int
    photos_grab_amount: int
    follow_likers_per_photo: int
    sleep_delay: int

    def __str__(self):
        result = ''
        result += f'🧔  {self.username}\n'
        result += f'{eval_param(self.headless_browser)}  Headless browser\n'
        result += '\n'
        idx = 0
        for target in self.targets:
            if idx == 0:
                result += f'🎯  {target}\n'
            else:
                result += f'    {target}\n'
            idx += 1
        result += '\n'
        result += f'{eval_param(self.do_unfollow)}  Unfollow'
        if self.do_unfollow:
            result += f' : [cyan]{self.unfollow_amount}[/cyan]'
            result += f'\n     after [cyan]{self.unfollow_after}[/cyan] hours'
        result += '\n\n'
        result += f'{eval_param(self.do_follow_likers)}  Follow likers\n'
        if self.do_follow_likers:
            result += f'     - Grab [cyan]{self.photos_grab_amount}[/cyan] photo(s) per target\n'
            result += (
                f'     - Follow [cyan]{self.follow_likers_per_photo}[/cyan] liker(s) per photo\n'
            )
        # result += (
        #     f'{self.eval_param(self.do_follow_followers)} Follow followers (not implemented)\n'
        # )
        # result += (
        #     f'{self.eval_param(self.do_follow_following)} Follow following (not implemented)\n'
        # )
        result += '\n'
        result += f'😴  Sleep delay: [cyan]{self.sleep_delay}[/cyan]'
        return result
