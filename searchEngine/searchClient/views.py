from django.shortcuts import render
from .forms import FileSelectionForm
import os
from django.contrib.auth.decorators import login_required

from .engine import *


@login_required
def index(request):
    if request.method == 'POST':
        # Create a form with the data from the request
        form = FileSelectionForm(request.POST)
        if form.is_valid():
            # Get the data from the form
            filename = form.cleaned_data['filename']
            top = form.cleaned_data['top']
            model = form.cleaned_data['dropdown']

            file_path = os.path.join('searchClient/static/', filename)

            if os.path.exists(file_path):
                # Make the search with engine.py
                base_image, images, _ = search(filename[:-4], top, model)
                images.insert(0, base_image)

                return render(request, 'searchClient/results.html', {'images': images})
            else:
                form.add_error('filename', "Le fichier n'existe pas.")
    else:
        form = FileSelectionForm()
    return render(request, 'searchClient/index.html', {'form': form})