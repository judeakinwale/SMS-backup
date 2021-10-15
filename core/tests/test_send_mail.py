# import smtplib
# from unittest import TestCase
# from core.utils import send_results_to_course_adviser


# class TestSMTP(TestCase):

#     def setUp(self):

#         pass

#     def test_smtp_connection(self, host, port):
#         # connect to actual host on actual port
#         smtp = smtplib.SMTP(host, port)
#         smtp.starttls()

#         # check we have an open socket
#         self.assertIsNotNone(smtp.sock)

#         # run a no-operation, which is basically a server-side pass-through
#         self.assertEqual(smtp.noop(), (250, '2.0.0 OK'))

#         # assert disconnected
#         self.assertEqual(smtp.quit(), (221, '2.0.0 Service closing transmission channel'))
#         self.assertIsNone(smtp.sock)

# result = send_results_to_course_adviser()
# print(result)
