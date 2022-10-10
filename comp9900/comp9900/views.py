import email

from django.http import HttpResponse
from rest_framework import serializers, generics
from rest_framework.views import APIView
from . import models
from rest_framework.response import Response
from rest_framework import serializers
from .models import Charity, Sponsor, Event
from django.db.models import Q


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=255)
    charity = serializers.BooleanField()
    sponsor = serializers.BooleanField()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=255)
    confirm_password = serializers.CharField(required=True, max_length=255)
    name = serializers.CharField(required=True, max_length=255)
    description = serializers.CharField(max_length=65535, required=True)
    charity = serializers.BooleanField()
    sponsor = serializers.BooleanField()


class LoginView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        """
        登录接口
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        login_data = serializer.data
        if login_data['charity'] and not login_data['sponsor']:
            charity = Charity.objects.filter(email=login_data['email'])
            if not charity:
                return Response(data={'message': 'The email does not exists'})
            elif charity[0].password == login_data['password']:
                detail = {
                    'name': charity[0].charity_name,
                    'needs': charity[0].needs,
                    'description': charity[0].description,
                    'email': charity[0].email
                }
                return Response(data={'message': 'success', 'detail': detail})
            else:
                return Response(data={'message': 'Wrong password or email'})
        elif login_data['sponsor'] and not login_data['charity']:
            sponsor = Sponsor.objects.filter(email=login_data['email'])
            if not sponsor:
                return Response(data={'message': 'The email does not exists'})
            elif sponsor[0].password == login_data['password']:
                detail = {
                    'name': sponsor[0].sponsor_name,
                    'description': sponsor[0].description,
                    'email': sponsor[0].email,
                    'follow': sponsor[0].follows,
                }
                return Response(data={'message': 'success', 'detail': detail})
            else:
                return Response(data={'message': 'Wrong password or email'})
        else:
            return Response(data={'message': 'You should be a charity or a sponsor'})


class RegisterView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterSerializer

    def post(self, request):
        """
        注册接口
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        register_data = (serializer.data)
        if register_data['charity'] and not register_data['sponsor']:
            charity = Charity.objects.filter(Q(email=register_data['email']) | Q(charity_name=register_data['name']))
            if charity:
                return Response(data={'message': 'The email or name has exists'})
            elif register_data['password'] != register_data['confirm_password']:
                return Response(data={'message': 'The password is different from your confirm password'})
            else:
                Charity.objects.create(
                    charity_name=register_data['name'],
                    email=register_data['email'],
                    description=register_data['description'],
                    password=register_data['password']
                )
                return Response(data={'message': 'Successful register'})
        elif register_data['sponsor'] and not register_data['charity']:
            sponsor = Sponsor.objects.filter(Q(email=register_data['email']) | Q(sponsor_name=register_data['name']))
            if not sponsor:
                return Response(data={'message': 'The email or name has exists'})
            elif register_data['password'] != register_data['confirm_password']:
                return Response(data={'message': 'The password is different from your confirm password'})
            else:
                Sponsor.objects.create(
                    sponsor_name=register_data['name'],
                    email=register_data['email'],
                    description=register_data['description'],
                    password=register_data['password']
                )
                return Response(data={'message': 'Successful register'})
        else:
            return Response(data={'message': 'You should be a charity or a sponsor'})
