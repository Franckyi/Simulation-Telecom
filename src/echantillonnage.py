#!/usr/bin/env python
# coding: utf-8
import numpy as np


def creer_echantillons(seq, db, fech):
    """
    Créé un vecteur temporel en fonction de la séquence de bits,
    de son débit binaire et de la fréquence d'échantillonnage.
    :param seq: Séquence de bits
    :param db: Débit binaire
    :param fech: Fréquence d'échantillonnage
    :return: Le vecteur temporel associé aux paramètres
    """
    return np.arange(0, len(seq) / (1.0 * db), 1.0 / fech).tolist()
