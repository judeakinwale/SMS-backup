from user.models import CourseRegistration

# TODO:
# send mail with formatted relevant student test results to course adviser
# generate a list of courses registered buy a student for the current semester and session


def get_registered_courses(student, session, semester):
    reg = CourseRegistration.objects.filter(student=student, session=session, semester=semester)
    return reg


def get_current_registered_courses(student, semester):
    reg = CourseRegistration.objects.filter(student=student, session__is_current=True, semester=semester)
    return reg
