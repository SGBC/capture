# The Capture-Seq assembler

[![Build Status](https://travis-ci.org/SGBC/capture.svg?branch=master)](https://travis-ci.org/SGBC/capture)
[![made-with-python](https://img.shields.io/badge/made%20with-python3-blue.svg)](https://www.python.org/)
[![LICENSE](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://github.com/SGBC/capture)

`capture` is an assembler developed to recover complete genome from ultra-high coverage samples

The repository is a work in progress and the assembler is not completely functional yet.
Thanks for your interest and come back soon!

## Installation

`capture` requires the following to be installed:

* python >= 3.6
* SPAdes
* Canu

To install capture-assembler, simply type the following in your terminal:

    pip install capture-assembler
It requires python 3.6 and canu and spades already installed.

If you use conda you can install it using:

    conda install -c rvandamme capture-assembler
It requires a conda environment with python 3.6 and canu and spades already installed.

To install capture-assembler, spades and canu in a conda environment (recommanded to create a new one), type the following:
 ```bash
 conda create -n env_name python=3.6 # create a new env in python 3.6 (optionnal)
 conda install -n env_name -c rvandamme capture-assembler  canu=1.7 spades=3.12.0
 conda activate env_name #start using the environment and the capture-assembler
 ```

## Quickstart

```bash
# paired-end reads, Illumina MiSeq
capture -f reads_R1.fastq.gz -r reads_R2.fastq.gz \
--genome_size 35000 --mean 300 -o output_dir
# compressed paired-end reads, Illumina HiSeq
capture -f reads_R1.fastq.gz -r reads_R2.fastq.gz \
--genome_size 35000 --mean 125 -o output_dir
# single end reads, Ion Torrent
capture -u reads.fastq.gz \
--genome_size 35000 --mean 240 -o output_dir
# reads in bam format (Ion Torrent)
capture --bam reads.bam \
--genome_size 35000 --mean 240 -o output_dir
# full list of subcommands and options
capture -h
# full list of options for a subcommand
capture -h
```
## Arguments

```
  -h, --help            show the help message and exit
  -v, --version         print version and exit
  -u, --uniq            Input reads file in format fastq fastq.gz
  -f, --forward         Input forward file in format fastq fastq.gz
  -r, --reverse         Input reverse file in format fastq fastq.gz
  -b, --bam             Input the reads file in bam format. It will be considerate as Ion Torrent data in Spades
  -g, --genome_size     The size of the genome specific to your reads in numeric value
  -m, --mean            The mean size of the reads present in the input file
  -o, --output          The output directory
  -s, --subsample       The number of subsample to produce. Default: the maximum
  -t, --thread          The number of threads available. Default: 4
  -M, --memory          The memory available in Gigs. Default: 16G
  -c, --clean           Clean the temporary files. Default: True

```


## External Links

Official link to:

* [SPAdes](http://cab.spbu.ru/software/spades/)
* [Canu](http://canu.readthedocs.io/en/latest/)

## License

Code is under the [MIT](LICENSE) license

## Issues

Found a bug or have a question? Please open an [issue](https://github.com/SGBC/capture/issues)

## Contributing

We welcome contributions from the community! See our [Contributing](CONTRIBUTING.md) guide.
