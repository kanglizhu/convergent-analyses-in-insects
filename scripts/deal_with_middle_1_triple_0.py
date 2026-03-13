#! /usr/local/python2.7.11
import sys
from Bio import SeqIO
import os

def mkdir(path):  
    folder = os.path.exists(path)  
    if not folder:
        os.makedirs(path)
direct = "./after_deal_with_m1_t0/" 
mkdir(direct)


myfiles = sys.argv[1:]
for i in myfiles:
    #fasta_file = i.replace('txt','fas')
    ID_list =[]
    fh = open(i,'r')
    line_1 = fh.readline()
    lines = list(fh.readlines())
    if lines:
        for j in lines:
            j_list = j.split()
            id_0 = j_list[0]
            mid = j_list[1]
            tri = j_list[2]
            if mid == '1' and tri == '0':
                ID_list.append(id_0)
        #print ID_list
        if ID_list:
            fasta_file = i.replace('txt','fas')
            #print fasta_file
            outfile = direct + fasta_file
            outhandle = open(outfile,'w')
            for record in SeqIO.parse(fasta_file, format = 'fasta'):
                id_2= record.id
                seq = record.seq
                seq_len = len(seq)
                yushu = seq_len%3
                desc = record.description
                if id_2 in ID_list:
                    keep_length = seq_len - yushu 
                    #print seq_len,seq
                    #print keep_length,seq[:keep_length]
                    seq_new = seq[:keep_length]
                    seqrecord = SeqIO.SeqRecord(seq_new,id = id_2, description = desc)
                    SeqIO.write(seqrecord,outhandle,'fasta')
                else:
                    seqrecord = SeqIO.SeqRecord(seq,id = id_2, description = desc)
                    SeqIO.write(seqrecord,outhandle,'fasta')
            os.rename(fasta_file,'Check_' + fasta_file)
            outhandle.close()
fh.close()
















     
            
                    
