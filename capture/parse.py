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


def parse(args, file, type_f, num_sub, number_records):
    c = 1
    c_sub = 1
    sub_rec = []
    if is_gzip(file):
        with gzip.open(file, "rt") as handle:
            file_record = SeqIO.parse(handle, "fastq")
            for record in file_record:
                if c_sub <= num_sub:
                    if c < number_records*c_sub:
                        sub_rec.append(record)
                        c += 1
                    else:
                        sub_rec.append(record)
                        SeqIO.write(
                            sub_rec,
                            f"{args.output}/subsample_{type_f}{c_sub}.fastq",
                            "fastq")
                        c_sub += 1
                        c += 1
                        sub_rec = []
                else:
                    sub_rec.append(record)
            if sub_rec != []:
                # if not sub_rec: Don't know the best one
                SeqIO.write(
                    sub_rec,
                    "subsample_extra.fastq" % c_sub,
                    "fastq")
    else:
        with open(file, "rt") as handle:
            file_record = SeqIO.parse(handle, "fastq")
            for record in file_record:
                if c_sub <= num_sub:
                    if c < number_records*c_sub:
                        sub_rec.append(record)
                        c += 1
                    else:
                        sub_rec.append(record)
                        SeqIO.write(
                            sub_rec,
                            f"{args.output}/subsample_{type_f}{c_sub}.fastq",
                            "fastq")
                        c_sub += 1
                        c += 1
                        sub_rec = []
                else:
                    sub_rec.append(record)
            if sub_rec != []:
                # if not sub_rec: Don't know the best one
                SeqIO.write(
                    sub_rec,
                    "subsample_extra.fastq" % c_sub,
                    "fastq")
