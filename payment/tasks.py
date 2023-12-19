from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Order, ShippingAddress


@shared_task
def send_order_confirmation_mail(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order {order.id} - Payment Confirmation'
    message = f'Hello {order.user.username}! Your order has been confirmed. Total amount: {order.amount}'
    recipient_data = ShippingAddress.objects.get(user=order.user)
    recipient_email = recipient_data.email
    send_mail_to_user = send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])
    return send_mail_to_user
