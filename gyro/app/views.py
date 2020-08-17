# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django.views import generic, View
from rest_framework import viewsets
from .api.serializers import StudySerializer
from .models import Study, Recon


@login_required(login_url="/login/")
def index(request):
    list_studies = Study.objects.all()
    list_recent_recons = Recon.objects.filter(created_by=request.user).order_by('-created_at')[:5]
    context = {
        'study_list' : list_studies,
        'user_recon_list' : list_recent_recons,
    }
    return render(request, "index.html", context=context)

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        template = loader.get_template('pages/' + load_template)
        return HttpResponse(template.render(context, request))

    except:

        template = loader.get_template( 'pages/error-404.html' )
        return HttpResponse(template.render(context, request))


