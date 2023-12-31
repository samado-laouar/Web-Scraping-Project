#Laouar Abdessamed
#Tougherghi Yacine


import re, sys, urllib
# urlib is a library used to open URLs and make some treatments with the website files (Get the content of HTML file for example)
from urllib.request import urlopen

try:
    website = urlopen("http://127.0.0.1:80/vidal/vidal-Sommaires-Substances-A.html")
    urlstring = "/vidal"
except urllib.error.HTTPError as e:
    try:
        website = urlopen("http://127.0.0.1/www.vidal.com/vidal-Sommaires-Substances-A.html")
        urlstring = "/www.vidal.com"
    except urllib.error.HTTPError as e:
        website = urlopen("http://127.0.0.1/vidal-Sommaires-Substances-A.html")
        urlstring = ""

# Verify if the first argument is syntaxicly correct
if len(sys.argv[1]) == 3 and re.match("[a-zA-Z]-[a-zA-Z]",sys.argv[1]):
    if sys.argv[1][0] <= sys.argv[1][2]:
        first = ord(sys.argv[1][0].upper())
        last = ord(sys.argv[1][2].upper())
    else:
        first = ord(sys.argv[1][2].upper())
        last = ord(sys.argv[1][0].upper())
else:
    first = ord("A")
    last = ord("Z")

subst = open('subst.dic', 'w', encoding="utf-16-le")
subst.write('\ufeff')
info = open('infos.txt', 'w')

cpt = 0
# ord(char): elle prend un charactere et nous donne son code ASCII.
# chr(int) : elle prend un code ASCII et nous donne son Char correspendent.
for i in range(first, last + 1):
    website = urlopen("http://127.0.0.1:"+sys.argv[2]+ urlstring + "/vidal-Sommaires-Substances-"+chr(i)+".html").read().decode("utf-8")

    medecine = re.findall(r'[0-9]+\.htm">(.+)<', website)

    for j in medecine:
        # if j.startswith('é'):
        #     j = 'e' + j[1:]
        subst.write(j + ",.N+subst\n")
    # subst.write("\n")

    info.write("Total de "+chr(i)+" : "+str(len(medecine)) + "\n")
    cpt += len(medecine)

info.write("Total number of medecine with substance preserved = " + str(cpt))
subst.close()
info.close()
