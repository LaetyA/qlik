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
from .models import Comment
from django.http import JsonResponse


@login_required(login_url="/login/")
def index(request):
    # Chemin absolu vers le fichier JSON
    json_file_path = os.path.abspath(os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'static/json/pays.json'))

    with open(json_file_path, 'r') as json_file:
        continentsData = json.load(json_file)

    # Obtenez l'utilisateur connecté
    user = request.user  # Utilisateur connecté

    context = {'continentsData': continentsData, 'user': user}
    # Vous pouvez ajouter des filtres ici si nécessaire
    comments = Comment.objects.all()
    context['comments'] = comments

    if request.method == 'POST' and request.is_ajax():
        # Assurez-vous que l'utilisateur est connecté
        if request.user.is_authenticated:
            # Récupérez le texte du commentaire depuis la requête POST
            text = request.POST.get('text')

            # Créez un nouveau commentaire en utilisant l'utilisateur connecté
            comment = Comment.objects.create(user=user, text=text)

            # Renvoyez une réponse JSON indiquant le succès
            return JsonResponse({
                'message': 'Comment added successfully!',
                'comment_user': {
                    'username': comment.user.username,
                    'first_name': comment.user.first_name,
                    'last_name': comment.user.last_name,
                }
            })
        else:
            # L'utilisateur n'est pas authentifié
            return JsonResponse({'message': 'User not authenticated.'}, status=401)

    elif request.method == 'POST':
        # Gérer la soumission non-AJAX (si nécessaire)
        # Vous pouvez rediriger ici après avoir ajouté le commentaire
        # par exemple: return redirect('home')

        # Sinon, renvoyer une réponse appropriée
        return JsonResponse({'message': 'Invalid request method.'}, status=400)
    else:
        # Renvoyer la page normale en cas de requête GET
        return render(request, 'home/index.html', context)


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


def comments(request):
    subscribers = Subscriber.objects.all()
    comments = Comment.objects.order_by('-date')
    context = {'subscribers': subscribers, 'comments': comments}
    return render(request, 'index.html', context)


def add_comment(request):
    if request.method == 'POST':
        suscriber_id = request.POST.get('suscriber_id')
        post = request.POST.get('post')
        suscriber = Subscriber.objects.get(id=suscriber_id)
        comment = Comment.objects.create(suscriber=suscriber, post=post)

        # Renvoyer une réponse JSON indiquant le succès
        return JsonResponse({'message': 'Comment added successfully!', 'comment_id': comment.id})
    else:
        # Renvoyer une réponse JSON en cas de requête invalide
        return JsonResponse({'message': 'Invalid request method.'}, status=400)
