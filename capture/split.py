#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip

from Bio import SeqIO

from capture import parse


def split(args):
    logger = logging.getLogger(__name__)
    for file in args.input_file.split(","):
        wanted_cov = 100
        # caclul the number of reads in each subsample for a coverage
        number_records = (wanted_cov * args.genome-size) / args.length_read
        # the subsampling is the same for fastq gzip and not gzip
        # as we can have more than one file, we use the name for subsample
        file_record, name = parse.parse(file)
        tot_records = sum(1 for line in file_record)
        num_sub = tot_records//number_records
        c = 1
        c_sub = 1
        sub_rec = []
        # while c_sub <= num_sub:
        #         while c <= number_records*c_sub:
        #             EXTRACT1read
        #             c += 1
        #         c_sub += 1
        for record in file_record:
            if c_sub <= num_sub:
                if c < number_records*c_sub:
                    sub_rec.append(record)
                    c += 1
                else:
                    sub_rec.append(record)
                    SeqIO.write(
                        sub_rec,
                        f"subsample_{name}{c_sub}.fastq",
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
