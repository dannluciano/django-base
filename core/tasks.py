import uuid

from django.conf import settings
from django.core.mail import EmailMessage
from django.tasks import task


@task()
def send_email(
    subject, message, sender_name, sender_email, to=settings.DEFAULT_FROM_EMAIL
):
    email = EmailMessage(
        subject,
        message,
        f"{sender_name}<{sender_email}>",
        [to],
        reply_to=[sender_email],
        headers={"Message-ID": f"{uuid.uuid4()}"},
    )
    email.send(fail_silently=False)
