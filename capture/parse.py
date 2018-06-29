#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip
import pysam
import logging
import itertools
import random as rnd

from Bio import SeqIO
from capture import bam


def is_gzip(file):
    """ test if the file is gzip
        Arguments:
            file =  the path to the file to test
        return:
            boolean answer
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
    """count the number of reads present in the fastq file
        Arguments:
            file = the the path to the file where to count
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
    """ read the file, make a sum of the reads
        for each occurence, the number of reads for the wanted coverage
        is saved in a subfile. The software keep reading the infile to
        get the next subfile. All the read will be selected, because
        the number of subsample required is the highest possible.
        Only for fastq files
        Arguments:
            output = the path to the output directory
            file = the fastq file where we retrieve the sequence
            type_f = the type of file (bam/fastq)
            num_sub = the number of subsample (first, second,...)
            number_records = number  of record needed in each subsample
            handle = the file open to be read
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
                handle, tot_records
                ):
    """ Read the file, make a sum of the reads
        for each occurence, the number of reads for the wanted coverage
        is saved in a subfile. the software keep reading the infile to
        get the next subfile. Here the reads are chosen randomly because
        the number of subsample is limited.
        Only for Fastq
        Arguments:
            output = the path to the output directory
            file = the fastq file where we retrieve the sequence
            type_f = the type of file (bam/fastq)
            num_sub = the number of subsample (first, second,...)
            number_records = number  of record needed in each subsample
            handle = the file open to be read
    """
    total_record = tot_records
    wanted_record = num_sub * number_records
    file_record = SeqIO.parse(handle, "fastq")
    record_gen = reservoir(total_record, wanted_record, file_record)
    for x in range(num_sub):
        subsample = itertools.islice(record_gen, number_records)
        subsample_number = x + 1
        SeqIO.write(subsample,
                    f"{output}/subsample_{type_f}{subsample_number}.fastq",
                    "fastq"
                    )


def reservoir(total_record, wanted_record, file_record):
    """yield a number of records from a fasta file using reservoir sampling
    Args:
        records (obj): fasta records from SeqIO.parse
    Yields:
        record (obj): a fasta record
    """
    samples = sorted(rnd.sample(
                        range(1, total_record),
                        (wanted_record)
                        ))
    # rnd_rec = rnd_rec.sort()
    counter = 0
    for sample in samples:
        while counter < sample:
            counter += 1
            _ = file_record.__next__()
        record = file_record.__next__()
        counter += 1
        yield record


def parse_bam(output, file, type_f, num_sub, number_records):
    """ Read the file, make a sum of the reads
        for each occurence, the number of reads for the wanted coverage
        is saved in a subfile.the software keep reading the infile to
        get the next subfile. All the reads will be parsed
        and write in a subsample since the highest number of subsample
        possible is required
        Only for bam files
        Arguments:
            output = the path to the output directory
            file = the fastq file where we retrieve the sequence
            type_f = the type of file (bam/fastq)
            num_sub = the number of subsample (first, second,...)
            number_records = number  of record needed in each subsample
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
    if sub_rec:
        # if not sub_rec: Don't know the best one
        c_sub = "extra"
        bam.write(sub_rec, output, c_sub, file_record)
    file_record.close()


def parse_bam_rnd(output, file, type_f, num_sub, fraction):
    """  parse the bam file and create only a chosen number
    of subsample. Each subsample contains randomly chosen reads
    Only for bam files
    Arguments:
        output = the path to the output directory
        file = the fastq file where we retrieve the sequence
        type_f = the type of file (bam/fastq)
        num_sub = the number of subsample (first, second,...)
        number_records = number  of record needed in each subsample
        fraction = the fraction of the bamfile needed to do the subsample one
    """
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
