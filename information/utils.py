from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template

from information import models
from user import models as umodels
from academics import models as amodels


def send_simple_email(template_path: str, reciepients: list, subject: str = "Email", context: dict = {}, cc: list = [], message: str = '') -> bool:
  try:
    sender_email = f"{settings.DEFAULT_FROM_NAME} <{settings.EMAIL_HOST_USER}>"
    if message == '':
      message = get_template(template_path).render(context) # path to the email template - 'email/results.html'

    msg = EmailMessage(
      subject=subject,
      body=message,
      from_email=sender_email,
      to=reciepients,
      cc=cc
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()

    print(f"\nMail successfully sent: {msg}")
    return True
  except Exception as e:
    print(f"There was an exception sending mail: {e}")
    raise Exception(f"Error Sending Email: {e}")
    return False


def get_related_students(scope):
  """Get all students related to a scope"""
  students = umodels.Student.objects.none()
  department_id_set = set()
  specialization_id_set = set()
  student_id_set = set()
  
  try:
    if scope.is_general:
      students = umodels.Student.objects.all()
      for student in students: student_id_set.add(student.id)
      
    if scope.faculty:
      departments = scope.faculty.department_set.all()
      for department in departments:
        specializations = department.specialization_set.all()
        for specialization in specializations: specialization_id_set.add(specialization.id)
        
      students = umodels.Student.objects.filter(specialization__id__in=specialization_id_set)
      for student in students: student_id_set.add(student.id)

    if scope.department:
      specializations = scope.department.specialization_set.all()
      for specialization in specializations: specialization_id_set.add(specialization.id)
      
      students = umodels.Student.objects.filter(specialization__id__in=specialization_id_set)
      for student in students: student_id_set.add(student.id)
      
    if scope.specialization:
      students = scope.specialization.student_set.all()
      for student in students: student_id_set.add(student.id)
      
    if scope.course:
      course_registrations = scope.course.courseregistration_set.all()
      for registration in course_registrations: student_id_set.add(registration.student.id)

    # if a level, is first year or is final year is specified with other properties, 
    # it filters the responses of those properties 
    # NOTE: This code block has to be here 
    if scope.level and student_id_set:
      students = umodels.Student.objects.filter(id__in=student_id_set, academic_data__level__code=scope.level.code)
      for student in students: student_id_set.add(student.id)
    elif scope.level:
      students = umodels.Student.objects.filter(academic_data__level__code=scope.level.code)
      for student in students: student_id_set.add(student.id)
      
    if scope.is_first_year and student_id_set:
      students = umodels.Student.objects.filter(id__in=student_id_set, academic_data__level__code=100)
      for student in students: student_id_set.add(student.id)
    elif  scope.is_first_year:
      students = umodels.Student.objects.filter(academic_data__level__code=100)
      for student in students: student_id_set.add(student.id)

    if scope.is_final_year and student_id_set:
      students = umodels.Student.objects.filter(id__in=student_id_set)
      for student in students: 
        if student.specialization.max_level == student.academic_data.level:
          student_id_set.add(student.id)
    elif scope.is_final_year:
      students = umodels.Student.objects.all()
      for student in students: 
        if student.specialization.max_level == student.academic_data.level:
          student_id_set.add(student.id)
    # get the students after the above filtering
    students = umodels.Student.objects.filter(id__in=student_id_set)
    # print(student_id_set)
  except Exception as e:
    # print(student_id_set)
    print(f"There was an exception getting the students for a scope: {e}")
  return students


def send_student_notice_email(notice, context: dict = {}) -> bool:
  try:
    students = get_related_students(notice.scope)
    if not students:
      raise Exception("There are no students related to notice's scope")
    reciepients = [student.user.email for student in students]
    subject = notice.title
    context["notice"] = notice

    mail = send_simple_email(
      template_path='email/notice.html', 
      reciepients=reciepients,
      subject=subject,
      context=context, 
      cc=[notice.source.email, "judeakinwale@gmail.com"]
    )
    print(f'Notice mail sent successfully: {mail}')
    if not mail:
      raise Exception("Error Sending Notice Email")
    return True
  except Exception as e:
    print(f'There was an exception sending notice emails: {e}')
    return False
