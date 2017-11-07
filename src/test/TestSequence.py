#!/usr/bin/env python
# coding: utf-8
from sequence import Sequence

print "Séquence par défaut (aléatoire de 8 bits, débit de 1 kbit/s)"
s = Sequence()
print(s.bits, s.debit)
print

print "Séquence aléatoire de 4 bits à 200 bit/s"
s = Sequence(nb_bits=4, debit=200)
print(s.bits, s.debit)
print

print "Séquence donnée à partir d'une chaîne (à 1kbit/s)"
s = Sequence(bits="01010101")
print(s.bits, s.debit)
print

print "Séquence donnée à partir d'une liste à 2 kbit/s"
s = Sequence(bits=[1, 0, 1, 0, 1, 0, 1, 0, 1, 0], debit=2000)
print(s.bits, s.debit)
print

print "Séquence erronée #1"
try:
    s = Sequence(bits="11001200")
except Exception as e:
    print e.message
print

print "Séquence erronée #2"
try:
    s = Sequence(bits="erreur")
except Exception as e:
    print e.message
print
