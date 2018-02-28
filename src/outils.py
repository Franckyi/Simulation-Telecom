#!/usr/bin/env python
# coding: utf-8


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
