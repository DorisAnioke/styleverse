from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_tracking_update_email(tracking):
    subject = f"Order Tracking Update - Order #{tracking.order.id}"
    html_message = render_to_string(
        'emails/tracking_update.html',  
        {
            'user': tracking.order.user,
            'order': tracking.order,
            'tracking': tracking,
        }
    )
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [tracking.order.user.email]

    send_mail(
        subject,
        plain_message,
        from_email,
        to_email,
        html_message=html_message
    )