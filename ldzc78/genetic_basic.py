import random


map = [[0, 31, 32, 5, 30, 9, 15, 40, 14, 21, 7, 13], [31, 0, 5, 30, 40, 15, 8, 2, 4, 17, 50, 27], [32, 5, 0, 32, 25, 16, 3, 3, 10, 8, 40, 21], [5, 30, 32, 0, 50, 6, 30, 53, 10, 35, 12, 20], [30, 40, 25, 50, 0, 32, 10, 20, 34, 7, 20, 6], [9, 15, 16, 6, 32, 0, 15, 15, 4, 14, 21, 25], [15, 8, 3, 30, 10, 15, 0, 6, 9, 4, 9, 9], [40, 2, 3, 53, 20, 15, 6, 0, 7, 8, 30, 29], [14, 4, 10, 10, 34, 4, 9, 7, 0, 13, 31, 35], [21, 17, 8, 35, 7, 14, 4, 8, 13, 0, 12, 11], [7, 50, 40, 12, 20, 21, 9, 30, 31, 12, 0, 5], [13, 27, 21, 20, 6, 25, 9, 29, 35, 11, 5, 0]]
best_tour = []

def max_tour(map):
    total = 0
    for crossing in map:
        total += max(crossing)
    return total

tau = max_tour(map)

def genRandomTour(city_num):
    tour = [num for num in range(int(city_num))]
    random.shuffle(tour)
    return tour

def genStartPopulation(population_num, example_pop):
    population = []
    for p in range(population_num):
        rand_tour = genRandomTour(len(example_pop))
        population.append(rand_tour)
    return population

def tourFitness(tour):
    distance = 0
    for cty_order in range(len(tour)):
        if tour[cty_order] == tour[-1]:
            distance += map[tour[-1]][tour[0]]
        else:
            distance += map[tour[cty_order]][tour[cty_order +1]]
    return tau - distance

def findDuplicate(list):
    dupes = []
    for char in list:
        if list.count(char) != 1:
            dupes.append(char)
    return dupes

def findMissing(original, trial):
    missing = []
    for char in original:
        if char not in trial:
            missing.append(char)
    return list(set(missing))


def basicCrossoverTours(A_tour, B_tour):
    if len(A_tour) != len(B_tour):
        print("tours not of same length")
        return False

    division_index = random.randint(0, len(A_tour)-1)

    A_prefix = A_tour[0:division_index]
    A_suffix = A_tour[division_index  :]
    B_prefix = B_tour[0:division_index]
    B_suffix = B_tour[division_index :]

    A_trial = A_prefix + B_suffix
    B_trial = B_prefix + A_suffix

    if set(A_trial) == set(A_tour) and set(B_trial) == set(B_tour):
        #what a lovely occurrence!
        return A_trial, B_trial
    else:
        A_dupes = list(set(findDuplicate(A_trial)))
        B_dupes = list(set(findDuplicate(B_trial)))

        A_missing = findMissing(A_tour, A_trial)
        B_missing = findMissing(B_tour, B_trial)

        for i in range(len(A_suffix)):
            if A_suffix[i] in B_dupes and len(B_missing)!=0:
                A_suffix[i] = B_missing.pop()
        B_trial = B_prefix + A_suffix

        for i in range(len(B_suffix)):
            if B_suffix[i] in A_dupes and len(A_missing)!=0:
                B_suffix[i] = A_missing.pop()
        A_trial = A_prefix + B_suffix

        if set(A_trial) == set(A_tour) and set(B_trial) == set(B_tour):
            return A_trial, B_trial
        return False


def basicSwapMutation(tour):
    A_city = random.randint(0, len(tour) - 1)
    B_city = random.randint(0, len(tour) - 1)

    while B_city == A_city:
        B_city = random.randint(0, len(tour) - 1)

    tour[A_city], tour[B_city] = tour[B_city], tour[A_city]
    return tour

def applyMutations(new_pop, mutation_chance):
    final_new_pop = []
    for child in new_pop:
        if random.randint(1, mutation_chance) == 1:
            new_child = basicSwapMutation(child)

        else:
            new_child = child
        final_new_pop.append(new_child)

    return final_new_pop

def testPopulation(population, top_fitness, top_tour):
    for tour in population:
        if top_fitness >= tourFitness(tour):
            top_fitness = tourFitness(tour)
            top_tour = tour
    return top_fitness, top_tour

def runTraining(iterations, mutation_chance):
    top_fitness = tau
    top_tour = []
    population = genStartPopulation(10, map[0])

    for i in range(iterations):
        #looping over each generation
        print(f"{(i/iterations)*100}")

        population_fitness = [tourFitness(t) for t in population]
        total_fitness = sum(population_fitness)
        population_percentage = [fitness/total_fitness for fitness in population_fitness]

        new_pop = []

        for j in range(len(population[0])):
            #making as many children as there are parents
            parents = random.choices(population, weights=population_percentage, k=2)
            childA, childB = basicCrossoverTours(parents[0], parents[1])

            childA_fitness = tourFitness(childA)
            childB_fitness = tourFitness(childB)

            if childA_fitness >= childB_fitness:
                new_pop.append(childA)
            else:
                new_pop.append(childB)

        population = applyMutations(new_pop, mutation_chance)
        #print(population)

        top_fitness, top_tour = testPopulation(population, top_fitness, top_tour)

    return top_tour, top_fitness



if __name__ == '__main__':
    print(runTraining(100000, 10))