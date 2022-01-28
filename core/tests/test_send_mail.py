from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
import smtplib
from unittest import TestCase
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from core.utils import send_results_to_course_adviser, send_sample_email

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


class TestSMTP(TestCase):

    def setUp(self):
        settings.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
        self.host = settings.EMAIL_HOST
        self.port = settings.EMAIL_PORT

    def tearDown(self):
        settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    # def test_smtp_connection(self, host, port):
    #     # connect to actual host on actual port
    #     smtp = smtplib.SMTP(host, port)
    #     smtp.starttls()

    #     # check we have an open socket
    #     self.assertIsNotNone(smtp.sock)

    #     # run a no-operation, which is basically a server-side pass-through
    #     self.assertEqual(smtp.noop(), (250, '2.0.0 OK'))

    #     # assert disconnected
    #     self.assertEqual(smtp.quit(), (221, '2.0.0 Service closing transmission channel'))
    #     self.assertIsNone(smtp.sock)

    def test_smtp_connection(self):
        # connect to actual host on actual port
        smtp = smtplib.SMTP(self.host, self.port)
        smtp.starttls()

        # check we have an open socket
        self.assertIsNotNone(smtp.sock)

        # run a no-operation, which is basically a server-side pass-through
        # doesn't work for gmail smtp, gmail has extra information
        # self.assertEqual(smtp.noop(), (250, '2.0.0 OK'))
        self.assertIn(250, smtp.noop())

        # assert disconnected
        # doesn't work for gmail smtp, gmail has extra information
        # self.assertEqual(smtp.quit(), (221, '2.0.0 Service closing transmission channel'))
        self.assertIn(221, smtp.quit())
        self.assertIsNone(smtp.sock)

    # def test(self):
    #     result = self.test_smtp_connection(self.host, self.port)
    #     print(result)

    def test_send_result_to_course_adviser(self):
        result = send_results_to_course_adviser(request)
        # print(result)
        self.assertTrue(result)

    def test_sample_email(self):
        result = send_sample_email(request)
        # print(result)
        self.assertTrue(result)
