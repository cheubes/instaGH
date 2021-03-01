# instaGH

Simple [InstaPy](https://github.com/timgrossmann/InstaPy) template that implements a unfollow / follow likers pattern.

This template provide a rich console interface thanks to the [Rich API](https://github.com/willmcgugan/rich).



## Install prerequisites
```
pip install instapy
```
```
pip install rich
```



## Usage
```
python insta_gh.py parameters.yaml
```


### parameters
* `username` (str): Instagram user name.
* `password` (str): Instagram password.
* `target_list` (str[]): List of targeted users for the follow likers step.
* `target_size` (int): Number of user to randomly pick from the targets list.
* `do_follow_likers` (bool): Enable follow likers step.
* `do_unfollow` (bool): Enable unfollow step.
* `dont_include_list` (str[]): List of user not to unfollow.
* `unfollow_after` (int) : Unfollow only if a user has been following for this amount of time _(in hours)_.
* `headless_browser` (bool): Enable InstaPy to run background.
* `unfollow_amount` (int): Maximum number of people to unfollow.
* `photos_grab_amount` (int): Number of photos to grab from each target user to get likers from.
* `follow_likers_per_photo` (int): Number of likers to follow per photo.
* `sleep_delay` (int): Used to define break time after 10 follows _(in seconds)_.

The maximum of user followed will be `target_size` * `photos_grab_amount` * `follow_likers_per_photo`.
