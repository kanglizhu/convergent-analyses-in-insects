#! /usr/local/python2.7.11
import sys
import os
import subprocess as sp

def mkdir(path):  
    folder = os.path.exists(path)  
    if not folder:
        os.makedirs(path)
mydir = './fasta_with_premature_stop_codon/'
mkdir(mydir)

myfiles = sys.argv[1:]
for i in myfiles:
    txt = i
    fasta = i.split('.')[0] + '.fas'
    mycommond_1 = 'mv %s %s' %  (txt, mydir)
    proc_1 = sp.Popen(mycommond_1.split())
    mycommond_2 = 'mv %s %s' %  (fasta, mydir)
    proc_2 = sp.Popen(mycommond_2.split())

    
