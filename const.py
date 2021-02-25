def constant(f):
    def fset(self, value):
        raise TypeError

    def fget(self):
        return f()

    return property(fget, fset)


class Const(object):
    @constant
    def UNFOLLOWED_KEY():
        return 'unfollowed'

    @constant
    def UNFOLLOWED_ON_KEY():
        return 'unfollowed_on'

    @constant
    def FOLLOWED_KEY():
        return 'followed'

    @constant
    def FOLLOWED_ON_KEY():
        return 'followed_on'

    @constant
    def ALREADY_FOLLOWED_KEY():
        return 'already_followed'

    @constant
    def NOT_VALID_USER_KEY():
        return 'not_valid_users'

    @constant
    def UNFOLLOW_STEP_KEY():
        return 'unfollow_step'

    @constant
    def FOLLOW_STEP_KEY():
        return 'follow_likers_step'

    @constant
    def PROGRESS_KEY():
        return 'progress'

    @constant
    def JOB_KEY():
        return 'job'
