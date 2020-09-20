from django.conf.urls import url,patterns
from django.conf import settings
from django.contrib import admin
from hospital import views
from . import views

urlpatterns = [
    url(r'^/$', views.index, name='index'),
]
