---
title: mykrobe
drugs: ['amikacin',  'capreomycin',  'ciprofloxacin',  'delamanid',  'ethambutol',  'ethionamide',  'isoniazid',  'kanamycin',  'levofloxacin',  'linezolid',  'moxifloxacin',  'ofloxacin',  'pyrazinamide',  'rifampicin',  'streptomycin']
architecture: DirectAssociation
input: fastq
docker: jodyphelan/mykrobe
---
# {{title}}

This container wraps around the `mykrobe` prediction tool that reads in fastq data and performs resistance prediction to a multitude of drugs using the direct association method.

For more information visit https://github.com/Mykrobe-tools/mykrobe.