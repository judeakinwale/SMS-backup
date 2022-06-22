from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template

from assessment import models
from information import models as imodels
from user import models as umodels

from datetime import datetime
# from academics import serializers as aserializers
# from user import serializers as userializers


def can_modify_or_create_assessment_response(request ,taker, _type: str = "assignment") -> bool:
  instance = taker.assignment if _type == "assignment" else taker.quiz

  # raise exception if current day is past the due date for an assessment
  if _type == "assignment" and datetime.today().date() > instance.due_date:
    raise Exception(f"You are unable to submit this {_type}. the due date is past.")

  # raise exception if assessment has been submitted / completed
  if taker.completed:
    raise Exception(f"You have submitted this {_type}")

  # raise exception if authenticated user is not authorized
  if taker.student.user != request.user and  not request.user.is_superuser:
    raise Exception(f"You are not authorized to submit an answer to this {_type}")
  
  return True


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


# def post_assignment_submission():
#   pass


# # Not used
# def send_assigned_assessment_email(student):
#   email = student.user.email
#   subject = "New Assessment Assigned"
#   context = {"student": student}
  
#   try:
#     mail = send_simple_email(request, 'email/assigned_assessment.html', [email], subject, context)
#     print(f'Assigned Assessment mail sent successfully')
#     return True
#   except:
#     print(f'An exception occurred while sending Assigned Assessment: {e}')
#     return False  


def create_scoped_student_assessment_notice(request, assessment, _type="assignment"):
  """
  Assessment can be either a test or assessment.
  _type can be either "assignment" or "test"
  """
  message = f"You have a new {_type} for course {assessment.course.code}."
  
  if _type == "assignment":
    message = f"{message} Remember to submit your {_type} before, {assessment.due_date}."

  scope = imodels.Scope.objects.none()
  try:
    scope = imodels.Scope.objects.filter(course=assessment.course, is_general=False).first()
    # scope = imodels.Scope.objects.filter(
    #   course=assessment.course, 
    #   faculty=None,
    #   department=None,
    #   specialization=None,
    #   level=None,
    #   is_general=False,
    #   is_first_year=False,
    #   is_final_year=False,
    # ).first()  # reduce chance of false postives
    if not scope:
      raise Exception("Relevant Scope doesn't exist")
  except Exception as e:
    print("Relevant scope created")
    print(f"because of error: {e}")
    scope = imodels.Scope.objects.create(course=assessment.course, is_general=False)

  try:
    notice, created = imodels.Notice.objects.get_or_create(
      source=request.user,
      scope=scope,
      title=f"New {_type.title()} for {assessment.course.code}",
      message=message,
    )
    # run the functionality in the .save method to send mail
    if not created:
      notice.save()
    return True
  except Exception as e:
    print(f"Error creating {_type.title()} notice: {e}")
    return False


def register_assessment_takers(assessment, _type="assignment"):
  """
  _type can be either "assignment" or "test"
  """
  course_registrations = umodels.CourseRegistration.objects.filter(course=assessment.course)
  if not course_registrations:
    raise Exception(f"There are no students registered for the course {assessment.course.code}")
  
  for registration in course_registrations:
    takers = None
    try:
      if _type == "assignment":
        takers = models.AssignmentTaker.objects.filter(student=registration.student, assignment=assessment)
        taker, created = models.AssignmentTaker.objects.get_or_create(student=registration.student, assignment=assessment)
      elif _type == "test":
        takers = models.QuizTaker.objects.filter(student=registration.student, quiz=assessment)
        taker, created = models.QuizTaker.objects.get_or_create(student=registration.student, quiz=assessment)
    except Exception as e:
      if not takers:
        raise Exception(e)
  print("Students Registered!")
