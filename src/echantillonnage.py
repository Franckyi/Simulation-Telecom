#!/usr/bin/env python
# coding: utf-8
import numpy as np


class Echantillonnage:
    """
    Contient les informations à propos de l'échantillonnage, c'est à dire le vecteur temporel (attribut vec) et
    la fréquence d'échantillonnage (attribut fech).
    """

    def __init__(self, vec, fech):
        """
        Construit un object échantillonnage
        :param vec: Le vecteur temporel qui contient le temps associé à chaque échantillon
        :param fech: La fréquence d'échantillonnage
        """
        self.vec = vec
        self.fech = fech


def creer_echantillons(sequence, fech):
    """
    Créé un vecteur temporel en fonction de la séquence de bits,
    de son débit binaire et de la fréquence d'échantillonnage.
    :param sequence: Séquence de bits
    :param fech: Fréquence d'échantillonnage
    :return: Le vecteur temporel associé aux paramètres
    """
    return Echantillonnage(np.arange(0, len(sequence.bits) / sequence.debit, 1 / fech).tolist(), fech)
