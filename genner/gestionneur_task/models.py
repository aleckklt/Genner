from django.db import models

class Tasks(models.Model) :
    titre = models.CharField(max_length=255)

    def __str__(self):
        return self.titre