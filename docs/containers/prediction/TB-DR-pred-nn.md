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

Get the onehot encoded sequence from bam file

docker run -v $PWD:/data \
    linfengwang/tb-ml-one-hot-encoded-seqs-from-raw-reads-with-gap-insertion \
    -b file.bam \
    -o nn_target_loci.csv
    
Predict resistance against 13 drugs from one-hot-encoded sequences 

docker run -v $PWD:/data \
    linfengwang/tb-dr-pred-nn \
    input_seqs.csv
