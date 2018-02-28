#!/usr/bin/env python
# coding: utf-8

import numpy as np


def binaire_vers_decimal(bits):
    """
    Transforme un tableau de bits en entier
    :param bits: Le tableau de bits
    :return: L'entier représentant la valeur binaire
    """
    s = ""
    for bit in bits:
        s += str(bit)
    return int(s, 2)


def verifier_parametres(n_args):
    """
    Vérifie que le nombre de paramètres de la modulation donne bien un nombre de bits par symbole entier, lève une exception si ce n'est pas le cas
    :param n_args: Le nombre de paramètres de la modulation
    :return: Le nombre de bits par symbole
    """
    bits_symbole = np.log2(n_args)
    if not bits_symbole.is_integer():
        raise Exception("Impossible de moduler avec {} amplitudes différentes !".format(n_args))
    return int(bits_symbole)


def moduler_ask(seq, db, ech, fech, fp, args):
    """
    Module une séquence binaire en amplitude
    :param seq: La séquence à moduler
    :param db: Le débit binaire
    :param ech: L'échantillonnage
    :param fech: La fréquence d'échantillonnage
    :param fp La fréquence porteuse
    :param args: Les différentes tensions
    :return: Le vecteur échantillonnage ainsi que le signal échantillonné modulé en amplitude
    """
    bits_symbole = verifier_parametres(
        len(args))  # on vérifie les paramètres et on récupère le nombre de bits par symbole
    y = []
    i = 0
    for j in range(len(ech)):  # pour chaque échantillon
        tension = args[
            binaire_vers_decimal(seq[i:i + bits_symbole])]  # on récupère la tension correspondant au symbole
        y.append(np.sin(2 * np.pi * fp * ech[j]) * tension)  # on l'ajoute
        if j >= fech / db * (i + bits_symbole):  # test pour changer de symbole
            i += bits_symbole  # on passe au symbole suivant
    return y


def moduler_fsk(seq, db, ech, fech, v, args):
    """
    Module une séquence binaire en fréquence
    :param seq: La séquence à moduler
    :param db: Le débit binaire
    :param ech: L'échantillonnage
    :param fech: La fréquence d'échantillonnage
    :param v: L'amplitude
    :param args: Les différentes fréquences
    :return: Le vecteur échantillonnage ainsi que le signal échantillonné modulé en fréquence
    """
    bits_symbole = verifier_parametres(
        len(args))  # on vérifie les paramètres et on récupère le nombre de bits par symbole
    y = []
    i = 0
    for j in range(len(ech)):  # pour chaque echantillon
        frequence = args[
            binaire_vers_decimal(
                seq[i:i + bits_symbole])]  # on récupère la fréquence correspondant au symbole
        y.append(np.sin(2 * np.pi * ech[j] * frequence) * v)  # on l'ajoute
        if j >= fech / db * (i + bits_symbole):  # test pour changer de symbole
            i += bits_symbole  # on passe au symbole suivant
    return y


def moduler_psk(seq, db, ech, fech, v, fp, args):
    """
    Module une séquence binaire en phase
    :param seq: La séquence à moduler
    :param db: Le débit binaire
    :param ech: L'échantillonnage
    :param fech: La fréquence d'échantillonnage
    :param v: L'amplitude
    :param fp: La fréquence porteuse
    :param args: Les différentes phases
    :return: Le vecteur échantillonnage ainsi que le signal échantillonné modulé en phase
    """
    bits_symbole = verifier_parametres(
        len(args))  # on vérifie les paramètres et on récupère le nombre de bits par symbole
    y = []
    i = 0
    for j in range(len(ech)):  # pour chaque échantillon
        phase = args[
            binaire_vers_decimal(seq[i:i + bits_symbole])]  # on récupère la phase correspondant au symbole
        y.append(np.sin((2 * np.pi * fp * ech[j]) + phase) * v)  # on l'ajoute
        if j >= fech / db * (i + bits_symbole):  # test pour changer de symbole
            i += bits_symbole  # on passe au symbole suivant
    return y

def moduler_maq(seq, db, ech, fech, fp, args):
    """
    Module une séquence binaire en amplitude
    :param seq: La séquence à moduler
    :param db: Le débit binaire
    :param ech: L'échantillonnage
    :param fech: La fréquence d'échantillonnage
    :param fp La fréquence porteuse
    :param args: Les différentes tensions
    :return: Le vecteur échantillonnage ainsi que le signal échantillonné modulé en amplitude
    """
    bits_symbole = verifier_parametres(
        len(args))  # on vérifie les paramètres et on récupère le nombre de bits par symbole
    I = []
    Q = []
    S = []
    i = 0
    for j in range(len(ech)):  # pour chaque échantillon
        tensionI = args[binaire_vers_decimal(seq[i:i + bits_symbole/2])] # on récupère la tension correspondant au symbole I
        tensionQ = args[binaire_vers_decimal(seq[i+ bits_symbole / 2 :i + bits_symbole])]  # on récupère la tension correspondant au symbole Q
        I.append(np.cos(2 * np.pi * fp * ech[j]) * tensionI)  # on l'ajoute I
        Q.append(np.sin(2 * np.pi * fp * ech[j]) * tensionQ)  # on l'ajoute Q
        if j >= fech / db * (i + bits_symbole):  # test pour changer de symbole
            i += bits_symbole  # on passe au symbole suivant

    for x in len(I):
        S.append(I[x]+Q[x])

    return S