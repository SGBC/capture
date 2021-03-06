# The Capture-Seq assembler

[![Build Status](https://travis-ci.org/SGBC/capture.svg?branch=master)](https://travis-ci.org/SGBC/capture)
[![made-with-python](https://img.shields.io/badge/made%20with-python3-blue.svg)](https://www.python.org/)
[![LICENSE](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://github.com/SGBC/capture)

`capture` is an assembler developed to recover complete genome from ultra-high coverage samples

The repository is a work in progress and the assembler is not functional yet.
Thanks for your interest and come back soon!

## Installation

`capture` requires the following to be installed:

* python >= 3.6
* SPAdes

*TODO*

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
# reads in bam format
capture assemble --bam reads.bam \
--genome_size 35000 --mean 240 -o output_dir
# full list of subcommands and options
capture -h
# full list of options for a subcommand
capture assemble -h
```

## License

Code is under the [MIT](LICENSE) license

## Contributing

We welcome contributions from the community! See our [Contributing](CONTRIBUTING.md) guide.
