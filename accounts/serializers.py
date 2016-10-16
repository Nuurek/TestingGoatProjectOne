from rest_framework import serializers
from accounts.models import User, Token


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    uid = serializers.CharField(max_length=40)

    def create(self, validated_data):
        return Token.objects.create(**validated_data)
