#!/usr/bin/env python
# coding: utf-8


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


def coder_nrz(seq, db, ech, fech, v0, v1):
    y = []  # contient les tensions correspondant au signal échantilloné codé NRZ
    i = 0  # on commence au bit 0
    for j in range(len(ech)):  # pour chaque échantillon
        y.append(v0 if seq[i] == 0 else v1)  # on ajoute la tension correspondant au bit actuel
        if j >= fech / db * (i + 1):  # test pour changer de bit
            i += 1  # on passe au bit suivant
    return y


def coder_rz(seq, db, ech, fech, v0, v1):
    y = []  # contient les tensions correspondant au signal échantilloné codé RZ
    i = 0  # on commence au bit 0
    for j in range(len(ech)):  # pour chaque échantillon
        if j < fech / db * (i + 0.5):  # si on est avant la moitié du bit
            y.append(v0 if seq[i] == 0 else v1)  # on ajoute la tension correspondant au bit actuel
        else:  # sinon
            y.append(0)  # on ajoute 0
        if j >= fech / db * (i + 1):  # test pour changer de bit
            i += 1  # on passe au bit suivant
    return y


def coder_manchester(seq, db, ech, fech, vm, vp):
    y = []  # contient les tensions correspondant au signal échantilloné codé manchester
    i = 0  # on commence au bit 0
    for j in range(len(ech)):  # pour chaque échantillon
        if seq[i] == 0:  # si le bit vaut 0,
            y.append(
                vm if j < fech / db * (i + 0.5) else vp)  # représente un front montant à la moitié de la durée du bit
        else:  # si le bit vaut 1,
            y.append(vp if j < fech / db * (
                    i + 0.5) else vm)  # représente un front déscendant à la moitié de la durée du bit

        if j >= fech / db * (i + 1):  # test pour changer de bit
            i += 1  # on passe au bit suivant
    return y


def coder_2b1q_max(seq, db, ech, fech, vmax):
    return coder_2b1q(seq, db, ech, fech, -vmax, -vmax + (2. * vmax / 3), vmax - (2. * vmax / 3), vmax)


def coder_2b1q(seq, db, ech, fech, v00, v01, v10, v11):
    y = []  # contient les tensions correspondant au signal échantilloné codé 2B1Q
    i = 0  # on commence au bit 0
    for j in range(len(ech)):  # pour chaque échantillon
        # On attribue la valeur correspondante de v à chaque dibit
        valeur_dibit = binaire_vers_decimal(seq[i:i + 2])
        if valeur_dibit == 0:  # Dibit 00
            y.append(v00)
        elif valeur_dibit == 1:  # Dibit 01
            y.append(v01)
        elif valeur_dibit == 2:  # Dibit 10
            y.append(v10)
        elif valeur_dibit == 3:  # Dibit 11
            y.append(v11)
        if j >= fech / db * (i + 2):  # test pour changer de bit
            i += 2  # on passe aux deux bits suivant
    return y

