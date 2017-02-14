#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join
import re
import argparse


# --------------------------------------------------------------------------------- argument parsing
def sigle(v):
    try:
        return re.match("[A-Z]{3}\d{4}", v).group(0)
    except:
        raise argparse.ArgumentTypeError('"{}" n’est pas un sigle de cours correct'.format(v))

parser = argparse.ArgumentParser(description='Script du TD2, similarité de textes')
parser.add_argument('SIGLE', type=sigle, help='Nom du cours à verifier',
                    default='INF8007')
parser.add_argument('-d', type=str, dest='path', default='02/PolyHEC',
                    help='Chemin vers la liste de fichiers')

args = parser.parse_args()

files = [f for f in listdir(args.path) if isfile(join(args.path, f))]
