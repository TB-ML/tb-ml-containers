# Contribute

## How to develop a container

A container is essentially a mini virtual machine that contains all software needed to run predictions on new data.
[Docker](https://www.docker.com/) is used to build the containers and they can then be run on any system which has docker installed. There are a few steps required to build a container. We'll go through these by going through a whole example, from training to prediction. 

### Step 1 - Training the model

As an example we will train a random forest classifier to predict resistance to rifampicin. The input data is a set of 100 resistant and 100 sensitive isolates randomly taken from the SRA. The input data and scripts are available from [this repository](https://github.com/jodyphelan/simple-rif-rf). This is a very quick and dirty model that takes a lot of shortcuts, it is just meant for demonstration purposes.

First lets set up a conda environment for our code:

```
mamba create -n ml -c conda-forge -c bioconda scikit-learn bcftools
conda activate ml
```

This is our training code.

``` python
from sklearn.ensemble import RandomForestClassifier
import pickle
import subprocess as sp
from collections import defaultdict

genos = defaultdict(dict)

# get genotypes for all samples at all positions in the vcf
for l in sp.Popen(r"bcftools query -f '[%POS\t%SAMPLE\t%GT\n]' snps.vcf.gz",shell=True,stdout=sp.PIPE).stdout:
    # l is a byte string, so we need to decode it to a string and strip the newline character at the end
    pos,sample,gt = l.decode().strip().split()
    # convert the position to an integer
    pos = int(pos)
    # if the genotype is missing or reference, set it to 0 (otherwise set it to 1)
    if gt=="./." or gt=="0/0":
        gt = 0
    else:
        gt = 1
    # add the genotype to the dictionary
    genos[sample][pos] = gt

# get the phenotype for each sample
pheno = {}
for l in open("pheno.txt"):
    row = l.strip().split()
    pheno[row[0]] = int(row[1])

# convert the genotype dictionary to a list of lists
X = [list(genos[s].values()) for s in pheno] 
y = [pheno[s] for s in pheno]
# use scikit-learn to train a random forest classifier
clf = RandomForestClassifier(max_depth=2, random_state=0)
clf.fit(X, y)

# dump the model and the positions to a pickle file
positions = list(list(genos.values())[0])
pickle.dump({"model":clf,"positions":positions}, open("model.pkl","wb"))
```

Execute the code to run the training:

```
python train.py
```

Importantly you see that we have dumped the model object to a file. We can then use the `.predict()` method from the object when we reload it somewhere else.

### Step 2 - Set up your prediction script

Now that we have the model saved, we can create a script to load it along with a vcf from a new sample and make a prediction. Here is the code for that.

``` python
""" read in genotypes from VCF file and predict outcome """
import sys
import os
import argparse
import pickle
import subprocess as sp

# parse command line arguments
parser = argparse.ArgumentParser(description='Predict outcome from VCF file')
parser.add_argument('--vcf', help='VCF file', required=True)
parser.add_argument('--model', help='model file', required=True)
args = parser.parse_args()

# load model
items = pickle.load(open(args.model, "rb"))
clf = items['model']
positions = items['positions']



# extract genotypes
genos = {}
for l in sp.Popen(r"bcftools query -f '%POS[\t%GT\n]' "+ args.vcf,shell=True,stdout=sp.PIPE).stdout:
    row = l.decode().strip().split()
    if row[1]!="0/0":
        genos[int(row[0])] = 1
    else:
        genos[int(row[0])] = 0

# fill in missing genotypes with 0 (ref)
for p in positions:
    if p not in genos:
        genos[p] = 0

genos = [[genos[p] for p in positions]]

# predict outcome
pred = clf.predict(genos)
# write output
sys.stdout.write("drug,prediction\nrifampicin,%s\n" % pred[0])
```

We can then use this script to predict on some new data.

```
$ python predict.py --vcf por5A1.vcf.gz --model model.pkl
drug,prediction
rifampicin,1
```

Now we are ready to package our prediction pipeline into a container.

### Step 3 - Create container

To build a container you first need docker installed. Head over to https://www.docker.com/ to download the latest version. Once you have it installed you can start the build process. First we need to define what software we need.
It is very important to use the exact same versions of libraries and software in the docker container as you used to train. You can check this with conda

```
$ conda list | grep bcftools
bcftools                  1.16                 h83fc8ca_1    bioconda
$ conda list | grep scikit-learn
scikit-learn              1.2.1           py311h087fafe_0    conda-forge
```

So we can see we need to use `bcftools=1.16` and `scikit-learn=1.2.1`. To build our container we need to create a file called `Dockerfile` and insert our software dependencies. We also need to add our saved model file and the prediction script. 

``` 
FROM mambaorg/micromamba:latest
LABEL image.name="jodyphelan/simple-rif-rf"

# This needs to be set for the PATH variable to be set correctly
ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Install our software
RUN micromamba install -y -n base -c bioconda -c conda-forge \
    scikit-learn=1.2.1 \
    bcftools=1.16 \
    tqdm && \
    micromamba clean --all --yes

# create a directory for the internal data used by the container
USER root
RUN mkdir /internal_data /data

# copy the model, data files, and scripts
COPY model.pkl /internal_data/model.pkl
COPY predict.py /internal_data

# set `/data` as working directory so that the output is written to the
# mount point when run with `docker run -v $PWD:/data ... -o output.csv`
WORKDIR /data

ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "python", "/internal_data/predict.py", "--model", "/internal_data/model.pkl"]
```

We can then build the container with 

``` bash
$ docker build -t simple-rif-rf . 
```

In a nutshell, this installs our required software, copies the data files and scripts to the container and finally defines an "entrypoint" script that will be run when the container is executed.

We can then use this container in a similar way to how we used the script to predict. Since, we already point the `--model` flag to the right file in the ENTRYPOINT variable we only need to give the `--vcf` argument.

``` bash
$ docker run --rm -it -v $PWD:/data  simple-rif-rf  
drug,prediction
rifampicin,1
```

Now finally you can publish your container to dockerhub. Head over to https://hub.docker.com/ and set yourself up with an account. Once you have done this you can link your account with your local docker installation.

``` bash
$ docker login
```

And finally you can push the container to dockerhub

``` bash
$ docker push jodyphelan/simple-rif-rf:latest
```

## Adding your container to TB-ML-Containers

If you want to publicise your container you can add it to this website to improve its visibility. To do this you just have to fork [this repo](https://github.com/TB-ML/tb-ml-containers). After this, you should add a markdown file to the appropriate location `/docs/containers/prediction` for prediction containers or `/docs/containers/preprocessing` for preprocessing containers. The markdown file should contain a few variables that are defined at the top of the page in yaml format. In particular, for prediction containers they need:

* title - Name of the model
* drugs - A list of drugs it predicts for
* architecture - The type of ML model
* input - The input type it needs (e.g. VCF)
* docker - The name of the container on dockerhub

After defining these you can write about your model using standard markdown. For example:

```
---
title: simple-rif-rf
drugs: ['rifampicin']
architecture: RandomForest
docker: jodyphelan/simple-rif-rf
input: variants/VCF
---

# Rifampicin RandomForest

This container predicts rifampicin resistance from variants in VCF format.
```

Now just put in a pull request and we will add it in to the website. You model will automatically appear on the tables on the front page. A dedicated rendering your markdown content will also be generated using the markdown filename as the link.


