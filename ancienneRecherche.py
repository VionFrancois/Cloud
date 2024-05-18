import numpy as np
import operator
import math
import os
import csv
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

global features1
global folder_model1

def euclidianDistance(l1,l2):
    distance = 0
    length = min(len(l1),len(l2))
    for i in range(length):
        distance += pow((l1[i] - l2[i]), 2)
    return math.sqrt(distance)

def getkVoisins(lfeatures, test, k) :
    ldistances = []
    for i in range(len(lfeatures)):
        dist = euclidianDistance(test[1], lfeatures[i][1])
        ldistances.append((lfeatures[i][0], lfeatures[i][1], dist))
    ldistances.sort(key=operator.itemgetter(2))
    lvoisins = []
    for i in range(k):
        lvoisins.append(ldistances[i])
    return lvoisins


files = "image.orig"         #Chemin vers la base d'images
features1 = []               #Stocker les caractérstiques
big_folder="Features_train/" #Dossier pour stocker les caractéristiques
if not os.path.exists(big_folder):
    os.makedirs(big_folder)


def read_features_from_files(folder_model1, files_folder):
    features1 = []

    for txt_file in os.listdir(folder_model1):
        if txt_file.endswith(".txt"):
            feature_file_path = os.path.join(folder_model1, txt_file)
            
            feature = np.loadtxt(feature_file_path)

            image_basename = os.path.splitext(txt_file)[0] + ".jpg"
            image_path = os.path.join(files_folder, image_basename)

            features1.append((image_path, feature))

    return features1



def recherche(image_req,top):
  voisins = getkVoisins(features1, features1[image_req],top)
  #print(voisins)
  nom_images_proches = []
  nom_images_non_proches = []
  for k in range(top):
      nom_images_proches.append(voisins[k][0])
      #print("done")

  nom_image_requete=os.path.splitext(os.path.basename(features1[image_req][0]))[0]

  for j in range(top):
      print(nom_images_proches[j][11:])
      nom_images_non_proches.append(os.path.splitext(os.path.basename(nom_images_proches[j]))[0])

  return nom_image_requete, nom_images_proches, nom_images_non_proches



RP_file=""
def compute_RP(RP_file, top,nom_image_requete, nom_images_non_proches):
  text_file = open(RP_file, "w")
  rappel_precision=[]
  rp = []
  position1=int(nom_image_requete)//100
  for j in range(top):
    position2=int(nom_images_non_proches[j])//100
    if position1==position2:
      rappel_precision.append("pertinant")
    else:
      rappel_precision.append("non pertinant")

  for i in range(top):
    j=i
    val=0
    while j>=0:
      if rappel_precision[j]=="pertinant":
        val+=1
      j-=1
    rp.append(str((val/(i+1))*100)+" "+str((val/top)*100))

  with open(RP_file, 'w') as s:
    for a in rp:
      s.write(str(a) + '\n')


def display_RP(fichier, model):
  x = []
  y = []
  with open(fichier) as csvfile:
      plots = csv.reader(csvfile, delimiter=' ')
      for row in plots:
          x.append(float(row[0]))
          y.append(float(row[1]))
          fig = plt.figure()
  plt.plot(y,x,'C1', label=model);
  plt.xlabel('Rappel')
  plt.ylabel('Précison')
  plt.title("R/P")
  plt.legend()
  plt.savefig("searchClient/static/RP.png")
  plt.close()


def search(image_req, top, model):
    image_req = int(image_req)
    print("HELLO")
    print(image_req)
    if model == "VGG":
      folder_model1="/../Features_train/VGG16/"
    elif model == "ResNet":
      folder_model1="/../Features_train/ResNet50/"
    else:
      folder_model1="/../Features_train/MobileNet/"

    features1 = read_features_from_files(folder_model1, "image.orig/")
    nom_image_requete, nom_images_proches, nom_images_non_proches = recherche(image_req, top)
    compute_RP("RP.txt", top,nom_image_requete, nom_images_non_proches)
    display_RP("RP.txt", model)
    
    return nom_image_requete, nom_images_proches, nom_images_non_proches