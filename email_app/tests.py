from django.test import TestCase
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile

class SendEmailTests(TestCase):

    @patch("email_app.views.send_email_message")
    def test_valid_email(self, mock_send):
        response = self.client.post(
            "/send-email/",
            {
                "sender": "sender@example.com",
                "receiver": "receiver@example.com",
                "subject": "Test Email",
                "message": "This is a test message.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["message"],
            "Email sent successfully."
        )
        mock_send.assert_called_once()

    def test_missing_required_field(self):
        response = self.client.post(
            "/send-email/",
            {
                "sender": "sender@example.com",
                "receiver": "receiver@example.com",
                "subject": "",
                "message": "Test message",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("required", response.json()["error"])

    def test_invalid_sender_email(self):
        response = self.client.post(
            "/send-email/",
            {
                "sender": "not-an-email",
                "receiver": "receiver@example.com",
                "subject": "Test",
                "message": "Test message",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"],
            "Invalid sender email address."
        )

    def test_invalid_receiver_email(self):
        response = self.client.post(
            "/send-email/",
            {
                "sender": "sender@example.com",
                "receiver": "not-an-email",
                "subject": "Test",
                "message": "Test message",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"],
            "Invalid receiver email address."
        )

    def test_invalid_cc_email(self):
        response = self.client.post(
            "/send-email/",
            {
                "sender": "sender@example.com",
                "receiver": "receiver@example.com",
                "subject": "Test",
                "message": "Test message",
                "cc": "valid@example.com,not-an-email",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid CC", response.json()["error"])

    @patch("email_app.views.send_email_message")
    def test_multiple_cc_recipients(self, mock_send):
        response = self.client.post(
            "/send-email/",
            {
                "sender": "sender@example.com",
                "receiver": "receiver@example.com",
                "subject": "CC Test",
                "message": "Testing multiple CC recipients.",
                "cc": "cc1@example.com, cc2@example.com",
            },
        )

        self.assertEqual(response.status_code, 200)
        mock_send.assert_called_once()

        call_kwargs = mock_send.call_args.kwargs

        self.assertEqual(
            call_kwargs["cc_recipients"],
            ["cc1@example.com", "cc2@example.com"]
        )

    @patch("email_app.views.send_email_message")
    def test_email_attachment(self, mock_send):

        attachment = SimpleUploadedFile(
            "test.txt",
            b"This is a test attachment.",
            content_type="text/plain",
        )

        response = self.client.post(
            "/send-email/",
            {
                "sender": "sender@example.com",
                "receiver": "receiver@example.com",
                "subject": "Attachment Test",
                "message": "Testing an attachment.",
                "attachment": attachment,
            },
        )

        self.assertEqual(response.status_code, 200)
        mock_send.assert_called_once()

        call_kwargs = mock_send.call_args.kwargs

        self.assertIsNotNone(call_kwargs["attachment"])
        self.assertEqual(
            call_kwargs["attachment"].name,
            "test.txt"
        )

    @patch("email_app.views.send_email_message")
    def test_email_sending_failure(self, mock_send):
        mock_send.side_effect = Exception("SMTP connection failed")

        response = self.client.post(
            "/send-email/",
            {
                "sender": "sender@example.com",
                "receiver": "receiver@example.com",
                "subject": "Failure Test",
                "message": "Testing SMTP failure.",
            },
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json()["error"],
            "Failed to send email. Please try again."
        )