from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from QnA.models import User

# Create your views here.

class UserAPI(APIView):

	def get(self, request):
		data = []
		userdata = User.objects.all()
		for user in userdata:
			data.append(user.serialize())
		return Response("users": data, 200)
