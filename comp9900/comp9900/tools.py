from .models import Charity, Sponsor, Event, Needs, SponsorScore, CharityScore, SponsorEvent


def get_charity_sponsor(email):
    charity = Charity.objects.filter(email=email)
    sponsors = {}
    events = Event.objects.filter(Charity=charity)
    if charity and events:
        for e in events:
            for s in e.Sponsor:
                if s.sponsor_name not in sponsors.keys():
                    sponsors[s.email] = 0
                obj = SponsorEvent.objects.filter(sponsor=s, event=e)
                if obj:
                    sponsors[s.email] += obj[0].money
    return sponsors


def get_charity_needs(email):
    charity = Charity.objects.filter(email=email)
    needs = charity[0].needs.all()
    data = []
    if needs:
        for n in needs:
            data.append(n.needs_name)
    return data


def get_sponsor_help(email):
    sponsor = Sponsor.objects.filter(email=email)
    helps = sponsor[0].help.all()
    data = []
    if helps:
        for n in helps:
            data.append(n.needs_name)
    return data


def get_recommand_sponsor_withconnections(email):
    sponsor = get_charity_sponsor(email)
    needs = get_charity_needs(email)
    recommand_sponsors = []
    sponsor_all = Sponsor.objects.all()
    if sponsor_all:
        for s in sponsor_all:
            if s.email in sponsor.keys():
                helps = get_sponsor_help(s.email)
                if set(helps).intersection(set(needs)):
                    recommand_sponsors.append(s.email)
    return recommand_sponsors


def get_recommand_sponsor_withoutconnections(email):
    sponsor = get_charity_sponsor(email)
    needs = get_charity_needs(email)
    recommand_sponsors = []
    sponsor_all = Sponsor.objects.all()
    if sponsor_all:
        for s in sponsor_all:
            if s.email not in sponsor.keys():
                helps = get_sponsor_help(s.email)
                if set(helps).intersection(set(needs)):
                    recommand_sponsors.append(s.email)
    return recommand_sponsors


def get_recommand_sponsor(email):
    sponsor = get_charity_sponsor(email)
    needs = get_charity_needs(email)
    recommand_sponsors = []
    sponsor_all = Sponsor.objects.all()
    if sponsor_all:
        for s in sponsor_all:
            helps = get_sponsor_help(s.email)
            if set(helps).intersection(set(needs)):
                recommand_sponsors.append(s.email)
    return recommand_sponsors
