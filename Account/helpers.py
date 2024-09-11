

from django.core.mail import send_mail

from django.conf import settings 


def send_forget_password_mail(email , token):
    subject = 'Your forget password link'
    message = f'hi, click on the link to reset your password http://127.0.0.1:8000/change_password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def send_email_to_user():
    subject = 'Order Confirmation'
    message ='you order has been confirmed'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['djangotesting5@gmail.com']
    send_mail(subject, message, from_email, recipient_list)
