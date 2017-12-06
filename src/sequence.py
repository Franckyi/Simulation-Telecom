#!/usr/bin/env python
# coding: utf-8
import numpy.random as random


class Sequence:
    """
    Contient les informations à propos de la séquence (attribut 'bits') et de son débit binaire (attribut 'debit').
    """

    def __init__(self, bits=None, nb_bits=8, debit=1000):
        """
        Construit un objet séquence
        :param bits: Une chaîne de caractères ou une liste de nombres, ne pas remplir pour générer un signal aléatoire
        :param nb_bits: Le nombre de bits du signal aléatoire (8 par défaut), ignoré si vous avez déjà rempli bits
        :param debit: Le débit binaire de la séquence en bit/s (1000 par défaut)
        """
        if bits is None:
            self.bits = generer_aleatoire(nb_bits)
        else:
            if isinstance(bits, str):
                self.bits = verifier_liste(transformer_chaine(bits))
            elif isinstance(bits, list):
                self.bits = verifier_liste(bits)
        self.debit = debit


def generer_aleatoire(n):
    """
    Génère une liste aléatoire de n bits
    :param n: Le nombre de bits
    :return: La liste aléatoire
    """
    return random.randint(2, size=(n,)).tolist()


def transformer_chaine(chaine):
    """
    Transforme une chaîne de caractères en une liste de nombres entiers
    :param chaine: La chaîne de caractères
    :return: La liste de nombres entiers
    """
    liste = []
    for char in chaine:
        liste.append(int(char))
    return liste


def verifier_liste(liste):
    """
    Vérifie si la liste de nombres entiers ne contient que des 0 et des 1
    :param liste:  La liste de nombres entiers
    :return: La liste de nombre entiers
    """
    for nombre in liste:
        if nombre not in [0, 1]:
            raise Exception("La liste contient un caractère autre que 0 ou 1.")
    return liste
