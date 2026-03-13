#! /usr/local/python2.7.11
import sys
from Bio import SeqIO
from Bio import AlignIO
import os

def mkdir(path):  
    folder = os.path.exists(path)  
    if not folder:
        os.makedirs(path)
mydir = './_Phylip_files/'
mkdir(mydir)

myfiles = sys.argv[1:]
for myfile in myfiles:
    outfile =mydir +  myfile.split('.')[0] + '.phy'
    outhandle = open(outfile,'w')
    alignment = AlignIO.read(myfile, "fasta")
    align_length = alignment.get_alignment_length()
    row = len(alignment)
    outhandle.write(str(row) + '\t' + str(align_length) + '\n')
    for record in SeqIO.parse(myfile, format = 'fasta'):
        ID= record.id
        seq = record.seq
        desc = record.description
        outhandle.write(str(ID) + '    ' + str(seq) + '\n')
    outhandle.close()
    
