from django.test import TestCase
from .models import Feedback
from django.contrib.auth.models import Group, Permission
class FeedbackModelTests(TestCase):
    def test_feedback_creation(self):
        # Create a feedback instance
        feedback = Feedback.objects.create(
            name="John Doe",
            email="john@example.com",
            phone="1234567890",
            message="Great service!"
        )
        # Check if the feedback is created successfully
        self.assertEqual(feedback.name, "John Doe")
        self.assertEqual(feedback.email, "john@example.com")
        self.assertEqual(feedback.phone, "1234567890")
        self.assertEqual(feedback.message, "Great service!")
        self.assertIsNotNone(feedback.registration_id)  # Check UUID is generated
        self.assertIsNotNone(feedback.registered_time)  # Check timestamp is set
    def test_feedback_str(self):
        feedback = Feedback.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            phone="0987654321",
            message="Excellent support!"
        )
        expected_str = "Jane Doe - jane@example.com - 0987654321 - Excellent support! - {}".format(feedback.registration_id)
        self.assertEqual(str(feedback), expected_str)
