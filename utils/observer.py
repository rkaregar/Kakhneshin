import traceback


def non_recurse(f):
    def func(*args, **kwargs):
        if len([l[2] for l in traceback.extract_stack() if l[2] == f.__name__]) > 0:
            return
        return f(*args, **kwargs)
    return func