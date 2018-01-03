#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt

import modulation
import sequence

x, y = modulation.moduler_ask(sequence.sequence_aleatoire(16, 10.), 20., 1., 2., 3., 4.)
p = plt.plot(x, y)
plt.title(u"Signal échantillonné modulé ASK")  # titre du graphique
plt.legend(p, ["ASK"])  # legende du graphique
plt.xlabel("Temps (s)")
plt.ylabel("Tension (V)")
plt.show()
