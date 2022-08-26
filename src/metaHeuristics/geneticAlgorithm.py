# -*- coding: utf-8 -*-

"""
@author: Leonardo Rosas Leal, Daniel dos Santos and Cainã Figueiredo Pereira
@email: leoleal@cos.ufrj.br, ddsantos@cos.ufrj.br, cainafpereira@cos.ufrj.br
@date: 2022-08-25
"""

import numpy as np

from utils.instancesRepresentation import OptimizationInstance
from src.metaHeuristics.geneticAlgorithmLib.parser import ItemParser, KnapsackParser
from src.metaHeuristics.geneticAlgorithmLib.chromosome import Chromosome
from src.metaHeuristics.geneticAlgorithmLib.factory import ChromosomeFactory, PopulationFactory
from src.metaHeuristics.geneticAlgorithmLib.crossover import OnePoint
from src.metaHeuristics.geneticAlgorithmLib.item import ItemList
from src.metaHeuristics.geneticAlgorithmLib.knapsack import KnapsackList
from src.metaHeuristics.geneticAlgorithmLib.fitness import FitnessFunction
from src.metaHeuristics.geneticAlgorithmLib.selection import RouletteSelection
from src.metaHeuristics.geneticAlgorithmLib.population import Population
from src.metaHeuristics.geneticAlgorithmLib.mutation import Mutation
from random import choice

def __assertValidParams__(
	populationSize, 
	iterations,
	numberOfItems
):
	assert populationSize > 0
	assert iterations >= numberOfItems

def solve(
		input: OptimizationInstance,
		populationSize: int = -1,
		iterations: int = -1,
	):
	problemInstance = input['problemInstance']
	numberOfItems = problemInstance.numberOfItems
	numberOfKnapsacks = problemInstance.numberOfKnapsacks
	itemsProfits = problemInstance.itemsProfits
	itemsWeights = problemInstance.itemsWeights  
	knapsacksCapacities = problemInstance.knapsacksCapacities

	__assertValidParams__(
		populationSize, 
		iterations,
		numberOfItems
	)

	items = ItemList(ItemParser(itemsProfits, itemsWeights).items)

	knapsacks = KnapsackList(KnapsackParser(knapsacksCapacities))

	# print('population size = ' + str(populationSize))
	population = PopulationFactory(populationSize, numberOfItems, numberOfKnapsacks).gen()
	iterations = 30
	# print('iterations = {0}'.format(iterations))

	fittest_chromosome = None
	fittest_chromosomes = []
	for _ in range(iterations):
		pop_fsum = 0
		#calc population sum
		for i in range(populationSize):
			fitness_function = FitnessFunction(
				population[i], 
				items.get_all_on_items(population[i].solution, numberOfKnapsacks),
				problemInstance
			)
			pop_fsum = pop_fsum + fitness_function.sum_all_fitness()
			population[i] = fitness_function.chromosome

		parents = []
		for i in range(2):#select 2 chromosomes for crossover
			parent = RouletteSelection(population, problemInstance).do_selection()
			parents.append(parent)

		point = choice(range(0, len(parents[0]), 2))

		children = OnePoint().exe(parents[0], parents[1], point)

		probability = 100
		mutated_children = []
		for i in range(2):
			mutated_children.append(Mutation(children[i], probability, problemInstance).exe())      #mutate offspring

		i = 0
		for chromosome in population: #replace current population with new one
			if str(chromosome) == str(parents[0]):
				population[i] = mutated_children[0]
				i = i + 1
			elif str(chromosome) == str(parents[1]):
				population[i] = mutated_children[1]
				i = i + 1
			else:
				i = i + 1

		#get list of fitness for each individual
		fsums = []
		for i in range(populationSize):
			fitness_function = FitnessFunction(population[i], items.get_all_on_items(population[i].solution, numberOfKnapsacks), problemInstance)
			fsums.append(fitness_function.sum_all_fitness())
			population[i] = fitness_function.chromosome

		#get fittest individual of current population
		# print('fsums = ' + str(fsums))
		max_fsum = max(fsums)
		# print('this max fsum ' + str(max_fsum))
		for i in range(populationSize):
			if float(fsums[i]) == float(max_fsum):
				fittest_chromosome = population[i]

		fittest_chromosomes.append(fittest_chromosome)
		# print('fittest solution from this population ' + str(fittest_chromosome) + ' where fsum = ' + str(max_fsum))
		# print('population fsum = ' + str(pop_fsum))
		# print(population)

	fittest_fsums = []
	for i in range(numberOfItems):
		fitness_function = FitnessFunction(fittest_chromosomes[i], items.get_all_on_items(fittest_chromosomes[i].solution, numberOfKnapsacks), problemInstance)
		fittest_fsums.append(fitness_function.sum_all_fitness())
		if i < populationSize:
			population[i] = fitness_function.chromosome

	# print('fittest fsums = ' + str(fittest_fsums))

	fittest_max_fsum = max(fittest_fsums)
	for i in range(numberOfItems):
		if float(fittest_fsums[i]) == float(fittest_max_fsum):
			final_chromosome = fittest_chromosomes[i]

	# print('fittest solutions from all populations \n \n' + str(Population(fittest_chromosomes)))
	#f_max_fsum = fitness_function.sum_all_fitness()
	#final_chromosome = fitness_function.chromosome
	# print('final fittest solution = ' + str(final_chromosome) + ', where fsum = ' + str(fittest_max_fsum))
	result_knapsack = items.get_all_on_items(final_chromosome, numberOfKnapsacks)
	solution = np.zeros(numberOfItems, dtype = int)
	
	for knapsack in result_knapsack:
		for item in result_knapsack[knapsack]:
			solution[item.index] = knapsack

	problemInstance.updateSolution(solution)

	returnValue = {
		'problemInstance': problemInstance
	}

	return returnValue