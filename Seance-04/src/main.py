#coding:utf8

import numpy as np
import pandas as pd
import scipy
import scipy.stats
import os

#https://docs.scipy.org/doc/scipy/reference/stats.html


dist_names = ['norm', 'beta', 'gamma', 'pareto', 't', 'lognorm', 'invgamma', 'invgauss',  'loggamma', 'alpha', 'chi', 'chi2', 'bradford', 'burr', 'burr12', 'cauchy', 'dweibull', 'erlang', 'expon', 'exponnorm', 'exponweib', 'exponpow', 'f', 'genpareto', 'gausshyper', 'gibrat', 'gompertz', 'gumbel_r', 'pareto', 'pearson3', 'powerlaw', 'triang', 'weibull_min', 'weibull_max', 'bernoulli', 'betabinom', 'betanbinom', 'binom', 'geom', 'hypergeom', 'logser', 'nbinom', 'poisson', 'poisson_binom', 'randint', 'zipf', 'zipfian']

print(dist_names)


# 0. CRÉATION DU DOSSIER IMAGES SI ABSENT

if not os.path.exists("images"):
    os.makedirs("images")



# 1. FONCTIONS POUR CALCULER MOYENNE ET ECART-TYPE

def calcul_stats(distribution, params, size=10000):
    data = distribution.rvs(*params, size=size)
    return np.mean(data), np.std(data)


# -----------------------------------------------------------
# 2. FONCTIONS POUR SAUVER LES GRAPHES
# -----------------------------------------------------------
def save_discrete(name, data, bins=None):
    plt.figure()
    plt.hist(data, bins=bins, density=True)
    plt.title(f"Distribution discrète : {name}")
    plt.xlabel("Valeurs")
    plt.ylabel("Probabilité")
    plt.grid()

    filename = f"images/{name.replace(' ', '_')}.png"
    plt.savefig(filename)
    plt.close()
    print(f"[OK] Image enregistrée : {filename}")


def save_continuous(name, data):
    plt.figure()
    plt.hist(data, bins=50, density=True)
    plt.title(f"Distribution continue : {name}")
    plt.xlabel("Valeurs")
    plt.ylabel("Densité")
    plt.grid()

    filename = f"images/{name.replace(' ', '_')}.png"
    plt.savefig(filename)
    plt.close()
    print(f"[OK] Image enregistrée : {filename}")


# -----------------------------------------------------------
# 3. DISTRIBUTIONS DISCRÈTES
# -----------------------------------------------------------

# Dirac
data_dirac = np.full(10000, 3)
save_discrete("Dirac_3", data_dirac)

# Uniforme discrète
data_uniforme_discrete = randint.rvs(0, 10, size=10000)
save_discrete("Uniforme_discrete_0_10", data_uniforme_discrete)

# Binomiale
data_binom = binom.rvs(n=20, p=0.4, size=10000)
save_discrete("Binomiale_n20_p04", data_binom)

# Poisson discrète
data_poisson = poisson.rvs(mu=5, size=10000)
save_discrete("Poisson_discrete_mu5", data_poisson)

# Zipf
data_zipf = zipf.rvs(a=2, size=10000)
save_discrete("Zipf_Mandelbrot_a2", data_zipf, bins=50)


# -----------------------------------------------------------
# 4. DISTRIBUTIONS CONTINUES
# -----------------------------------------------------------

# Poisson continue (approx)
data_poisson_cont = poisson.rvs(10, size=10000) + np.random.normal(0, 0.2, 10000)
save_continuous("Poisson_continue_approx", data_poisson_cont)

# Normale
data_normale = norm.rvs(loc=0, scale=1, size=10000)
save_continuous("Normale_0_1", data_normale)

# Log-normale
data_lognorm = lognorm.rvs(s=0.9, size=10000)
save_continuous("Log_normale_s09", data_lognorm)

# Uniforme continue
data_uniforme = uniform.rvs(loc=0, scale=10, size=10000)
save_continuous("Uniforme_continue_0_10", data_uniforme)

# Chi-deux
data_chi2 = np.random.chisquare(df=4, size=10000)
save_continuous("Chi2_df4", data_chi2)

# Pareto
data_pareto = pareto.rvs(b=3, size=10000)
save_continuous("Pareto_b3", data_pareto)


# -----------------------------------------------------------
# 5. CALCUL DES STATISTIQUES POUR TOUTES LES DISTRIBUTIONS
# -----------------------------------------------------------

print("\n--- STATISTIQUES DES DISTRIBUTIONS ---\n")

distributions = {
    "Uniforme discrète": (randint, (0, 10)),
    "Binomiale": (binom, (20, 0.4)),
    "Poisson discrète": (poisson, (5,)),
    "Normale": (norm, (0, 1)),
    "Log-normale": (lognorm, (0.9,)),
    "Uniforme continue": (uniform, (0, 10)),
    "Pareto": (pareto, (3,))
}

for name, (dist, params) in distributions.items():
    m, s = calcul_stats(dist, params)
    print(f"{name} → moyenne = {m:.2f}, écart-type = {s:.2f}")
