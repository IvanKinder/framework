import sqlite3

from patterns.creational_patterns import Student, Category, Course

connection = sqlite3.connect('db.sqlite')


class StudentMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'students'
        self.student_course = 'student_course'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, username = item
            student = Student(username)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, username FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise Exception(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (username) VALUES (?)"
        self.cursor.execute(statement, (obj.username,))
        try:
            self.connection.commit()
        except Exception as e:
            raise Exception(e.args)

    def courses(self, obj):
        statement = f"select course from {self.student_course} where student = '{str(obj.username)}'"
        result = self.cursor.execute(statement)
        tmp_list = []
        for course in result.fetchall():
            tmp_list.append(course[0])
        return tmp_list

    def add_to_course(self, obj, course):
        try:
            statement = f"insert into {self.student_course} (student, course) values (?, ?)"
            self.cursor.execute(statement, (obj.username, course))
            self.connection.commit()
        except:
            pass

    # def update(self, obj):
    #     statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
    #     # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
    #     self.cursor.execute(statement, (obj.name, obj.id))
    #     try:
    #         self.connection.commit()
    #     except Exception as e:
    #         raise Exception(e.args)
    #
    # def delete(self, obj):
    #     statement = f"DELETE FROM {self.tablename} WHERE id=?"
    #     self.cursor.execute(statement, (obj.id,))
    #     try:
    #         self.connection.commit()
    #     except Exception as e:
    #         raise Exception(e.args)


# class MapperRegistry:
#     mappers = {
#         'student': StudentMapper,
#         #'category': CategoryMapper
#     }
#
#     @staticmethod
#     def get_student_mapper(obj):
#         if isinstance(obj, Student):
#             return StudentMapper(connection)
#
#     @staticmethod
#     def get_current_mapper(name):
#         return MapperRegistry.mappers[name](connection)


class CategoryMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'categories'
        self.category_course = 'category_course'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            category = Category(name)
            category.id = id
            result.append(category)
        return result

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        try:
            self.cursor.execute(statement, (obj.name,))
            self.connection.commit()
        except Exception as e:
            raise Exception(e.args)

    def course_count(self, category_name):
        statement = f"SELECT count(category) FROM {self.category_course} where category = {str(category_name)}"
        my_count = self.cursor.execute(statement)
        return my_count.fetchone()[0]

    def courses(self, obj):
        statement = f"select course from {self.category_course} where category = {obj.name}"
        result = self.cursor.execute(statement)
        tmp_list = []
        for course in result.fetchall():
            tmp_list.append(course[0])
        return tmp_list


class CourseMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'courses'
        self.category_course = 'category_course'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            course = Course(name)
            course.id = id
            result.append(course)
        return result

    def insert(self, obj, category):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        statement_to_category = f"INSERT INTO {self.category_course} (category, course) VALUES (?, ?)"
        try:
            self.cursor.execute(statement, (obj.name,))
            self.cursor.execute(statement_to_category, (category.name, obj.name,))
            self.connection.commit()
        except Exception as e:
            raise Exception(e.args)
