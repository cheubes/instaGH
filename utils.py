import argparse
import os
import yaml
import random
from typing import NamedTuple


class Parameters(NamedTuple):
    username: str
    password: str
    targets: list
    do_follow_likers: bool
    do_follow_followers: bool
    do_follow_following: bool
    do_unfollow: bool
    dont_include: list
    headless_browser: bool

    def __str__(self):
        result = ''
        result += '🧔 %s\n' % self.username
        result += '🎯 %s\n' % self.targets
        result += '%s Follow likers\n' % ('✅' if self.do_follow_likers else '❌')
        result += '%s Follow followers\n' % ('✅' if self.do_follow_followers else '❌')
        result += '%s Follow following\n' % ('✅' if self.do_follow_following else '❌')
        result += '%s Unfollow\n' % ('✅' if self.do_unfollow else '❌')
        result += '%s Headless browser\n' % ('✅' if self.headless_browser else '❌')
        return result

def load_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', help='Yaml file to get parameters from.')
    args = parser.parse_args()
    # Loading data
    current_path = os.path.abspath(os.path.dirname(__file__))
    data = yaml.safe_load(open('%s/%s' % (current_path, args.data_file)))
    parameters = Parameters(data['username'], data['password'],
                            random.sample(data['target_list'], 3),
                            data['do_follow_likers'], data['do_follow_followers'], data['do_follow_following'], data['do_unfollow'],
                            data['dont_include_list'],
                            data['headless_browser'])
    return parameters
