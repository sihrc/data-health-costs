import time

"""
* Debug/Timer Wrapper
    prints debug statements
    prints the timing of a function

author: chris
"""
def debug(func):
    """
    Debug Wrapper that prints time elapsed
    """
    def wrapper(*arg, **kwargs):
        # print "===========w============================"
        # print "Currently Running:%s %s"% (func.func_name, func.__doc__)
        t1 = time.time()
        res = func(*arg,**kwargs)
        t2 = time.time()
        # print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
        # print "=======================================\n"
        return res
    return wrapper