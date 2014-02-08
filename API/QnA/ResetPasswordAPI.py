from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import *
from QnA.view_utils import *
from QnA.utils import *
import json
import re

from view_utils import post_abstract_message, exclude_old_versions

from django.core.mail import send_mail
import hashlib
import random
import string

def send_recovery_email(email, hash):
    try:
        send_mail('Kiitti password recovery', 'Your hash is: %s' % has, 'info@kiitti.fi', [email], fail_silently=False)
        return False
    except:
        return compose_message("Sending email to: %s falied." % email)

def create_hash(user):
    salt = ""
    for i in range(5):
        salt += random.choice(string.letters)

    e = ResetEntry(user=user, salt=salt)
    has = e.create()
    e.save()
    return has


class ResetPasswordAPI(APIView):

    def get(self, request):
        '''
            This method sends password reset email to user.email
        '''
        messages = []
        data = request.GET.get("usernameOrEmail")
        if not data:
            messages.append(compose_message("Please provide username or email address.","usernameOrEmail"))
        else:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", data):
                try:
                    user = User.objects.get(username = data)
                except:
                    messages.append(compose_message("The username did not match any user.","usernameOrEmail"))
            else:
                try:
                    user = User.objects.get(email = data)
                except:
                    messages.append(compose_message("The email did not match any user.","usernameOrEmail"))

        if len(messages) == 0:
            has = create_hash(user)
            output = send_recovery_email(user.email, has)
            if output:
                messages.append(output)
            if len(messages) == 0:
                return Response({"messages":create_message("Sending mail to %s was successful!" % user.email)},200)
            else:
                return Response({"messages":messages}, 500)

        return Response({"messages":messages}, 400)

    def post(self, request):
        '''
            This method resets the password is given hash is valid and password is of correct format
        '''
        data = json.loads(request.body)
        messages = []

        has = data.get("m")
        if not has:
            messages.append(compose_message("You must provide hash in order to reset password.","m"))

        email = data.get("email")
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.append(compose_message("You must provide a valid email address.","email"))

        pw = data.get("password")
        if not has:
            messages.append(compose_message("You must provide password.","password"))

        pwc = data.get("passwordConfirm")
        if not has:
            messages.append(compose_message("You must provide password confirmation.","passwordConfirm"))

        if pw != pwc:
            messages.append(compose_message("The passwords did not match.","password"))

        if len(pw) < 4 or len(pw) > 15:
            messages.append(compose_message("The password must be between 4 and 15 characters.","password"))

        if len(messages) == 0:
            try:
                user = User.objects.get(email=email)
                try:
                    entry = ResetEntry.objects.get(user=user)
                    if entry.is_valid(has):
                        user.set_password(pw)
                        user.save()
                        return Response({"messages":create_message("Password reset was successful!")}, 200)
                except:
                    messages.append(compose_message("You have not requested a password reset.","m"))
            except:
                messages.append(compose_message("Provided email address did not match any user.","email"))

        return Response({"messages":messages}, 400)




