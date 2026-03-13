#! cafe
#version
#date
load -i Orthogroups.less.than.100.tsv -t 3 -l lhtest_log.txt
tree (((((Dponderosae:200,Tcastaneum:200):33,Otaurus:233):13,(Aplanipennis:201,Ppyralis:201):45):81,((((Dplexippus:90,Banynana:90):3,Prapae:93):12,Pxuthus:105):12,Bmori:117):210):46,(((Ofasciatus:219,Clectularius:219):80,Nlugens:299):10,(Apisum:251,Btabaci:251):58):64)
errormodel -model cafeerror_1/cafe_errormodel_0.0125.txt -all
lambda -l 0.00107954
genfamily tutorial_genfamily/rnd -t 100 
lhtest -d tutorial_genfamily  -t (((((1,1)1,1)1,(1,2)1)1,((((2,1)1,1)1,1)1,1)1)1,(((2,1)1,1)1,(1,1)1)1) -l 0.00107954 -o lhtest_result.txt
