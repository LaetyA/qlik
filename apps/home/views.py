# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import datetime
from dateutil.relativedelta import relativedelta
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import os
import json
from .models import Comment,Donqlick
from django.http import JsonResponse
from django.db import connection


@login_required(login_url="/login/")
def index(request):
    # Chemin absolu vers le fichier JSON
    json_file_path = os.path.abspath(os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'static/json/pays.json'))

    with open(json_file_path, 'r') as json_file:
        continentsData = json.load(json_file)

    # Obtenez l'utilisateur connecté
    user = request.user  # Utilisateur connecté

    doneqlick = Donqlick.objects.all()  # Récupérer les données Qlik

    context = {'continentsData': continentsData, 'user': user, 'segment': 'index', 'doneqlick': doneqlick}



    if request.is_ajax():
        data = [{'event_date': donqlick.event_date, 'notes': donqlick.notes, 'country': donqlick.country, 'type': donqlick.event_type,
                 'main-actor': donqlick.actor1, 'source': donqlick.source, 'fatalities': donqlick.fatalities,'year':donqlick.year,'sub_event_type':donqlick.sub_event_type,'id':donqlick.id} for donqlick in doneqlick]
        return JsonResponse(data, safe=False)


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


def fetch_event_data(request):
    if request.method == 'GET':
        selected_countries = request.GET.getlist('selectedCountries[]')
        # Échappez correctement les noms de pays avec des guillemets simples
        selected_countries_string = ",".join(f"'{country}'" for country in selected_countries)

        sql_query = f"""
            SELECT
                country,
                COUNT(event_id_cnty) AS event_count,
                SUM(fatalities) AS total_fatalities,
                GROUP_CONCAT(DISTINCT year ORDER BY year ASC SEPARATOR ', ') AS years
            FROM donqlick
            WHERE country IN ({selected_countries_string})
            GROUP BY country;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            results = cursor.fetchall()

        data = [
            {
                'country': country,
                'event_count': event_count,
                'total_fatalities': total_fatalities,
                'years': years
            }
            for country, event_count, total_fatalities, years in results
        ]


        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=400)
    
    
def fetch_event_period(request):
    if request.method == 'GET':
        selected_countries = request.GET.getlist('selectedCountries[]')
        selected_countries_string = ",".join(f"'{country}'" for country in selected_countries)

        # Obtenez la date actuelle
        current_date = datetime.datetime.now()

        # Calculez la date il y a 12 mois à partir de la date actuelle
        twelve_months_ago = current_date - relativedelta(months=11)

        month_dates = [twelve_months_ago + relativedelta(months=i) for i in range(12)]

        # Initialisez un dictionnaire pour stocker les données par mois
        data_by_month = {date.strftime('%Y-%m'): 0 for date in month_dates}

        sql_query = f"""
            SELECT DATE_FORMAT(event_date, '%%Y-%%m') AS month, COUNT(event_id_cnty) AS event_count
            FROM donqlick
            WHERE country IN ({selected_countries_string})
            AND event_date >= %s
            AND event_date <= %s
            GROUP BY month;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query, [twelve_months_ago, current_date])

            results = cursor.fetchall()

            # Mettez à jour le dictionnaire des données avec les résultats
            for row in results:
                month = row[0]
                event_count = row[1]
                data_by_month[month] = event_count

        # Convertissez le dictionnaire en une liste pour la réponse JSON
        data = [{'month': month, 'event_count': event_count} for month, event_count in data_by_month.items()]
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'marche pas data per period'}, status=400)



def fetch_event_type(request):
    if request.method == 'GET':
        selected_countries = request.GET.getlist('selectedCountries[]')
        selected_countries_string = ",".join(f"'{country}'" for country in selected_countries)

        sql_query = f"""
            SELECT event_type, latitude, longitude
            FROM donqlick
            WHERE country IN ({selected_countries_string});
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)

            results = cursor.fetchall()

            # Créez un dictionnaire pour stocker les données par catégorie
            data_by_category = {}

            for row in results:
                category, latitude, longitude = row

                if category not in data_by_category:
                    data_by_category[category] = {
                        'category': category,
                        'coordinates': []
                    }

                data_by_category[category]['coordinates'].append([latitude, longitude])

            # Convertissez le dictionnaire en une liste pour la réponse JSON
            data_list = list(data_by_category.values())

        # Ajoutez le nombre d'événements par catégorie en parcourant à nouveau la base de données
        for category_data in data_list:
            category = category_data['category']
            sql_query_count = f"""
                SELECT COUNT(event_id_cnty) AS event_count
                FROM donqlick
                WHERE country IN ({selected_countries_string}) AND event_type = %s;
            """
            with connection.cursor() as cursor:
                cursor.execute(sql_query_count, [category])
                result = cursor.fetchone()
                if result:
                    category_data['event_count'] = result[0]
                else:
                    category_data['event_count'] = 0

        # Renvoyez la liste de données au format JSON
        print("noouuu:",data_list)
        return JsonResponse(data_list, safe=False)
    else:
        return JsonResponse({'error': 'marche pas data per category'}, status=400)

