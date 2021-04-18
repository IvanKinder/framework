# from wsgiref.simple_server import make_server
from random import randint

from templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('templates/index.html', data=request.get('data', None))


class PageNotFound404:
    def __call__(self, request):
        return '404 BAD REQUEST', 'Page not found'


class Help:
    def __call__(self, request):
        return '200 OK', 'some help text'


routes = {
    '/': Index(),
    '/help/': Help(),
}


def some_front(request):
    request['data'] = randint(0, 50)


def other_front(request):
    request['key'] = 'key'


fronts = [some_front, other_front]


class Framework:
    def __init__(self, routes_obj, front_obj):
        self.routes_list = routes_obj
        self.front_list = front_obj

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if path in self.routes_list:
            view = self.routes_list[path]
        else:
            view = PageNotFound404()
        request = {}

        for front in self.front_list:
            front(request)

        # print(request)
        code, body = view(request)
        start_response(code, [('Content-type', 'text/html')])
        return [body.encode('utf-8')]


application = Framework(routes, fronts)




