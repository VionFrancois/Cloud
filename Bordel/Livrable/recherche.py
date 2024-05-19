import sys

import matplotlib.pyplot as plt
import numpy as np
import operator
import math
import os
import csv
import warnings
warnings.filterwarnings('ignore')

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
folder_model1="Features_train/VGG16/"
if not os.path.exists(folder_model1):
    os.makedirs(folder_model1)



def read_features_from_files(folder_model1, files_folder):
    features1 = []

    # Liste tous les fichiers de caractéristiques dans le répertoire
    for txt_file in os.listdir(folder_model1):
        if txt_file.endswith(".txt"):
            # Obtenir le chemin complet du fichier texte
            feature_file_path = os.path.join(folder_model1, txt_file)
            
            # Lire les caractéristiques à partir du fichier texte
            feature = np.loadtxt(feature_file_path)

            # Retrouver le nom de l'image d'origine à partir du nom du fichier texte
            image_basename = os.path.splitext(txt_file)[0] + ".jpg"
            image_path = os.path.join(files_folder, image_basename)

            # Ajouter le tuple (chemin de l'image, caractéristiques) à la liste
            features1.append((image_path, feature))

    return features1

features1 = read_features_from_files("Features_train/VGG16/", "image.orig/")

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

image_req = int(sys.argv[1])
top = int(sys.argv[2])
nom_image_requete, nom_images_proches, nom_images_non_proches = recherche(image_req, top)

print("")
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

  for a in rp:
     print(str(a))


compute_RP("VGG_RP.txt", top,nom_image_requete, nom_images_non_proches)