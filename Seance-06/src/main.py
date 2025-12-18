#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import math
import os


# FONCTIONS


def ouvrirUnFichier(nom):
    """Lecture CSV"""
    with open(nom, "r", encoding="utf8") as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

def conversionLog(liste):
    """Conversion logarithmique"""
    return [math.log(float(x)) for x in liste if float(x) > 0]

def ordreDecroissant(liste):
    """Tri décroissant natif Python"""
    liste.sort(reverse=True)
    return liste

def ordrePopulation(pop, etat):
    """Classement (rang, pays) trié par population décroissante"""
    ordrepop = []
    for i in range(len(pop)):
        if not np.isnan(pop[i]):
            ordrepop.append([float(pop[i]), etat[i]])

    ordrepop = ordreDecroissant(ordrepop)

    for i in range(len(ordrepop)):
        ordrepop[i] = [i + 1, ordrepop[i][1]]

    return ordrepop

def classementPays(ordre1, ordre2):
    """
    Fusion des classements sous forme :
    [rang_pop, rang_dens, État]
    """
    classement = []
    for r1, state1 in ordre1:
        for r2, state2 in ordre2:
            if state1 == state2:
                classement.append([r1, r2, state1])
                break
    return classement

# PARTIE I : LES ÎLES


print("\nPARTIE I : Classement des îles (rank-size)")

iles = pd.DataFrame(ouvrirUnFichier("./data/island-index.csv"))

print("Colonnes trouvées dans island-index.csv :", list(iles.columns))

#  Extraction de la colonne surface
col_surface = "Surface (km²)"
print("Colonne utilisée pour la surface :", col_surface)

surface = list(iles[col_surface])

# Ajout des 5 continents 
ajouts = [
    85545323,  # Asie/Afrique/Europe
    37856841,  # Amérique
    7768030,   # Antarctique
    7605049    # Australie
]

surface.extend([float(x) for x in ajouts])

#  Tri décroissant 
surface_triee = ordreDecroissant(surface.copy())

#  Construction du classement 
noms = list(iles["Toponyme"])
noms.extend(["Asie/Afrique/Europe", "Amérique", "Antarctique", "Australie"])

# Nom et surface triée 
classement_iles = pd.DataFrame({
    "rank": list(range(1, len(surface_triee) + 1)),
    "name": noms[:len(surface_triee)],
    "surface_km2": surface_triee
})

os.makedirs("images", exist_ok=True)
classement_iles.to_csv("images/rank_size_islands.csv", index=False)

print("Classement des îles enregistré : images/rank_size_islands.csv (top 10)")
print(classement_iles.head(10))

# Plot linéaire 
plt.figure(figsize=(8,5))
plt.plot(classement_iles["rank"], classement_iles["surface_km2"])
plt.xlabel("Rang")
plt.ylabel("Surface")
plt.title("Rank-size des îles (linéaire)")
plt.savefig("images/rank_size_islands_linear.png")
print("Image enregistrée : images/rank_size_islands_linear.png")

# Version logarithmique 
log_rang = conversionLog(classement_iles["rank"])
log_surf = conversionLog(classement_iles["surface_km2"])

plt.figure(figsize=(8,5))
plt.plot(log_rang, log_surf)
plt.xlabel("log(Rang)")
plt.ylabel("log(Surface)")
plt.title("Rank-size des îles (log-log)")
plt.savefig("images/rank_size_islands_log.png")
print("Image enregistrée : images/rank_size_islands_log.png")


#    PARTIE II : POPULATION  


print("\nPARTIE II : Classements mondiaux (population et densité)")

monde = pd.DataFrame(ouvrirUnFichier("./data/Le-Monde-HS-Etats-du-monde-2007-2025.csv"))

print("Colonnes trouvées dans Le-Monde :", list(monde.columns))

col_etat = "État"
col_pop_2007 = "Pop 2007"
col_pop_2025 = "Pop 2025"
col_dens_2007 = "Densité 2007"
col_dens_2025 = "Densité 2025"

print("Colonnes choisies :")
print("Etat:", col_etat)
print("Pop 2007:", col_pop_2007)
print("Pop 2025:", col_pop_2025)
print("Dens 2007:", col_dens_2007)
print("Dens 2025:", col_dens_2025)

# Extraction
etat = list(monde[col_etat])
pop2007 = list(monde[col_pop_2007])
pop2025 = list(monde[col_pop_2025])
dens2007 = list(monde[col_dens_2007])
dens2025 = list(monde[col_dens_2025])

# Ordonnancement
ordre_pop2007 = ordrePopulation(pop2007, etat)
ordre_pop2025 = ordrePopulation(pop2025, etat)
ordre_dens2007 = ordrePopulation(dens2007, etat)
ordre_dens2025 = ordrePopulation(dens2025, etat)

# Sauvegarde CSV
pd.DataFrame(ordre_pop2007).to_csv("images/classement_population_2007_2025.csv", index=False)
pd.DataFrame(ordre_dens2007).to_csv("images/classement_densite_2007_2025.csv", index=False)

# Fusion des classements
classement_pop = classementPays(ordre_pop2007, ordre_pop2025)
classement_dens = classementPays(ordre_dens2007, ordre_dens2025)

# Récupération rangs seuls
rang_pop_2007 = [x[0] for x in classement_pop]
rang_pop_2025 = [x[1] for x in classement_pop]

rang_dens_2007 = [x[0] for x in classement_dens]
rang_dens_2025 = [x[1] for x in classement_dens]

#  CORRÉLATIONS SPEARMAN / KENDALL 

print("\nCorrélation des rangs population (2007 vs 2025) :")
spearman_pop = scipy.stats.spearmanr(rang_pop_2007, rang_pop_2025)
kendall_pop = scipy.stats.kendalltau(rang_pop_2007, rang_pop_2025)
print("Spearman:", spearman_pop.correlation, "p-value:", spearman_pop.pvalue)
print("Kendall :", kendall_pop.correlation, "p-value:", kendall_pop.pvalue)

print("\nCorrélation des rangs densité (2007 vs 2025) :")
spearman_dens = scipy.stats.spearmanr(rang_dens_2007, rang_dens_2025)
kendall_dens = scipy.stats.kendalltau(rang_dens_2007, rang_dens_2025)
print("Spearman:", spearman_dens.correlation, "p-value:", spearman_dens.pvalue)
print("Kendall :", kendall_dens.correlation, "p-value:", kendall_dens.pvalue)


# BONUS : Factorisation et analyse multi-années


def analyse_concordance(popA, popB):
    """Retourne Spearman + Kendall"""
    s = scipy.stats.spearmanr(popA, popB)
    k = scipy.stats.kendalltau(popA, popB)
    return s.correlation, s.pvalue, k.correlation, k.pvalue

# Analyse 2007 à 2025 pour population
annees = list(range(2007, 2026))
correlations = []

for year in annees:
    colA = f"Pop 2007"
    colB = f"Pop {year}"

    popA = list(monde[colA])
    popB = list(monde[colB])

    # classements
    ordA = ordrePopulation(popA, etat)
    ordB = ordrePopulation(popB, etat)
    fusion = classementPays(ordA, ordB)

    rA = [x[0] for x in fusion]
    rB = [x[1] for x in fusion]

    corrS, pS, corrK, pK = analyse_concordance(rA, rB)
    correlations.append([year, corrS, pS, corrK, pK])

pd.DataFrame(correlations, columns=["year", "spearman", "pS", "kendall", "pK"]).to_csv(
    "images/correlations_population_2007_2025.csv", index=False
)

print("\nBonus : corrélations annuelles enregistrées dans images/correlations_population_2007_2025.csv")
