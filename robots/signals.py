from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from .models import Robot

TEMPLATE_EMAIL_REMINDER = """Добрый день!
Недавно вы интересовались нашим роботом модели {}, версии {}. 
Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами"""


@receiver(post_save, sender=Robot)
def send_email_order_notification(sender, instance, created, **kwargs):
    if created:
        robot_orders = Order.objects.filter(is_email_notified=False, robot_serial=f'{instance.model}-{instance.version}')
        for robot_order in robot_orders:
            send_mail(subject='Новый робот для вас!',
                      message=TEMPLATE_EMAIL_REMINDER.format(instance.model, instance.version),
                      from_email='no_reply@example.com',
                      recipient_list=[robot_order.customer.email])
            robot_order.is_email_notified = True
            robot_order.save()
