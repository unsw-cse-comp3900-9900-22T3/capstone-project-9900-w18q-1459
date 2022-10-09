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
]
