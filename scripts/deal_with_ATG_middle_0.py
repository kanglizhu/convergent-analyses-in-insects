#! /usr/local/python2.7.11
import sys
from Bio import SeqIO
import os

def mkdir(path):  
    folder = os.path.exists(path)  
    if not folder:
        os.makedirs(path)
direct = "./after_deal_with_ATG_m0/" 
mkdir(direct)

outfile_of_delete_species = '_species_deleted.xls'
outh = open(outfile_of_delete_species,'w')

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
            star = j_list[1]
            middle = j_list[3]
            if star == '1' and middle == '0':
                ID_list.append(id_0)
        #print ID_list
        if ID_list:
            fasta_file = i.replace('txt','fas')
            outh.write(fasta_file + '\t' + str(ID_list) + '\n')
            #print fasta_file
            outfile = direct + fasta_file
            outhandle = open(outfile,'w')
            for record in SeqIO.parse(fasta_file, format = 'fasta'):
                id_2= record.id
                seq = record.seq
                desc = record.description
                if id_2 in ID_list:
                    pass
                else:
                    seqrecord = SeqIO.SeqRecord(seq,id = id_2, description = desc)
                    SeqIO.write(seqrecord,outhandle,'fasta')
            os.rename(fasta_file,'Check_' + fasta_file)
            outhandle.close()
fh.close()
outh.close()















     
            
                    
