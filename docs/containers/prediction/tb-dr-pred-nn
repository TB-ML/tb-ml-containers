---
title: tb-dr-pred-nn
drugs: ['AMIKACIN', 'CAPREOMYCIN', 'CIPROFLOXACIN', 'ETHAMBUTOL', 'ETHIONAMIDE', 'ISONIAZID', 'KANAMYCIN', 'LEVOFLOXACIN', 'MOXIFLOXACIN', 'OFLOXACIN', 'PYRAZINAMIDE', 'RIFAMPICIN', 'STREPTOMYCIN']
architecture: CNN
docker: linfengwang/tb-dr-pred-nn
input:  onehot encoded loci sequences in the form of csv
---


# Small CNN model for prediction TB drug resistance from onehot encoded loci sequences


Model adapted from the below paper: Green, A.G. et al. (2021) “A convolutional neural network highlights mutations relevant to antimicrobial resistance in mycobacterium tuberculosis.” Available at: https://doi.org/10.1101/2021.12.06.471431.

Reduced in model size (1/3 original size) but retain equal accuracy (~93%)

Input one-hot-encoded consensus sequence Loci used: acpM-kasA, gid, rpsA, clpC, embCAB, aftB-ubiA, rrs-rrl, ethAR, oxyR-ahpC, tlyA, katG, rpsLrpoBC, fabG1-inhA, eis, gyrBA, panD, pncA.

Output one-hot-encoded vector for drug resistance prediction of 13 drugs: 'AMIKACIN', 'CAPREOMYCIN', 'CIPROFLOXACIN', 'ETHAMBUTOL', 'ETHIONAMIDE', 'ISONIAZID', 'KANAMYCIN', 'LEVOFLOXACIN', 'MOXIFLOXACIN', 'OFLOXACIN', 'PYRAZINAMIDE', 'RIFAMPICIN', 'STREPTOMYCIN'
