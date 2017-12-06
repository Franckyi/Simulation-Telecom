#!/usr/bin/env python
# coding: utf-8
import codage
from sequence import Sequence
import echantillonnage
import matplotlib.pyplot as plt

sequence = Sequence(nb_bits=8, debit=2.)
ech = echantillonnage.creer_echantillons(sequence, 200.)
y = codage.coder_NRZ(sequence, ech)
plt.plot(ech.vec, y, label="NRZ")
plt.title(u"Signal échantillonné codé NRZ en utilisant les classes")  # titre du graphique
plt.xlabel("Temps (s)")
plt.ylabel("Tension (V)")
plt.show()


