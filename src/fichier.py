#!/usr/bin/env python
# coding: utf-8
"""
Effectue des simulations depuis un fichier JSON
"""
import json
import sys
from pprint import pprint

import affichage
import canal
import codage
import echantillonnage
import modulation
import outils
import sequence

print
print "############################"
print "#                          #"
print "#        fichier.py        #"
print "#                          #"
print "############################"
print

if len(sys.argv) < 2:
    print "Veuillez passer un fichier en paramètre"
    exit(1)
fichier = sys.argv[1]
print "> Lecture du fichier"
data = json.load(open(fichier))
print "> Affichage du fichier"
print "#####"
pprint(data)
print "#####"

# Séquence
print "> Analyse de la séquence"
if 'sequence' not in data:
    print "!!! Elément 'sequence' introuvable !!!"
    exit(2)
if 'seq' in data['sequence']:
    seq = sequence.sequence_chaine(data['sequence']['seq'])
elif 'repetitions' in data['sequence']:
    seq = sequence.sequence_pseudo_aleatoire(data['sequence']['taille'], data['sequence']['repetitions'])
else:
    seq = sequence.sequence_aleatoire(data['sequence']['taille'])
db = data['sequence']['db']

# Affichage séquence
print "> Analyse de l'affichage de la séquence"
if 'aff_sequence' not in data:
    print "!!! Elément 'aff_sequence' introuvable !!!"
    exit(2)
aff_sequence = data['aff_sequence']
aff_sequence_texte = aff_sequence['sequence']
aff_repartition = 'repartition' in aff_sequence
if aff_repartition:
    bps = aff_sequence['repartition']['bps']

# Codage
has_codage = 'codage' in data
if has_codage:
    print "> Analyse du codage"
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
        print "!!! Codage '{}' inconnu !!!".format(data['codage']['type'])
        exit(3)

    # Affichage codage
    print "> Analyse de l'affichage du codage"
    if 'aff_codage' not in data:
        print "!!! Elément 'aff_codage' introuvable !!!"
        exit(2)
    aff_codage = data['aff_codage']
    aff_chronogramme_codage = 'chronogramme' in aff_codage
    if aff_chronogramme_codage:
        aff_chronogramme_codagej = aff_codage['chronogramme']
        aff_chronogramme_codage_tmin = aff_chronogramme_codagej['tmin'] if 'tmin' in aff_chronogramme_codagej else None
        aff_chronogramme_codage_tmax = aff_chronogramme_codagej['tmax'] if 'tmax' in aff_chronogramme_codagej else None
        aff_chronogramme_codage_vmin = aff_chronogramme_codagej['vmin'] if 'vmin' in aff_chronogramme_codagej else None
        aff_chronogramme_codage_vmax = aff_chronogramme_codagej['vmax'] if 'vmax' in aff_chronogramme_codagej else None
        aff_chronogramme_codage_xlegend = aff_chronogramme_codagej[
            'xlegend'] if 'xlegend' in aff_chronogramme_codagej else None
        aff_chronogramme_codage_ylegend = aff_chronogramme_codagej[
            'ylegend'] if 'ylegend' in aff_chronogramme_codagej else None
        aff_chronogramme_codage_titre = aff_chronogramme_codagej[
            'titre'] if 'titre' in aff_chronogramme_codagej else u"Chronogramme de la séquence codée"
    aff_spectre_codage = 'spectre' in aff_codage
    if aff_spectre_codage:
        aff_spectre_codagej = aff_codage['spectre']
        aff_spectre_codage_fmin = aff_spectre_codagej['fmin'] if 'fmin' in aff_spectre_codagej else None
        aff_spectre_codage_fmax = aff_spectre_codagej['fmax'] if 'fmax' in aff_spectre_codagej else None
        aff_spectre_codage_vmin = aff_spectre_codagej['vmin'] if 'vmin' in aff_spectre_codagej else None
        aff_spectre_codage_vmax = aff_spectre_codagej['vmax'] if 'vmax' in aff_spectre_codagej else None
        aff_spectre_codage_xlegend = aff_spectre_codagej['xlegend'] if 'xlegend' in aff_spectre_codagej else None
        aff_spectre_codage_ylegend = aff_spectre_codagej['ylegend'] if 'ylegend' in aff_spectre_codagej else None
        aff_spectre_codage_titre = aff_spectre_codagej[
            'titre'] if 'titre' in aff_spectre_codagej else u"Spectre de la séquence codée"
    aff_diagramme_oeil = 'diagramme_oeil' in aff_codage
    if aff_diagramme_oeil:
        aff_diagramme_oeilj = aff_codage['diagramme_oeil']
        aff_diagramme_oeil_n = aff_diagramme_oeilj['nb_yeux']
        aff_diagramme_oeil_titre = aff_diagramme_oeilj[
            'titre'] if 'titre' in aff_diagramme_oeilj else u"Diagramme de l'oeil de la séquence codée"

    # Affichage démodulation
    print "> Analyse de l'affichage du codage à travers le canal"
    if 'aff_codage_canal' not in data:
        print "!!! Elément 'aff_codage_canal' introuvable !!!"
        exit(2)
    aff_codage_canal = data['aff_codage_canal']
    aff_chronogramme_codage_canal = 'chronogramme' in aff_codage_canal
    if aff_chronogramme_codage_canal:
        aff_chronogramme_codage_canalj = aff_codage_canal['chronogramme']
        aff_chronogramme_codage_canal_tmin = aff_chronogramme_codage_canalj[
            'tmin'] if 'tmin' in aff_chronogramme_codage_canalj else None
        aff_chronogramme_codage_canal_tmax = aff_chronogramme_codage_canalj[
            'tmax'] if 'tmax' in aff_chronogramme_codage_canalj else None
        aff_chronogramme_codage_canal_vmin = aff_chronogramme_codage_canalj[
            'vmin'] if 'vmin' in aff_chronogramme_codage_canalj else None
        aff_chronogramme_codage_canal_vmax = aff_chronogramme_codage_canalj[
            'vmax'] if 'vmax' in aff_chronogramme_codage_canalj else None
        aff_chronogramme_codage_canal_xlegend = aff_chronogramme_codage_canalj[
            'xlegend'] if 'xlegend' in aff_chronogramme_codage_canalj else None
        aff_chronogramme_codage_canal_ylegend = aff_chronogramme_codage_canalj[
            'ylegend'] if 'ylegend' in aff_chronogramme_codage_canalj else None
        aff_chronogramme_codage_canal_titre = aff_chronogramme_codage_canalj['titre'] \
            if 'titre' in aff_chronogramme_codage_canalj else u"Chronogramme de la séquence codée à travers le canal"
    aff_spectre_codage_canal = 'spectre' in aff_codage_canal
    if aff_spectre_codage_canal:
        aff_spectre_codage_canalj = aff_codage_canal['spectre']
        aff_spectre_codage_canal_fmin = aff_spectre_codage_canalj[
            'fmin'] if 'fmin' in aff_spectre_codage_canalj else None
        aff_spectre_codage_canal_fmax = aff_spectre_codage_canalj[
            'fmax'] if 'fmax' in aff_spectre_codage_canalj else None
        aff_spectre_codage_canal_vmin = aff_spectre_codage_canalj[
            'vmin'] if 'vmin' in aff_spectre_codage_canalj else None
        aff_spectre_codage_canal_vmax = aff_spectre_codage_canalj[
            'vmax'] if 'vmax' in aff_spectre_codage_canalj else None
        aff_spectre_codage_canal_xlegend = aff_spectre_codage_canalj[
            'xlegend'] if 'xlegend' in aff_spectre_codage_canalj else None
        aff_spectre_codage_canal_ylegend = aff_spectre_codage_canalj[
            'ylegend'] if 'ylegend' in aff_spectre_codage_canalj else None
        aff_spectre_codage_canal_titre = aff_spectre_codage_canalj['titre'] \
            if 'titre' in aff_spectre_codage_canalj else u"Spectre de la séquence codée à travers le canal"
    aff_diagramme_oeil_canal = 'diagramme_oeil' in aff_codage_canal
    if aff_diagramme_oeil_canal:
        aff_diagramme_oeil_canalj = aff_codage_canal['diagramme_oeil']
        aff_diagramme_oeil_canal_n = aff_diagramme_oeil_canalj['nb_yeux']
        aff_diagramme_oeil_canal_titre = aff_diagramme_oeil_canalj['titre'] if 'titre' in aff_diagramme_oeil_canalj \
            else u"Diagramme de l'oeil de la séquence codée à travers le canal"


# Modulation
has_modulation = 'modulation' in data
if has_modulation:
    print "> Analyse de la modulation"
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
    # elif data['modulation']['type'] == 'maq':
    #     y_modulation = modulation.moduler_maq(seq, db, ech_modulation, fech_modulation, data['modulation']['v'],
    #                                       data['modulation']['fp'], data['modulation']['p'])
    else:
        print "!!! Modulation '{}' inconnue !!!".format(data['modulation']['type'])
        exit(3)

    # Affichage modulation
    print "> Analyse de l'affichage de la modulation"
    if 'aff_modulation' not in data:
        print "!!! Elément 'aff_modulation' introuvable !!!"
        exit(2)
    aff_modulation = data['aff_modulation']
    aff_chronogramme_modulation = 'chronogramme' in aff_modulation
    if aff_chronogramme_modulation:
        aff_chronogramme_modulationj = aff_modulation['chronogramme']
        aff_chronogramme_modulation_tmin = aff_chronogramme_modulationj[
            'tmin'] if 'tmin' in aff_chronogramme_modulationj else None
        aff_chronogramme_modulation_tmax = aff_chronogramme_modulationj[
            'tmax'] if 'tmax' in aff_chronogramme_modulationj else None
        aff_chronogramme_modulation_vmin = aff_chronogramme_modulationj[
            'vmin'] if 'vmin' in aff_chronogramme_modulationj else None
        aff_chronogramme_modulation_vmax = aff_chronogramme_modulationj[
            'vmax'] if 'vmax' in aff_chronogramme_modulationj else None
        aff_chronogramme_modulation_xlegend = aff_chronogramme_modulationj[
            'xlegend'] if 'xlegend' in aff_chronogramme_modulationj else None
        aff_chronogramme_modulation_ylegend = aff_chronogramme_modulationj[
            'ylegend'] if 'ylegend' in aff_chronogramme_modulationj else None
        aff_chronogramme_modulation_titre = aff_chronogramme_modulationj[
            'titre'] if 'titre' in aff_chronogramme_modulationj else u"Chronogramme de la porteuse modulée"
    aff_spectre_modulation = 'spectre' in aff_modulation
    if aff_spectre_modulation:
        aff_spectre_modulationj = aff_modulation['spectre']
        aff_spectre_modulation_fmin = aff_spectre_modulationj['fmin'] if 'fmin' in aff_spectre_modulationj else None
        aff_spectre_modulation_fmax = aff_spectre_modulationj['fmax'] if 'fmax' in aff_spectre_modulationj else None
        aff_spectre_modulation_vmin = aff_spectre_modulationj['vmin'] if 'vmin' in aff_spectre_modulationj else None
        aff_spectre_modulation_vmax = aff_spectre_modulationj['vmax'] if 'vmax' in aff_spectre_modulationj else None
        aff_spectre_modulation_xlegend = aff_spectre_modulationj[
            'xlegend'] if 'xlegend' in aff_spectre_modulationj else None
        aff_spectre_modulation_ylegend = aff_spectre_modulationj[
            'ylegend'] if 'ylegend' in aff_spectre_modulationj else None
        aff_spectre_modulation_titre = aff_spectre_modulationj[
            'titre'] if 'titre' in aff_spectre_modulationj else u"Spectre de la porteuse modulée"
    aff_constellation = 'constellation' in aff_modulation
    if aff_constellation:
        aff_constellation_j = aff_modulation['spectre']
        aff_constellation_titre = aff_constellation_j[
            'titre'] if 'titre' in aff_constellation_j else u"Constellation de la porteuse modulée"

    # Affichage canal
    print "> Analyse de l'affichage de la modulation à travers le canal"
    if 'aff_modulation_canal' not in data:
        print "!!! Elément 'aff_modulation_canal' introuvable !!!"
        exit(2)
    aff_modulation_canal = data['aff_modulation_canal']
    aff_chronogramme_modulation_canal = 'chronogramme' in aff_modulation_canal
    if aff_chronogramme_modulation_canal:
        aff_chronogramme_modulation_canalj = aff_modulation_canal['chronogramme']
        aff_chronogramme_modulation_canal_tmin = aff_chronogramme_modulation_canalj[
            'tmin'] if 'tmin' in aff_chronogramme_modulation_canalj else None
        aff_chronogramme_modulation_canal_tmax = aff_chronogramme_modulation_canalj[
            'tmax'] if 'tmax' in aff_chronogramme_modulation_canalj else None
        aff_chronogramme_modulation_canal_vmin = aff_chronogramme_modulation_canalj[
            'vmin'] if 'vmin' in aff_chronogramme_modulation_canalj else None
        aff_chronogramme_modulation_canal_vmax = aff_chronogramme_modulation_canalj[
            'vmax'] if 'vmax' in aff_chronogramme_modulation_canalj else None
        aff_chronogramme_modulation_canal_xlegend = aff_chronogramme_modulation_canalj[
            'xlegend'] if 'xlegend' in aff_chronogramme_modulation_canalj else None
        aff_chronogramme_modulation_canal_ylegend = aff_chronogramme_modulation_canalj[
            'ylegend'] if 'ylegend' in aff_chronogramme_modulation_canalj else None
        aff_chronogramme_modulation_canal_titre = aff_chronogramme_modulation_canalj[
            'titre'] if 'titre' in aff_chronogramme_modulation_canalj else \
            u"Chronogramme de la porteuse modulée à travers le canal"
    aff_spectre_modulation_canal = 'spectre' in aff_modulation_canal
    if aff_spectre_modulation_canal:
        aff_spectre_modulation_canalj = aff_modulation_canal['spectre']
        aff_spectre_modulation_canal_fmin = aff_spectre_modulation_canalj[
            'fmin'] if 'fmin' in aff_spectre_modulation_canalj else None
        aff_spectre_modulation_canal_fmax = aff_spectre_modulation_canalj[
            'fmax'] if 'fmax' in aff_spectre_modulation_canalj else None
        aff_spectre_modulation_canal_vmin = aff_spectre_modulation_canalj[
            'vmin'] if 'vmin' in aff_spectre_modulation_canalj else None
        aff_spectre_modulation_canal_vmax = aff_spectre_modulation_canalj[
            'vmax'] if 'vmax' in aff_spectre_modulation_canalj else None
        aff_spectre_modulation_canal_xlegend = aff_spectre_modulation_canalj[
            'xlegend'] if 'xlegend' in aff_spectre_modulation_canalj else None
        aff_spectre_modulation_canal_ylegend = aff_spectre_modulation_canalj[
            'ylegend'] if 'ylegend' in aff_spectre_modulation_canalj else None
        aff_spectre_modulation_canal_titre = aff_spectre_modulation_canalj['titre'] \
            if 'titre' in aff_spectre_modulation_canalj else u"Spectre de la porteuse modulée à travers le canal"
    aff_constellation_canal = 'constellation' in aff_modulation_canal
    if aff_constellation_canal:
        aff_constellation_canalj = aff_modulation_canal['spectre']
        aff_constellation_canal_titre = aff_constellation_canalj['titre'] \
            if 'titre' in aff_constellation_canalj else u"Constellation de la porteuse modulée à travers le canal"

# Canal
print "> Analyse du canal de transmission"
if 'canal' not in data:
    print "!!! Elément 'canal' introuvable !!!"
    exit(2)
has_bruit = 'bruit' in data['canal']
if has_bruit:
    if data['canal']['bruit']['type'] == 'gaussien':
        if has_codage:
            y_codage_bruit = canal.bruit_gaussien(y_codage, data['canal']['bruit']['intensite'])
        if has_modulation:
            y_modulation_bruit = canal.bruit_gaussien(y_modulation, data['canal']['bruit']['intensite'])
    elif data['canal']['bruit']['type'] == 'aleatoire':
        if has_codage:
            y_codage_bruit = canal.bruit_aleatoire(y_codage, data['canal']['bruit']['intensite'])
        if has_modulation:
            y_modulation_bruit = canal.bruit_aleatoire(y_modulation, data['canal']['bruit']['intensite'])

print "#####"
print "> Affichage"

fig = 0

if aff_sequence_texte:
    print "Séquence : " + outils.chaine_binaire(seq)

if aff_repartition:
    print "> Affichage de la répartition de la séquence"
    affichage.figure_sequence(seq, fig, bps)
    fig += 1

if has_codage:
    xf_codage, yf_codage = outils.calculer_spectre(ech_codage, y_codage)
    if has_bruit:
        xf_codage_bruit, yf_codage_bruit = outils.calculer_spectre(ech_codage, y_codage_bruit)
        if aff_chronogramme_codage:
            aff_chronogramme_codage_tmin = min(
                ech_codage) if aff_chronogramme_codage_tmin is None else aff_chronogramme_codage_tmin
            aff_chronogramme_codage_tmax = max(
                ech_codage) if aff_chronogramme_codage_tmax is None else aff_chronogramme_codage_tmax
            aff_chronogramme_codage_vmin = min(
                y_codage_bruit) if aff_chronogramme_codage_vmin is None else aff_chronogramme_codage_vmin
            aff_chronogramme_codage_vmax = max(
                y_codage_bruit) if aff_chronogramme_codage_vmax is None else aff_chronogramme_codage_vmax
        if aff_spectre_codage:
            aff_spectre_codage_fmin = min(
                xf_codage_bruit) if aff_spectre_codage_fmin is None else aff_spectre_codage_fmin
            aff_spectre_codage_fmax = max(
                xf_codage_bruit) if aff_spectre_codage_fmax is None else aff_spectre_codage_fmax
            aff_spectre_codage_vmin = min(
                yf_codage_bruit) if aff_spectre_codage_vmin is None else aff_spectre_codage_vmin
            aff_spectre_codage_vmax = max(
                yf_codage_bruit) if aff_spectre_codage_vmax is None else aff_spectre_codage_vmax
    y = y_codage_bruit if has_bruit else y_codage
    xf = xf_codage_bruit if has_bruit else xf_codage
    yf = yf_codage_bruit if has_bruit else yf_codage
    aff_diagramme_oeil_vmin = min(y_codage_bruit) if has_bruit else min(y_codage)
    aff_diagramme_oeil_vmax = max(y_codage_bruit) if has_bruit else max(y_codage)
    if aff_chronogramme_codage:
        print "> Affichage du chronogramme de la séquence codée"
        affichage.figure_chronogramme(ech_codage, y_codage, fig, aff_chronogramme_codage_titre,
                                      aff_chronogramme_codage_xlegend, aff_chronogramme_codage_ylegend,
                                      aff_chronogramme_codage_tmin, aff_chronogramme_codage_tmax,
                                      aff_chronogramme_codage_vmin, aff_chronogramme_codage_vmax)
        fig += 1
    if aff_spectre_codage:
        print "> Affichage du spectre de la séquence codée"
        affichage.figure_spectre(xf_codage, yf_codage, fig, aff_spectre_codage_titre,
                                 aff_spectre_codage_xlegend, aff_spectre_codage_ylegend,
                                 aff_spectre_codage_fmin, aff_spectre_codage_fmax,
                                 aff_spectre_codage_vmin, aff_spectre_codage_vmax)
        fig += 1
    if aff_diagramme_oeil:
        print "> Affichage du diagramme de l'oeil de la séquence codée"
        affichage.figure_diagramme_oeil(ech_codage, y_codage, fig, seq, aff_diagramme_oeil_vmin,
                                        aff_diagramme_oeil_vmax, aff_diagramme_oeil_n, aff_diagramme_oeil_titre)
        fig += 1
    if aff_chronogramme_codage_canal:
        print "> Affichage du chronogramme de la séquence codée à travers le canal"
        affichage.figure_chronogramme(ech_codage, y, fig, aff_chronogramme_codage_canal_titre,
                                      aff_chronogramme_codage_canal_xlegend, aff_chronogramme_codage_canal_ylegend,
                                      aff_chronogramme_codage_canal_tmin, aff_chronogramme_codage_canal_tmax,
                                      aff_chronogramme_codage_canal_vmin, aff_chronogramme_codage_canal_vmax)
        fig += 1
    if aff_spectre_codage_canal:
        print "> Affichage du spectre de la séquence codée à travers le canal"
        affichage.figure_spectre(xf, yf, fig, aff_spectre_codage_canal_titre,
                                 aff_spectre_codage_canal_xlegend, aff_spectre_codage_canal_ylegend,
                                 aff_spectre_codage_canal_fmin, aff_spectre_codage_canal_fmax,
                                 aff_spectre_codage_canal_vmin, aff_spectre_codage_canal_vmax)
        fig += 1
    if aff_diagramme_oeil_canal:
        print "> Affichage du diagramme de l'oeil de la séquence codée à travers le canal"
        affichage.figure_diagramme_oeil(ech_codage, y, fig, seq, aff_diagramme_oeil_vmin, aff_diagramme_oeil_vmax,
                                        aff_diagramme_oeil_canal_n, aff_diagramme_oeil_canal_titre)
        fig += 1

if has_modulation:
    xf_modulation, yf_modulation = outils.calculer_spectre(ech_modulation, y_modulation)
    if has_bruit:
        xf_modulation_bruit, yf_modulation_bruit = outils.calculer_spectre(ech_modulation, y_modulation_bruit)
        if aff_chronogramme_modulation:
            aff_chronogramme_modulation_tmin = min(
                ech_modulation) if aff_chronogramme_modulation_tmin is None else aff_chronogramme_modulation_tmin
            aff_chronogramme_modulation_tmax = max(
                ech_modulation) if aff_chronogramme_modulation_tmax is None else aff_chronogramme_modulation_tmax
            aff_chronogramme_modulation_vmin = min(
                y_modulation_bruit) if aff_chronogramme_modulation_vmin is None else aff_chronogramme_modulation_vmin
            aff_chronogramme_modulation_vmax = max(
                y_modulation_bruit) if aff_chronogramme_modulation_vmax is None else aff_chronogramme_modulation_vmax
        if aff_spectre_modulation:
            aff_spectre_modulation_fmin = min(
                xf_modulation_bruit) if aff_spectre_modulation_fmin is None else aff_spectre_modulation_fmin
            aff_spectre_modulation_fmax = max(
                xf_modulation_bruit) if aff_spectre_modulation_fmax is None else aff_spectre_modulation_fmax
            aff_spectre_modulation_vmin = min(
                yf_modulation_bruit) if aff_spectre_modulation_vmin is None else aff_spectre_modulation_vmin
            aff_spectre_modulation_vmax = max(
                yf_modulation_bruit) if aff_spectre_modulation_vmax is None else aff_spectre_modulation_vmax
    y = y_modulation_bruit if has_bruit else y_modulation
    xf = xf_modulation_bruit if has_bruit else xf_modulation
    yf = yf_modulation_bruit if has_bruit else yf_modulation
    if aff_chronogramme_modulation:
        print "> Affichage du chronogramme de la porteuse modulée"
        affichage.figure_chronogramme(ech_modulation, y_modulation, fig, aff_chronogramme_modulation_titre,
                                      aff_chronogramme_modulation_xlegend, aff_chronogramme_modulation_ylegend,
                                      aff_chronogramme_modulation_tmin, aff_chronogramme_modulation_tmax,
                                      aff_chronogramme_modulation_vmin, aff_chronogramme_modulation_vmax)
        fig += 1
    if aff_spectre_modulation:
        print "> Affichage du spectre de la porteuse modulée"
        affichage.figure_spectre(xf_modulation, yf_modulation, fig, aff_spectre_modulation_titre,
                                 aff_spectre_modulation_xlegend, aff_spectre_modulation_ylegend,
                                 aff_spectre_modulation_fmin, aff_spectre_modulation_fmax,
                                 aff_spectre_modulation_vmin, aff_spectre_modulation_vmax)
        fig += 1
    if aff_constellation:
        print "> Affichage de la constellation de la porteuse modulée"
        affichage.figure_constellation()
        fig += 1
    if aff_chronogramme_modulation_canal:
        print "> Affichage du chronogramme de la séquence codée à travers le canal"
        affichage.figure_chronogramme(ech_modulation, y, fig, aff_chronogramme_modulation_canal_titre,
                                      aff_chronogramme_modulation_canal_xlegend,
                                      aff_chronogramme_modulation_canal_ylegend,
                                      aff_chronogramme_modulation_canal_tmin, aff_chronogramme_modulation_canal_tmax,
                                      aff_chronogramme_modulation_canal_vmin, aff_chronogramme_modulation_canal_vmax)
        fig += 1
    if aff_spectre_modulation_canal:
        print "> Affichage du spectre de la séquence codée à travers le canal"
        affichage.figure_spectre(xf, yf, fig, aff_spectre_modulation_canal_titre,
                                 aff_spectre_modulation_canal_xlegend, aff_spectre_modulation_canal_ylegend,
                                 aff_spectre_modulation_canal_fmin, aff_spectre_modulation_canal_fmax,
                                 aff_spectre_modulation_canal_vmin, aff_spectre_modulation_canal_vmax)
        fig += 1
    if aff_constellation_canal:
        print "> Affichage de la constellation de la porteuse modulée à travers le canal"
        affichage.figure_constellation()
        fig += 1

print "> Affichage en cours..."
affichage.afficher()
