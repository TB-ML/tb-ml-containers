---
title: tb-dr-pred-nn
drugs: ['amikacin', 'capreomycin', 'ciprofloxacin', 'ethambutol', 'ethionamide', 'isoniazid', 'kanamycin', 'levofloxacin', 'moxifloxacin', 'ofloxacin', 'pyrazinamide', 'rifampicin', 'streptomycin']
architecture: CNN
docker: linfengwang/tb-dr-pred-nn
input:  One-hot-encoded-sequence/CSV
---


# Small CNN model for prediction TB drug resistance from one-hot-encoded sequences of target loci


Model adapted from: Green, A.G. et al. (2021) “A convolutional neural network highlights mutations relevant to antimicrobial resistance in Mycobacterium tuberculosis.”;
Available at: https://doi.org/10.1101/2021.12.06.471431.

Compared to the original, this model is reduced in size (1/3 original size), but retains comparable accuracy (~93%).

Input one-hot-encoded consensus sequences of the following loci: acpM-kasA, gid, rpsA, clpC, embCAB, aftB-ubiA, rrs-rrl, ethAR, oxyR-ahpC, tlyA, katG, rpsLrpoBC, fabG1-inhA, eis, gyrBA, panD, pncA.

## Example usage

Get the one-hot-encoded sequences from a BAM file

```
docker run -v $PWD:/data \
    linfengwang/tb-ml-one-hot-encoded-seqs-from-raw-reads-with-gap-insertion \
    -b file.bam \
    -o nn_target_loci.csv
```

Predict resistance against 13 drugs from the one-hot-encoded sequences

```
docker run -v $PWD:/data \
    linfengwang/tb-dr-pred-nn \
    input_seqs.csv
```