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
    id = models.BigAutoField(primary_key=True)
    event_id_cnty = models.CharField(max_length=255,default='')
    event_date =models.DateField(max_length=255,default='')
    year =models.IntegerField(null=True)
    time_precision =models.IntegerField(null=True)
    discoder_type=models.CharField(max_length=255,default='')
    event_type=models.CharField(max_length=255,default='')
    sub_event_type=models.CharField(max_length=255,default='')
    actor1=models.CharField(max_length=255,default='')
    assoc_actor_1=models.CharField(max_length=255,default='')
    inter1=models.IntegerField(null=True)
    actor2=models.CharField(max_length=255,default='')
    assoc_actor_2=models.CharField(max_length=255,default='')
    inter2=models.IntegerField(null=True)
    interaction=models.IntegerField(null=True)
    civilian_targeting =models.CharField(max_length=255,default='')
    iso=models.IntegerField(null=True)
    region=models.CharField(max_length=255,default='')
    country=models.CharField(max_length=255,default='')
    admin1=models.CharField(max_length=255,default='')
    admin2=models.CharField(max_length=255,default='')
    admin3=models.CharField(max_length=255,default='')
    location=models.CharField(max_length=255,default='')
    latitude=models.FloatField(null=True)
    longitude=models.FloatField(null=True)
    geo_precision=models.IntegerField(null=True)
    source=models.CharField(max_length=255,default='')
    source_scale=models.CharField(max_length=255,default='')
    notes=models.CharField(max_length=255,default='')
    fatalities=models.IntegerField(null=True)
    tags=models.CharField(max_length=255,default='')
    timestamp = models.DecimalField(max_digits=20, decimal_places=6,default=None)

    class Meta:
        db_table = 'donqlick'  # Le nom de la table dans la base de données
