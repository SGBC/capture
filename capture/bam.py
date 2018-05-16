#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pysam


def count_bam(file):
    # bam_file = pysam.AlignmentFile(file, "rb")
    # Needs the bam file and bam index file to work
    map_seq = 0
    unmap_seq = 0
    for l in pysam.idxstats(file).split("\n")[:-1]:
        map_seq += int(l.split()[2])
        unmap_seq += int(l.split()[3])
    tot_records = map_seq + unmap_seq
    return(tot_records)


def write(reads, args, type_f, c_sub, file_record):
    # Will be add if need of only paired reads in bam
    # if args.paired:
    #     for read in reads:
    #         if read.is_paired:
    #          pairedreads.write(read)
    #     pairedreads.close()
    # else:
    allreads = pysam.AlignmentFile(
        f"{args.output}/subsample_{type_f}{c_sub}.bam",
        "wb",
        template=file_record)
    for read in reads:
        allreads.write(read)
    allreads.close()
