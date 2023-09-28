from django.http import HttpResponse

from customers.models import Customer
from robots.models import Robot
from .models import Order


def make_order(request, model, version):
    # TODO переделать заглушку определения покупателя
    customer = Customer.objects.get(id=request.user.id) if request.user.is_authenticated else Customer.objects.get(id=1)
    if Order.objects.filter(is_email_notified=False, robot_serial=f"{model}-{version}", customer=customer).exists():
        return HttpResponse(
            f"<h2>Ранее вы уже заказывали робота модели {model} версии {version}. Мы отправим вам email, как только робот будет готов.</h2>")
    Order.objects.create(robot_serial=f"{model}-{version}", customer=customer)

    # проверяем доступность робота (число определенных роботов больше числа заказов на этих роботов)
    if Robot.objects.filter(model=model, version=version).count() > Order.objects.filter(
            robot_serial=f"{model}-{version}").count():
        return HttpResponse(
            f"<h2>Вы успешно заказали робота модели {model} версии {version}. Ваш заказ будет доставлен в ближайшее время.</h2>")
    else:
        return HttpResponse(
            f"<h2>К сожалению сейчас робота модели {model} версии {version} нет в наличии. Мы отправим вам email, как только робот будет готов.</h2>")
