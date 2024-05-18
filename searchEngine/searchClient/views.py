from django.shortcuts import render
from .forms import FileSelectionForm
import subprocess
import os
import matplotlib.pyplot as plt
from django.contrib.auth.decorators import login_required
from .recherche import *


@login_required
def index(request):
    results_dir = 'results'
    if request.method == 'POST':
        form = FileSelectionForm(request.POST)
        if form.is_valid():
            filename = form.cleaned_data['filename']
            top = form.cleaned_data['top']
            file_path = os.path.join('searchClient/static/', filename)

            if os.path.exists(file_path):

                base_image, images, _ = search(filename[:-4], top, "VGG16")

                images.insert(0, base_image)
                print(images)

                return render(request, 'searchClient/results.html', {'images': images})
            else:
                form.add_error('filename', "Le fichier n'existe pas.")
    else:
        form = FileSelectionForm()
    return render(request, 'searchClient/index.html', {'form': form})