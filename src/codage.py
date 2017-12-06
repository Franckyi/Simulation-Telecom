#!/usr/bin/env python
# coding: utf-8
import numpy as np


NRZ = 0
RZ = 1
MANCHESTER = 2
_2B1Q = 3


def coder(sequence, echantillonnage, codage, v0=0, v1=1):
    if codage == NRZ:
        return coder_NRZ(sequence, echantillonnage, v0, v1)
    if codage == RZ:
        pass  # coder_RZ
    if codage == MANCHESTER:
        pass  # coder_manchester
    if codage == _2B1Q:
        pass  # coder_2B1Q


def coder_NRZ(sequence, echantillonnage, v0=0, v1=1):
    y = []  # contient les tensions correspondant au signal échantilloné codé NRZ
    i = 0  # on commence au bit 0
    for j in range(len(echantillonnage.vec)):  # pour chaque échantillon
        y.append(v0 if sequence.bits[i] == 0 else v1)  # on ajoute la tension correspondant au bit actuel
        if j >= echantillonnage.fech / sequence.debit * (i + 1):  # test pour changer de bit
            i += 1  # on passe au bit suivant
    return y
