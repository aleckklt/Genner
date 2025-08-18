from django.db import models
from django.utils import timezone

class Tasks(models.Model):
    titre = models.CharField(max_length=200)
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
    ]
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='en_cours')
    date = models.DateField(default=timezone.now)
    heure = models.TimeField(default=timezone.now)

    def __str__(self):
        return self.titre