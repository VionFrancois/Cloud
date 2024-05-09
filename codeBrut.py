from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications import vgg16
from keras.applications import vgg19
from tensorflow.keras.applications import resnet50
from keras.applications import inception_v3
from keras.applications import mobilenet
from keras.applications import xception
from matplotlib.pyplot import imread
import matplotlib.pyplot as plt
import numpy as np
import operator
import math
from keras.models import Model
import os
import tensorflow as tf
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

model0=vgg16.VGG16(weights='imagenet', include_top=True,pooling='avg')
model1 = Model(inputs=model0.input, outputs=model0.layers[-2].output)

model1.summary()


files = "image.orig"         #Chemin vers la base d'images
features1 = []               #Stocker les caractérstiques
big_folder="Features_train/" #Dossier pour stocker les caractéristiques
if not os.path.exists(big_folder):
    os.makedirs(big_folder)
folder_model1="Features_train/VGG16/"
if not os.path.exists(folder_model1):
    os.makedirs(folder_model1)


def indexation(output_file):
  pas =0
  for j in os.listdir(files) :
      data = os.path.join(files, j)
      print (data)
      if not data.endswith(".jpg"):
          continue
      file_name = os.path.basename(data)
      # load an image from file
      image = load_img(data, target_size=(224, 224))
      # convert the image pixels to a numpy array
      image = img_to_array(image)
      # reshape data for the model
      image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
      # prepare the image for the VGG model
      image = preprocess_input(image)
      # predict the probability across all output classes
      feature = model1.predict(image)
      feature = np.array(feature[0])
      np.savetxt(folder_model1+"/"+os.path.splitext(file_name)[0]+".txt",feature)
      features1.append((data,feature))
      print (pas)
      pas = pas+1
  with open(output_file, "w") as output:
        output.write(str(features1))

indexation("Features_train/VGG16.txt")

def recherche(image_req,top):
  top=20
  voisins = getkVoisins(features1, features1[image_req],top)
  #print(voisins)
  nom_images_proches = []
  nom_images_non_proches = []
  for k in range(top):
      nom_images_proches.append(voisins[k][0])
      #print("done")
  plt.figure(figsize=(5, 5))
  plt.imshow(imread(features1[image_req][0]), cmap='gray', interpolation='none')
  plt.title("Image requête")
  nom_image_requete=os.path.splitext(os.path.basename(features1[image_req][0]))[0]
  print(nom_image_requete)
  plt.figure(figsize=(25, 25))
  plt.subplots_adjust(hspace=0.2, wspace=0.2)

  for j in range(top):
      plt.subplot(int(top/4),int(top/5),j+1)
      plt.imshow(imread(nom_images_proches[j]), cmap='gray', interpolation='none')
      nom_images_non_proches.append(os.path.splitext(os.path.basename(nom_images_proches[j]))[0])
      title = "Image proche n°"+str(j)
      plt.title(title)
  return nom_image_requete, nom_images_proches, nom_images_non_proches

nom_image_requete, nom_images_proches, nom_images_non_proches = recherche(805,20)


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


compute_RP("VGG_RP.txt", 20,nom_image_requete, nom_images_non_proches)

def display_RP(fichier):
  x = []
  y = []
  with open(fichier) as csvfile:
      plots = csv.reader(csvfile, delimiter=' ')
      for row in plots:
          x.append(float(row[0]))
          y.append(float(row[1]))
          fig = plt.figure()
  plt.plot(y,x,'C1', label="VGG16" );
  plt.xlabel('Rappel')
  plt.ylabel('Précison')
  plt.title("R/P")
  plt.legend()

display_RP("VGG_RP.txt")