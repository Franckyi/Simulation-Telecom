#!/usr/bin/env python
# coding: utf-8
import codage
from sequence import Sequence
import echantillonnage
import matplotlib.pyplot as plt

Liste_codages=["NRZ","RZ","Manchester","2B1Q"] #Liste des codages pour l'affichage dans la fenêtre mathplotlib

type_codage = -1
while type_codage not in range(4):
    print("Choisir le type de modulation :")
    print("0) NRZ")
    print("1) RZ")
    print("2) Manchester")
    print("3) 2B1Q")
    type_codage = input()
sequence = Sequence(nb_bits=8, debit=2.)  # création d'une séquence aléatoire de 8 bits à un débit de 2 bits/s
print("Séquence aléatoire : " + sequence.__str__())  # affichage de la séquence
ech = echantillonnage.creer_echantillons(sequence, 200.)  # création de l'échantillonnage à 200 Hz
y = codage.coder(sequence, ech, type_codage)  # codage de la séquence avec échantillonnage
p, = plt.plot(ech.vec, y)  # création du graphique
plt.title(u"Signal échantillonné codé "+Liste_codages[type_codage]+" en utilisant les classes")  # titre du graphique
plt.xlabel("Temps (s)")  # légende abscisses
plt.ylabel("Tension (V)")  # légende ordonnées
plt.legend([p], [Liste_codages[type_codage]])  # nom de la série de données
plt.show()  # affichage


