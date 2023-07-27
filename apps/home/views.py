# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import os
import json

@login_required(login_url="/login/")
def index(request):
    # Chemin absolu vers le fichier JSON
    json_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/json/pays.json'))

    with open(json_file_path, 'r') as json_file:
        continentsData = json.load(json_file)

    # Faites passer les données JSON à votre modèle de rendu ou à votre modèle de contexte
    return render(request, 'home/index.html', {'continentsData': continentsData})


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
