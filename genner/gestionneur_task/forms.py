from django import forms
from .models import Tasks

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['titre', 'statut', 'date', 'heure', 'commentaire']

        def clean(self):
            cleaned_data = super().clean()
            statut = cleaned_data.get('statut')
            commentaire = cleaned_data.get('commentaire')

            if statut == 'Terminé' and not commentaire :
                raise forms.ValidationError('Veuillez ajouter un commentaire lorsque la tâche est terminée.')