#! /usr/local/python2.7.11
import sys
from Bio import SeqIO

myfiles = sys.argv[1:]
for myfile in myfiles:
    outfile = myfile.split('.')[0] + '_longest_iso.fas'
    outh = open(outfile,'w')
    
    ID_length = {}
    ID_seq = {}
    gene_id = {}
    for record in SeqIO.parse(myfile,format='fasta'):
        ID = record.id
        sequence = record.seq
        length = len(sequence)
        ID_length[ID] = length
        ID_seq[ID] = sequence
        desc = record.description
        desc_list = desc.split()
        #print desc_list
        gene = ''
        for ele in desc_list:
            if ele.startswith('[db_xref'):
                gene = ele.split(':')[1].replace(']','')
        #print gene
        if gene not in gene_id:
            gene_id[gene] =[ID]
        else:
            gene_id[gene].append(ID)
        #break        

    keys = gene_id.keys()
    keys.sort()
    for m in keys:
        #print m
        value = gene_id[m]
        #print value
        if len(value)  == 1:
            seq_id = value[0]
            sequ = ID_seq[seq_id]
            outh.write('>'+seq_id + '\n' + str(sequ) + '\n')
        else:
            max_length = 0
            max_id = ''
            max_seq =''
            for l in value:
                gene_length = ID_length[l]
                if gene_length > max_length:
                    max_length = gene_length
                    max_id = l
                    max_seq = ID_seq[l]
            outh.write('>'+ max_id + '\n' + str(max_seq) + '\n')
    outh.close()

                 
    
    
   
    
