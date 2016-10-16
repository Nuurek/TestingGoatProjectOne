from django.test import TestCase
from accounts.models import Token
from accounts.serializers import TokenSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.utils.six import BytesIO

TEST_EMAIL = 'example@example.com'

class TokenSerializerTest(TestCase):

    def test_serialized_and_then_deserialized_data_is_valid(self):
        token = Token(email=TEST_EMAIL)
        token.save()
        serializer = TokenSerializer(token)
        content = JSONRenderer().render(serializer.data)
        stream = BytesIO(content)
        data = JSONParser().parse(stream)
        serializer = TokenSerializer(data=data)
        self.assertTrue(serializer.is_valid())
