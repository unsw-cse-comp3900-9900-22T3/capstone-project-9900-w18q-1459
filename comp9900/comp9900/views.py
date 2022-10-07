import email

from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from . import models
from rest_framework.response import Response


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    charity = serializers.BooleanField()
    sponsor = serializers.BooleanField()

class RegisterSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    charity = serializers.BooleanField()
    sponsor = serializers.BooleanField()


def login(GenericAPIView):
    def post(self, request):
        login_data = LoginSerializer(data=request.data)
        if login_data.charity and not login_data.sponsor:
            charity = models.Charity.objects.get(email=email)
            if not charity:
                return Response(data={'message': 'The email does not exists'})
            elif charity.password == login_data.password:
                return Response(data={'message': 'success'})
            else:
                return Response(data={'message': 'Wrong password or email'})
        elif login_data.sponsor and not login_data.charity:
            sponsor = models.Sponsor.objects.get(email=email)
            if not sponsor:
                return Response(data={'message': 'The email does not exists'})
            elif sponsor.password == login_data.password:
                return Response(data={'message': 'success'})
            else:
                return Response(data={'message': 'Wrong password or email'})
        else:
            return Response(data={'message': 'You should be a charity or a sponsor'})

# def register(GenericAPIView):


