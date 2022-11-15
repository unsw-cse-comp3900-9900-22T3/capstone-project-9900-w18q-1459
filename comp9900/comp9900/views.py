import datetime
import email

from django.http import HttpResponse
from rest_framework import serializers, generics
from rest_framework.views import APIView
from . import models
from rest_framework.response import Response
from rest_framework import serializers
from .models import Charity, Sponsor, Event, Needs, SponsorScore, CharityScore
from django.db.models import Q
from django.forms.models import model_to_dict
from .tools import *


class CharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = ('charity_name', 'email', 'description')


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ('sponsor_name', 'email', 'description', 'website_link')


class EventSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    description = serializers.CharField(required=True, max_length=65535)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    location = serializers.CharField(required=True)
    target_f = serializers.IntegerField(required=True)
    title = serializers.CharField(required=True)


class RatingSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    rating = serializers.IntegerField(required=True)
    type = serializers.CharField(required=True)


class SearchEventSerializer(serializers.Serializer):
    keyword = serializers.CharField(required=True)


class SponsorEventSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    title = serializers.CharField(required=True, max_length=65535)
    money = serializers.IntegerField(required=True)


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


class ChooseTagSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    needs = serializers.CharField(required=True, max_length=255)


class ChooseHelpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    help = serializers.CharField(required=True, max_length=255)


class FollowSerializer(serializers.Serializer):
    sponsor_email = serializers.EmailField(required=True)
    charity_email = serializers.EmailField(required=True)


class CreateNeedsSerializer(serializers.Serializer):
    needs = serializers.CharField(required=True, max_length=255)


class ShowCharityNeedsSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)


class SearcheventSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    title = serializers.CharField(required=True, max_length=65535)


class RecommandSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    type = serializers.IntegerField(required=True)


class TopsponsorSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ShowEventSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)


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


class DeleteneedsView(generics.GenericAPIView):
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
        Needs.objects.filter(needs_name=needs_name['needs']).delete()
        return Response(data={'message': 'has deleted', 'data': needs_name['needs']})


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


class Deleteneeds_cView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ChooseNeedsSerializer

    def post(self, request):
        """
        Delete needs of a charity
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
        n_charity = Needs.objects.filter(needs_name=charity_needs['needs'])
        if n_charity:
            charity[0].needs.remove(n_charity[0])
        return Response({"message": 'has deleted'})


class AddtagsView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ChooseTagSerializer

    def post(self, request):
        """
        Add tags into a event
        :param request: needs name
        :return: if succeed
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        event_tag = (serializer.data)
        event = Event.objects.filter(title=event_tag['title'])
        if not event:
            return Response({"message": 'event does not exist'})
        tags = event[0].Tags.filter(needs_name=event_tag['needs'])
        if tags:
            return Response({"message": 'needs has exists'})
        tag = Needs.objects.filter(needs_name=event_tag['needs'])
        if not tag:
            return Response({"message": 'please create tag firstly'})
        event[0].Tags.add(tag[0])
        return Response({"message": 'has added'})


class DeletetagsView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ChooseTagSerializer

    def post(self, request):
        """
        Delete tags of a event
        :param request: needs name
        :return: if succeed
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        event_tag = (serializer.data)
        event = Event.objects.filter(title=event_tag['title'])
        if not event:
            return Response({"message": 'event does not exist'})
        tags = event[0].Tags.filter(needs_name=event_tag['needs'])
        if tags:
            event[0].Tags.remove(tags[0])
        return Response({"message": 'has deleted'})


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


class DeletehelpView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ChooseHelpSerializer

    def post(self, request):
        """
        Delete help of a sponsor
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
            sponsor[0].help.remove(n_sponsor[0])
        return Response({"message": 'has deleted'})


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


class FollowView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = FollowSerializer

    def post(self, request):
        """
        Add help into a sponsor
        :param request: needs name
        :return: if succeed
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        data = (serializer.data)
        sponsor = Sponsor.objects.filter(email=data['sponsor_email'])
        charity = Charity.objects.filter(email=data['charity_email'])
        if not sponsor:
            return Response({"message": 'sponsor does not exist'})
        if not charity:
            return Response({"message": 'charity does not exist'})
        charities = sponsor[0].follows.all()
        if charities and charity in charities:
            return Response({"message": 'has followed'})
        sponsor[0].follows.add(charity)
        return Response({"message": 'has added'})


class UnfollowView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = FollowSerializer

    def post(self, request):
        """
        Add help into a sponsor
        :param request: needs name
        :return: if succeed
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        data = (serializer.data)
        sponsor = Sponsor.objects.filter(email=data['sponsor_email'])
        charity = Sponsor.objects.filter(email=data['charity_email'])
        if not sponsor:
            return Response({"message": 'sponsor does not exist'})
        if not charity:
            return Response({"message": 'charity does not exist'})
        sponsor[0].follows.remove(charity)
        return Response({"message": 'has added'})


class ShowfollowView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ShowCharityNeedsSerializer

    def post(self, request):
        """
        Add help into a sponsor
        :param request: needs name
        :return: if succeed
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        data = (serializer.data)
        sponsor = Sponsor.objects.filter(email=data['email'])
        if not sponsor:
            return Response({"message": 'sponsor does not exist'})
        charity = sponsor[0].follows.all()
        data = []
        if charity:
            for n in charity:
                data.append({'email': charity.email, 'name': charity.charity_name})
        return Response({"follow_list": data})


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
            pass
        sponsor = (serializer.data)
        Sponsor.objects.filter(email=sponsor['email']).update(**sponsor)
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
            pass
        charity = (serializer.data)
        Charity.objects.filter(email=charity['email']).update(**charity)
        return Response({"message": "success"})


class ShowCharityView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ShowCharityNeedsSerializer

    def post(self, request):
        """
        update sponsor some details
        :return: success
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        charity = (serializer.data)
        data = Charity.objects.filter(email=charity['email']).values('charity_name', 'email', 'description')
        return Response({"type": 'charity', 'data': data[0]})


class ShowSponsorView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ShowCharityNeedsSerializer

    def post(self, request):
        """
        update sponsor some details
        :return: success
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        sponsor = (serializer.data)
        data = Sponsor.objects.filter(email=sponsor['email']).values('sponsor_name', 'email', 'description',
                                                                     'website_link')
        return Response({"type": 'sponsor', 'data': data[0]})


class CreateEventView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = EventSerializer

    def post(self, request):
        """
        :param request: create event by charity
        :return:success
        """
        print('a')
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        event = (serializer.data)
        print(event)
        charity = Charity.objects.filter(email=event['email'])
        if not charity:
            return Response({"message": 'charity does not exist'})
        charity = charity[0]
        event.pop('email')
        Event.objects.create(Charity=charity, **event)
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
                n = model_to_dict(n)
                for i in range(len(n['Tags'])):
                    n['Tags'][i] = model_to_dict(n['Tags'][i])
                for i in range(len(n['Sponsor'])):
                    n['Sponsor'][i] = n['Sponsor'][i].email
                n.pop('Charity')
                print(n)
                data.append(n)
        return Response({"events_list": data})


class ShowEventbyS(generics.GenericAPIView):
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
        sponsor = (serializer.data)
        sponsor = Sponsor.objects.filter(email=sponsor['email'])
        if not sponsor:
            return Response({"message": 'charity does not exist'})
        sponsor = sponsor[0]
        events = Event.objects.all()
        data = []
        if events:
            for n in events:
                n = model_to_dict(n)
                if sponsor in n['Sponsor']:
                    for i in range(len(n['Tags'])):
                        n['Tags'][i] = model_to_dict(n['Tags'][i])
                    for i in range(len(n['Sponsor'])):
                        n['Sponsor'][i] = n['Sponsor'][i].email
                    n['Charity'] = Charity.objects.filter(pk=n['Charity'])[0].email
                    print(n)
                    data.append(n)
        return Response({"events_list": data})


class ShowEvent(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ShowEventSerializer

    def post(self, request):
        """
        :param request: show the events of a charity
        :return: a list of events
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        title = (serializer.data)['title']
        print(title)
        event = Event.objects.filter(title=title)
        if event:
            event = model_to_dict(event[0])
            for i in range(len(event['Tags'])):
                event['Tags'][i] = model_to_dict(event['Tags'][i])
            for i in range(len(event['Sponsor'])):
                event['Sponsor'][i] = event['Sponsor'][i].email
            event['Charity'] = Charity.objects.filter(pk=event['Charity'])[0].email
            print(event)
        return Response({"events_list": event})


class UpdateEvent(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = EventSerializer

    def post(self, request):
        """
        :param request: show the events of a charity
        :return: a list of events
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            pass
        event = (serializer.data)
        charity = Charity.objects.filter(email=event['email'])
        if not charity:
            return Response({"message": 'charity does not exist'})
        charity = charity[0]
        event.pop('email')
        Event.objects.filter(event['title']).update(**event)
        return Response({"message": 'success'})


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
        event = Event.objects.get(title=data['title'])
        if not event:
            return Response({"message": 'There is no such event to sponsor'})
        event.Sponsor.add(sponsor)  # I have not take time into consideration
        models.SponsorEvent.objects.create(event=event, sponsor=sponsor, money=data['money'])
        return Response({"message": 'has sponsored'})


class RatingEvent(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RatingSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        data = (serializer.data)
        score = data['rating']
        if score not in range(1, 6, 1):
            return Response({"message": 'not accepted score'})
        if data['type'] == 'sponsor':
            obj = Sponsor.objects.filter(email=data['email'])
            if not obj:
                return Response({"message": 'No such one to rate'})
            s = SponsorScore.objects.filter(sponsor=obj[0])
            if s:
                s = s[0]
                s.score = (s.score * s.times + score) / (s.times + 1)
                s.times = s.times + 1
            else:
                models.SponsorScore.objects.create(sponsor=obj[0], score=score, times=1)
            return Response({"message": 'has rated'})
        else:
            obj = Charity.objects.filter(email=data['email'])
            if not obj:
                return Response({"message": 'No such one to rate'})
            s = CharityScore.objects.filter(charity=obj[0])
            if s:
                s = s[0]
                s.score = (s.score * s.times + score) / (s.times + 1)
                s.times = s.times + 1
            else:
                models.CharityScore.objects.create(charity=obj[0], score=score, times=1)
            return Response({"message": 'has rated'})


class SearchEvent(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = SearchEventSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        data = (serializer.data)
        keyword = data['keyword']
        if not keyword:
            return Response({"message": "No keyword"})
        events = Event.objects.filter(
            Q(title__icontains=keyword) | Q(description__icontains=keyword)
        )
        data = []
        if events:
            for n in events:
                n = model_to_dict(n)
                for i in range(len(n['Tags'])):
                    n['Tags'][i] = model_to_dict(n['Tags'][i])
                for i in range(len(n['Sponsor'])):
                    n['Sponsor'][i] = n['Sponsor'][i].email
                n['Charity'] = Charity.objects.filter(pk=n['Charity'])[0].email
                print(n)
                data.append(n)
        return Response({"events_list": data})


class Recommandations(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RecommandSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        data = (serializer.data)
        email = data['email']
        type = data['type']
        if type == 0:
            data = get_recommand_sponsor(email)
        elif type == 1:
            data = get_recommand_sponsor_withconnections(email)
        elif type == 2:
            data = get_recommand_sponsor_withoutconnections(email)
        return Response({"data": data})


class Topsponsors(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = TopsponsorSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": str(serializer.errors), "data": {}})
        data = (serializer.data)
        sponsors = get_charity_sponsor(data['email'])
        sorted_sponsors = sorted(sponsors.items(), key=lambda kv: kv[1][0])
        print(sorted_sponsors)
        return Response({"data": sorted_sponsors[:10]})
