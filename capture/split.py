#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from Bio import SeqIO
from capture import bam
from capture import parse


def split_fq(genome_size, mean_size, output, file, type_f, wanted_cov=50):
    """ calcul the number of reads needed in each subsample then
        parse the file and make the subsample
    """
    logger = logging.getLogger(__name__)
    # caclul the number of reads in each subsample for a coverage
    number_records = (wanted_cov * genome_size) / mean_size
    # the subsampling is the same for fastq gzip and not gzip
    # as we can have more than one file, we use the name for subsample
    tot_records = parse.count_record(file)
    num_sub = tot_records//number_records
    parse.parse_fq(output, file, type_f, num_sub, number_records)


def split_bam(genome_size, mean_size, output, file, type_f, wanted_cov=50):
    logger = logging.getLogger(__name__)
    # caclul the number of reads in each subsample for a coverage
    number_records = (wanted_cov * genome_size) / mean_size
    # the subsampling is the same for fastq gzip and not gzip
    # as we can have more than one file, we use the name for subsample
    tot_records = bam.count_bam(file)
    num_sub = tot_records//number_records
    parse.parse_bam(output, file, type_f, num_sub, number_records)
