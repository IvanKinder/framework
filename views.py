from templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', data=request.get('data', None))


class PageNotFound404:
    def __call__(self, request):
        return '404 BAD REQUEST', 'Page not found'


class Help:
    def __call__(self, request):
        return '200 OK', 'some help text'


class ContactUs:
    def __call__(self, request):
        return '200 OK', render('contact_us.html')
