# Author: Guled
# Problem: Multiple Knapsack

import random
from typing import Dict
import numpy as np
import copy
import random
from collections import namedtuple
from utils.instancesRepresentation import KnapsackInstance, OptimizationInstance

# Class to represent biological processes
class BiologicalProcessManager:
		'''
			Crossover Function
			- The process of One-Point crossover is exercised in this function.
		'''
		def crossover(crossoverRate, parentOne, parentTwo, problemInstance):
			random_probability = random.random()

			if random_probability < crossoverRate:
				return (parentOne, parentTwo)
			else:
				pivot = random.randint(0, len(parentOne.genotype_representation)-1)

				child_one_genotype = parentOne.genotype_representation[:pivot] + parentTwo.genotype_representation[pivot:]
				child_two_genotype = parentTwo.genotype_representation[:pivot] + parentOne.genotype_representation[pivot:]

				child_one = Chromosome(parentOne.numberOfKnapsacksReference, parentOne.numberOfObjectsReference, child_one_genotype, problemInstance = problemInstance)
				child_two = Chromosome(parentOne.numberOfKnapsacksReference, parentOne.numberOfObjectsReference, child_two_genotype, problemInstance = problemInstance)

				child_one.phenotype_representation = parentOne.phenotype_representation
				child_two.phenotype_representation = parentOne.phenotype_representation


				return (child_one, child_two)

		'''
			Mutation function
			- The process of Random Resetting is exercised in this function.
		'''
		def mutate(mutationRate, child, numberOfKnapsacks):
			for index, position in enumerate(child.genotype_representation):
				random_probability = random.random()
				'''
					(Random Resetting) "Flip" the position with another knapsack if probability < mutationRate
				'''
				if random_probability < mutationRate:
					child.genotype_representation[index] = random.randint(0,numberOfKnapsacks)

# Class to represent chromosome
class Chromosome:

	fitness = None # Chromosomes fitness
	phenotype_representation = None # Phenotype representation

	def __init__(self, numberOfKnapsacks, numberOfItems, genotype_representation = None, problemInstance = None):
		self.numberOfKnapsacksReference = numberOfKnapsacks
		self.numberOfObjectsReference = numberOfItems
		self.problemInstance = problemInstance

		if genotype_representation == None:
			self.genotype_representation = [random.randint(0,(numberOfKnapsacks)) for x in range(0, numberOfItems)]
		else:
			self.genotype_representation = genotype_representation

		self.length_of_encoding = len(self.genotype_representation)

	'''
	 Generates a fitness for all the chromosomes by aggregating their benefits/values
	'''
	def generateFitness(self, knapsackList):
		''' Make a copy of the knapsack list to be used to evaluate if objects in the chromsome
			exceed C using the 'amountUsed' attribute
		'''

		#print("ORIGINAL CHROM: {}".format(self.genotype_representation))
		knapsacks = copy.deepcopy(knapsackList)
		fitnessScore = 0
		done = False
		for i, placement_of_object in enumerate(self.genotype_representation):
			if placement_of_object == 0:
				continue
			else:
				for knapsack in knapsacks:
					if knapsack.id == placement_of_object:
						# if it's over the capacity, change it's bag and revaluate
						if self.phenotype_representation[i].weight > knapsack.capacity:
							while(not done):
								self.genotype_representation[i] = random.randint(0,(self.numberOfKnapsacksReference))

								if self.genotype_representation[i] == 0:
									break
								else:
									current_knapsack = next((sack for sack in knapsacks if sack.id == self.genotype_representation[i]),None)
									if self.phenotype_representation[i].weight > current_knapsack.capacity:
										continue
									if self.phenotype_representation[i].weight <= current_knapsack.capacity:
										fitnessScore += self.phenotype_representation[i].value
										'''We now subtract the objects weight by the knapsacks capacity
										   so that we can keep track of how much space the knapsack has left
										   in the event that another object goes into the same knapsack
										'''
										current_knapsack.capacity = (current_knapsack.capacity - self.phenotype_representation[i].weight)
										break
						else:
							fitnessScore += self.phenotype_representation[i].value
							'''We now subtract the objects weight by the knapsacks capacity
							   so that we can keep track of how much space the knapsack has left
							   in the event that another object goes into the same knapsack
							'''
							knapsack.capacity = (knapsack.capacity - self.phenotype_representation[i].weight)

		solution = np.array(self.genotype_representation, dtype = int)
		fitnessScore = self.problemInstance.objective(solution, isMinimizing = False)		

		# update the chromosomes fitness
		self.fitness = fitnessScore

class Knapsack:
	def __init__(self, id, capacity):
		self.id = id
		self.capacity = capacity

class Population:

	Phenotype = namedtuple('Phenotype', 'id weight value')
	knapsackList = [] # list of knapsacks
	knapSackEvaluationList = [] # used for generating fitness of chromosomes
	population = []

	def __init__(self, size):
		self.populationSize = size
		self.numberOfKnapsacks = 0

	def select_parents(self,tournament):
		'''
			Tournament selection is being used to find two parents
		'''
		first_fittest_indiv = None
		second_fittest_indiv = None

		for individual in tournament:
			# Check if this indivudal is fitter than the current fittist individual
			if first_fittest_indiv == None or individual.fitness > first_fittest_indiv.fitness:
				first_fittest_indiv = individual

		tournament.remove(first_fittest_indiv)

		for individual in tournament:
			# Check if this indivudal is fitter than the current fittist individual
			if second_fittest_indiv == None or individual.fitness > second_fittest_indiv.fitness:
				second_fittest_indiv = individual

		#print("FIRST: {},  SECOND: {}".format(first_fittest_indiv.fitness,second_fittest_indiv.fitness))
		return (first_fittest_indiv,second_fittest_indiv)


	def initialize_population(self, problemInstance: OptimizationInstance):
		numberOfKnapsacks = problemInstance.numberOfKnapsacks
		self.numberOfKnapsacks = numberOfKnapsacks
		numberOfItems = problemInstance.numberOfItems
		itemsProfits = problemInstance.itemsProfits
		itemsWeights = problemInstance.itemsWeights
		knapsacksCapacities = problemInstance.knapsacksCapacities

		for i, knapsackCapacity in enumerate(knapsacksCapacities, start = 1):
			self.knapsackList.append(Knapsack((i), knapsackCapacity))

		phenotype_representation = []
		for i, profitWeight in enumerate(zip(itemsProfits, itemsWeights)):
			value,weight = profitWeight
			phenotype_representation.append(self.Phenotype(i,int(weight),int(value)))

		# Create the initial population
		for j in range(0,self.populationSize):
			# Create a new chromosome
			new_chromosome = Chromosome(numberOfKnapsacks,numberOfItems,problemInstance = problemInstance)
			#  Give each chromosome it's phenotype representation
			new_chromosome.phenotype_representation = phenotype_representation
			# Evaluate each chromosome
			new_chromosome.generateFitness(self.knapsackList)
			# Add the chromsome to the population
			self.population.append(new_chromosome)

def find_the_best(population):
	best = None
	for individual in population:
		if best == None or individual.fitness > best.fitness:
			best = individual
	return best

def solve(
		input: Dict,
		crossoverRate: float = None,
		populationSize: float = None,
		mutationRate: float = None,
		generations: float = None,
		**kwargs
	):
	problemInstance = input['problemInstance']

	# Initialize population with random candidate solutions
	population = Population(populationSize)
	population.initialize_population(problemInstance)

	# Get a reference to the number of knapsacks
	numberOfKnapsacks = population.numberOfKnapsacks

	generation_counter = 0
	while(generation_counter != generations):
		current_population_fitnesses = [chromosome.fitness for chromosome in population.population]
		# print("CURRENT GEN FITNESS: {} \n ".format(current_population_fitnesses))
		new_gen = []
		while(len(new_gen) != population.populationSize):
			# Create tournament for tournament selection process
			tournament = [population.population[random.randint(1, population.populationSize-1)] for individual in range(1, population.populationSize)]
			# Obtain two parents from the process of tournament selection
			parent_one, parent_two = population.select_parents(tournament)
			# Create the offspring from those two parents
			child_one,child_two = BiologicalProcessManager.crossover(crossoverRate,parent_one,parent_two,problemInstance)

			# Try to mutate the children
			BiologicalProcessManager.mutate(mutationRate, child_one, numberOfKnapsacks)
			BiologicalProcessManager.mutate(mutationRate, child_two, numberOfKnapsacks)

			# Evaluate each of the children
			child_one.generateFitness(population.knapsackList)
			child_two.generateFitness(population.knapsackList)

			# Add the children to the new generation of chromsomes
			new_gen.append(child_one)
			new_gen.append(child_two)

		# Replace old generation with the new one
		population.population = new_gen
		generation_counter += 1

	bestSolution = np.array(find_the_best(population.population).genotype_representation, dtype = int)

	problemInstance.updateSolution(bestSolution)

	returnValue = {
		'problemInstance': problemInstance
	} 

	return returnValue