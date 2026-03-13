#! cafe
#version
#date
load -i Orthogroups.less.than.100.tsv -t 4 -l cafe_pre_log.txt -p 0.05
tree (((((Dponderosae:200,Tcastaneum:200):33,Otaurus:233):13,(Aplanipennis:201,Ppyralis:201):45):81,((((Dplexippus:90,Banynana:90):3,Prapae:93):12,Pxuthus:105):12,Bmori:117):210):46,(((Ofasciatus:219,Clectularius:219):80,Nlugens:299):10,(Apisum:251,Btabaci:251):58):64)
lambda -s 
report orthologs_of_15_species_with_single_lamda
