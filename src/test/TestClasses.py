#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt

import codage
import echantillonnage
import sequence

CODAGES = ["NRZ", "RZ", "Manchester", "2B1Q"]  # Liste des codages pour l'affichage dans la fenêtre matplotlib

type_codage = -1

while type_codage not in range(4):
    print("Choisir le type de codage :")
    print("0) NRZ")
    print("1) RZ")
    print("2) Manchester")
    print("3) 2B1Q")
    type_codage = input()

sequence = sequence.sequence_aleatoire(9, 2.)
print("Séquence aléatoire : " + sequence.__str__())  # affichage de la séquence
ech = echantillonnage.creer_echantillons(sequence, 200.)  # création de l'échantillonnage à 200 Hz
y = codage.coder(sequence, ech, type_codage)  # codage de la séquence avec échantillonnage

p, = plt.plot(ech.vec, y)  # création du graphique
plt.title(u"Signal échantillonné codé " + CODAGES[type_codage] + " en utilisant les classes")  # titre du graphique
plt.xlabel("Temps (s)")  # légende abscisses
plt.ylabel("Tension (V)")  # légende ordonnées
plt.legend([p], [CODAGES[type_codage]])  # nom de la série de données
plt.show()  # affichage


