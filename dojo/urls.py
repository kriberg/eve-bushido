"""dojo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from dojo.main.views import LoginView, CapsulerView, LogoutView, LocationView

urlpatterns = [
    url(r'^dojo/login/', LoginView.as_view(), name='main_login'),
    url(r'^dojo/logout/', LogoutView.as_view(), name='main_logout'),
    url(r'^dojo/capsuler/', CapsulerView.as_view(), name='main_capsuler'),
    url(r'^dojo/location/', LocationView.as_view(), name='main_location'),
    url(r'^dojo/admin/', include(admin.site.urls)),
]
