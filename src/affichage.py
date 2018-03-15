#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt

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


def figure_spectre(xf, yf, fig, titre=None, xlegend=None, ylegend=None, xmin=None, xmax=None, ymin=None, ymax=None):
    figure(xf, yf, fig, "Spectre" if titre is None else titre, u"Fréquence (Hz)" if xlegend is None else xlegend,
           "Puissance (W)" if ylegend is None else ylegend, min(xf) if xmin is None else xmin,
           max(xf) if xmax is None else xmax, min(yf) if ymin is None else ymin, max(yf) if ymax is None else ymax)


def figure_diagramme_oeil(x, y, fig, seq, vmin, vmax, nb_yeux, titre=None):
    window_size = (2 * nb_yeux - nb_yeux + 1) * len(x) / len(seq)
    t = x[1] - x[0]
    eyediagram_lines(fig, y, t, window_size, window_size / (2 * (nb_yeux + 1)), vmin, vmax, titre)


def eyediagram_lines(fig, y, t, window_size, offset, vmin, vmax, titre):
    # SOURCE : https://github.com/WarrenWeckesser/eyediagram/blob/master/eyediagram/mpl.py
    plt.figure(fig)
    plt.title(titre)
    plt.xlabel("Temps (s)")
    plt.ylabel("Tension (V)")
    start = offset
    while start < len(y):
        end = start + window_size
        if end > len(y):
            end = len(y)
        yy = y[start:end + 1]
        plt.plot(np.arange(len(yy)) * t, yy, '#1f77b4')
        start = end
    plt.axis([0, window_size * t, vmin, vmax])


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
