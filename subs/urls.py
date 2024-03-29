"""subs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib.auth.views import logout
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   url(r'^$', views.index, name='index'),
   url(r'^upload/?', views.upload, name='upload'),
   url(r'^save_all/?', views.all_down, name='all_down'),
   url(r'^save_new/?', views.new_down, name='new_down'),
   url(r'^save/?', views.down, name='down'),
   url(r'^login/?$', auth_views.login, name='login'), 
   url(r'^register/?$', views.register, name='register'),
   url(r'^logout/?$', logout, name='logout'),
   url(r'^.*$', views.fourohfour, name='404'),


]
