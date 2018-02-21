#!/usr/bin/env python
# coding: utf-8

import numpy as np

import echantillonnage


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


def moduler_ask(seq, db, fp, args):
    """
    Module une séquence binaire en amplitude
    :param seq: La séquence à moduler
    :param db: Le débit binaire
    :param fp La fréquence porteuse
    :param args: Les différentes tensions
    :return: Le vecteur échantillonnage ainsi que le signal échantillonné modulé en amplitude
    """
    fech = fp * 100
    ech = echantillonnage.creer_echantillons(seq, db, fech)  # on échantillonne à 100 * fp
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
    return ech, y


def moduler_fsk(seq, db, v, args):
    """
    Module une séquence binaire en fréquence
    :param seq: La séquence à moduler
    :param db: Le débit binaire
    :param v: L'amplitude
    :param args: Les différentes fréquences
    :return: Le vecteur échantillonnage ainsi que le signal échantillonné modulé en fréquence
    """
    fech = max(args) * 100
    ech = echantillonnage.creer_echantillons(seq, db, fech)  # on échantillonne à 100 * fmax
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
    return ech, y


def moduler_psk(seq, db, v, fp, args):
    """
    Module une séquence binaire en phase
    :param seq: La séquence à moduler
    :param db: Le débit binaire
    :param v: L'amplitude
    :param fp: La fréquence porteuse
    :param args: Les différentes phases
    :return: Le vecteur échantillonnage ainsi que le signal échantillonné modulé en phase
    """
    fech = fp * 100
    ech = echantillonnage.creer_echantillons(seq, db, fech)  # on échantillonne à 100 * fp
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
    return ech, y
