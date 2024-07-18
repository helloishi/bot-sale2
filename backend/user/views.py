from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.db import IntegrityError

from .serializers import *
from .models import User
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

class MobilePhoneChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = MobilePhoneChangeSerializer(data=request.data)
        if serializer.is_valid():
            request.user.mobile_phone = serializer.validated_data['mobile_phone']
            request.user.save()
            return Response({"detail": "Mobile phone updated successfully"}, status=status.HTTP_200_OK)
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
