"""comp9900 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path
from django.contrib import admin
from . import views
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path('docs/', include_docs_urls(title='API interface document',
                                       authentication_classes=[],
                                       permission_classes=[])),
    re_path(r'^login/', views.LoginView.as_view(), name='login'),
    re_path(r'^register/', views.RegisterView.as_view(), name='register'),
    re_path(r'^create_needs/', views.CreateneedsView.as_view(), name='create needs'),
    re_path(r'^add_needs_to_c/', views.AddneedsView.as_view(), name='add needs to a charity'),
    re_path(r'^show_20_needs/', views.ShowneedsView.as_view(), name='show top20 needs'),
    re_path(r'^show_charity_needs/', views.ShowCharityNeedsView.as_view(), name='show charity needs'),
    re_path(r'^show_sponsor_help/', views.ShowsponsorhelpView.as_view(), name='show sponsor help list'),
    re_path(r'^add_help_to_s/', views.AddhelpView.as_view(), name='add help to a sponsor'),
    re_path(r'^update_sponsor/', views.UpdateSponsorView.as_view(), name='update sponsor'),
    re_path(r'^update_charity/', views.UpdateCharityView.as_view(), name='update charity'),
    re_path(r'^create_event/', views.CreateEventView.as_view(), name='create event'),
    re_path(r'^show_event/', views.ShowEventbyC.as_view(), name='show events of a charity'),
    re_path(r'^sponsor_event/', views.SponsorEvent.as_view(), name='sponsor event'),
    re_path(r'^delete_needs/', views.DeleteneedsView.as_view(), name='delete needs'),
    re_path(r'^follow_c/', views.FollowView.as_view(), name='follow charity'),
    re_path(r'^unfollow_c/', views.UnfollowView.as_view(), name='unfollow charity'),
    re_path(r'^showfollow_c/', views.ShowfollowView.as_view(), name='show follow charity'),
    re_path(r'^show_c/', views.ShowCharityView.as_view(), name='show charity details'),
    re_path(r'^show_s/', views.ShowSponsorView.as_view(), name='show sponsor details'),
    re_path(r'^update_event/', views.UpdateEvent.as_view(), name='update event'),
    re_path(r'^rate_event/', views.RatingEvent.as_view(), name='rate c by s or rate s by c'),
    re_path(r'^add_tag_event/', views.AddtagsView.as_view(), name='add tag to a event'),
    re_path(r'^show_event/', views.ShowEvent.as_view(), name='show a event'),
    re_path(r'^show_event_s/', views.ShowEventbyS.as_view(), name='show sponsors events'),
    re_path(r'^del_needs/', views.Deleteneeds_cView.as_view(), name='delete needs of a c'),
    re_path(r'^del_help/', views.DeletehelpView.as_view(), name='del help of a sponsor'),
    re_path(r'^recommandations/', views.Recommandations.as_view(), name='recommand to a charity'),
    re_path(r'^search_event/', views.SearchEvent.as_view(), name='search event'),
    re_path(r'^Top_sponsor/', views.Topsponsors.as_view(), name='get top sponsor of a charity'),
]
