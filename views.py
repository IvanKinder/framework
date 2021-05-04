from datetime import date

from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, BaseSerializer, ListView, CreateView
from patterns.creational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug
from templator import render


site = Engine()
logger = Logger('main')
routes = {}
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


@AppRoute(routes=routes, url='/')
class Index:
    @Debug()
    def __call__(self, request):
        return '200 OK', render('index.html', data=request.get('data', None))


class PageNotFound404:
    @Debug()
    def __call__(self, request):
        return '404 BAD REQUEST', 'Page not found!'


@AppRoute(routes=routes, url='/help/')
class Help:
    @Debug()
    def __call__(self, request):
        return '200 OK', 'some help text'


@AppRoute(routes=routes, url='/about/')
class About:
    @Debug()
    def __call__(self, request):
        return '200 OK', 'About us'


@AppRoute(routes=routes, url='/contact_us/')
class ContactUs:
    @Debug()
    def __call__(self, request):
        return '200 OK', render('contact_us.html')


@AppRoute(routes=routes, url='/study_programs/')
class StudyPrograms:
    @Debug()
    def __call__(self, request):
        return '200 OK', render('study_programs.html', data=date.today())


@AppRoute(routes=routes, url='/courses_list/')
class CoursesList:
    @Debug()
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('courses_list.html', objects_list=category.courses, name=category.name, id=category.id)
        except KeyError:
            return '200 OK', render('courses_list.html', objects_list=['нет курсов'])


@AppRoute(routes=routes, url='/create_course/')
class CreateCourse:
    category_id = -1

    @Debug()
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)


            return '200 OK', render('course_list.html', objects_list=category.courses, name=category.name, id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', render('create_course.html', name='Нет категорий')


@AppRoute(routes=routes, url='/create_category/')
class CreateCategory:

    @Debug()
    def __call__(self, request):
        if request['method'] == 'POST':
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


@AppRoute(routes=routes, url='/categories_list/')
class CategoryList:
    @Debug()
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('categories_list.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/copy_course/')
class CopyCourse:
    @Debug()
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('course_list.html', objects_list=site.courses)
        except KeyError:
            return '200 OK', render('course_list.html', objects_list=['Нет курсов'])


@AppRoute(routes=routes, url='/students/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'students.html'


@AppRoute(routes=routes, url='/create_student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)



@AppRoute(routes=routes, url='/api/')
class CategoryApi:
    @Debug()
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.categories).save()
