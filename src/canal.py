#!/usr/bin/env python
# coding: utf-8
# Ici : Codage du bruit,
from random import randint

import numpy as np


def ajout_bruit(y, mvmax, signe):
    """
    Ajoute un 'bruit' en additionnant l'amplitude du signal par des valeurs aléatoires.
    :param y : le signal à bruiter
    :param mvmax : la valeur maximum en mV rajoutée par le bruit
    :param signe : -1 = bruit négatif, 0 = bruit positif et négatif, 1 = bruit positif
    """

    for i in range(len(y)):
        if signe == -1:
            y[i] += randint(-(mvmax * 100), 0) / 100000.
        elif signe == 0:
            y[i] += randint(-(mvmax * 100), (mvmax * 100)) / 100000.
        elif signe == 1:
            y[i] += randint(0, (mvmax * 100)) / 100000.
    return y


def generer_bruit(nbech, mvmax, signe):
    """
    Ajoute un 'bruit' en additionnant l'amplitude du signal par des valeurs aléatoires.
    :param nbech : nombre d'échantillons du signal de bruit
    :param mvmax : la valeur maximum en mV du bruit
    :param signe : -1 = bruit négatif, 0 = bruit positif et négatif, 1 = bruit positif
    """
    ybr = []

    for i in range(nbech):
        if signe == -1:
            ybr.append(randint(-(mvmax*100), 0)/100000.)
        elif signe == 0:
            ybr.append(randint(-(mvmax*100), (mvmax * 100))/100000.)
        elif signe == 1:
            ybr.append(randint(0, (mvmax * 100))/100000.)
    return ybr


def bruit_gaussien(y, intensite):
    bruit = (np.random.normal(0, 1, len(y)) - 0.5) * intensite
    return np.array(y) + bruit


def bruit_aleatoire(y, intensite):
    bruit = (np.random.rand(len(y)) - 0.5) * intensite
    return np.array(y) + bruit
