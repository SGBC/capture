#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip
import pysam
import logging
import random as rnd

from Bio import SeqIO
from capture import bam


def is_gzip(file):
    """ test if the file is gzip using the 4 first byte of the file
        who are characteristic of the type of file
    """
    logger = logging.getLogger(__name__)
    magic_number = b"\x1f\x8b\x08"
    f = open(file, "rb")
    with f:
        try:
            assert f.read(3) == magic_number
        except AssertionError as e:
            logger.info(f"{file} is not gzipped")
            return False
        else:
            return True


def count_record(file):
    """count the number of reads present in the file
    """
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


def parse_fq(output, file, type_f, num_sub, number_records, handle):
    """ we read the file, we make a sum of the reads
        each time we get the number of reads for the wanted coverage
        we save them in a subfile, and keep reading the infile to
        get the next subfile
    """
    c = 1
    c_sub = 1
    sub_rec = []
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
                    f"{output}/subsample_{type_f}{c_sub}.fastq",
                    "fastq")
                c_sub += 1
                c += 1
                sub_rec = []
        else:
            sub_rec.append(record)
    # if there is still reads we save them in an extrafile
    if sub_rec != []:
        # OR if not sub_rec: Don't know the best method
        SeqIO.write(
            sub_rec,
            f"{output}/subsample_extra.fastq",
            "fastq"
            )


def parse_fq_rnd(
                output, file, type_f,
                num_sub, number_records,
                handle, rndseed, tot_records
                ):
    rnd.seed(rndseed)
    rnd_rec = rnd.sample(
                        range(1, tot_records),
                        (num_sub * number_records)
                        )
    print(type(rnd_rec))
    # rnd_rec = rnd_rec.sort()
    c = 1  # saved record counter
    rec_c = 1  # record counter
    c_sub = 1
    sub_rec = []
    file_record = SeqIO.parse(handle, "fastq")
    for record in file_record:
        if c_sub <= num_sub:
            if c < number_records*c_sub:
                if rec_c in rnd_rec:
                    sub_rec.append(record)
                    c += 1
                    rec_c += 1
                else:
                    rec_c += 1
            else:
                if rec_c in rnd_rec:
                    sub_rec.append(record)
                    SeqIO.write(
                        sub_rec,
                        f"{output}/subsample_{type_f}{c_sub}.fastq",
                        "fastq")
                    c_sub += 1
                    c += 1
                    sub_rec = []
                    rec_c += 1
                else:
                    rec_c += 1



def parse_bam(output, file, type_f, num_sub, number_records):
    """ same as parse_fq but for bam format
    """
    c = 1
    c_sub = 1
    sub_rec = []
    file_record = pysam.AlignmentFile(file, "rb")
    for record in file_record.fetch():
        if c_sub <= num_sub:
            if c < number_records*c_sub:
                sub_rec.append(record)
                c += 1
            else:
                sub_rec.append(record)
                bam.write(sub_rec, output, c_sub, file_record)
                c_sub += 1
                c += 1
                sub_rec = []
        else:
            sub_rec.append(record)
    if sub_rec != []:
        # if not sub_rec: Don't know the best one
        c_sub = "extra"
        bam.write(sub_rec, output, c_sub, file_record)
    file_record.close()


def parse_bam_rnd(output, file, type_f, num_sub, fraction):
    """  parse the bam file and create only a chosen number
    of subsample"""
    c_sub = 1
    for sub in range(num_sub):
        pysam.view(
            "-b",
            "-s",
            f"{c_sub}.{fraction}",
            file,
            "-O",
            "bam",
            "-o",
            f"{output}/subsample_{c_sub}.bam",
            catch_stdout=False  # pysam issue #342
             )
        c_sub += 1
