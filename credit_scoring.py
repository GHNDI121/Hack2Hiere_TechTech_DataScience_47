# -*- coding: utf-8 -*-
"""credit_scoring.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IsxYVqsJ3P4RkqH-Ei_YkuJOpfkj6u6x

# **PROJET CREDIT SCORING**

## **EXPLORATION DES DONNEES**
"""

##importer la base######
import pandas as pd
german_credit_data=pd.read_table("/content/german_credit_data.csv",sep=",",header=0,index_col=0)
german_credit_data

##renommer les colonnes
german_credit_data.rename(columns={"Saving accounts":"compte d'epargne","Checking account":"compte courant","Credit amount":"montant du credit","Duration":"duree","Purpose":"but"},inplace=True)
german_credit_data

#####statistique descriptive######
print(german_credit_data.describe(include="all"))

##les information de la base
german_credit_data.info()

##variables
german_credit_data.columns

#nombre total de valeur nul#

print("nous constatons que les variables qui ont des valeurs nuls sont au nombre de:", german_credit_data.isnull().sum().sum())

##afficher les variables qui ont des valeurs nul
german_credit_data.isnull().sum()

#nombre de doublons
german_credit_data.duplicated().sum()

#traçons les boxplots
import seaborn as sn
import matplotlib.pyplot as plt
sn.boxplot(german_credit_data['montant du credit'])

plt.title('montant du credit')
plt.show()

plt.show()

##les valeurs aberrantes par la methodes de z-score
lim_sup=german_credit_data['montant du credit'].mean()+3*german_credit_data['montant du credit'].std()

lim_inf=german_credit_data['montant du credit'].mean()-3*german_credit_data['montant du credit'].std()

val_aber=german_credit_data.loc[(german_credit_data['montant du credit']>lim_sup)| (german_credit_data['montant du credit']<lim_inf),:]
val_aber

##bonne base sans les valeurs aberrantes
german_credit=german_credit_data[(german_credit_data['montant du credit']>lim_inf)&(german_credit_data['montant du credit']<lim_sup)]
german_credit

# Supprimer les colonnes spécifiques
german_credit = german_credit.drop(columns=['Housing', 'compte courant', 'compte d\'epargne', 'but'])


german_credit

##renommer##
# Remplacer 'Femme' par 0 et 'Homme' par 1 dans la colonne 'Genre'
german_credit['Sex'] = german_credit['Sex'].replace({'female': 0, 'male': 1})

german_credit

"""##**visualisation de donnees**"""

##voir les lignes et les colonnes##

german_credit.shape

##valeur existentielle daans job
german_credit['Job'].value_counts()

###visuaalisation

from matplotlib import pyplot as plt

plt.scatter(german_credit['montant du credit'],german_credit['Job'])

plt.show()

###importer la library k-means##
from sklearn.cluster import KMeans

##definir le model k-means##
model=KMeans(n_clusters=4)

##entrainer le modele dans la dataset ##
model.fit(german_credit)

##predire les nouvelles classes##
model.predict(german_credit)

##inertie intraclasse

model.inertia_

##position des centroides

model.cluster_centers_

##visualisation avec des groupes predites avec la variable Job
from matplotlib import pyplot as plt

plt.scatter(german_credit['montant du credit'],german_credit['Job'],c=model.predict(german_credit))

plt.show()

##visualisation avec des groupes predites avec la variable
from matplotlib import pyplot as plt

plt.scatter(german_credit['montant du credit'],german_credit['Age'],c=model.predict(german_credit))

plt.show()

##visualisation avec des groupes predites avec la variable Sex
from matplotlib import pyplot as plt

plt.scatter(german_credit['montant du credit'],german_credit['Sex'],c=model.predict(german_credit))

plt.show()

##visualisation avec des groupes predites avec la variable duree
from matplotlib import pyplot as plt

plt.scatter(german_credit['montant du credit'],german_credit['duree'],c=model.predict(german_credit))

plt.show()

#centrage et reduction
from sklearn import preprocessing
german_credit_cr=preprocessing.scale(german_credit)
german_credit_cr

##chercher le cas optimal

##liste vide
inertie=[]


#### generer des entiers ####
gener=range(1,15)


for i in gener:
    ########### construitre le mpodéle de kmeans et l'entrainer dans le dataset X




    models=KMeans(n_clusters=i).fit(german_credit_cr)
    ####### ajouter linertie de chaque classe dans la liste
    inertie.append(models.inertia_)



plt.plot(gener,inertie)
plt.xlabel(' clusters K')
plt.ylabel('inertie intraclasse')
plt.title(" determination du nombre de k optimale ")
plt.show()

##modelisons avec le k-optimal=5
##definir le model k-means##
model=KMeans(n_clusters=4)

##entrainer le modele dans la dataset fromage_cr##
model.fit(german_credit_cr)

##predire les nouvelles classes##
model.predict(german_credit_cr)

##afficher les differents types de groupes

##index tries les groupes
import numpy as np

idk=np.argsort(model.labels_) ##model.labels c'est ce que le modele a predit ##np.argsort permet de trier les indices d'un tableau de facon croissant

##affichage des observationt et leur groupes
dd=pd.DataFrame(german_credit.index[idk],model.labels_[idk])
dd

##ajouter la variables classes
german_credit['classe']=model.predict(german_credit_cr)
german_credit['classe']

german_credit

moy = pd.DataFrame(german_credit)
# Calculer la moyenne pour chaque classe par rapport à chaque variable
moyennes_par_classe = moy.groupby('classe').mean()

# Afficher le résultat
moyennes_par_classe

import matplotlib.pyplot as plt
import seaborn as sns


# Utiliser seaborn pour améliorer la visibilité du graphique
sns.set(style="whitegrid")

# Tracer le graphique en utilisant un point pour chaque classe
plt.figure(figsize=(12, 6))
sns.scatterplot(data=moyennes_par_classe, palette="tab10", s=100)
plt.title('Moyennes par Classe pour Chaque Variable')
plt.xlabel('Classes')
plt.ylabel('Moyenne')
plt.show()

"""## conclusion"""