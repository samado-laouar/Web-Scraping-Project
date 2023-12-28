import sys, re,os

corpus_medical = open(sys.argv[1], 'r', encoding="utf-8").readlines()
subst = open('subst.dic', 'r', encoding="utf-16-le").readlines()
enrich = open("subts_enrichi.dic", 'w', encoding="utf-16-le")

enrich.write('\ufeff')
enrich_list = []
unique_portions_set = set()

for i in corpus_medical:
    token = re.search(r"^-? ?(\w+) :? ?(\d+|\.|,)+ (mg|ml).+", i, re.I)
    if token:
        medecine = str(token.group(1)).lower()
        # some special cases that should not be included

            # Check for uniqueness based on a portion of the medicine name
        if not medecine.startswith("ø") and medecine != "témesta" and medecine != "intraveineuse" and medecine != "kardégic":
            portion = medecine.split()[0]  # Use the first word as the portion
            if portion not in unique_portions_set:
                enrich_list.append(re.sub(r'\d+$', '', str(token.group(1))))
                unique_portions_set.add(portion)
                subst.append(medecine + ",.N+subst\n")

    another_token = re.search(r"^(\w+\s*\d+|\w+\s\w+\s*\d+)\s:\s(½\s|\d+\s)(goutte|sachet|par|le|\s|jour|j|jour|nuit|matin|midi|soir|coucher|agitation|douleur|h|ge)+", i , re.I)
    if another_token:
        medecine = str(another_token.group(1)).lower()
        # some special cases that should not be included
        if not medecine.startswith("ø") and medecine != "témesta" and medecine != "intraveineuse" and medecine != "kardégic":
            portion = medecine.split()[0]  # Use the first word as the portion
            if portion not in unique_portions_set:
                enrich_list.append(re.sub(r'\d+$', '', medecine))
                unique_portions_set.add(portion)
                subst.append(medecine + ",.N+subst\n")

# Writing the subts_enrichi.dic File
count = 1
for i in enrich_list:
    enrich.write(i.lower() + ",.N+subst\n")
    # print(str(count) + " - " + i)
    count += 1
enrich.close()





# Building infos2.txt
infos2 = open('infos2.txt', 'w')
infos2l = open('MedCM.txt', 'w')
count = 0
# Utiliser une liste en compréhension pour convertir tous les éléments en minuscules
enrich_list = [element.lower() for element in enrich_list]
enrich_list = list(dict.fromkeys(sorted(enrich_list)))
first_char = enrich_list[0][0]

# Afficher la liste mise à jour
for i in enrich_list:
    if (i.startswith(first_char)):
        infos2.write("\t"+i.lower()+"\n")
        infos2l.write(i.lower()+"\n")
        count += 1
    else:
        infos2.write("--------------------------------------------\n")
        infos2.write("Nombre Total de '"+ first_char.upper() +"' : " + str(count) + "\n")
        infos2.write("--------------------------------------------\n")
        infos2.write("\t"+i.lower()+"\n")
        infos2l.write(i.lower()+"\n")
        first_char = i[0]
        count = 1
# Write the number with letter "Z"
infos2.write("Number of medecines starting with letter '"+ first_char.upper() +"' : " + str(count) + "\n")
infos2.write("\nTotal number of enriched medecines : " + str(len(enrich_list)))
infos2.close()
infos2l.close()


# Définir le nom des fichiers
# Définir le nom des fichiers
fichier_enrichi = "MedCM.txt"
fichier_subst = "MedUrl.txt"
fichier_info = "infos3.txt"
cpt=0
# Lire les éléments du fichier enrichi
with open(fichier_enrichi, 'r') as fichier_enrichi:
    elements_enrichis = set(ligne.strip() for ligne in fichier_enrichi)

# Lire les éléments du fichier subst
with open(fichier_subst, 'r') as fichier_subst:
    elements_subst = set(ligne.strip() for ligne in fichier_subst)

# Ouvrir le fichier infos3.txt en mode écriture
with open(fichier_info, 'w') as fichier_info:
    # Parcourir les éléments du fichier enrichi
    for element in elements_enrichis:
        # Vérifier si l'élément est présent dans le fichier subst
        if element not in elements_subst:
            # Écrire l'élément dans le fichier infos3.txt
            cpt=cpt+1
            fichier_info.write(element + '\n')
#print("Vérification terminée. Les éléments absents ont été écrits dans info3.txt.")


file_path = "infos3.txt"

# Read the lines from the file
with open(file_path, 'r') as file:
    lines = file.readlines()

# Sort the lines
sorted_lines = sorted(lines)

# Write the sorted lines back to the file
with open(file_path, 'w') as file:
    file.writelines(sorted_lines)
    file.write("Nombre total de médicaments conservés pour l’enrichissement : " + str(cpt) + "\n")


infos2l.close()
#os.remove("m.txt")
#os.remove("l.txt")


# Updating the subst.dic with all new changes
temp = open("subst.dic","w",encoding="utf-16-le")
temp.write('\ufeff')

subst = list(dict.fromkeys(sorted(subst)))

temp.write(subst[-1])

for i in subst:
    if i[0] <= 'e':
        temp.write(i)

for i in subst:
    if i[0] == 'é':
        temp.write(i)

for i in subst:
    if i[0] > 'e' and i[0] <= 'z':
        temp.write(i)

temp.close()