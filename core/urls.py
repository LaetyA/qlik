# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, re_path
from django.urls import path, include  # add this
from apps.home import views

urlpatterns = [

     path('admin/', admin.site.urls),
    path("", include("apps.authentication.urls")),

    # The home page
    path('', views.index, name='home'),
    path('fetch_event_data/', views.fetch_event_data, name='fetch_event_data'),  
    path('fetch_event_period/', views.fetch_event_period, name='fetch_event_period'),
    path('fetch_event_type/', views.fetch_event_type, name='fetch_event_type'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]


