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
    

## Quickstart

```bash
# paired-end reads, Illumina MiSeq
capture assemble -f reads_R1.fastq.gz -r reads_R2.fastq.gz \
--genome_size 35000 --mean 300 -o output_dir
# compressed paired-end reads, Illumina HiSeq
capture assemble -f reads_R1.fastq.gz -r reads_R2.fastq.gz \
--genome_size 35000 --mean 125 -o output_dir
# single end reads, Ion Torrent
capture assemble -u reads.fastq.gz \
--genome_size 35000 --mean 240 -o output_dir
# reads in bam format (Ion Torrent)
capture assemble --bam reads.bam \
--genome_size 35000 --mean 240 -o output_dir
# full list of subcommands and options
capture -h
# full list of options for a subcommand
capture assemble -h
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


## License

Code is under the [MIT](LICENSE) license

## Issues

Found a bug or have a question? Please open an [issue](https://github.com/SGBC/capture/issues)

## Contributing

We welcome contributions from the community! See our [Contributing](CONTRIBUTING.md) guide.
