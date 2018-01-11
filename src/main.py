#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt
import numpy as np

import codage
import echantillonnage
import modulation
import sequence


def verif_non_nul(s):
    return s is not None


def verif_nombre(s):
    try:
        float(s)
        return verif_non_nul(s)
    except ValueError:
        return False


def verif_entier(s):
    try:
        int(s)
        return verif_non_nul(s)
    except ValueError:
        return False


def verif_nombre_positif(s):
    try:
        return float(s) > 0.
    except ValueError:
        return False


def verif_entier_positif(s):
    try:
        return int(s) > 0
    except ValueError:
        return False


def verif_chaine_binaire(s):
    for char in s:
        if char not in ("0", "1"):
            return False
    return True


def verif_choix(s, valeurs):
    try:
        return int(s) in valeurs
    except ValueError:
        return False


def format_string(s):
    return s


def format_int(s):
    return int(s)


def format_float(s):
    try:
        return float(s)
    except ValueError:
        return float(int(s))


def entree(prompt="string? ", default=None, verif=verif_non_nul, format=format_string, args=None):
    s = raw_input(prompt)
    if s in ["quit", "exit"]:
        print "Au revoir !"
        quit(0)
    if s == "" and default is not None:
        return default
    try:
        if verif(s):
            return format(s)
    except TypeError:
        if verif(s, args):
            return format(s)
    print "Choix incorrect !"
    return entree(prompt, default, verif, format, args)


def entree_entier_positif(default):
    return entree(prompt="int+? ", default=default, verif=verif_entier_positif, format=format_int)


def entree_nombre_positif(default):
    return entree(prompt="float+? ", default=default, verif=verif_nombre_positif, format=format_float)


def entree_choix(n):
    return entree(prompt="[1-{}] ".format(n), verif=verif_choix, format=format_int, args=range(1, n + 1))


def main():
    print "   _____ _                 _       _   _             "
    print "  / ____(_)               | |     | | (_)            "
    print " | (___  _ _ __ ___  _   _| | __ _| |_ _  ___  _ __  "
    print "  \___ \| | '_ ` _ \| | | | |/ _` | __| |/ _ \| '_ \ "
    print "  ____) | | | | | | | |_| | | (_| | |_| | (_) | | | |"
    print " |_____/|_|_| |_| |_|\__,_|_|\__,_|\__|_|\___/|_| |_|"
    print "        _______   _                                  "
    print "       |__   __| | |                                 "
    print "          | | ___| | ___  ___ ___  _ __ ___          "
    print "          | |/ _ \ |/ _ \/ __/ _ \| '_ ` _ \         "
    print "          | |  __/ |  __/ (_| (_) | | | | | |        "
    print "          |_|\___|_|\___|\___\___/|_| |_| |_|        "


def info():
    print u"Simulation Télécom v0.1 par la Fougère"
    print
    print u"Bienvenue dans Simulation Télécom ! Ce programme vous permet de simuler une chaîne de transmission numérique."
    print
    print u"Pour l'instant, le programme possède les fonctionnalités suivantes :"
    print u"- Génération de séquences aléatoires et pseudo-aléatoires"
    print u"- Échantillonnage d'un signal"
    print u"- Codage d'un signal : NRZ, RZ, Manchester, 2B1Q ; affichage sous forme d'un chronogramme"
    print u"- Modulation d'un signal : ASK, PSK, FSK ; affichage sous forme d'un chronogramme"
    print
    print u"Les fonctionnalités planifiées sont les suivantes :"
    print u"- Affichage sous forme de spectre, et sous forme de constellation pour les modulations"
    print u"- Simulation du canal de transmission (bruit, filtre passe-bas)"
    print u"- Interface graphique"
    print
    print "Pour quitter le programme, tapez 'quit' ou 'exit'."


def creer_sequence():
    val = entree_choix(2)
    if val == 1:
        print u"Choisir le nombre de bits que contient la séquence : [default=8]"
        nb_bits = entree_entier_positif(8)
        print u"Choisir le débit du signal (en Hertz) : [default=1000.0]"
        debit = entree_nombre_positif(1000.)
        s = sequence.sequence_aleatoire(nb_bits, debit)
        print u"Séquence générée : " + s.__str__()
        return s
    elif val == 2:
        print u"Entrer la séquence donnée :"
        bits = entree(prompt="{0,1}.?", verif=verif_chaine_binaire)
        print u"Choisir le débit du signal (en Hertz) : [default=1000.0]"
        debit = entree_nombre_positif(1000.)
        return sequence.sequence_chaine(bits, debit)
    else:
        print "Choix incorrect !"
        return creer_sequence()


def afficher(seq, x, y, legende, titre):
    p, = plt.plot(x, y)  # création du graphique
    plt.title(titre + " : " + seq.__str__())  # titre du graphique
    plt.xlabel("Temps (s)")  # légende abscisses
    plt.ylabel("Tension (V)")  # légende ordonnées
    plt.legend([p], [legende])  # nom de la série de données
    plt.show()  # affichage


def nrz(seq, ech):
    print
    print u"Choisir la tension V0 : [default=0.0]"
    v0 = entree_nombre_positif(0.)
    print u"Choisir la tension V1 : [default=1.0]"
    v1 = entree_nombre_positif(1.)
    return codage.coder_nrz(seq, ech, v0, v1)


def rz(seq, ech):
    print
    print u"Choisir la tension V : [default=1.0]"
    v = entree_nombre_positif(1.)
    return codage.coder_rz(seq, ech, v)


def manchester(seq, ech):
    print
    print u"Choisir la tension V+ : [default=1.0]"
    v0 = entree_nombre_positif(1.)
    print u"Choisir la tension V- : [default=-1.0]"
    v1 = entree_nombre_positif(-1.)
    return codage.coder_manchester(seq, ech, v0, v1)


def _2b1q(seq, ech):
    print
    print u"Choisir la tension V : [default=1.0]"
    v = entree_nombre_positif(1.)
    return codage.coder_2b1q(seq, ech, v)


def _codage(seq, ech):
    c = entree_choix(4)
    if c == 1:
        y = nrz(seq, ech)
        nom = "NRZ"
    elif c == 2:
        y = rz(seq, ech)
        nom = "RZ"
    elif c == 3:
        y = manchester(seq, ech)
        nom = "Manchester"
    elif c == 4:
        y = _2b1q(seq, ech)
        nom = "2B1Q"
    else:
        print "Choix incorrect !"
        _codage(seq, ech)
        return
    afficher(seq, ech.vec, y, nom, u"Signal échantillonné codé {}".format(nom))


def ask(seq, ordre):
    print u"Choisir une fréquence porteuse : [default=1000.0]"
    fp = entree_nombre_positif(1000.)
    args = []
    for i in range(ordre):
        print u"Choisir une amplitude ({}/{}) :".format(i, ordre)
        args.append(entree_nombre_positif(None))
    return modulation.moduler_ask(seq, fp, args)


def fsk(seq, ordre):
    args = []
    for i in range(ordre):
        print u"Choisir une fréquence ({}/{}) :".format(i, ordre)
        args.append(entree_nombre_positif(None))
    return modulation.moduler_fsk(seq, args)


def psk(seq, ordre):
    print u"Choisir une fréquence porteuse : [default=1000.0]"
    fp = entree_nombre_positif(1000.)
    args = []
    for i in range(ordre):
        print u"Choisir une phase (automatiquement multiplié par PI) ({}/{}) :".format(i, ordre)
        args.append(entree(prompt="float? ", verif=verif_nombre, format=format_float) * np.pi)
    return modulation.moduler_psk(seq, fp, args)


def _modulation(seq):
    m = entree_choix(3)
    if m in range(1, 4):
        print u"Choisir l'ordre de la modulation : [default=2]"
        ordre = entree_entier_positif(2)
        try:
            modulation.verifier_parametres(ordre)
        except Exception as e:
            print e.message
            _modulation(seq)
            return
        if m == 1:
            x, y = ask(seq, ordre)
            nom = "ASK"
        elif m == 2:
            x, y = fsk(seq, ordre)
            nom = "FSK"
        else:
            x, y = psk(seq, ordre)
            nom = "PSK"
        afficher(seq, x, y, nom, u"Signal échantillonné modulé {}".format(nom))
    else:
        print "Choix incorrect !"
        _modulation(seq)
        return


def actions(seq):
    a = entree_choix(2)
    if a == 1:
        print
        print u"Avant de coder, veuillez choisir une fréquence d'échantillonnage : [default=20000.0]"
        fech = entree_nombre_positif(20000.)
        ech = echantillonnage.creer_echantillons(seq, fech)
        print
        print "------"
        print
        print u"Étape 3 : Codage"
        print u"Quel codage voulez-vous utiliser ?"
        print u"1) NRZ"
        print u"2) RZ"
        print u"3) Manchester"
        print u"4) 2B1Q"
        _codage(seq, ech)
    elif a == 2:
        print
        print "------"
        print
        print u"Étape 3 : Modulation"
        print u"Quelle modulation voulez-vous utiliser ?"
        print u"1) ASK"
        print u"2) FSK"
        print u"3) PSK"
        _modulation(seq)
    else:
        print "Choix incorrect !"
        return actions(seq)


main()
print
print "------"
print
info()
print
entree(u"Appuyez sur [Entrée] pour commencer...")
print "------"
print
print u"Étape 1 : Création de la séquence"
print u"Voulez vous générer une séquence aléatoire ou utiliser une séquence donnée ?"
print u"1) Générer une séquence aléatoire"
print u"2) Utiliser une séquence donnée"
_seq = creer_sequence()
print
print "------"
print
print u"Étape 2 : Actions"
print u"Que voulez-vous faire avec cette séquence ?"
print u"1) Coder la séquence"
print u"2) Moduler la séquence"
actions(_seq)
