#!/bin/bash


cat *.fna > all.fna
bowtie2-build all.fna base
