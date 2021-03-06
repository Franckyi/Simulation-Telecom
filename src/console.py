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
        print u"Choisir le débit du signal (en bit/s) : [default=1000.0]"
        db = entree_nombre_positif(1000.)
        seq = sequence.sequence_aleatoire(nb_bits)
        print u"Séquence générée : " + seq.__str__()
        return seq, db
    elif val == 2:
        print u"Entrer la séquence donnée :"
        bits = entree(prompt="{0,1}.?", verif=verif_chaine_binaire)
        print u"Choisir le débit du signal (en bit/s) : [default=1000.0]"
        db = entree_nombre_positif(1000.)
        return sequence.sequence_chaine(bits), db
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


def nrz(seq, db, ech, fech):
    print
    print u"Choisir la tension V0 : [default=0.0]"
    v0 = entree_nombre_positif(0.)
    print u"Choisir la tension V1 : [default=1.0]"
    v1 = entree_nombre_positif(1.)
    return codage.coder_nrz(seq, db, ech, fech, v0, v1)


def rz(seq, db, ech, fech):
    print
    print u"Choisir la tension V0 : [default=-1.0]"
    v0 = entree_nombre_positif(-1.)
    print u"Choisir la tension V1 : [default=1.0]"
    v1 = entree_nombre_positif(1.)
    return codage.coder_rz(seq, db, ech, fech, v0, v1)


def manchester(seq, db, ech, fech):
    print
    print u"Choisir la tension V+ : [default=1.0]"
    v0 = entree_nombre_positif(1.)
    print u"Choisir la tension V- : [default=-1.0]"
    v1 = entree_nombre_positif(-1.)
    return codage.coder_manchester(seq, db, ech, fech, v0, v1)


def _2b1q(seq, db, ech, fech):
    print
    print u"Choisir la tension V : [default=1.0]"
    v = entree_nombre_positif(1.)
    return codage.coder_2b1q_max(seq, db, ech, fech, v)


def _codage(seq, db, ech, fech):
    c = entree_choix(4)
    if c == 1:
        y = nrz(seq, db, ech, fech)
        nom = "NRZ"
    elif c == 2:
        y = rz(seq, db, ech, fech)
        nom = "RZ"
    elif c == 3:
        y = manchester(seq, db, ech, fech)
        nom = "Manchester"
    elif c == 4:
        y = _2b1q(seq, db, ech, fech)
        nom = "2B1Q"
    else:
        print "Choix incorrect !"
        _codage(seq, db, ech, fech)
        return
    afficher(seq, ech, y, nom, u"Signal échantillonné codé {}".format(nom))


def ask(seq, db, ordre):
    print u"Choisir une fréquence porteuse (Hz) : [default=1000.0]"
    fp = entree_nombre_positif(1000.)
    args = []
    for i in range(ordre):
        print u"Choisir une amplitude (V) ({}/{}) :".format(i+1, ordre)
        args.append(entree_nombre_positif(None))
    return modulation.moduler_ask(seq, db, fp, args)


def fsk(seq, db, ordre):
    print u"Choisir une amplitude (V) : [default=1.0]"
    v = entree_nombre_positif(1.)
    args = []
    for i in range(ordre):
        print u"Choisir une fréquence (Hz) ({}/{}) :".format(i+1, ordre)
        args.append(entree_nombre_positif(None))
    return modulation.moduler_fsk(seq, db, v, args)


def psk(seq, db, ordre):
    print u"Choisir une fréquence porteuse (Hz): [default=1000.0]"
    fp = entree_nombre_positif(1000.)
    print u"Choisir une amplitude (V): [default=1.0]"
    v = entree_nombre_positif(1.)
    args = []
    for i in range(ordre):
        print u"Choisir une phase (automatiquement multiplié par PI) ({}/{}) :".format(i+1, ordre)
        args.append(entree(prompt="float? ", verif=verif_nombre, format=format_float) * np.pi)
    return modulation.moduler_psk(seq, db, v, fp, args)

def maq(seq, db, ordre):
    print u"Choisir une fréquence porteuse (Hz) : [default=1000.0]"
    fp = entree_nombre_positif(1000.)
    args = []
    for i in range(ordre/2):
        args.append((i + 1) * 2.)
        args.append((i + 1) * - 2.)
    return modulation.moduler_maq(seq, db, fp, args)


def _modulation(seq, db):
    m = entree_choix(4)
    if m in range(1, 5):
        print u"Choisir l'ordre de la modulation : [default=2]"
        ordre = entree_entier_positif(2) #trouver un façon de prendre en compte la maq (MAQ 4 / MAQ 16 etc)
        try:
            modulation.verifier_parametres(ordre)
        except Exception as e:
            print e.message
            _modulation(seq, db)
            return
        if m == 1:
            x, y = ask(seq, db, ordre)
            nom = "ASK"
        elif m == 2:
            x, y = fsk(seq, db, ordre)
            nom = "FSK"
        elif m == 3:
            x, y = psk(seq, db, ordre)
            nom = "PSK"
        else:
            x,y = maq(seq,db,ordre)
            nom = "MAQ"

        afficher(seq, x, y, nom, u"Signal échantillonné modulé {}".format(nom))
    else:
        print "Choix incorrect !"
        _modulation(seq, db)
        return


def actions(seq, db):
    a = entree_choix(2)
    if a == 1:
        print
        print u"Avant de coder, veuillez choisir une fréquence d'échantillonnage : [default=20000.0]"
        fech = entree_nombre_positif(20000.)
        ech = echantillonnage.creer_echantillons(seq, db, fech)
        print
        print "------"
        print
        print u"Étape 3 : Codage"
        print u"Quel codage voulez-vous utiliser ?"
        print u"1) NRZ (Non-Return to Zero)"
        print u"2) RZ (Return to Zero)"
        print u"3) Manchester"
        print u"4) 2B1Q (2 Binary 1 Quaterary)"
        _codage(seq, db, ech, fech)
    elif a == 2:
        print
        print "------"
        print
        print u"Étape 3 : Modulation"
        print u"Quelle modulation voulez-vous utiliser ?"
        print u"1) ASK (Modulation d'amplitude)"
        print u"2) FSK (Modulation de fréquence)"
        print u"3) PSK (Modulation de phase)"
        print u"4) MAQ (Modulation d'amplitude en quadrature)"
        _modulation(seq, db)
    else:
        print "Choix incorrect !"
        return actions(seq, db)


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
_seq, _db = creer_sequence()
print
print "------"
print
print u"Étape 2 : Actions"
print u"Que voulez-vous faire avec cette séquence ?"
print u"1) Coder la séquence"
print u"2) Moduler la séquence"
actions(_seq, _db)
