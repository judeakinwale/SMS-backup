from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template


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
  