import sqlite3
from datetime import date

from database.mappers import StudentMapper, CategoryMapper, CourseMapper
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, BaseSerializer, ListView, CreateView
from patterns.creational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug
from templator import render

connection = sqlite3.connect('database/db.sqlite')
site = Engine()
student_mapper = StudentMapper(connection)
category_mapper = CategoryMapper(connection)
course_mapper = CourseMapper(connection)
site.students = student_mapper.all()
site.categories = category_mapper.all()
site.courses = course_mapper.all()
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
        student_name = ''
        try:
            category = site.find_category_by_name(request['request_params']['name'])
            try:
                student_name = request['request_params']['student_name']
            except:
                pass
            return '200 OK', render('courses_list.html', objects_list=category_mapper.courses(category), name=category.name, category=category, student_name=student_name)
        except KeyError:
            return '200 OK', render('courses_list.html', objects_list=['нет курсов'])


@AppRoute(routes=routes, url='/create_course/')
class CreateCourse:
    category_name = ''

    @Debug()
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']

            course_name = data['name']
            course_name = site.decode_value(course_name)

            category = None
            if self.category_name != '':
                category = site.find_category_by_name(self.category_name)

                course = site.create_course(course_name)
                course_mapper.insert(course, category)
                site.courses.append(course)

            return '200 OK', render('courses_list.html', objects_list=category_mapper.courses(category), name=category.name)

        else:
            try:
                self.category_name = request['request_params']['category']
                category = site.find_category_by_name(self.category_name)

                return '200 OK', render('create_course.html', name=category.name)
            except KeyError:
                return '200 OK', render('create_course.html', name='Нет категорий')


@AppRoute(routes=routes, url='/create_category/')
class CreateCategory:

    @Debug()
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_name = data.get('category_name')

            # category = None
            # if category_name:
            #     category = site.find_category_by_name(category_name)

            new_category = site.create_category(name)
            try:
                category_mapper.insert(new_category)
                site.categories.append(new_category)

                return '200 OK', render('categories_list.html', objects_list=site.categories)
            except Exception:
                return '404 BAD_REQUEST', render('bad.html')
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


@AppRoute(routes=routes, url='/categories_list/')
class CategoryList:
    @Debug()
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('categories_list.html', objects_list=site.categories, category_mapper=category_mapper)


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


@AppRoute(routes=routes, url='/students_list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'students_list.html'


@AppRoute(routes=routes, url='/student_courses/')
class StudentCoursesListView(ListView):
    def __call__(self, request):
        student_name = request['request_params']['name']
        student = site.find_student_by_name(student_name)
        return '200 OK', render('student_courses.html', name=student_name, courses_list=student.courses)


@AppRoute(routes=routes, url='/add_to_course/')
class StudentAddToCourseView(ListView):
    def __call__(self, request):
        all_courses = site.courses
        student_name = request['request_params']['name']
        # student = site.find_student_by_name(student_name)
        return '200 OK', render('categories_list.html', name=student_name, courses_list=all_courses, objects_list=site.categories)


@AppRoute(routes=routes, url='/added/')
class StudentAddedToCourseView(ListView):
    def __call__(self, request):
        course_name = request['request_params']['course_name']
        student_name = request['request_params']['student_name']
        student = site.find_student_by_name(student_name)
        course = site.find_course_by_name(course_name)
        student.courses.add(course)
        return '200 OK', render('add_to_course.html', name=student_name, course_name=course_name)


@AppRoute(routes=routes, url='/create_student/')
class StudentCreateView(CreateView):

    @Debug()
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            student_name = data.get('student_name')

            # student = None
            # if student_name:
            #     student = site.find_student_by_name(student_name)

            new_student = site.create_student(name)
            student_mapper.insert(new_student)
            site.students.append(new_student)

            return '200 OK', render('students_list.html', objects_list=site.students)
        else:
            students = site.students
            return '200 OK', render('create_student.html', students=students)


@AppRoute(routes=routes, url='/api/')
class CategoryApi:
    @Debug()
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.categories).save()
