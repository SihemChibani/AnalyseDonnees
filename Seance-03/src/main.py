#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


# Source des données : https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/

# Sources des données : production de M. Forriez, 2016-2023

# Question 4 : ouverture ficher avec "with"


with open("data/resultats-elections-presidentielles-2022-1er-tour.csv", "r", encoding="utf8") as f:
    df = pd.read_csv(f)

print("\n Données chargées ")
print(df.head())

# Création du dossier images
if not os.path.exists("images"):
    os.makedirs("images")


# Question 5 : séléction des colonnes et calculs statistiques


colonnes_quanti = df.select_dtypes(include=["int64", "float64"]).columns

print("\nColonnes quantitatives :")
for col in colonnes_quanti:
    print("-", col)




stats = []  # liste avec tous les résultats

for col in colonnes_quanti:

    moyenne = df[col].mean().round(2)
    mediane = df[col].median().round(2)

    mode = df[col].mode()
    if len(mode) > 0:
        mode = mode.iloc[0].round(2)
    else:
        mode = None

    ecart_type = df[col].std().round(2)
    ecart_abs = np.abs(df[col] - df[col].mean()).mean().round(2)
    etendue = (df[col].max() - df[col].min()).round(2)

    stats.append([col, moyenne, mediane, mode, ecart_type, ecart_abs, etendue])



# Question 6 : afficher les paramètres.


print("\n--- Statistiques des colonnes quantitatives ---")
for element in stats:
    print(element)



# Question 7 : Distance interquartile et interdécile 


print("\n Distances interquartile (IQR) et interdécile (IDR) ")

for col in colonnes_quanti:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    D1 = df[col].quantile(0.10)
    D9 = df[col].quantile(0.90)

    IQR = round(Q3 - Q1, 2)
    IDR = round(D9 - D1, 2)

    print(col, "→ IQR =", IQR, " | IDR =", IDR)



# Question 8 : boîtes à moustache 


for col in colonnes_quanti:
    plt.figure()
    df.boxplot(column=[col])
    plt.title(f"Boxplot — {col}")
    plt.savefig(f"images/boxplot_{col}.png")
    plt.close()

print("\nLes boxplots ont été enregistrés dans le dossier images/.")




df_island = pd.read_csv("data/island-index.csv")

surface = df_island["Surface (km²)"]


# Question 10 : catégorisation des surfaces


classes = {
    "]0-10]": ((surface > 0) & (surface <= 10)).sum(),
    "]10-25]": ((surface > 10) & (surface <= 25)).sum(),
    "]25-50]": ((surface > 25) & (surface <= 50)).sum(),
    "]50-100]": ((surface > 50) & (surface <= 100)).sum(),
    "]100-2500]": ((surface > 100) & (surface <= 2500)).sum(),
    "]2500-5000]": ((surface > 2500) & (surface <= 5000)).sum(),
    "]5000-10000]": ((surface > 5000) & (surface <= 10000)).sum(),
    "]10000+]": (surface >= 10000).sum()
}

print("\n--- Catégorisation des surfaces des îles ---")
for intervalle, nombre in classes.items():
    print(intervalle, ":", nombre)



# BONUS : 


df_stats = pd.DataFrame(stats, columns=[
    "Colonne", "Moyenne", "Mediane", "Mode", "Ecart type", "Ecart absolu", "Etendue"
])

df_stats.to_csv("images/statistiques.csv", index=False)
df_stats.to_excel("images/statistiques.xlsx", index=False)

print("\nFichiers statistiques.csv et statistiques.xlsx créés dans images/.")
