# Importing library
import re
import os
import itertools
import difflib
import datetime
from itertools import combinations

begin_time = datetime.datetime.now()

c = "\033[1;31;40m"
clear = "\033[0;00;00m"


print(c + "[+]"+clear+" Generating CPEs from System")
os.system("mkdir tmp 2>/dev/null")
# Generating value files
os.system("dpkg -l | tail -n +6 > tmp/output.txt")
os.system("cat tmp/output.txt | awk '{print $2}' > tmp/name.txt")
os.system("cat tmp/output.txt | awk '{print $3}' | sed 's/debian-buster//g' | sed 's/-[0-9]//g' | sed 's/[0-9]://g' | sed 's/+[0-9]//g' |  sed 's/+[a-z][0-9]//g' | sed 's/kali[0-9]//g' | sed 's/.dfsg//g' | sed 's/+nmu[0-9]//g' | sed 's/+git[0-99999999]//g' | sed 's/~git[0-99999999]//g' | sed 's/+ds//g' | sed 's/+debian//g' | sed 's/+//g' | sed 's/.ds[0-9]//g' | sed 's/~[[:alnum:]]//g' | sed 's/.git[1-9999999999]//g' | sed 's/.[A-Z]//g' | sed 's/-release//g'  > tmp/version.txt")
os.system("cat tmp/output.txt | awk '{print $4}' > tmp/archi.txt")

# Getting values from files to create list 
f1 = open('tmp/name.txt', 'r')
f2 = open('tmp/version.txt', 'r')
f3 = open('tmp/archi.txt', 'r')
f4 = open('tmp/name.txt', 'r')
f5 = open('official-cpe-dictionary_v2.3.xml', 'r')

name=[]
for n in f1:
    name.append(n)

version=[]
for v in f2:
    version.append(v)

archi=[]
for a in f3:
    archi.append(a)

os.system("touch tmp/results-1.txt tmp/results-2.txt tmp/results-3.txt")

outF = open("tmp/results-1.txt", "w")
for (na,ver) in zip(name,version):
	outF.write("cpe:2.3:a:"+na+":"+na+":"+ver+":*:*:*:*:*:*:*")

outF = open("tmp/results-2.txt", "w")
for (na,ver) in zip(name,version):
	outF.write("cpe:2.3:a:"+na+":"+na+":"+"-"+":*:*:*:*:*:*:*")

outF = open("tmp/results-3.txt", "w")
for (na,ver) in zip(name,version):
	outF.write("cpe:2.3:a:"+na+":"+na+":"+ver+":-:*:*:*:*:*:*")


# Right Formating of created list
os.system("cat tmp/results-1.txt | tr -d '\n' | sed -e 's/cpe/\\ncpe/g' | rev | cut -d'*' -f2- | rev | awk \'{print $0\"*\"}\' | tail -n +2 > tmp/active_result_1.txt")
os.system("cat tmp/results-2.txt | tr -d '\n' | sed -e 's/cpe/\\ncpe/g' | rev | cut -d'*' -f2- | rev | awk \'{print $0\"*\"}\' | tail -n +2 > tmp/active_result_2.txt")
os.system("cat tmp/results-3.txt | tr -d '\n' | sed -e 's/cpe/\\ncpe/g' | rev | cut -d'*' -f2- | rev | awk \'{print $0\"*\"}\' | tail -n +2 > tmp/active_result_3.txt")
print(c + "[+]"+clear+" Getting CPEs from official-cpe-dictionary")
os.system('cat official-cpe-dictionary_v2.3.xml | grep \'cpe:2.3:a:\' | cut -d \'\"\' -f2 > tmp/database.txt')
os.system("cat tmp/database.txt | awk -F: '{print $4,\":\",$5}' | sort | uniq -d | tr -d '[:blank:]' > tmp/ven-name.txt")
os.system("awk -F':' -v OFS=':' 'NR==FNR{map[$2]=$1} NR>FNR && ($5 in map) {$4=map[$5]} NR>FNR' tmp/ven-name.txt tmp/active_result_1.txt > tmp/guess_vendor_2.txt")
os.system("awk -F':' -v OFS=':' 'NR==FNR{map[$2]=$1} NR>FNR && ($5 in map) {$4=map[$5]} NR>FNR' tmp/ven-name.txt tmp/active_result_2.txt > tmp/guess_vendor_3.txt")
os.system("awk -F':' -v OFS=':' 'NR==FNR{map[$2]=$1} NR>FNR && ($5 in map) {$4=map[$5]} NR>FNR' tmp/ven-name.txt tmp/active_result_3.txt > tmp/guess_vendor_4.txt")
print(c + "[+]"+clear+" Comparing Both")

os.system("cat tmp/results-1.txt | tr -d '\n' | sed -e 's/cpe/\\ncpe/g' | rev | cut -d'*' -f2- | rev | awk \'{print $0\"*\"}\' | tail -n +2 > tmp/active_result-2.txt")
os.system("cat tmp/results-2.txt | tr -d '\n' | sed -e 's/cpe/\\ncpe/g' | rev | cut -d'*' -f2- | rev | awk \'{print $0\"*\"}\' | tail -n +2 > tmp/active_result-3.txt")
os.system("awk 'NR==FNR{a[$1]++;next} a[$1]' tmp/active_result-2.txt tmp/database.txt > tmp/final-2.txt")
os.system("awk 'NR==FNR{a[$1]++;next} a[$1]' tmp/active_result-3.txt tmp/database.txt > tmp/final-3.txt")
os.system("awk 'NR==FNR{a[$1]++;next} a[$1]' tmp/guess_vendor_2.txt tmp/database.txt > tmp/final-7.txt")
os.system("awk 'NR==FNR{a[$1]++;next} a[$1]' tmp/guess_vendor_3.txt tmp/database.txt > tmp/final-8.txt")
os.system("awk 'NR==FNR{a[$1]++;next} a[$1]' tmp/guess_vendor_4.txt tmp/database.txt > tmp/final-9.txt")

os.system("echo ''")
os.system("awk '{print $0}' tmp/final-2.txt tmp/final-3.txt tmp/final-7.txt tmp/final-8.txt tmp/final-9.txt | sort -u > cpe_results.txt")
r_amount = os.popen("cat cpe_results.txt | wc -l").read()
t_amount = os.popen("cat tmp/active_result-2.txt | wc -l").read()
d_amount = os.popen("cat tmp/database.txt | wc -l").read()
print("Total CPE Generated from System: "+c+str(t_amount)+clear+clear)
print("Total CPE Generated from cpe-dictionary: "+c+str(d_amount)+clear)
print("Total Matches: "+c+str(r_amount)+clear+clear+"Results:")
os.system("awk '{print $0}' tmp/final-2.txt tmp/final-3.txt tmp/final-7.txt tmp/final-8.txt | sort -u")
print("")

#os.system("rm -r tmp")
print(c + "Result save as cpe_results.txt" + clear)
print("Script Execution Duration: "+ c + str(datetime.datetime.now() - begin_time) + clear)



# allen_disk_project:allen_disk:1.5
# cpe:2.3:a:microsoft:windows:1.1:*:*:*:*:*:*:*
# cpe:2.3:a:vendor:name:version:*:*:*:*:*:*:archi
# awk -F: '$4 == $5 { print $0 }' tmp/database.txt | wc -l (Vendor name same as package name)
# os.system("awk -F: '$4 == $5 { print $0 }' tmp/active_result.txt > tmp/same_vendor.txt")