#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip
import logging

from Bio import SeqIO


def is_gzip(file):
    logger = logging.getLogger(__name__)
    magic_number = b"\x1f\x8b\x08\x08"
    f = open(file, "rb")
    with f:
        try:
            assert f.read(4) == magic_number
        except AssertionError as e:
            logger.info(f"{file} is not gzipped")
            return False
        else:
            return True


def count_record(file):
    if is_gzip(file):
        with gzip.open(file, "rt") as handle:
            file_record = SeqIO.parse(handle, "fastq")
            tot_records = sum(1 for line in file_record)
            return(tot_records)
    else:
        with open(file, "rt") as handle:
            file_record = SeqIO.parse(handle, "fastq")
            tot_records = sum(1 for line in file_record)
            return(tot_records)


def parse(file):
    if is_gzip(file):
        with gzip.open(file, "rt") as handle:
            file_record = SeqIO.parse(handle, "fastq")
            return(file_record)
    else:
        with open(file, "rt") as handle:
            file_record = SeqIO.parse(handle, "fastq")
            return(file_record)
