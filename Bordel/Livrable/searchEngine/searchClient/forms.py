from django import forms

class FileSelectionForm(forms.Form):
    filename = forms.CharField(label="Nom du fichier", max_length=20)
    top = forms.IntegerField(label="Nombre de résultats à afficher", min_value=1, max_value=80)