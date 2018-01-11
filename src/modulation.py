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


def moduler_ask(sequence, fp, args):
    """
    Module une séquence binaire en amplitude
    :param sequence: La séquence à moduler
    :param fp La fréquence porteuse
    :param args: Les différentes tensions
    :return: Le vecteur échantillonnage ainsi que le signal échantillonné modulé en amplitude
    """
    ech = echantillonnage.creer_echantillons(sequence, fp * 100)  # on échantillonne à 100 * fp
    bits_symbole = verifier_parametres(
        len(args))  # on vérifie les paramètres et on récupère le nombre de bits par symbole
    y = []
    i = 0
    for j in range(len(ech.vec)):  # pour chaque échantillon
        tension = args[
            binaire_vers_decimal(sequence.bits[i:i + bits_symbole])]  # on récupère la tension correspondant au symbole
        y.append(np.sin(2 * np.pi * fp * ech.vec[j]) * tension)  # on l'ajoute
        if j >= ech.fech / sequence.debit * (i + bits_symbole):  # test pour changer de symbole
            i += bits_symbole  # on passe au symbole suivant
    return ech.vec, y


def moduler_fsk(sequence, v, args):
    """
    Module une séquence binaire en fréquence
    :param sequence: La séquence à moduler
    :param v: L'amplitude
    :param args: Les différentes fréquences
    :return: Le vecteur échantillonnage ainsi que le signal échantillonné modulé en fréquence
    """
    ech = echantillonnage.creer_echantillons(sequence, max(args) * 100)  # on échantillonne à 100 * fmax
    bits_symbole = verifier_parametres(
        len(args))  # on vérifie les paramètres et on récupère le nombre de bits par symbole
    y = []
    i = 0
    for j in range(len(ech.vec)):  # pour chaque echantillon
        frequence = args[
            binaire_vers_decimal(
                sequence.bits[i:i + bits_symbole])]  # on récupère la fréquence correspondant au symbole
        y.append(np.sin(2 * np.pi * ech.vec[j] * frequence) * v)  # on l'ajoute
        if j >= ech.fech / sequence.debit * (i + bits_symbole):  # test pour changer de symbole
            i += bits_symbole  # on passe au symbole suivant
    return ech.vec, y


def moduler_psk(sequence, v, fp, args):
    """
    Module une séquence binaire en phase
    :param sequence: La séquence à moduler
    :param v: L'amplitude
    :param fp: La fréquence porteuse
    :param args: Les différentes phases
    :return: Le vecteur échantillonnage ainsi que le signal échantillonné modulé en phase
    """
    ech = echantillonnage.creer_echantillons(sequence, fp * 100)  # on échantillonne à 100 * fp
    bits_symbole = verifier_parametres(
        len(args))  # on vérifie les paramètres et on récupère le nombre de bits par symbole
    y = []
    i = 0
    for j in range(len(ech.vec)):  # pour chaque échantillon
        phase = args[
            binaire_vers_decimal(sequence.bits[i:i + bits_symbole])]  # on récupère la phase correspondant au symbole
        y.append(np.sin((2 * np.pi * fp * ech.vec[j]) + phase) * v)  # on l'ajoute
        if j >= ech.fech / sequence.debit * (i + bits_symbole):  # test pour changer de symbole
            i += bits_symbole  # on passe au symbole suivant
    return ech.vec, y
