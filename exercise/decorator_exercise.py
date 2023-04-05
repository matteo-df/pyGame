import time


def execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print(f'Execution time: {time.time() - start} s')
    return wrapper


def execute_n_times(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator


@execution_time
@execute_n_times(5)
def my_function(name):
    time.sleep(0.5)
    print('Hello')
    time.sleep(0.5)
    print(name)
    time.sleep(0.5)
    print('Bye')


if __name__ == '__main__':
    my_function(name='Matteo')
