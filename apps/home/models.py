from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    # Ajoutez une méthode pour récupérer le nom d'utilisateur
    def get_username(self):
        return self.user.username



from django.db import models

class Donqlick(models.Model):
    event_id_cnty = models.CharField(max_length=8, null=True)
    event_date = models.DateField(null=True)
    year = models.SmallIntegerField(null=True)
    time_precision = models.IntegerField(null=True)
    disorder_type = models.CharField(max_length=22, null=True)
    event_type = models.CharField(max_length=26, null=True)
    sub_event_type = models.CharField(max_length=35, null=True)
    actor1 = models.CharField(max_length=111, null=True)
    assoc_actor_1 = models.CharField(max_length=118, null=True)
    inter1 = models.SmallIntegerField(null=True)
    actor2 = models.CharField(max_length=111, null=True)
    assoc_actor_2 = models.CharField(max_length=91, null=True)
    inter2 = models.SmallIntegerField(null=True)
    interaction = models.SmallIntegerField(null=True)
    civilian_targeting = models.CharField(max_length=18, null=True)
    iso = models.SmallIntegerField(null=True)
    region = models.CharField(max_length=14, null=True)
    country = models.CharField(max_length=13, null=True)
    admin1 = models.CharField(max_length=25, null=True)
    admin2 = models.CharField(max_length=28, null=True)
    admin3 = models.CharField(max_length=33, null=True)
    location = models.CharField(max_length=27, null=True)
    latitude = models.CharField(max_length=7, null=True)
    longitude = models.CharField(max_length=8, null=True)
    geo_precision = models.SmallIntegerField(null=True)
    source = models.CharField(max_length=69, null=True)
    source_scale = models.CharField(max_length=27, null=True)
    notes = models.CharField(max_length=576, null=True)
    fatalities = models.SmallIntegerField(null=True)
    tags = models.CharField(max_length=55, null=True)
    timestamp = models.IntegerField(null=True)

    #def __str__(self):
        #return self.event_id_cnty  # Changez ceci pour renvoyer un champ significatif

    class Meta:
        db_table = 'donqlick'  # Le nom de la table dans la base de données
