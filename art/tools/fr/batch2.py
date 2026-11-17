"""Batch 2: Kestrel (Lance base), Juno (May base), player back sprites."""
import sys
import numpy as np
from fs import *
from ow_fr import rows
from pc_a import JACK, TEAL, HAIR as HAIR_A
from pc_b import HAIR as HAIR_B

K_HAIR = ['#20202e', '#34334a', '#4e4d68', '#6e6c8c']
K_COAT = ['#1c1a24', '#2e2c3a', '#46445a']
K_SHIRT = ['#5a1e2a', '#8c2f3a', '#b04a52']
K_LINING = '#4a1e28'
J_HAIR = ['#5e2412', '#8e3c1e', '#b9542a', '#d8763e']
J_KER = ['#8a5c16', '#c48a28', '#e8b448']
J_DRESS = ['#3e5a2c', '#5a7a40', '#7c9c5a']
J_GLOVE = ['#8a6a44', '#d9b77c']


def kestrel():
    a = T('ELITEFOUR_Lance')
    hair = rect(a, 14, 0, 50, 15)
    a = remap(a, {'#a84840': K_HAIR[0], '#c05848': K_HAIR[1], '#e06858': K_HAIR[2], '#f09078': K_HAIR[3]}, hair)
    a = remap(a, {'#a84840': K_SHIRT[0], '#c05848': K_SHIRT[1], '#e06858': K_SHIRT[2]}, ~hair)
    a = remap(a, {'#383858': K_COAT[0], '#585880': K_COAT[1], '#7878a0': K_COAT[2], '#684848': K_LINING})
    a = remap(a, {'#f8e0c8': K_HAIR[3], '#e0b890': K_HAIR[3], '#c89878': K_HAIR[2]}, rect(a, 14, 0, 50, 8))
    return a


def kestrel_ow():
    a = C('trainer_ELITEFOUR_Lance')
    head = rows(a, 0, 10)
    a = remap(a, {'#e66b4a': K_HAIR[2], '#943a29': K_HAIR[1], '#521000': K_HAIR[0]}, head)
    a = remap(a, {'#e66b4a': K_SHIRT[1], '#943a29': K_SHIRT[0], '#521000': '#2a1018', '#7b4242': K_LINING,
                  '#4a4a5a': K_COAT[0], '#8c8c94': K_COAT[2]}, ~head)
    return a


def juno():
    a = T('POKEMONTRAINER_May')
    head = rect(a, 0, 0, 63, 16)
    hair = rect(a, 0, 0, 63, 31)
    a = remap(a, {'#c04040': J_KER[0], '#f86058': J_KER[2], '#f8f8f8': '#f8e8b0', '#c8c8d8': J_KER[1]}, head)
    a = remap(a, {'#483038': J_HAIR[0], '#785850': J_HAIR[1], '#a06850': J_HAIR[2]}, hair)
    body = rect(a, 0, 17, 63, 63) & ~rect(a, 13, 26, 23, 35)
    a = remap(a, {'#c04040': J_DRESS[0], '#f86058': J_DRESS[1], '#f8f8f8': '#f2ead2', '#c8c8d8': '#d4c8a8',
                  '#b89858': '#8a5a34', '#f8c058': '#b07a44'}, body)
    hands = rect(a, 12, 26, 22, 36) | rect(a, 42, 30, 52, 40)
    a = remap(a, {'#283840': J_GLOVE[0], '#606070': J_GLOVE[1]}, hands)
    a = remap(a, {'#283840': '#3a2e22', '#606070': '#5a4a36'}, ~hands)
    feet = rect(a, 0, 54, 63, 63)
    a = remap(a, {J_DRESS[0]: '#5a3a22', J_DRESS[1]: '#7a4c30'}, feet)
    a = pix(a, [(29, 20), (31, 21), (34, 20), (35, 21)], '#d0806a')    # freckles
    return a


def juno_ow():
    a = C('trainer_POKEMONTRAINER_May')
    head = rows(a, 0, 10)
    a = remap(a, {'#e07050': J_KER[2], '#904028': J_KER[1], '#501000': J_KER[0], '#ffffff': '#f8e8b0', '#c0c8d8': J_KER[1]}, head)
    a = remap(a, {'#383818': J_HAIR[0], '#787040': J_HAIR[1], '#c8b068': J_HAIR[2]})
    a = remap(a, {'#e07050': J_DRESS[1], '#904028': J_DRESS[0], '#501000': '#2e4020', '#484858': '#5a4a36',
                  '#ffffff': '#f2ead2', '#c0c8d8': '#d4c8a8'}, ~head)
    return a


def back_a():
    a = T('POKEMONTRAINER_Brendan_back')
    hat = colmask(a, ['#d8e0e8', '#f8f8f8']) & rect(a, 0, 0, 399, 54)
    # head region per frame = hat pixels grown downward/sideways to catch the hat band + nape hair
    g = hat.copy()
    for _ in range(4):
        n = g.copy(); n[1:] |= g[:-1]; n[:, 1:] |= g[:, :-1]; n[:, :-1] |= g[:, 1:]; g = n
    head = g & rect(a, 0, 0, 399, 56)
    a = remap(a, {'#d8e0e8': HAIR_A[2], '#f8f8f8': HAIR_A[3], '#182850': HAIR_A[0], '#304068': HAIR_A[1],
                  '#485880': HAIR_A[1], '#607898': HAIR_A[2], '#c04040': HAIR_A[0], '#f86058': HAIR_A[1]}, head)
    a = remap(a, {'#182850': '#7c7c96', '#304068': JACK[0], '#485880': JACK[1], '#607898': JACK[2],
                  '#c04040': TEAL[0], '#f86058': TEAL[2], '#b89858': '#7a5a3e', '#f8c058': '#b08458'}, ~head)
    return a


def back_b():
    a = T('POKEMONTRAINER_May_back')
    hair = rect(a, 0, 0, 399, 60)
    a = remap(a, {'#483038': HAIR_B[0], '#785850': HAIR_B[1], '#a06850': HAIR_B[2],
                  '#c04040': HAIR_B[1], '#f86058': HAIR_B[2], '#f8f8f8': HAIR_B[3], '#c8c8d8': HAIR_B[2]}, hair & ~colmask(a, ['#d8a090', '#f8d8c8', '#c88070']))
    a = remap(a, {'#c04040': JACK[0], '#f86058': JACK[1], '#283840': '#232436', '#606070': '#3e4258',
                  '#b89858': '#7a5a3e', '#f8c058': '#b08458', '#f8f8f8': JACK[2], '#c8c8d8': JACK[1]}, ~hair)
    return a


if __name__ == '__main__':
    tag = sys.argv[1] if len(sys.argv) > 1 else 'r1'
    P = '/home/claude/fangame/art/previews/fr/'
    for n, fn in (('kestrel', kestrel), ('juno', juno), ('kestrel_ow', kestrel_ow), ('juno_ow', juno_ow), ('back_a', back_a), ('back_b', back_b)):
        to_img(fn()).save(P + f'{n}_{tag}.png')
