from django.db import models

class Tasks(models.Model):
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
    ]

    titre = models.CharField(max_length=200)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='en_cours')
    date = models.DateField(blank=True, null=True)
    heure = models.TimeField(blank=True, null=True)
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titre
