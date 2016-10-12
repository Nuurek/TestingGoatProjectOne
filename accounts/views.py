from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib import auth, messages
from accounts.models import Token


def login(request):
    uid = request.GET.get('token')
    user = auth.authenticate(uid=uid)
    if user:
        auth.login(request, user)
    return redirect('/')


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token={uid}'.format(uid=str(token.uid))
    )
    message_body = 'Use this link to log in\n\n:{url}'.format(url=url)
    send_mail(
        'Your login link for SuperLists',
        message_body,
        'noreply@superlists.com',
        [email],
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')
