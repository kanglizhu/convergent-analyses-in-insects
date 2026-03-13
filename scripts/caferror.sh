#! cafe
tree (((((Dponderosae:200,Tcastaneum:200):33,Otaurus:233):13,(Aplanipennis:201,Ppyralis:201):45):81,((((Dplexippus:90,Banynana:90):3,Prapae:93):12,Pxuthus:105):12,Bmori:117):210):46,(((Ofasciatus:219,Clectularius:219):80,Nlugens:299):10,(Apisum:251,Btabaci:251):58):64)
load -i Orthogroups.less.than.100.tsv -t 10 -l cafeerror_1/cafe_final_log.txt
errormodel -model cafeerror_1/cafe_errormodel_0.0125.txt -sp Tcastaneum
errormodel -model cafeerror_1/cafe_errormodel_0.0125.txt -sp Dplexippus
errormodel -model cafeerror_1/cafe_errormodel_0.0125.txt -sp Bmori
errormodel -model cafeerror_1/cafe_errormodel_0.0125.txt -sp Pxuthus
errormodel -model cafeerror_1/cafe_errormodel_0.0125.txt -sp Ppyralis
errormodel -model cafeerror_1/cafe_errormodel_0.0125.txt -sp Prapae
errormodel -model cafeerror_1/cafe_errormodel_0.0125.txt -sp Otaurus
errormodel -model cafeerror_1/cafe_errormodel_0.0125.txt -sp Nlugens
errormodel -model cafeerror_1/cafe_errormodel_0.0125.txt -sp Btabaci
errormodel -model cafeerror_1/cafe_errormodel_0.0125.txt -sp Clectularius
errormodel -model cafeerror_1/cafe_errormodel_0.0125.txt -sp Dponderosae
errormodel -model cafeerror_1/cafe_errormodel_0.0125.txt -sp Aplanipennis
errormodel -model cafeerror_1/cafe_errormodel_0.0125.txt -sp Banynana
errormodel -model cafeerror_1/cafe_errormodel_0.0125.txt -sp Ofasciatus
errormodel -model cafeerror_1/cafe_errormodel_0.0125.txt -sp Apisum
lambda -s 
report cafeerror_1/cafe_final_report