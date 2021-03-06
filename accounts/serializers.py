from rest_framework import serializers
from accounts.models import User, Token


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('email', 'uid')
