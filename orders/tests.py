from django.test import TestCase, Client
from django.urls import reverse

from customers.models import Customer
from robots.models import Robot


class MakeOrderTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = Customer.objects.create(email="customer@example.com")
        Robot.objects.create(model="R2", version="D2", created="2023-01-01 00:00:00")

    def test_successful_order(self):
        """Успешный заказ робота"""
        response = self.client.get(reverse('make', args=['R2', 'D2']))
        self.assertEqual(response.status_code, 200)
