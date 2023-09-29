import json

from django.test import TestCase, Client
from django.urls import reverse

from .models import Robot


class AddRobotViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.add_robot_url = reverse('add')

    def test_valid_data_creates_robot(self):
        """Успешное создание робота"""
        data = {
            "model": "X1",
            "version": "V2",
            "created": "2023-09-26T12:00:00"
        }
        response = self.client.post(self.add_robot_url, json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "robot created")
        self.assertTrue(Robot.objects.filter(model="X1", version="V2").exists())
