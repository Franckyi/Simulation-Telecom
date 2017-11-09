#!/usr/bin/env python
# coding: utf-8
import sequence
import codage
import matplotlib.pyplot as plt


seq = sequence.Sequence()
nrz = codage.CodageNRZ(1)
pos = nrz.generer_positions(seq)
p, = plt.plot(pos[0], pos[1])
plt.legend([p], [str(seq.bits)])
plt.title(nrz.nom)
plt.show()
