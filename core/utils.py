from user.models import AcademicData, CourseAdviser, CourseRegistration, Result, Staff
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from reportlab.pdfgen import canvas


# TODO:
# send mail with formatted relevant student test results to course adviser
# generate a list of courses registered buy a student for the current semester and session


def generate_pdf(name, **kwargs):
    pass


def get_all_registered_courses(student):
    regs = CourseRegistration.objects.filter(student=student)
    return regs


def get_registered_courses(student, session, semester):
    reg = CourseRegistration.objects.filter(student=student, session=session, semester=semester)
    # TODO: setup pdf for course registration
    
    return reg


def get_current_registered_courses(student, semester):
    reg = CourseRegistration.objects.filter(student=student, session__is_current=True, semester=semester)
    # TODO: setup pdf for course registration
    
    return reg


def send_results_to_course_adviser():
    # get all staff that are course advisers
    course_advisers = Staff.objects.filter(is_course_adviser=True)

    # get their department and level
    for adviser in course_advisers:
        course_adviser_email = adviser.user.email
        course_adviser = CourseAdviser.objects.get(staff=adviser)

        # students = AcademicData.filter(
        #     department=course_adviser.department,
        #     level=course_adviser.level,
        # )

        registered_courses = CourseRegistration.objects.filter(
            student__department=course_adviser.department,
            student__level=course_adviser.level
        )

        # for each course adviser get all students in their department and level
        for registered_course in registered_courses:
            # get the results for each student
            course = registered_course.course
            results = Result.objects.filter(course)

            # TODO: write the results to a pdf file

            # send it as mail to the course advisers email
            subject = f"{course.name} Results"
            html_message = render_to_string(
                'mail/results.html',
                {
                    'course': course,
                    'results': results,
                })
            plain_message = strip_tags(html_message)
            sender_email = 'from@example.com'  # TODO: Change email address

            # try:
            #     send_mail(
            #         subject=subject,
            #         message=plain_message,
            #         from_email=sender_email,
            #         recipient_list=[course_adviser_email],
            #         html_message=html_message,
            #         fail_silently=False,
            #     )
            #     print("Results sent")
            # except Exception as e:
            #     print("Results not sent")
            #     print(f"{e}")

            # Using EmailMessage
            context = {
                'course': course,
                'results': results,
            }
            message = get_template('mail/results.html').render(context)
            msg = EmailMessage(
                subject,
                message,
                sender_email,
                [course_adviser_email],
            )
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            print("Mail successfully sent")
