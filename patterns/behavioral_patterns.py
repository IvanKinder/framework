from templator import render
import json


class Subject:

    def __init__(self):
        self.observers = []

    def notify(self):
        for observer in self.observers:
            observer.update(self)


class Observer:

    def update(self, subject):
        print(f'updated {subject}')


class SmsNotifier(Observer):

    def update(self, subject):
        print(f'SMS: updated {subject}')


class EmailNotifier(Observer):

    def update(self, subject):
        print(f'Email: updated {subject}')


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return json.dumps(self.obj)

    @staticmethod
    def load(data):
        return json.loads(data)


class TemplateView:
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template_name(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template_name()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)
            return self.render_template_with_context()
        else:
            return super().__call__(request)