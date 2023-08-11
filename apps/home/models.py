from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    # Ajoutez une méthode pour récupérer le nom d'utilisateur
    def get_username(self):
        return self.user.username
