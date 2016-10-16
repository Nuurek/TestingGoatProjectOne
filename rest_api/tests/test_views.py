from django.test import TestCase
from django.contrib.auth import SESSION_KEY
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser


TEST_MAIL = 'example@example.com'


class JSONResponseTest(TestCase):

    def test_view_responds_with_200_status_code(self):
        response = self.client.get(
            '/rest-api/session_key/{}/'.format(TEST_MAIL),
        )
        self.assertEqual(response.status_code, 200)

    def test_view_responds_with_JSON(self):
        response = self.client.get(
            '/rest-api/session_key/{}/'.format(TEST_MAIL),
        )
        self.assertEqual(
            response.__getitem__('Content-Type'),
            'application/json'
        )

    def test_view_returns_proper_session_key(self):
        response = self.client.get(
            '/rest-api/session_key/{}/'.format(TEST_MAIL),
        )
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        session_key = data['session_key']
        session = Session.objects.get(session_key=session_key)
        session_email = session.get_decoded().get('_auth_user_id')
        self.assertEqual(TEST_MAIL, session_email)
