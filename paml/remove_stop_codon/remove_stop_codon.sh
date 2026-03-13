#identify fasta files without stop codon and modify its length to 3x
for i in *.fas
do
perl cds2aa_only_mid_and_tri.pl -check  $i > ${i%.*}.txt
done
python deal_with_middle_1_triple_0.py *txt
rm Check*
cp after_deal_with_m1_t0/*fas ./

#deal with fasta files staring with start codon but ending with stop codon
for i in *fas
do 
perl cds2aa.pl -check $i > ${i%.*}.txt
done
python deal_with_ATG_middle_0.py *txt
rm  Check*
cp after_deal_with_ATG_m0/*fas ./
rm *txt 

#check again
for i in *.fas
do
perl cds2aa_only_mid_and_tri.pl -check  $i > ${i%.*}.txt
done

#deal with real pseudogenes
python remove_txt_with_only_line.py *txt
python move_fasta__with_premature_stop_codon.py *txt
