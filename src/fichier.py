#!/usr/bin/env python
# coding: utf-8
"""
Effectue des simulations depuis un fichier JSON
"""
import json
import sys
from pprint import pprint

import affichage
import codage
import echantillonnage
import modulation
import sequence

if len(sys.argv) < 2:
    print "Veuillez passer un fichier en paramètre"
    exit(1)
fichier = sys.argv[1]
data = json.load(open(fichier))
pprint(data)

# Séquence
if 'sequence' not in data:
    print "Elément 'sequence' introuvable"
    exit(2)
if 'seq' in data['sequence']:
    seq = sequence.sequence_chaine(data['sequence']['seq'])
elif 'repetitions' in data['sequence']:
    seq = sequence.sequence_pseudo_aleatoire(data['sequence']['taille'], data['sequence']['repetitions'])
else:
    seq = sequence.sequence_aleatoire(data['sequence']['taille'])
db = data['sequence']['db']
aff = data['sequence']['aff']

# Codage
has_codage = 'codage' in data
if has_codage:
    fech_codage = data['codage']['fech']
    ech_codage = echantillonnage.creer_echantillons(seq, db, fech_codage)
    if data['codage']['type'] == 'nrz':
        y_codage = codage.coder_nrz(seq, db, ech_codage, fech_codage, data['codage']['v0'], data['codage']['v1'])
    elif data['codage']['type'] == 'rz':
        y_codage = codage.coder_rz(seq, db, ech_codage, fech_codage, data['codage']['v0'], data['codage']['v1'])
    elif data['codage']['type'] == 'manchester':
        y_codage = codage.coder_manchester(seq, db, ech_codage, fech_codage, data['codage']['vp'], data['codage']['vm'])
    elif data['codage']['type'] == '2b1q':
        if 'vmax' in data['codage']:
            y_codage = codage.coder_2b1q_max(seq, db, ech_codage, fech_codage, data['codage']['vmax'])
        else:
            y_codage = codage.coder_2b1q(seq, db, ech_codage, fech_codage, data['codage']['v00'], data['codage']['v01'],
                                         data['codage']['v10'], data['codage']['v11'])
    else:
        print "Codage '{}' inconnu".format(data['codage']['type'])
        exit(3)
    chronogramme_codage = data['codage']['chronogramme']
    spectre_codage = data['codage']['spectre']
    diagramme_oeil_codage = data['codage']['diagramme_oeil']

# Modulation
has_modulation = 'modulation' in data
if has_modulation:
    fech_modulation = data['modulation']['fech']
    ech_modulation = echantillonnage.creer_echantillons(seq, db, fech_modulation)
    if data['modulation']['type'] == 'ask':
        y_modulation = modulation.moduler_ask(seq, db, ech_modulation, fech_modulation, data['modulation']['fp'],
                                              data['modulation']['v'])
    elif data['modulation']['type'] == 'fsk':
        y_modulation = modulation.moduler_fsk(seq, db, ech_modulation, fech_modulation, data['modulation']['v'],
                                              data['modulation']['f'])
    elif data['modulation']['type'] == 'psk':
        y_modulation = modulation.moduler_psk(seq, db, ech_modulation, fech_modulation, data['modulation']['v'],
                                              data['modulation']['fp'], data['modulation']['p'])
    elif data['modulation']['type'] == 'maq':
        y_modulation = modulation.moduler_maq(seq, db, ech_modulation, fech_modulation, data['modulation']['v'],
                                          data['modulation']['fp'], data['modulation']['p'])
    else:
        print "Modulation '{}' inconnue".format(data['modulation']['type'])
        exit(3)
    chronogramme_modulation = data['modulation']['chronogramme']
    spectre_modulation = data['modulation']['spectre']
    constellation_modulation = data['modulation']['constellation']

# Canal

fig = 0

if aff:
    affichage.figure_sequence(seq, fig)
    fig += 1

if has_codage:
    if chronogramme_codage:
        affichage.figure_chronogramme(ech_codage, y_codage, u"Chronogramme du signal codé", fig)
        fig += 1

if has_modulation:
    if chronogramme_modulation:
        affichage.figure_chronogramme(ech_modulation, y_modulation, u"Chronogramme de la porteuse modulée", fig)
        fig += 1

affichage.afficher()
