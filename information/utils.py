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
      # print("is_general")
      students = umodels.Student.objects.all()
      for student in students: student_id_set.add(student.id)
      # print(f"student count: {len(student_id_set)}")

    if scope.is_first_year:
      # print("is_first_year")
      students = umodels.Student.objects.filter(academic_data__level__code=100)
      for student in students: student_id_set.add(student.id)
      # print(f"student count: {len(student_id_set)}")

    if scope.is_final_year:
      # print("is_final_year")
      students = umodels.Student.objects.all()
      for student in students: 
        student_id_set.add(student.id)
      
      students = umodels.Student.objects.filter(specialization__id__in=specialization_id_set)
      for student in students: student_id_set.add(student.id)
      # print(f"student count: {len(student_id_set)}")      
      
    if scope.department:
      # print("department")
      specializations = scope.department.specialization_set.all()
      for specialization in specializations: specialization_id_set.add(specialization.id)
      
      students = umodels.Student.objects.filter(specialization__id__in=specialization_id_set)
      for student in students: student_id_set.add(student.id)
      # print(f"student count: {len(student_id_set)}")      
      
    if scope.specialization:
      # print("specialization")
      # students = umodels.Student.objects.filter(specialization=scope.specialization)
      students = scope.specialization.student_set.all()
      for student in students: student_id_set.add(student.id)
      # print(f"student count: {len(student_id_set)}")      
      
    if scope.course:
      # print("course")
      course_registrations = scope.course.courseregistration_set.all()
      for registration in course_registrations: student_id_set.add(registration.student.id)
      # print(f"student count: {len(student_id_set)}")      
      
    if scope.level:
      # print("level")
      students = umodels.Student.objects.filter(academic_data__level__code=scope.level.code)
      for student in students: student_id_set.add(student.id)
      
    students = umodels.Student.objects.filter(id__in=student_id_set)
    print(student_id_set)
  except Exception as e:
    print(student_id_set)
    print(f"There was an exception getting the students for a scope: {e}")
  return students


def send_student_notice_email(notice, context: dict = {}):
  try:
    students = get_related_students(notice.scope)
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
    print(f'An exception occurred: {e}')
    return False
