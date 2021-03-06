from django.core import exceptions
from django.db import reset_queries
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
import datetime, jwt

class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        password = request.data["password"]

        if "email" in request.data.keys():
            email = request.data["email"]
            user = User.objects.filter(email=email).first()
        else:
            username = request.data["username"]
            user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed("User Not Found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")

        payload = {
            "id" : user.id,
            "first_name" : user.first_name,
            "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
            "iat" : datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'admin', algorithm='HS256').decode('utf-8')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            "jwt": token
        }
        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Token Expired")
        
        try:
            payload = jwt.decode(token, 'admin', algorithm=['HS256'])
        except:
            raise AuthenticationFailed("Token Expired")
        
        user = User.objects.filter(id=payload["id"]).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {
            "message" : "Success"
        }
        return response