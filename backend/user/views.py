import base64

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
#from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import int_to_base36, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from allauth.account.forms import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import IntegrityError

from .serializers import *
#from .models import User#, PasswordRecovery
from tools import validate_username


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        if 'username' in request.data:
            username = request.data['username']
            username = validate_username(username)
            request.data['username'] = username

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
         
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class UsernameCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.query_params.get('username', None)

        if username is None:
            return Response({"error": "Username parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        username = validate_username(username)

        user_exists = User.objects.filter(username=username).exists()
        return Response({"exists": user_exists}, status=status.HTTP_200_OK)

class UsernameChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UsernameChangeSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']

            username = validate_username(username)

            request.user.username = username
            request.user.save()
            return Response({"detail": "Username updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        username = validate_username(username)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        else:
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class PasswordRecoveryRequest(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        email = request.query_params.get('email', None)

        if email is None:
            return Response({"error": "Email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(email=email).exists():
            return Response({"error": "User with this email wasn't found."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=email)
        uid = int_to_base36(user.pk)
        token = default_token_generator.make_token(user)

        self.__send_password_reset_email(user, uid, token)
        #PasswordRecovery.objects.create(uid=uid, token=token, username=user.username)
        return Response({"info": "sent"}, status=status.HTTP_200_OK)

    def __send_password_reset_email(self, user, uid, token):
        subject = "Password Reset Request"
        html_message = render_to_string('registration/password_reset_email.html', {'user': user, 'uid': uid, 'token': token})
        plain_message = strip_tags(html_message)
        from_email = "daniildiveev@yandex.ru"
        to = user.email

        send_mail(subject, plain_message, from_email, [to], html_message=html_message)

