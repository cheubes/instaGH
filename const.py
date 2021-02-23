def constant(f):
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)

class Const(object):

    @constant
    def UNFOLLOW_STEP_KEY():
        return 'unfollow_step'
    @constant
    def PROGRESS_KEY():
        return 'progress'
    @constant
    def JOB_KEY():
        return 'job'
