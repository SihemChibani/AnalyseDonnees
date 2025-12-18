# coding: utf8

import pandas as pd
import matplotlib.pyplot as plt
import os


# Chargement du fichier CSV


chemin_csv = "./data/resultats-elections-presidentielles-2022-1er-tour.csv"

with open(chemin_csv, "r", encoding="utf-8") as fichier:
    contenu = pd.read_csv(fichier)

print("Contenu du tableau :")
print(contenu)


# Question 6 : dimensions


nb_lignes = len(contenu)
nb_colonnes = len(contenu.columns)

print("Nombre de lignes :", nb_lignes)
print("Nombre de colonnes :", nb_colonnes)


# Question 7 : types des variables


types_variables = []

for col in contenu.columns:
    t = contenu[col].dtype
    if "int" in str(t):
        types_variables.append(("int", col))
    elif "float" in str(t):
        types_variables.append(("float", col))
    elif "bool" in str(t):
        types_variables.append(("bool", col))
    else:
        types_variables.append(("str", col))

print("Types de chaque colonne :")
for t, col in types_variables:
    print(col, ":", t)


# Question 8 : premières lignes


print("Premières lignes :")
print(contenu.head())


# Question 9 : colonne Inscrits


if "Inscrits" in contenu.columns:
    print(contenu["Inscrits"])


# Question 10 : sommes


print("Somme des colonnes quantitatives :")
for t, col in types_variables:
    if t in ("int", "float"):
        print(col, ":", contenu[col].sum())


# Création dossier images


if not os.path.exists("images"):
    os.makedirs("images")


# Question 11 : diagrammes en barres


for _, ligne in contenu.iterrows():
    code = ligne["Code du département"]
    nom = ligne["Libellé du département"]

    plt.figure()
    plt.bar(
        ["Inscrits", "Votants"],
        [ligne["Inscrits"], ligne["Votants"]]
    )
    plt.title(f"Inscrits et votants – {nom} ({code})")
    plt.savefig(f"images/bar_{code}.png")
    plt.close()


# Question 12 : diagrammes circulaires


colonnes_pie = ["Blancs", "Nuls", "Exprimés", "Abstentions"]

for _, ligne in contenu.iterrows():
    code = ligne["Code du département"]
    nom = ligne["Libellé du département"]
    valeurs = [ligne[col] for col in colonnes_pie]

    plt.figure()
    plt.pie(valeurs, labels=colonnes_pie, autopct="%1.1f%%")
    plt.title(f"Répartition des votes – {nom} ({code})")
    plt.savefig(f"images/pie_{code}.png")
    plt.close()

# Question 13 : histogramme


plt.figure()
plt.hist(contenu["Inscrits"], density=True)
plt.title("Histogramme des inscrits (tous départements)")
plt.savefig("images/histogramme_inscrits.png")
plt.close()


# BONUS : voix par candidat


colonnes_candidats = [col for col in contenu.columns if "Voix" in col]

# Par département
for _, ligne in contenu.iterrows():
    code = ligne["Code du département"]
    nom = ligne["Libellé du département"]
    valeurs = [ligne[col] for col in colonnes_candidats]

    plt.figure()
    plt.pie(valeurs, labels=colonnes_candidats, autopct="%1.1f%%")
    plt.title(f"Voix par candidat – {nom} ({code})")
    plt.savefig(f"images/pie_candidats_{code}.png")
    plt.close()

# France entière
totaux_france = [contenu[col].sum() for col in colonnes_candidats]

plt.figure()
plt.pie(totaux_france, labels=colonnes_candidats, autopct="%1.1f%%")
plt.title("Voix par candidat – France entière")
plt.savefig("images/pie_candidats_france.png")
plt.close()
