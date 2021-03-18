from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from .serializers import UserSerializer, LoginSerializer,AllUsers
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib import auth
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativLink+"?token="+str(token)
        email_body = 'Hi ' + user.username + ' use link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email ,'email_subject': 'Verify your email'}
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token=request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({'email': 'Successffuly activated!'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user:

            payload = {
                "username": user.username,
            }
            key = settings.JWT_SECRET_KEY

            auth_token = jwt.encode(payload, key, algorithms='HS256')
            serializer = UserSerializer(user)
            data = {'user': serializer.data, 'token': auth_token}
            return Response(data, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
