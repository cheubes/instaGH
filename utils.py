import argparse
import os
import yaml
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

def load_parameters():

    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', help='Yaml file to get parameters from.')
    args = parser.parse_args()

    # Loading data
    current_path = os.path.abspath(os.path.dirname(__file__))
    print('\n')

    print('📄 %s/%s' % (current_path, args.data_file))
    data = yaml.safe_load(open('%s/%s' % (current_path, args.data_file)))

    parameters = Parameters(data['username'], data['password'],
                            data['target_list'],
                            data['do_follow_likers'], data['do_follow_followers'], data['do_follow_following'], data['do_unfollow'],
                            data['dont_include_list'],
                            data['headless_browser'])

    print('\t🧔 %s' % parameters.username)
    print('\t🎯 %s' % parameters.targets)
    print('\t%s Follow likers' % ('✅' if parameters.do_follow_likers else '❌'))
    print('\t%s Follow followers' % ('✅' if parameters.do_follow_followers else '❌'))
    print('\t%s Follow following' % ('✅' if parameters.do_follow_following else '❌'))
    print('\t%s Unfollow' % ('✅' if parameters.do_unfollow else '❌'))
    print('\t%s Headless browser' % ('✅' if parameters.headless_browser else '❌'))

    print('\n')

    return parameters
