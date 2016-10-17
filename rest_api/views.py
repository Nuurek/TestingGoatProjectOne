from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from accounts.models import Token
from accounts.serializers import TokenSerializer
from django.conf import settings
from django.contrib.auth import (
    BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
)
from django.contrib.sessions.backends.db import SessionStore


User = get_user_model()


@api_view(['GET'])
@permission_classes((permissions.AllowAny, ))
def create_pre_authenticated_session(request, email):
    if request.method == 'GET':
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        return Response({"session_key": session.session_key})

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
