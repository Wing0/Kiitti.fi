from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import User
import json

# Create your views here...

class UserAPI(APIView):

    def get(self, request):
        data = []
        userdata = User.objects.all()
        for user in userdata:
            data.append(user.serialize())
        return Response({"users": data}, 200)

    #VALIDATE
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        user_id = data['user_id']
        reputation = data['reputation']
        user = User()
        user.username = username
        user.user_id = user_id
        user.reputation = reputation
        user.save()
        return Response(200)
