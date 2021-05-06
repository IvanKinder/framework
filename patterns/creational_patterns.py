import copy
import quopri
from datetime import datetime


class User:
    def __init__(self, username, student):
        self.username = username
        self.student = student
        self.courses = []


class Teacher(User):
    pass


class Student(User):
    pass


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    # Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


# Прототип
class CoursePrototype:

    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class InteractiveCourse(Course):
    pass


class RecordedCourse(Course):
    pass


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


# class CourseFactory:
#     @classmethod
#     def create(cls, name, category):
#         return cls(name, category)
    # types = {
    #     'interactive': InteractiveCourse,
    #     'recorded': RecordedCourse
    # }

    # Фабричный метод
    # @classmethod
    # def create(cls, type_, name, category):
    #     return cls.types[type_](name, category)


class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_student(name, student=None):
        return Student(name, student)

    def find_student_by_id(self, id):
        for student in self.students:
            print('student', student.id)
            if student.id == id:
                return student
        raise Exception(f'Нет студента с id = : {id}')

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_name(self, name):
        for category in self.categories:
            # print('category', category.name)
            if category.name == name:
                return category
        raise Exception(f'Нет категории с названием : {name}')

    @staticmethod
    def create_course(name, category):
        # return CourseFactory.create(type_, name, category)
        return Course(name, category)

    def get_course(self, name):
        for course in self.courses:
            if course.name == name:
                return course
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace('+', ' '), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# Singleton
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log: ', text)
        # with open(f'{datetime.now()}.log', 'a', encoding='utf-8') as log_file:
        #     log_file.write(f'{datetime.now()}:  {text}\n')
