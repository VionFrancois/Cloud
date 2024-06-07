from django import forms

class FileSelectionForm(forms.Form):
    # Structure of the form
    filename = forms.CharField(label="Nom du fichier", max_length=20)
    top = forms.IntegerField(label="Nombre de résultats à afficher", min_value=1, max_value=80)

    model_choices = [
        ('VGG16', 'VGG16'),
        ('ResNet50', 'ResNet50'),
        ('MobileNet', 'MobileNet')
    ]
    dropdown1 = forms.ChoiceField(choices=model_choices, label='Choix du modèle')

    dist_choices = [
        ('Euclidean', 'Euclidean'),
        ('Chi2', 'Chi2'),
        ('Bhattcharyya', 'Bhattcharyya')
    ]
    dropdown2 = forms.ChoiceField(choices=dist_choices, label='Choix de la mesure de distance')