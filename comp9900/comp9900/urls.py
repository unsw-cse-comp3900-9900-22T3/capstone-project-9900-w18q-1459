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
from django.urls import include, re_path
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
]
