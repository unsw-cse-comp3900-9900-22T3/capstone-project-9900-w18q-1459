import email

from django.http import HttpResponse
from rest_framework import serializers, generics
from rest_framework.views import APIView
from . import models
from rest_framework.response import Response
from rest_framework import serializers
from .models import Charity, Sponsor, Event, Needs
from django.db.models import Q


class CharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = ('charity_name', 'email', 'description')


class CreateEventSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    description = serializers.CharField(max_length=65535, required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)


class SponsorEventSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    event_id = serializers.IntegerField(required=True)



class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ('sponsor_name', 'email', 'description', 'website_link')


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


class ChooseNeedsSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    needs = serializers.CharField(required=True, max_length=255)


class ChooseHelpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    help = serializers.CharField(required=True, max_length=255)


class CreateNeedsSerializer(serializers.Serializer):
    needs = serializers.CharField(required=True, max_length=255)


class ShowCharityNeedsSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)


class LoginView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Login interface
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
                    'description': charity[0].description,
                    'email': charity[0].email
                }
                print(detail, type(detail))
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
                    'website_link': sponsor[0].website_link
                }
                print(detail, type(detail))
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
        Register interface
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
            if sponsor:
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


class ShowneedsView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """
        show exists needs list
        """
        needs_lsit = Needs.objects.all()[:20]
        data = []
        for n in needs_lsit:
            data.append(n.needs_name)
        return Response(data={'needs top 20': data})


class CreateneedsView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CreateNeedsSerializer

    def post(self, request):
        """
        create needs which hasn't been created
        :param request: needs name
        :return: if succeed
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        needs_name = (serializer.data)
        needs = Needs.objects.filter(needs_name=needs_name['needs'])
        if needs:
            return Response({"message": 'has exists'})
        print(needs_name['needs'])
        Needs.objects.create(needs_name=needs_name['needs'])
        return Response(data={'message': 'has added', 'data': needs_name['needs']})


class AddneedsView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ChooseNeedsSerializer

    def post(self, request):
        """
        Add needs into a charity
        :param request: needs name
        :return: if succeed
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        charity_needs = (serializer.data)
        charity = Charity.objects.filter(email=charity_needs['email'])
        if not charity:
            return Response({"message": 'charity does not exist'})
        n_charity = charity[0].needs.filter(needs_name=charity_needs['needs'])
        if n_charity:
            return Response({"message": 'needs has exists'})
        n_charity = Needs.objects.filter(needs_name=charity_needs['needs'])
        if not n_charity:
            return Response({"message": 'please create needs firstly'})
        charity[0].needs.add(n_charity[0])
        return Response({"message": 'has added'})


class ShowCharityNeedsView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ShowCharityNeedsSerializer

    def post(self, request):
        """
        Show the needs list of a charity
        :param request: charity email
        :return: its needs list
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        charity_needs = (serializer.data)
        charity = Charity.objects.filter(email=charity_needs['email'])
        if not charity:
            return Response({"message": 'charity does not exist'})
        n_charity = charity[0].needs.all()
        data = []
        if n_charity:
            for n in n_charity:
                data.append(n.needs_name)
        return Response({"needs_list": data})


class AddhelpView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ChooseHelpSerializer

    def post(self, request):
        """
        Add help into a sponsor
        :param request: needs name
        :return: if succeed
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        sponsor_needs = (serializer.data)
        sponsor = Sponsor.objects.filter(email=sponsor_needs['email'])
        if not sponsor:
            return Response({"message": 'sponsor does not exist'})
        n_sponsor = sponsor[0].help.filter(needs_name=sponsor_needs['help'])
        if n_sponsor:
            return Response({"message": 'help has exists'})
        n_sponsor = Needs.objects.filter(needs_name=sponsor_needs['help'])
        if not n_sponsor:
            return Response({"message": 'There is no such needs to help'})
        sponsor[0].help.add(n_sponsor[0])
        return Response({"message": 'has added'})


class ShowsponsorhelpView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ShowCharityNeedsSerializer

    def post(self, request):
        """
        Show the help list of a sponsor
        :param request: charity email
        :return: its help list
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        sponsor_needs = (serializer.data)
        sponsor = Sponsor.objects.filter(email=sponsor_needs['email'])
        if not sponsor:
            return Response({"message": 'sponsor does not exist'})
        help = sponsor[0].help.all()
        data = []
        if help:
            for n in help:
                print(n)
                data.append(n.needs_name)
        return Response({"help_list": data})


class UpdateSponsorView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = SponsorSerializer

    def post(self, request):
        """
        update sponsor some details
        :return: success
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        sponsor = (serializer.data)
        Sponsor.objects.filter(email=sponsor['email']).update(
            sponsor_name=sponsor['sponsor_name'],
            description=sponsor['description'],
            websitelink=sponsor['websitelink']
        )
        return Response({"message": "success"})


class UpdateCharityView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CharitySerializer

    def post(self, request):
        """
        update sponsor some details
        :return: success
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        charity = (serializer.data)
        Charity.objects.filter(email=charity['email']).update(
            sponsor_name=charity['sponsor_name'],
            description=charity['description']
        )
        return Response({"message": "success"})


class CreateEventView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CreateEventSerializer

    def post(self, request):
        """
        :param request: create event by charity
        :return:success
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        event = (serializer.data)
        charity = Charity.objects.filter(email=event['email'])
        if not charity:
            return Response({"message": 'charity does not exist'})
        charity = charity[0]
        Event.objects.create(
            description=event['description'],
            start_date=event['start_date'],
            end_date=event['end_date'],
            Charity=charity
        )
        return Response({"message": "success"})


class ShowEventbyC(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ShowCharityNeedsSerializer

    def post(self, request):
        """
        :param request: show the events of a charity
        :return: a list of events
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        charity = (serializer.data)
        charity = Charity.objects.filter(email=charity['email'])
        if not charity:
            return Response({"message": 'charity does not exist'})
        charity = charity[0]
        events = Event.objects.filter(Charity=charity)
        data = []
        if events:
            for n in events:
                data.append(
                    {'description': n.description, 'start_data': n.start_date, 'end_date': n.end_date, 'pk': n.id})
        return Response({"events_list": data})


class SponsorEvent(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = SponsorEventSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        data = (serializer.data)
        sponsor = Sponsor.objects.filter(email=data['email'])
        if not sponsor:
            return Response({"message": 'sponsor does not exist'})
        sponsor = sponsor[0]
        event = Event.objects.get(id=data['event_id'])
        if not event:
            return Response({"message": 'There is no such event to sponsor'})
        event.Sponsor.add(sponsor)  # I have not take time into consideration
        return Response({"message": 'has sponsored'})
