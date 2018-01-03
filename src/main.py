#!/usr/bin/env python
# coding: utf-8
import sequence


def verif_non_nul(s):
    return s is not None


def verif_entier(s):
    try:
        int(s)
        return True
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


def entree(prompt="string? ", default=None, verif=verif_non_nul, format=format_string, args=None):
    s = raw_input(prompt)
    if s in ["quit", "exit"]:
        print "Au revoir !"
        quit(0)
    if s == "":
        return default
    try:
        if verif(s):
            return format(s)
    except TypeError:
        if verif(s, args):
            return format(s)
    print "Choix incorrect !"
    return entree(prompt, default, verif, args)


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
    val = entree(prompt="{1,2}? ", verif=verif_choix, args=[1, 2])
    if val == "1":
        print u"Choisir le nombre de bits que contient la séquence : [default=8]"
        nb_bits = entree(prompt="int+? ", default=8, verif=verif_entier_positif, format=format_int)
        print u"Choisir le débit du signal (en Hertz) : [default=1000]"
        debit = entree(prompt="int+? ", default=1000, verif=verif_entier_positif, format=format_int)
        return sequence.sequence_aleatoire(nb_bits, debit)
    if val == "2":
        print u"Entrer la séquence donnée :"
        bits = entree(prompt="{0,1}.?", verif=verif_chaine_binaire)
        print u"Choisir le débit du signal (en Hertz) : [default=1000]"
        debit = entree(prompt="int+? ", default=1000, verif=verif_entier_positif, format=format_int)
        return sequence.sequence_chaine(bits, debit)
    else:
        print "Choix incorrect !"
        return creer_sequence()


main()
print
print "------"
print
info()
print
print u"Appuyez sur [Entrée] pour commencer..."
entree("")
print "------"
print
print u"Étape 1 : Création de la séquence"
print u"Voulez vous générer une séquence aléatoire ou utiliser une séquence donnée ?"
print u"1) Générer une séquence aléatoire"
print u"2) Utiliser une séquence donnée"
seq = creer_sequence()
print
print "------"
