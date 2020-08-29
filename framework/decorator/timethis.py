import time
import functools


def timethis(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        print("method: %s, run time: %f" % (func.__name__, end-start))
        return r
    return wrapper
