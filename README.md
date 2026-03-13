# convergent-analyses-in-insects

# convergent-analyses-in-insects

Installation
perl 5.12 or higher
python 2.7 or higher
Biopython in python 2 or python 3
UPhO pipeline (git version 4ec1589)
OrthoFinder (v2.3.1)
MAFFT (v7.407)
TrimAl (v1.4)
FastTree (v2.1.11)
CAFE
TranslatorX
PAML (v4.9i)
Gblocks
topGO
Trinity (v2.8.4)


usage

******orthogroup identification******
step1 download translated cds file from Genbank and choose the longest isoform for each gene
python pick_the_longest_isoform_for_genomic.py *faa

step2  infer orthogroups with default parameters using OrthoFinder
orthofinder -f ./genome_data -S diamond

step3 delinate orthogroups using UPhO pipeline for non single copy orthogroups, for example for OG0000002.fa
mafft --anysymbol --auto --quiet  --thread 3 ./UPHO/OG0000002.fa > ./UPHO/OG0000002.mafft.fa
trimal -fasta -gappyout -in ./UPHO/OG0000002.mafft.fa  -out   ./UPHO/OG0000002.trimal.fa
python Al2Phylo.py -m 20 -p 0.30 -t 2 -in ./UPHO/OG0000002.trimal.fa
#result of Al2Phylo.py is OG0000002_clean.fa
#since for the following analyses, we used nucleotide sequences, so we need translate the amino acid sequecne back to nucleotide. Here we used seqkit software, and download the cds file for each species from Genbank.
seqkit common ./genome_data/origin_genome/Danaus_plexippus_GCF_009731565.1_Dplex_v4_cds_from_genomic.fna OG0000002_clean.fa --quiet  --threads 3 >> OG0000002.cds.fa
FastTree OG0000002.cds.fa > OG0000002.tree
python UPhO.py -m 4 -iP -S 0.95   -R OG0000002.cds.fa -in OG0000002.tree -ouT
#after these steps, we can get two copies of sequences, OG0000002_0.fasta and OG0000002_1.fasta

******Gene family expansion and contraction******
step1 we first excluded orthogroups with more than 100 members following CAFE’s manual
python ./Cafe/change_orthofinder_count_to_tab.py Orthogroups.GeneCount.tsv

step2 In order to account for assembly errors, we estimated an error parameter with a single lambda of gene birth and death
cafe ./Cafe/cafe_single_lambda_pre.sh
cafe ./Cafe/caferror.sh

step3  we re-estimated the birth and death rates separately for two lambda model and single lambda model, and compared them by performing a likelihood ratio test according to the CAFE’s manual
cafe ./Cafe/cafe_single_lambda_with_error_model.sh
cafe ./Cafe/cafe_two_lambda_with_error_model.sh
cafe ./Cafe/cafe_comparison_between_single_and_two_lambda_with_error_model.sh


******PAMl analyses******
step1 remove sequences with premature stop codons 
#put your fasta files for running paml in one folder (for example ./paml/remove_stop_codon), and remove sequences with premature stop codons for each cds
cd ./paml/remove_stop_codon
sh remove_stop_codon.sh

step2 aligned the coding sequences and removed poorly align regions with TranslatorX 
#for cds without premature stop codons, we aligned these coding sequences and removed poorly align regions with TranslatorX
cd ./paml/TranslatorX
perl translatorx_vLocal.pl -i OG0006853.fas -o ./after_translatorx/OG0006853_out -p F -t F  -g "-b1=11 -b3=2 -b4=5 -b5=h"
perl translatorx_vLocal.pl -i OG0006858.fas -o ./after_translatorx/OG0006858_out -p F -t F  -g "-b1=11 -b3=2 -b4=5 -b5=h"
note: after running TranslatorX, we extract *nt_cleanali.fasta from after_translatorx folder, and used these fasta files for the following analyses.

step3 construct raxml tree
#for the *nt_cleanali.fasta files, we excluded sequences with 90% missing data (outputs are *out_10_more.fasta), and manually checked several alignments to confirm their accuracy. Gene trees were built with RAxML using the GTRGAMMA model, and they were used for the following selective pressure and convergence analyses
cd ./paml/raxml
python remove_seq_with_90_missing_data.py *nt_cleanali.fasta
cd ./_remove_seq_with_90_missing_data
raxmlHPC-PTHREADS-AVX -f a -x 12345 -p 12345 -# 100 -m GTRGAMMA  -s OG0006853_out_10_more.fasta  -n ./RAxML_tree/OG0006853 -T 3
raxmlHPC-PTHREADS-AVX -f a -x 12345 -p 12345 -# 100 -m GTRGAMMA  -s OG0006858_out_10_more.fasta  -n ./RAxML_tree/OG0006853 -T 3
#for the fasta files, we change the fasta file to phylip format
python fastaConvertPhylip.py OG0006853_out_10_more.fasta
python fastaConvertPhylip.py OG0006858_out_10_more.fasta
note: the tree file and phylip file are used for running paml

step4 running codeml model in PAMl
put the tree file, fasta file and ctl files in one folder (for example ./paml/paml/OG0006853), and run codeml in PAMl 


******Detection of convergent amino acid substitutions******
From paml outputs, we used the rst file for each gene to extract the convergent amino acid substitutions in our target species. and the *_Convergent_target_species.xls file contains the identical site for CG-adapted species.
python detect_convergent_sites_specific_in_3_TGs.py *rst
