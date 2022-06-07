from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template

from information import models as imodels


def send_simple_email(request, template_path: str, reciepients: list, subject: str = "Email", context: dict = {}) -> bool:
  try:
    sender_email = f"{settings.DEFAULT_FROM_NAME} <{settings.EMAIL_HOST_USER}>"
    message = get_template(template_path).render(context) # path to the email template - 'email/results.html'

    msg = EmailMessage(
      subject,
      message,
      sender_email,
      reciepients,
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()

    print(f"\nMail successfully sent: {msg}")
    return True
  except Exception as e:
    print(f"There was an exception sending mail: {e}")
    return False


def send_assigned_assessment_email(student):
  email = student.user.email
  subject = "New Assessment Assigned"
  context = {"student": student}
  
  try:
    mail = send_simple_email(request, 'email/assigned_assessment.html', [email], subject, context)
    print(f'Assigned Assessment mail sent successfully')
    return True
  except:
    print(f'An exception occurred while sending Assigned Assessment: {e}')
    return False
  

def create_scoped_student_assignment_notice(request, assignment):
  """Assessment can be either a test or assignment"""
  scope = imodels.Scope.objects.none()
  try:
    scope = imodels.Scope.objects.filter(course=assignment.course) 
    if not scope:
      raise Exception("Relevant Scope doesn't exist")
    
    if len(scope) > 1: 
      scope = imodels.Scope.objects.filter(course=assignment.course).first()
    else:
      scope = imodels.Scope.objects.get(course=assignment.course)
  except Exception as e:
    print("Relevant scope created")
    print(f"because of error: {e}")
    scope = imodels.Scope.objects.create(course=assignment.course, is_general=False)

  try:
    notice = imodels.Notice.objects.create(
      source=request.user,
      scope=scope,
      title=f"New Assignment for {assignment.course.code}",
      message=f"You have a new assignment for {assignment.course.code}. Remember to submit your assignment before, {assignment.due_date}.",
    )
    return True
  except Exception as e:
    print(f"Error creating assignment notice: {e}")
    return False
