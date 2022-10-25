import random
import os

os.system("cls")

n = 10 # nombre de gênes considérés par individu
N = 20 # nombre d'individus dans la population
prob_mutation = 0.1
cible = [1 for i in range(n)]

def tamisage(tableau, comparaison, taille,indice):
	parent = indice
	enfant_gauche = 2 * indice + 1
	enfant_droit = 2 * indice + 2

	if enfant_gauche < taille and comparaison(tableau[parent], tableau[enfant_gauche]):
		parent = enfant_gauche

	if enfant_droit < taille and comparaison(tableau[parent], tableau[enfant_droit]):
		parent = enfant_droit

	if parent != indice:
		tableau[parent], tableau[indice] = tableau[indice], tableau[parent]
		tamisage(tableau, comparaison, taille, parent)

def tri_par_tas(tableau, comparaison, taille):
	milieu = taille//2

	for i in range(milieu - 1, -1, -1):
		tamisage(tableau, comparaison, taille, i)

	for i in range(taille-1,0,-1):
		tableau[i], tableau[0] = tableau[0], tableau[i]
		tamisage(tableau, comparaison, i, 0)

	return tableau

# Chaque individu est assimilé à une chaîne binaire de n bits
def generer_individu(n : int):
	if n > 0: return [random.randint(0,1) for i in range(n)]

def generer_population(n : int,N : int):
	return [generer_individu(n) for i in range(N)]

def afficher_individu(individu):
	n = len(individu)
	string = ""
	for k in range(n):
		string += str(individu[k])
	print(string)

def afficher_population(population):
	N = len(population)
	for k in range(N):
		print(f"{k+1} - ", end='')
		afficher_individu(population[k])

def sante_individu(individu):
	somme = sum(individu)
	return abs(sum(cible) - somme)

def croisement(individu1, individu2):
	n, m = len(individu1), len(individu2)
	if n == m:
		nouvel_individu = []
		nouvel_individu.extend([individu1[k] for k in range(n//2)])
		nouvel_individu.extend([individu2[k] for k in range(n//2, n)])
		return nouvel_individu

def mutation_individu(individu : list):
	n_individu = len(individu)
	if random.random() <= prob_mutation:
		i = random.randint(0, n_individu-1)
		individu[i] = 1 - individu[i]
	return individu

def mutation_population(population : list):
	N_population = len(population)
	for k in range(N_population):
		population[k] = mutation_individu(population[k])
	return population

comparer = lambda individu1, individu2 : sante_individu(individu1) < sante_individu(individu2)

if __name__ == "__main__":
	pop = tri_par_tas(generer_population(n,N), comparer, N)
	generation = 0
	while pop[0] != cible:
		print(f"{generation} - ", end='')
		afficher_individu(pop[0])
		generation += 1
		nouvelle_pop = []
		nouvelle_pop.append(pop[0])
		for i in range(0, N//2):
			for j in range(i+1, N//2):
				nouvelle_pop.append(croisement(pop[i], pop[j]))
		nouvelle_pop = mutation_population(nouvelle_pop)
		nouvelle_pop.extend(generer_population(n, N//2))
		pop = tri_par_tas(nouvelle_pop, comparer, N)
	print(f"{generation} - ", end='')
	afficher_individu(pop[0])
	print(f"\nProblème résolu après {generation} générations.")
