from datetime import timedelta

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .models import Robot


class GetOrdersViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.get_robots = reverse('get')

        Robot.objects.create(model='R2', version='D2', created=timezone.now() - timedelta(days=8))
        Robot.objects.create(model='R3', version='D3', created=timezone.now() - timedelta(days=6))

    def test_response_content_filename(self):
        response = self.client.get(self.get_robots)
        self.assertEquals(response['content-type'], 'application/vnd.ms-excel')
        self.assertIn('filename=last_7_days_robots.xlsx', response['Content-Disposition'])
