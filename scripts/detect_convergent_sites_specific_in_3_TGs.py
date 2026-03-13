#! /usr/local/python2.7.11
import sys
import re

myfiles = sys.argv[1:]


for myfile in myfiles:
    gene = myfile.split('_rst')[0]
    IN = open(myfile,'r')
    line_list = IN.readlines()
    IN.close()
    branches = []
    #store branch and amino acid change
    for line in line_list:
        line = line.strip()
        pattern_branch_inter = re.compile(r'^(Branch)\s+(\d+):\s+(\d+)\.\.(\d+)\s+\(n=')
        branch_inter = pattern_branch_inter.match(line)
        pattern_branch_desc = re.compile(r'^(Branch)\s+(\d+):\s+(\d+)\.\.(\d+)\s+\((\w+)')
        branch_desc = pattern_branch_desc.match(line)
        pattern_sites = re.compile(r'^(\d+)\s+[AGCTN]{3}\s+\(([A-Z-])\s+[0,1]\.\d+\)\s+->\s+[AGCT]{3}\s+\(([A-Z])\)')
        sites = pattern_sites.match(line)
        if branch_inter:
            inter_node = branch_inter.groups()
            branches.append('_'.join(inter_node))
        elif branch_desc:
            out_node = branch_desc.groups()
            #print out_node
            branches.append ('_' .join(out_node))
        elif sites:
            #site = sites.group(1)
            #change = sites.group(2) + '_' + sites.group(3)
            #print change
            site_change = sites.groups()
            site_inf = '_' .join(site_change)
            #print site_inf
            branches.append(site_inf)
    
    # generate branch => [branch + amino aicd changes dict]
    branch_site ={}
    for index,value in enumerate(branches):
        #print (value)
        if branches[index].startswith('Branch'):
            lab = branches[index]
            branch_site[lab]=[]
        branch_site[lab].append(branches[index])
    
    # generate site => [amino aicd change + branch]
    sites_dict = {}
    for key,value in branch_site.items():
        if len(value) ==1:
            pass
        else:
            branch = value[0]
            del value[0]
            for i,j in enumerate(value):
                site_list = value[i].split('_',1)
                site = site_list[0]
                change = site_list[1] + '_' + branch
                if sites_dict.get(site,None):
                    sites_dict[site].append(change)
                else:
                    sites_dict[site] = [change]
    
    # sort lists according to number
    keys =sorted (sites_dict.keys(),key = lambda i:int(re.match(r'(\d+)',i).group()))
    
    sites_changed_aa ={}
    #remove sites with no amino acid level changes
    #remove sites change of inter node
    #write original file 
    out_sites = open(gene + '_sites_to_aa_NonSyn_and_Syn.txt','w')
    for i in keys:
        out_sites.write(i)
        out_sites.write (str(sites_dict[i]) + '\n')
        sites_changed_aa[i] = []
        values = sites_dict[i]
        for index,value in enumerate(values):
            lists_of_aa = values[index].split('_')
            B_AA = lists_of_aa[0]
            A_AA = lists_of_aa[1]
            if B_AA == A_AA:
                pass
            elif len(lists_of_aa) ==6:
                pass
            else:
                sites_changed_aa[i].append(values[index])
    out_sites.close()

    convergent = {}
    divergent = {}
    #deal with sites with changed amino acid
    #filter sites with only one substitution or empty
    out_filter_excel = open(gene + '_sites_Convergent_Divergent.xls','w')
    for l,m in sites_changed_aa.items():
        site = l

        if len(m) ==0 or len(m) ==1:
            pass
        else:
            #write out convergent and divergent sites and get convergent sites
            out_filter_excel.write(site+ '\t')
            for index,value in enumerate(m):
                split_species = value.split('_',6)
                species_1 = split_species[-1]
                site_and_branch_1 = '_'.join(split_species[:-1])
                out_filter_excel.write(species_1+'_' + site_and_branch_1 + '\t')
            out_filter_excel.write('\n')
            
            convergent[site]=[]
            divergent[site] =[]
            #comparison among each element in the list
            flag_1 =0
            while flag_1 < len(m):
                flag_2 = flag_1+1
                site_1 = m[flag_1]
                list_of_element = site_1.split('_',6)
                descdant_1 = list_of_element[1]
                while flag_2 < len(m):
                    site_2 = m[flag_2]
                    list_2 = site_2.split('_',6)
                    descdant_2 = list_2[1]
                    sites = [site_1,site_2]
                    if descdant_1 == descdant_2:
                        convergent[site].append(sites)
                    if descdant_1 != descdant_2:
                        divergent[site].append(sites)
                    flag_2 = flag_2 + 1
                flag_1 = flag_1 +1     
    out_filter_excel.close()
    
    UV_mammals =['Danaus_plexippus','Oncopeltus_fasciatus','Photinus_pyralis']

    #write convergent sites to file and excel
    convergent_excel=open(gene + '_Convergent_all_species.xls','w')
    convergent_statis={}
    

    for i,j in convergent.items():
        if len(j) > 0:
            convergent_statis[i]={}
            convergent_excel.write(i + '\t')
            for x,y in enumerate(j):
                convergent_excel.write(str(y) + '\t')
                con_site_1 = y[0]
                con_list_1 = con_site_1.split('_',6)
                con_species_1 = con_list_1[-1]
                con_des_aa = con_list_1[1]
                #print (con_des_aa)
                con_site_2 = y[1]
                con_list_2 = con_site_2.split('_',6)
                con_species_2 = con_list_2[-1]
                
                if convergent_statis[i].get(con_des_aa,None):
                    convergent_statis[i][con_des_aa].extend([con_species_1,con_species_2])
                else:
                    convergent_statis[i][con_des_aa]=([con_species_1,con_species_2])
            convergent_excel.write('\n') 
    convergent_excel.close()
    
    convergent_uv_mammals = open(gene + '_Convergent_target_species.xls','w')
    for i,j in convergent_statis.items():
        #print (i)
        #print j
        for x,y in j.items():
            #print(y)
            if set (y).issubset(set(UV_mammals)):
                # print (y)
                convergent_uv_mammals.write(i + '\t')
                for m,n in enumerate(convergent[i]):
                    #print (y)
                    con_site_3 =n[0]
                    con_list_3 = con_site_3.split('_',6)
                    con_species_3 = con_list_3[-1]
                    site_branch_3 = '_'.join (con_list_3[:-1])
                    con_aa = con_list_3[1]
                    con_site_4 = n[1]
                    con_list_4 = con_site_4.split('_',6)
                    con_species_4 = con_list_4[-1]
                    site_branch_4 = '_'.join(con_list_4[:-1])
                    #print (con_aa)
                    if con_aa == x :
                        #print (y)
                        convergent_uv_mammals.write(str([con_species_3 + '_' + site_branch_3, con_species_4 + '_' + site_branch_4]) + '\t')
                convergent_uv_mammals.write('\n')    
          
  