#!/usr/bin/env python
# coding: utf-8


NRZ = 0
RZ = 1
MANCHESTER = 2
_2B1Q = 3


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


def coder(sequence, echantillonnage, codage, v0=0, v1=1):
    """
    Code une séquence avec échantillonnage au format choisi
    :param sequence: La séquence à coder
    :param echantillonnage: L'échantillonnage choisi
    :param codage: Le codage choisi
    :param v0: v0 pour NRZ, v0 pour Manchester
    :param v1: v1 pour NRZ, v pour RZ, v1 pour Manchster, vmax pour 2B1Q (vmin = -vmax)
    :return: La séquence échantillonnée codée
    """
    if codage == NRZ:
        return coder_nrz(sequence, echantillonnage, v0, v1)
    if codage == RZ:
        return coder_rz(sequence, echantillonnage, v1)
    if codage == MANCHESTER:
        return coder_manchester(sequence, echantillonnage, v0, v1)
    if codage == _2B1Q:
        return coder_2b1q(sequence, echantillonnage, v1)


def coder_nrz(sequence, echantillonnage, v0=0, v1=1):
    y = []  # contient les tensions correspondant au signal échantilloné codé NRZ
    i = 0  # on commence au bit 0
    for j in range(len(echantillonnage.vec)):  # pour chaque échantillon
        y.append(v0 if sequence.bits[i] == 0 else v1)  # on ajoute la tension correspondant au bit actuel
        if j >= echantillonnage.fech / sequence.debit * (i + 1):  # test pour changer de bit
            i += 1  # on passe au bit suivant
    return y


def coder_rz(sequence, echantillonnage, v):
    y = []  # contient les tensions correspondant au signal échantilloné codé RZ
    i = 0  # on commence au bit 0
    for j in range(len(echantillonnage.vec)):  # pour chaque échantillon
        if sequence.bits[i] == 0:  # si le bit vaut 0,
            y.append(0)  # la valeur pour cet échantillon vaut 0
        else:  # si le bit vaut 1, on ajoute la tension correspondant au bit actuel, selon s'il se situe avant ou après
            y.append(v if j < echantillonnage.fech / sequence.debit * (i + 0.5) else 0)  # la moitié de la durée du bit
        if j >= echantillonnage.fech / sequence.debit * (i + 1):  # test pour changer de bit
            i += 1  # on passe au bit suivant
    return y


def coder_manchester(sequence, echantillonnage, v0, v1):
    #  conseil : adapter le travail fait sur coder_RZ
    y = []  # contient les tensions correspondant au signal échantilloné codé manchester
    i = 0  # on commence au bit 0
    for j in range(len(echantillonnage.vec)):  # pour chaque échantillon
        if sequence.bits[i] == 0:  # si le bit vaut 0,
            y.append(v0 if j < echantillonnage.fech / sequence.debit * (i + 0.5) else v1)  # représente un front montant à la moitié de la durée du bit
        else:  # si le bit vaut 1,
            y.append(v1 if j < echantillonnage.fech / sequence.debit * (
                    i + 0.5) else v0)  # représente un front déscendant à la moitié de la durée du bit

        if j >= echantillonnage.fech / sequence.debit * (i + 1):  # test pour changer de bit
            i += 1  # on passe au bit suivant
    return y


def coder_2b1q(sequence, echantillonnage, v):
    #  conseils :
    #  - lire https://en.wikipedia.org/wiki/2B1Q et https://en.wikipedia.org/wiki/Gray_code
    #  - calculer les tensions pour chaque dibit, en sachant que vmax = v et vmin = -v, et que chaque dibit est séparé
    #    par une même tension (par exemple [0.45, 0.15, -0.15, -0.45] si v = 0.45,
    #    les dibits sont séparés de (2*v)/3 = 0.3)
    #  - prendre les bits deux par deux, et tester si ils valent 00, 01, 10 ou 11
    y = []  # contient les tensions correspondant au signal échantilloné codé 2B1Q
    i = 0  # on commence au bit 0
    for j in range(len(echantillonnage.vec)):  # pour chaque échantillon
        # On attribue la valeur correspondante de v à chaque dibit
        valeur_dibit = binaire_vers_decimal(sequence.bits[i:i + 2])
        if valeur_dibit == 0:  # Dibit 00
            y.append(-v)
        elif valeur_dibit == 1:  # Dibit 01
            y.append(-v+(2.*v/3))
        elif valeur_dibit == 2:  # Dibit 10
            y.append(v-(2.*v/3))
        elif valeur_dibit == 3:  # Dibit 11
            y.append(v)
        if j >= echantillonnage.fech / sequence.debit * (i + 2):  # test pour changer de bit
            i += 2  # on passe aux deux bits suivant
    return y
