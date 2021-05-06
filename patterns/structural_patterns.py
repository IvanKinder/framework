import time


class AppRoute:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debug:

    def __call__(self, cls):
        def timeit(function):
            def timed(*args, **kwargs):
                t1 = time.time()
                result = function(*args, **kwargs)
                t2 = time.time()

                print(f'Функция {cls} выполнялась {(t2 - t1):2.3f} миллисекунд')
                return result

            return timed

        return timeit(cls)