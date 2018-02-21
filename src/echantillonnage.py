#!/usr/bin/env python
# coding: utf-8
import numpy as np


def creer_echantillons(sequence, db, fech):
    """
    Créé un vecteur temporel en fonction de la séquence de bits,
    de son débit binaire et de la fréquence d'échantillonnage.
    :param sequence: Séquence de bits
    :param db: Débit binaire
    :param fech: Fréquence d'échantillonnage
    :return: Le vecteur temporel associé aux paramètres
    """
    return np.arange(0, len(sequence) / db, 1 / fech).tolist()
