from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer, LoanSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from .models import UserAccount

# Create your views here.


# Getting User Details API
class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        user_account = get_object_or_404(UserAccount, user=user)
        serializer = UserSerializer(user)
        user_data = serializer.data
        user_data['user_type'] = user_account.user_type
        user_data['is_blocked'] = user_account.is_blocked
        return Response(user_data)


# Registering the User
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# Create User Loan
class CreateLoanAPIView(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = LoanSerializer
