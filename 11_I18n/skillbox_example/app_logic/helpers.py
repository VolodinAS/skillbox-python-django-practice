from django.core import mail


def check_access_by_age(age):
    if age < 15:
        return False
    return True


def send_mail(subject, message, from_email, recipient_list):
    mail.send_mail(
        subject,
        message,
        from_email,
        recipient_list
    )
