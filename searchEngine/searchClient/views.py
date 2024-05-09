from django.shortcuts import render
from .forms import FileSelectionForm
import subprocess
import os
import matplotlib.pyplot as plt
from django.contrib.auth.decorators import login_required

def generate_RP(plots):
  x = []
  y = []
  for row in plots:
    x.append(float(row[0]))
    y.append(float(row[1]))
    fig = plt.figure()
  plt.plot(y,x,'C1', label="VGG16");
  plt.xlabel('Rappel')
  plt.ylabel('Précison')
  plt.title("R/P")
  plt.legend()
  plt.savefig("searchClient/static/RP.png")
  plt.close()

@login_required
def index(request):
    results_dir = 'results'
    if request.method == 'POST':
        form = FileSelectionForm(request.POST)
        if form.is_valid():
            filename = form.cleaned_data['filename']
            top = form.cleaned_data['top']
            file_path = os.path.join('searchClient/static/', filename)

            # Vérifie si le fichier existe avant d'exécuter Docker
            if os.path.exists(file_path):
                # Exécuter Docker ici (à modifier selon tes besoins)
                # command = f"docker run --rm -v $(pwd)/input_files:/input my-docker-image /input/{filename}"
                command = f"docker run recherche:latest {filename[:-4]} {top}"
                process = subprocess.run(command, stdout=subprocess.PIPE,shell=True, check=True)

                # Supposons que Docker génère les images dans le répertoire "results"
                print(process.stdout)
                results = process.stdout.decode("utf-8").split("\n")[:-1]
                index = results.index("")
                images = results[:index]
                plots = results[index+1:]
                for i in range(len(plots)):
                    plots[i] = plots[i].split(" ")

                base_image = filename
                images.insert(0, base_image)
                print(images)
                generate_RP(plots)
                return render(request, 'searchClient/results.html', {'images': images})
            else:
                form.add_error('filename', "Le fichier n'existe pas.")
    else:
        form = FileSelectionForm()
    return render(request, 'searchClient/index.html', {'form': form})