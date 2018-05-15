#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from Bio import SeqIO

from capture import parse


def split(args, file, type_f, wanted_cov=50):
    logger = logging.getLogger(__name__)
    # caclul the number of reads in each subsample for a coverage
    number_records = (wanted_cov * args.genome_size) / args.mean
    # the subsampling is the same for fastq gzip and not gzip
    # as we can have more than one file, we use the name for subsample
    tot_records = parse.count_record(file)
    num_sub = tot_records//number_records
    # while c_sub <= num_sub:
    #         while c <= number_records*c_sub:
    #             EXTRACT1read
    #             c += 1
    #         c_sub += 1
    parse.parse(args, file, type_f, num_sub, number_records)
