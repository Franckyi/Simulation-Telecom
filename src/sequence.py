#!/usr/bin/env python
# coding: utf-8
import numpy.random as random


class Sequence:
    """
    Contient les informations à propos de la séquence (attribut 'bits') et de son débit binaire (attribut 'debit').
    """

    def __init__(self, bits, debit):
        """
        Construit un objet séquence

        :param bits: Une liste de nombres ; si elle contient un nombre autre que 0 ou 1, une Exception est levée
        :param debit: Le débit binaire de la séquence (en bit/s)
        """
        self.bits = verifier_liste(bits)
        self.debit = debit

    def __str__(self):
        chaine = ""
        for bit in self.bits:
            chaine += str(bit)
        return chaine


def liste_aleatoire(n):
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


def sequence_chaine(chaine, debit=1000):
    """
    Créé une séquence à partir d'une chaîne de caractères

    :param chaine: La chaîne de caractères
    :param debit: Le débit binaire de la séquence
    :return: La séquence
    """
    return Sequence(transformer_chaine(chaine), debit)


def sequence_aleatoire(nb_bits=8, debit=1000):
    """
    Créé une séquence aléatoire

    :param nb_bits: La taille de la séquence
    :param debit: Le débit binaire de la séquence
    :return: La séquence
    """
    return Sequence(liste_aleatoire(nb_bits), debit)


def sequence_pseudo_aleatoire(n, m, debit):
    """
    Créé une séquence pseudo aléatoire

    :param n: La taille de la sous-séquence
    :param m: Le nombre de fois que la sous-séquence est répétée
    :param debit: Le débit binaire de la séquence
    :return: La séquence
    """
    bits = []
    for i in range(m):
        bits.extend(liste_aleatoire(n))
    return Sequence(bits, debit)
