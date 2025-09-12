from http.client import responses
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate
from .serializers import UserSerialization
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User

# Create your views here.

class UserRegistrationView(GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({
                "status":"failed",
                "message":"Email already exists!"
            }, status=status.HTTP_400_BAD_REQUEST)
        obj = UserSerialization(data=request.data)
        if obj.is_valid():
            obj.save()
            return Response({
                "status":"succees",
                "message":"User registered successfully!",
                "data":obj.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status":"failed",
            "message":"User registration failed!",
            "error":obj.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(GenericAPIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request, email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            response = Response({
                "status":"success",
                "message":"user logged in successfully!",
                "access_token":access_token
            }, status=status.HTTP_200_OK)

            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                max_age=86400,  # 1 day  #the number of seconds until the cookie expires
                secure=True,  # the cookie will only be sent over HTTPS connections
                httponly=True,
                samesite='Lax'
            )
            return response

        return Response({
            "status":"failed",
            "message":"Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)

class UserView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        user_obj = UserSerialization(user)
        return Response({
             "status":"success",
             "message":"User data fetched!",
             "data":user_obj.data
        }, status=status.HTTP_200_OK)


    def put(self, request):
        user = request.user
        user_obj = UserSerialization(instance=user, data=request.data, partial=True)
        if user_obj.is_valid():
            user_obj.save()
            return Response({
                "status":"success",
                "message":"User data updated!",
                "data":user_obj.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status":"failed",
            "message":"User data updation failed!",
            "errors":user_obj.errors
        }, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        user = request.user
        if user:
            user.delete()
            return Response({
                "status":"success",
                "message":"User data deleted!",
            }, status=status.HTTP_200_OK)
        return Response({
            "status":"failed",
            "message":"No user data found to delete!",
        }, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        x = Response()
        x.delete_cookie('refresh')
        x.delete_cookie('access')
        x.data={
            "message":"User logout successfully!"
        }
        return x


