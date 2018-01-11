#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt

import modulation
import sequence

# x, y = modulation.moduler_ask(sequence.sequence_aleatoire(16, 10.), 20., 1., 2., 3., 4.)
# x, y = modulation.moduler_psk(sequence.sequence_aleatoire(16, 10.), 5., 0., np.pi/2, np.pi, 3*np.pi/2)
x, y = modulation.moduler_fsk(sequence.sequence_aleatoire(4, 20.), [10., 30.])

p = plt.plot(x, y)
plt.title(u"Signal échantillonné modulé FSK")  # titre du graphique
plt.legend(p, ["FSK"])  # legende du graphique
plt.xlabel("Temps (s)")
plt.ylabel("Tension (V)")
plt.show()