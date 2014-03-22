import time

benchmarks = dict()

def time_it(name):
    print 'benchmarking for:', name
    benchmarks[name] = 0.0
    def decorator(func):
        def inner(*args, **kwargs):
            start = time.clock() 
            value = func(*args, **kwargs)
            benchmarks[name] += time.clock()  - start
            return value 
        return inner
    return decorator


