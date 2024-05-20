from django import forms

class FileSelectionForm(forms.Form):
    # Structure of the form
    filename = forms.CharField(label="Nom du fichier", max_length=20)
    top = forms.IntegerField(label="Nombre de résultats à afficher", min_value=1, max_value=80)

    choices = [
        ('VGG16', 'VGG16'),
        ('ResNet50', 'ResNet50'),
        ('MobileNet', 'MobileNet')
    ]
    dropdown = forms.ChoiceField(choices=choices, label='Choix du modèle')