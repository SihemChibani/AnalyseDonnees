# coding: utf8

import pandas as pd
import matplotlib.pyplot as plt
import os

# ---- Chargement du fichier CSV ----
chemin_csv = "./data/resultats-elections-presidentielles-2022-1er-tour.csv"

with open(chemin_csv, "r", encoding="utf-8") as fichier:
    contenu = pd.read_csv(fichier)

print("Contenu du tableau :")
print(contenu)

# ---- Question 6 : Nombre de lignes et colonnes ----
nb_lignes = len(contenu)
nb_colonnes = len(contenu.columns)

print("Nombre de lignes :", nb_lignes)
print("Nombre de colonnes :", nb_colonnes)

# ---- Question 7 : Type statistique des colonnes ----
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

# ---- Question 8 : Affichage des premières lignes ----
print("Premières lignes :")
print(contenu.head())

# ---- Question 9 : Sélection des inscrits ----
if "Inscrits" in contenu.columns:
    print("Colonne Inscrits :")
    print(contenu["Inscrits"])
else:
    print("Colonne 'Inscrits' introuvable.")

# ---- Question 10 : Somme des colonnes quantitatives ----
somme_colonnes = []

for t, col in types_variables:
    if t in ("int", "float"):
        somme_colonnes.append((col, contenu[col].sum()))

print("Somme des colonnes quantitatives :")
for col, val in somme_colonnes:
    print(col, ":", val)

# ---- Création du dossier images ----
if not os.path.exists("images"):
    os.makedirs("images")

# ---- Question 11 : Diagrammes en barres ----
if "Code département" in contenu.columns and "Inscrits" in contenu.columns and "Votants" in contenu.columns:
    for _, ligne in contenu.iterrows():
        dept = ligne["Code du département"]

        plt.figure()
        plt.bar(["Inscrits", "Votants"], [ligne["Inscrits"], ligne["Votants"]])
        plt.title(f"Inscrits et votants – Département {dept}")
        plt.savefig(f"images/bar_{dept}.png")
        plt.close()

# ---- Question 12 : Diagrammes circulaires ----
colonnes_pie = ["Blancs", "Nuls", "Exprimés", "Abstentions"]

if all(col in contenu.columns for col in colonnes_pie):
    for _, ligne in contenu.iterrows():
        dept = ligne["Code du département"]
        valeurs = [ligne[col] for col in colonnes_pie]

        plt.figure()
        plt.pie(valeurs, labels=colonnes_pie, autopct="%1.1f%%")
        plt.title(f"Répartition votes – Département {dept}")
        plt.savefig(f"images/pie_{dept}.png")
        plt.close()

# ---- Question 13 : Histogramme des inscrits ----
if "Inscrits" in contenu.columns:
    plt.figure()
    plt.hist(contenu["Inscrits"], density=True)
    plt.title("Histogramme des inscrits")
    plt.savefig("images/histogramme_inscrits.png")
    plt.close()

# ---- BONUS : Voix par candidat ----
colonnes_candidats = [col for col in contenu.columns if "Voix" in col]

if len(colonnes_candidats) > 0:
    # Par département
    for _, ligne in contenu.iterrows():
        dept = ligne["Code du département"]
        valeurs = [ligne[col] for col in colonnes_candidats]

        plt.figure()
        plt.pie(valeurs, labels=colonnes_candidats, autopct="%1.1f%%")
        plt.title(f"Voix par candidat – Département {dept}")
        plt.savefig(f"images/pie_candidats_{dept}.png")
        plt.close()

    # France entière
    totaux_france = [contenu[col].sum() for col in colonnes_candidats]

    plt.figure()
    plt.pie(totaux_france, labels=colonnes_candidats, autopct="%1.1f%%")
    plt.title("Voix par candidat – France entière")
    plt.savefig("images/pie_candidats_france.png")
    plt.close()
