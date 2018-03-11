#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt
import numpy as np

from outils import *


def figure_sequence(seq, fig, bps=1):
    nb = {}
    for i in range(0, len(seq), bps):
        bits = seq[i:i + bps]
        val = binaire_vers_decimal(bits)
        if val in nb:
            nb[val] += 1
        else:
            nb[val] = 1
    p = {}
    labels = {}
    for (sym, count) in nb.items():
        p[sym] = 1.0 * count / len(seq) * 100
        labels[sym] = ("Symbole " + chaine_binaire(decimal_vers_binaire(sym, bps)))
    plt.figure(fig)
    plt.pie(p.values(), labels=labels.values(), autopct='%1.2f%%')
    plt.title(u"Répartition en symboles de {} bits de la séquence".format(bps))


def figure_chronogramme(x, y, fig, titre=None, xlegend=None, ylegend=None, xmin=None, xmax=None, ymin=None, ymax=None):
    figure(x, y, fig, "Chronogramme" if titre is None else titre, "Temps (s)" if xlegend is None else xlegend,
           "Tension (V)" if ylegend is None else ylegend, min(x) if xmin is None else xmin,
           max(x) if xmax is None else xmax, min(y) if ymin is None else ymin, max(y) if ymax is None else ymax)


def figure_spectre(x, y, fig, titre=None, xlegend=None, ylegend=None, xmin=None, xmax=None, ymin=None, ymax=None):
    t = x[1] - x[0]
    yf = np.abs(np.fft.fft(y)) ** 2 / t
    n = len(yf)
    yf = yf[0:n / 2]
    xf = np.linspace(0, 1 / (2 * t), n / 2)
    figure(xf, yf, fig, "Spectre" if titre is None else titre, u"Fréquence (Hz)" if xlegend is None else xlegend,
           "Puissance (W)" if ylegend is None else ylegend, min(xf) if xmin is None else xmin,
           max(xf) if xmax is None else xmax, min(yf) if ymin is None else ymin, max(yf) if ymax is None else ymax)


def figure_diagramme_oeil():
    pass


def figure_constellation():
    pass


def figure(x, y, fig, titre, legende_x, legende_y, xmin, xmax, ymin, ymax):
    plt.figure(fig)
    plt.plot(x, y)
    plt.axis([xmin, xmax, ymin, ymax])
    plt.xlabel(legende_x)
    plt.ylabel(legende_y)
    plt.title(titre)


def afficher():
    plt.show()
