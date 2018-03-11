#!/usr/bin/env python
# coding: utf-8

import numpy as np

from codage import coder_nrz


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
    Module une porteuse en amplitude
    :param seq: La séquence modulante
    :param db: Le débit binaire
    :param ech: L'échantillonnage
    :param fech: La fréquence d'échantillonnage
    :param fp La porteuse à moduler
    :param args: Les différentes tensions
    :return: La porteuse modulée en amplitude
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
    Module une porteuse en fréquence
    :param seq: La séquence modulante
    :param db: Le débit binaire
    :param ech: L'échantillonnage
    :param fech: La fréquence d'échantillonnage
    :param v: L'amplitude
    :param args: Les différentes fréquences porteuses
    :return: La porteuse modulée en fréquence
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
    Module une porteuse en phase
    :param seq: La séquence modulante
    :param db: Le débit binaire
    :param ech: L'échantillonnage
    :param fech: La fréquence d'échantillonnage
    :param v: L'amplitude
    :param fp: La porteuse à moduler
    :param args: Les différentes phases
    :return: La porteuse modulée en phase
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


def moduler_maq(seq, db, ech, fech, fp, ordre, vmin, vmax):
    """
    Module une porteuse en amplitude en quadrature
    :param seq: La séquence modulante
    :param db: Le débit binaire
    :param ech: L'échantillonnage
    :param fech: La fréquence d'échantillonnage
    :param fp La porteuse à moduler
    :param args: Les différentes tensions
    :return: La porteuse modulée en amplitude en quadrature
    """
    bits_i = []
    bits_q = []
    flag = True
    for i in range(0, len(seq), ordre):
        bits = seq
        if flag:
            bits_i.append(bit)
            bits_i.append(bit)
        else:
            bits_q.append(bit)
            bits_q.append(bit)
        flag = not flag
    y0_i = coder_nrz(bits_i, db, ech, fech, vmin, vmax)
    y0_q = coder_nrz(bits_q, db, ech, fech, vmin, vmax)
    y1_i = moduler_psk()

    return
