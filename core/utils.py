from django.conf import settings
from user.models import CourseAdviser, CourseRegistration, Result, Staff
from django.core.mail import EmailMessage, send_mail
from django.template.loader import get_template, render_to_string  # TODO: add [, render_to_string]
# from django.utils.html import strip_tags
from django.shortcuts import HttpResponse
from reportlab.pdfgen import canvas


# TODO:
# send mail with formatted relevant student test results to course adviser
# generate a list of courses registered buy a student for the current semester and session


def generate_pdf(reqest, name, **kwargs):

    file_name = f"{name}.pdf"

    message = ""

    if 'data' in kwargs:
        data = kwargs.get('data')
        try:
            keys = data.keys()
            print(keys)

        except Exception as e:
            print(e)
            return HttpResponse("Data is not a python dictionary")

    # create a http response
    response = HttpResponse(content_type='application/pdf')

    # force a download of the pdf file
    response['Content-Disposition'] = f'attachment; filename={file_name}'

    pdf_file = canvas.Canvas(response)

    # Write content on the PDF
    pdf_file.drawString(100, 700, f"Hello {message}")
    pdf_file.showPage()
    pdf_file.save()

    return response


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


def send_results_to_course_adviser(request):
    # get all staff that are course advisers
    course_advisers = Staff.objects.filter(is_course_adviser=True)

    try:
        # get their department and level
        if len(course_advisers) < 1:
            return False
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

                # # for send_mail
                # subject = f"{course.name} Results"
                # html_message = render_to_string(
                #     'email/results.html',
                #     {
                #         'course': course,
                #         'results': results,
                #     })
                # plain_message = strip_tags(html_message)
                # sender_email = 'from@example.com'  # TODO: Change email address

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
                subject = f"{course.name} Results"
                sender_email = settings.EMAIL_HOST_USER  # TODO: Change email address
                context = {
                    'course': course,
                    'results': results,
                }
                message = get_template('email/results.html').render(context)
                msg = EmailMessage(
                    subject,
                    message,
                    sender_email,
                    [course_adviser_email],
                )
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()
                print("Mail successfully sent")
                return True

    except Exception as e:
        print(f"There was an exception: {e}")
        return False


def send_sample_email(request):
    try:
        subject = "Results"
        sender_email = settings.EMAIL_HOST_USER  # TODO: Change email address
        # print(sender_email)
        context = {
            'course': 'Mathematics',
            # 'results': results,
        }
        message = get_template('email/results.html').render(context)
        # print(message)

        msg = EmailMessage(
            subject,
            message,
            sender_email,
            ['judeakinwale@gmail.com'],
        )
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()

        # html_message = render_to_string(
        #     'email/results.html',
        #     {
        #         'course': "Physics",
        #         # 'results': results,
        #     }
        # )
        # test = send_mail(
        #     subject,
        #     "Sample Message",
        #     sender_email,
        #     ['judeakinwale@gmail.com',],
        #     # html_message=html_message,
        #     fail_silently=False,
        # )
        # print(test)
        print("\nMail successfully sent")
        return True
    except Exception as e:
        print(f"There was an exception: {e}")
        return False
