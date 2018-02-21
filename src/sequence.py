#!/usr/bin/env python
# coding: utf-8
import numpy.random as random


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


def sequence_chaine(chaine):
    """
    Créé une séquence à partir d'une chaîne de caractères

    :param chaine: La chaîne de caractères
    :return: La séquence
    """
    return verifier_liste(transformer_chaine(chaine))


def sequence_aleatoire(n):
    """
    Créé une séquence aléatoire

    :param n: La taille de la séquence
    :return: La séquence
    """
    return liste_aleatoire(n)


def sequence_pseudo_aleatoire(n, m):
    """
    Créé une séquence pseudo aléatoire

    :param n: La taille de la sous-séquence
    :param m: Le nombre de fois que la sous-séquence est répétée
    :return: La séquence
    """
    bits = []
    bn = liste_aleatoire(n)
    for i in range(m):
        bits.extend(bn)
    return bits
