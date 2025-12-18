#coding:utf8

import pandas as pd
import math
import scipy
import scipy.stats
from scipy import stats


#C'est la partie la plus importante dans l'analyse de données. D'une part, elle n'est pas simple à comprendre tant mathématiquement que pratiquement. D'autre, elle constitue une application des probabilités. L'idée consiste à comparer une distribution de probabilité (théorique) avec des observations concrètes. De fait, il faut bien connaître les distributions vues dans la séance précédente afin de bien pratiquer cette comparaison. Les probabilités permettent de définir une probabilité critique à partir de laquelle les résultats ne sont pas conformes à la théorie probabiliste.
#Il n'est pas facile de proposer des analyses de données uniquement dans un cadre univarié. Vous utiliserez la statistique inférentielle principalement dans le cadre d'analyses multivariées. La statistique univariée est une statistique descriptive. Bien que les tests y soient possibles, comprendre leur intérêt et leur puissance d'analyse dans un tel cadre peut être déroutant.
#Peu importe dans quelle théorie vous êtes, l'idée de la statistique inférentielle est de vérifier si ce que vous avez trouvé par une méthode de calcul est intelligent ou stupide. Est-ce que l'on peut valider le résultat obtenu ou est-ce que l'incertitude qu'il présente ne permet pas de conclure ? Peu importe également l'outil, à chaque mesure statistique, on vous proposera un test pour vous aider à prendre une décision sur vos résultats. Il faut juste être capable de le lire.

#Par convention, on place les fonctions locales au début du code après les bibliothèques.
def ouvrirUnFichier(nom):
    with open(nom, "r") as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

#Théorie de l'échantillonnage (intervalles de fluctuation)
#L'échantillonnage se base sur la répétitivité.
print("Résultat sur le calcul d'un intervalle de fluctuation")

donnees = pd.DataFrame(ouvrirUnFichier("./data/Echantillonnage-100-Echantillons.csv"))

#Théorie de l'estimation (intervalles de confiance)
#L'estimation se base sur l'effectif.
print("Résultat sur le calcul d'un intervalle de confiance")

#Théorie de la décision (tests d'hypothèse)
#La décision se base sur la notion de risques alpha et bêta.
#Comme à la séance précédente, l'ensemble des tests se trouve au lien : https://docs.scipy.org/doc/scipy/reference/stats.html
print("Théorie de la décision")



# 1) THÉORIE DE L'ÉCHANTILLONNAGE

print("\n 1) INTERVALLES DE FLUCTUATION")

# Population mère
pop_pour    = 852
pop_contre  = 911
pop_sans    = 422
N_pop       = pop_pour + pop_contre + pop_sans

freq_pop = {
    "Pour"  : pop_pour   / N_pop,
    "Contre": pop_contre / N_pop,
    "Sans"  : pop_sans   / N_pop,
}

# Chargement des 100 échantillons
donnees = ouvrirUnFichier("./data/Echantillonnage-100-Echantillons.csv")

# Moyenne arrondie de chaque opinion
moyennes = donnees.mean().round(0)
print("\nMoyennes observées dans les 100 échantillons :")
print(moyennes)

# Fréquences observées
total_moyen = moyennes.sum()
freq_obs = (moyennes / total_moyen).round(2)

print("\nFréquences observées :")
print(freq_obs)

print("\nFréquences population mère :")
print(freq_pop)

# Intervalle de fluctuation à 95 % (z=1.96)
z = 1.96

print("\nIntervalles de fluctuation à 95 % :")

for opinion in ["Pour", "Contre", "Sans opinion"]:
    p = freq_obs[opinion]
    n = total_moyen
    marge = z * math.sqrt(p * (1 - p) / n)
    print(f"{opinion} : [{round(p - marge, 3)}, {round(p + marge, 3)}]")



# 2) THÉORIE DE L'ESTIMATION

print("\n 2) INTERVALLES DE CONFIANCE")

# Premier échantillon
ech1 = list(donnees.iloc[0])
total_ech1 = sum(ech1)

freq_ech1 = [round(x / total_ech1, 3) for x in ech1]

print("\nFréquences du premier échantillon :")
print(f"Pour : {freq_ech1[0]}, Contre : {freq_ech1[1]}, Sans opinion : {freq_ech1[2]}")

# Intervalle de confiance pour proportions
print("\nIntervalles de confiance à 95 % :")

for i, opinion in enumerate(["Pour", "Contre", "Sans opinion"]):
    p = freq_ech1[i]
    marge = z * math.sqrt(p * (1 - p) / total_ech1)
    print(f"{opinion} : [{round(p - marge, 3)}, {round(p + marge, 3)}]")



# 3) THÉORIE DE LA DÉCISION : Test de Shapiro-Wilk

print("\n 3) TEST DE NORMALITÉ (Shapiro-Wilk) ")

data1 = ouvrirUnFichier("./data/Loi-normale-Test-1.csv")
data2 = ouvrirUnFichier("./data/Loi-normale-Test-2.csv")

stat1, p1 = stats.shapiro(data1)
stat2, p2 = stats.shapiro(data2)

print("\nTest Shapiro-Wilk :")
print(f"Test 1 → p = {p1}")
print(f"Test 2 → p = {p2}")

if p1 > 0.05:
    print(" Le fichier Test 1 suit une loi normale.")
else:
    print(" Le fichier Test 1 NE suit PAS une loi normale.")

if p2 > 0.05:
    print(" Le fichier Test 2 suit une loi normale.")
else:
    print(" Le fichier Test 2 NE suit PAS une loi normale.")

print("\nFIN DU PROGRAMME")