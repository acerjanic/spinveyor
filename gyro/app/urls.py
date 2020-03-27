# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from rest_framework import routers
from django.conf.urls import url
from django.urls import path, re_path, include
from app import views
from app.api import views as apiviews


router = routers.SimpleRouter()
router.register(r'studies', apiviews.StudyViewSet)
router.register(r'reconprotocols', apiviews.ReconProtocolViewSet)
router.register(r'recons', apiviews.ReconViewSet)


urlpatterns = [
    # Matches any html file - to be used for generalia
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    path('', views.index, name='home'),

    # Add endpoint for API
    url(r'^api/', include((router.urls, 'api'))),
]
