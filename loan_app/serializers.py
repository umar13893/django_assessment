from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import (
    UserAccount,
    Loan
)
from django.shortcuts import get_object_or_404
import datetime


class UserSerializer(serializers.ModelSerializer):

    # Serializer to Get User Details using Django Token Authentication
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username"]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = ('amount', 'due_date', )
        extra_kwargs = {
            'amount': {'required': True},
        }

    def validate(self, attrs):
        if attrs['amount'] % 500 != 0:
            raise serializers.ValidationError({"amount": "Loan's amount should be multiple of 500"})
        return attrs

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            user = request.user
            user_account = get_object_or_404(UserAccount, user=user)
            # Checking if current user creating multiple loan requests in single day
            is_loan_request_single_day = Loan.objects.filter(created_at__date=datetime.datetime.now()).exists()
            if is_loan_request_single_day:
                raise serializers.ValidationError({"error": "You cannot create multiple loan requests in a single day"})
            else:
                pass
            # End
            # Checking previous loan request open or in progress
            is_loan_request_open = Loan.objects.filter(user_account=user_account, status='PENDING').exists()
            if is_loan_request_open:
                raise serializers.ValidationError({"error": "You already have your previous loan request in pending/progress"})
            else:
                pass
            # END
            loan_obj = Loan()
            loan_obj.user_account = user_account
            loan_obj.amount = validated_data['amount']
            loan_obj.save()
            return loan_obj
        else:
            pass
