#!/usr/bin/env python
# coding: utf-8

import numpy as np


def binaire_vers_decimal(bits):
    """
    Transforme un tableau de bits en entier
    :param bits: Le tableau de bits
    :return: L'entier représentant la valeur binaire
    """
    nb = 0
    for bit in bits:
        nb = (nb << 1) | bit
    return nb


def decimal_vers_binaire(i, nb):
    """
    Transforme un entier en tableau de bits
    :param i: L'entier représentant la valeur binaire
    :param nb: Le nombre de bits
    :return: Le tableau de bits
    """
    return format(i, '0{}b'.format(nb))


def chaine_binaire(bits):
    """
    Transforme un tableau de bits en une chaine de caractères
    :param bits: Le tableau de bits
    :return: La chaîne de caractères
    """
    s = ""
    for bit in bits:
        s += str(bit)
    return s


def calculer_spectre(x, y):
    """
    Calcule la densité spectrale de puissance d'un signal
    :param x: L'échantillonnage
    :param y: Les tensions
    :return: Les fréquences, les puissances associées aux fréquences
    """
    t = x[1] - x[0]
    yf = np.abs(np.fft.fft(y)) ** 2 / t
    n = len(yf)
    yf = yf[0:n / 2]
    xf = np.linspace(0, 1 / (2 * t), n / 2)
    return xf, yf
