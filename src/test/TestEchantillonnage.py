#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt

# paramètres généraux
fech = 250.  # fréquence d'échantillonage en Hertz

# paramètres séquence
seq = [1, 0, 0, 1, 0, 1, 1, 0]  # séquence binaire
debit = 2.  # débit binaire en Hertz

# paramètres codage (NRZ)
v0_c = 0.  # tension associée à un bit égal à 0 en Volts
v1_c = 1.  # tension associée à un bit égal à 1 en Volts

# paramètres modulation (ASK-2)
fp = 50.  # fréquence de la porteuse en Hz
v0_m = 1.  # tension associée à un bit égal à 0 en Volts
v1_m = 2.  # tension associée à un bit égal à 1 en Volts

duree = len(seq) / debit  # durée totale de la séquence en seconde
x = np.arange(0, duree, 1/fech).tolist()  # liste des échantillons

y0 = []  # contient les tensions correspondant au signal échantilloné codé NRZ
i = 0  # on commence au bit 0
for j in range(len(x)):  # pour chaque échantillon
    y0.append(v0_c if seq[i] == 0 else v1_c)  # on ajoute la tension correspondant au bit actuel
    if j >= fech/debit*(i+1):  # test pour changer de bit
        i += 1  # on passe au bit suivant

y1 = []  # contient les tensions correspondant au signal échantilloné modulé ASK-2
i = 0  # on commence au bit 0
for k in range(len(x)):  # pour chaque échantillon
    y1.append(np.sin(2*np.pi*fp + x[k]*fp) * (v0_m if seq[i] == 0 else v1_m))  # on ajoute la tension correspondant au bit actuel
    if k >= fech/debit*(i+1):  # test pour changer de bit
        i += 1  # on passe au bit suivant

p0, = plt.plot(x, y0)
p1, = plt.plot(x, y1)
plt.title(u"Signal échantillonné codé NRZ et modulé ASK-2")  # titre du graphique
plt.legend([p0, p1], ["NRZ", "ASK-2"])  # legende du graphique
plt.xlabel(u"Temps (s)")
plt.ylabel("Tension (V)")
plt.show()
