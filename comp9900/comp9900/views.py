from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
import models


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    charity = serializers.BooleanField()
    sponsor = serializers.BooleanField()


def login(GenericAPIView):
    def post(self, request):
        login_data = LoginSerializer(data=request.data)
        if login_data.charity:


