from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Incident  # or whatever your model is called
from accounts.models import CustomUser, Device
from unittest.mock import patch

class SendToAdminNotificationTest(APITestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(
            username="admin", password="admin123", is_staff=True
        )
        self.regular_user = CustomUser.objects.create_user(
            username="user", password="user123"
        )
        self.device = Device.objects.create(
            user_id=self.admin_user,
            fcmToken="dummy_token",
            platformType="android"
        )

        self.incident = Incident.objects.create(
            title="Test Incident",
            description="This is a test",
            send_to_admin=False,
            created_by=self.regular_user
        )

        self.client.login(username="user", password="user123")
        self.url = reverse("incident-detail", kwargs={"uuid": self.incident.uuid})  # 👈 Adjust name

    @patch("account.utils.firebase.send_push_notification")
    def test_send_to_admin_switch_triggers_notification(self, mock_send):
        response = self.client.put(self.url, {"send_to_admin": True}, format="json")

        self.assertEqual(response.status_code, 200)
        mock_send.assert_called_once()
        self.assertTrue(response.data["data"]["send_to_admin"])

    @patch("account.utils.firebase.send_push_notification")
    def test_send_to_admin_false_does_not_trigger_notification(self, mock_send):
        # Already False → False, no change = no trigger
        response = self.client.put(self.url, {"send_to_admin": False}, format="json")

        self.assertEqual(response.status_code, 200)
        mock_send.assert_not_called()

    @patch("account.utils.firebase.send_push_notification")
    def test_send_to_admin_true_to_true_does_not_trigger_notification(self, mock_send):
        self.incident.send_to_admin = True
        self.incident.save()

        response = self.client.put(self.url, {"send_to_admin": True}, format="json")

        self.assertEqual(response.status_code, 200)
        mock_send.assert_not_called()
