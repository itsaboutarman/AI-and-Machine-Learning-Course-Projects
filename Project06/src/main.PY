import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import silhouette_score

# Reading and processing data from dataset
data = pd.read_excel('Dry_Bean_Dataset.xlsx')

data = data.dropna()
labelEncoder = LabelEncoder()
data['Class'] = labelEncoder.fit_transform(data['Class'])

X = data.drop('Class', axis=1)
y = data['Class']

scaler = StandardScaler()
X = scaler.fit_transform(X)


#Implementation of genetic algorithm
def initializePopulation(size, numFeatures):
    return np.random.rand(size, numFeatures)

def calculateFitness(population, X, y):
    fitness = []
    for individual in population:
        distances = np.linalg.norm(X[:, np.newaxis] - individual, axis=2)
        labels = np.argmin(distances, axis=1)
        if len(np.unique(labels)) > 1:
            fitness.append(silhouette_score(X, labels))
        else:
            fitness.append(0)
    return np.array(fitness)

def selection(population, fitness):
    indices = np.argsort(fitness)[-len(population)//2:]
    return population[indices]

def crossover(parent1, parent2):
    crossoverPoint = np.random.randint(0, len(parent1))
    child1 = np.concatenate([parent1[:crossoverPoint], parent2[crossoverPoint:]])
    child2 = np.concatenate([parent2[:crossoverPoint], parent1[crossoverPoint:]])
    return child1, child2

def mutation(child, mutationRate):
    for i in range(len(child)):
        if np.random.rand() < mutationRate:
            child[i] = np.random.rand()
    return child

populationSize = 50
numGenerations = 100
mutationRate = 0.1
numFeatures = X.shape[1]

population = initializePopulation(populationSize, numFeatures)

for generation in range(numGenerations):
    fitness = calculateFitness(population, X, y)
    selected_population = selection(population, fitness)
    nextPopulation = []

    while len(nextPopulation) < populationSize:
        parents = np.random.choice(range(len(selected_population)), size=2, replace=False)
        parent1, parent2 = selected_population[parents[0]], selected_population[parents[1]]
        child1, child2 = crossover(parent1, parent2)
        child1 = mutation(child1, mutationRate)
        child2 = mutation(child2, mutationRate)
        nextPopulation.extend([child1, child2])

    population = np.array(nextPopulation)

bestIndividual = population[np.argmax(calculateFitness(population, X, y))]
print(bestIndividual)
