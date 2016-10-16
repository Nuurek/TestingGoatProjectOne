from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_api import views
from rest_framework import urls, routers, serializers, viewsets


urlpatterns = [
    url(r'^session_key/(?P<email>[^\/]+)/$', views.create_pre_authenticated_session)
]
