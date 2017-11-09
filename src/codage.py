#!/usr/bin/env python
# coding: utf-8


class Codage:

    def __init__(self, nom):
        self.nom = nom

    def generer_positions(self, sequence):
        pass


class CodageNRZ(Codage):

    def __init__(self, v1, v0=0):
        Codage.__init__(self, "NRZ")
        self.v1 = v1
        self.v0 = v0

    def generer_positions(self, sequence):
        x = []
        y = []
        for i in range(0, len(sequence.bits)):
            y0 = self.v1 if sequence.bits[i] == 1 else self.v0
            x.append((i + 0.0) / sequence.debit)
            y.append(y0)
            x.append((i + 1.0) / sequence.debit)
            y.append(y0)
        return x, y
