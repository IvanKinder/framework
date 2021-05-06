from views import Index, Help, ContactUs, StudyPrograms, CoursesList, CreateCourse, CreateCategory, CategoryList, \
    CopyCourse, About

# routes = {
#     '/': Index(),
#     '/help/': Help(),
#     '/about/': About(),
#     '/contact_us/': ContactUs(),
#     '/study_programs/': StudyPrograms(),
#     '/courses_list/': CoursesList(),
#     '/create_course/': CreateCourse(),
#     '/create_category/': CreateCategory(),
#     '/categories_list/': CategoryList(),
#     '/copy_course/': CopyCourse(),
# }


def some_front(request):
    # request['data'] = ''
    pass


def other_front(request):
    # request['key'] = 'key'
    pass


fronts = [some_front, other_front]
