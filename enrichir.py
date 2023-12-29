import sys, re,os

corpus_medical = open(sys.argv[1], 'r', encoding="utf-8").readlines()
subst = open('subst.dic', 'r', encoding="utf-16-le").readlines()
tmp1 = open('subst.dic', 'r', encoding="utf-16-le").readlines()

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
tmp2  = open('subts_enrichi.dic', 'r', encoding="utf-16-le").readlines()
cpt=0
with open("infos3.txt", "w", encoding="utf-8") as fichier_write:
    # Convertir les lignes en ensembles
    tmp1_set = set(tmp1)
    tmp2_set = set(tmp2)

    # Trouver les éléments dans tmp2 qui ne sont pas dans tmp1
    elements_to_write = tmp2_set - tmp1_set

    # Écrire ces éléments dans le fichier_write
    for element in elements_to_write:
        cpt=cpt+1
        fichier_write.write(element)

fichier_write.close()
# Lire le contenu de fichier_write.txt
# Lire le contenu de infos3.txt
with open("infos3.txt", "r", encoding="utf-8") as file_infos3:
    contenu_infos3 = file_infos3.readlines()

# Trier les éléments de infos3.txt
elements_tries = sorted(contenu_infos3)

# Écrire les éléments triés dans le fichier tri_infos3.txt
with open("infos3.txt", "w", encoding="utf-8") as file_tri_infos3:
    for element in elements_tries:
        file_tri_infos3.write(element)

# Ajouter le nombre d'éléments à la fin de tri_infos3.txt
with open("infos3.txt", "a", encoding="utf-8") as file_tri_infos3:
    nombre_elements = len(elements_tries)
    file_tri_infos3.write("-----------------------------------------------------------------------------\n")
    file_tri_infos3.write("le nombre de médicaments conservés pour l’enrichissement : " + str(nombre_elements) + "\n")
    file_tri_infos3.write("-----------------------------------------------------------------------------\n")

file_path = "infos3.txt"

# Read the lines from the file
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Extract the words and remove the unnecessary parts
extracted_words = [line.split(",")[0] for line in lines]

# Write the extracted words back to the file
with open(file_path, 'w', encoding='utf-8') as file:
    file.writelines('\n'.join(extracted_words))


# Building infos2.txt
infos2 = open('infos2.txt', 'w')
count = 0
# Utiliser une liste en compréhension pour convertir tous les éléments en minuscules
enrich_list = [element.lower() for element in enrich_list]
enrich_list = list(dict.fromkeys(sorted(enrich_list)))
first_char = enrich_list[0][0]

# Afficher la liste mise à jour
for i in enrich_list:
    if (i.startswith(first_char)):
        infos2.write("\t"+i.lower()+"\n")
        count += 1
    else:
        infos2.write("--------------------------------------------\n")
        infos2.write("Nombre Total de '"+ first_char.upper() +"' : " + str(count) + "\n")
        infos2.write("--------------------------------------------\n")
        infos2.write("\t"+i.lower()+"\n")
        first_char = i[0]
        count = 1
# Write the number with letter "Z"
infos2.write("--------------------------------------------\n")
infos2.write("Nombre Total de '"+ first_char.upper() +"' : " + str(count) + "\n")
infos2.write("--------------------------------------------\n")
infos2.write("-----------------------------------------------------------------------------\n")
infos2.write("Le Nombre  total de médicaments issus du corpus : " + str(len(enrich_list))+"\n")
infos2.write("-----------------------------------------------------------------------------\n")
infos2.close()



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