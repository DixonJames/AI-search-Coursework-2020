import random
import time

map = [[0, 31, 32, 5, 30, 9, 15, 40, 14, 21, 7, 13], [31, 0, 5, 30, 40, 15, 8, 2, 4, 17, 50, 27], [32, 5, 0, 32, 25, 16, 3, 3, 10, 8, 40, 21], [5, 30, 32, 0, 50, 6, 30, 53, 10, 35, 12, 20], [30, 40, 25, 50, 0, 32, 10, 20, 34, 7, 20, 6], [9, 15, 16, 6, 32, 0, 15, 15, 4, 14, 21, 25], [15, 8, 3, 30, 10, 15, 0, 6, 9, 4, 9, 9], [40, 2, 3, 53, 20, 15, 6, 0, 7, 8, 30, 29], [14, 4, 10, 10, 34, 4, 9, 7, 0, 13, 31, 35], [21, 17, 8, 35, 7, 14, 4, 8, 13, 0, 12, 11], [7, 50, 40, 12, 20, 21, 9, 30, 31, 12, 0, 5], [13, 27, 21, 20, 6, 25, 9, 29, 35, 11, 5, 0]]

best_tour = []

def max_tour(distances):
    total = 0
    for crossing in distances:
        total += max(crossing)
    return total

def two_opt_mutation(tour, distances):
    A_city_i = random.randint(0, len(tour) -1)
    B_city_i = random.randint(0, len(tour) - 2)
    while B_city_i +1 == A_city_i or A_city_i + 1  == B_city_i or A_city_i == B_city_i or B_city_i < A_city_i or (B_city_i == len(tour) - 1 and A_city_i == 0):
        B_city_i = random.randint(0, len(tour) - 2)
        A_city_i = random.randint(0, len(tour) - 1)

    B_city = tour[B_city_i]
    B_n_city = tour[B_city_i + 1]
    A_city = tour[A_city_i]
    A_n_city = tour[A_city_i + 1]

    original_p_weight = distances[B_n_city][B_city] + distances[A_n_city][A_city]
    new_p_weight = distances[A_city][B_city] + distances[A_city_i][B_city_i]

    if original_p_weight > new_p_weight:
        mid_section = (tour[A_city_i + 2: B_city_i ])[::-1]
        front_section = tour[:A_city_i + 1]
        tail_section = tour[B_city_i + 1:]


        new = front_section + [B_city] + mid_section + [A_n_city] + tail_section
        if len(set(new)) != len(tour):
            print("s")

        tour = front_section + [B_city] + mid_section + [A_n_city] + tail_section

    return tour


def nearestNeighborAlg(map_distances, current):
    visited = [current]
    while len(visited) != len(map_distances[0]):
        valid_neighbors = []
        top_neighbor_score = 0
        top_neighbor_index = 0

        for i in range(len(map_distances[current])):
            if i not in visited:
                valid_neighbors.append(i)

        for neighbor_index in valid_neighbors:
            if map_distances[current][neighbor_index] > top_neighbor_score:
                top_neighbor_index = neighbor_index
                top_neighbor_score = map_distances[current][neighbor_index]

        visited.append(top_neighbor_index)
        current = top_neighbor_index

    return visited

def genGreedyPopulation(population_num, distances):
    population = []
    for p in range(population_num):
        rand_tour = nearestNeighborAlg(distances, p)
        population.append(rand_tour)
    return population

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

def tourFitness(tour, distances):
    check_tour_length = 0
    for i in range(0, len(tour) - 1):
        check_tour_length = check_tour_length + distances[tour[i]][tour[i + 1]]
    check_tour_length = check_tour_length + distances[tour[len(tour) - 1]][tour[0]]
    return check_tour_length

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

def cycleCrossoverOperator(A_tour, B_tour):
    offspring_alpha = [-1 for _ in range(len(A_tour))]
    offspring_beta = [-1 for _ in range(len(A_tour))]
    both_offpring = [offspring_alpha, offspring_beta]



    primary_parent = A_tour
    secondary_parent = B_tour

    taken_indexs = []
    i = 0
    current_index = i

    while current_index not in taken_indexs:
        offspring_alpha[current_index] = primary_parent[current_index]
        offspring_beta[current_index] = secondary_parent[current_index]
        taken_indexs.append(current_index)
        current_index = secondary_parent[current_index] - 1

    for i in range(len(offspring_alpha)):
        if offspring_alpha[i] == -1:
            offspring_alpha[i] = secondary_parent[i]
            offspring_beta[i] = primary_parent[i]

    if len(set(offspring_alpha)) != len(set(A_tour)):
        return A_tour, B_tour
    return offspring_alpha, offspring_beta

def shift_change_mutation(tour):

    B_i = random.randint(0, len(tour) - 1)
    A_i = random.randint(0, B_i)
    while B_i <= A_i:
        B_i = random.randint(0, len(tour) - 1)
        A_i = random.randint(0, B_i)

    prefix = tour[:A_i]
    postfix = tour[B_i + 1:]
    middle = tour[A_i + 1: B_i]

    new = prefix + [tour[B_i]] + middle + [tour[A_i]] + postfix

    if len(set(new)) != len(set(tour)):
        print("shit")

    return new


def basicSwapMutation(tour):
    A_city = random.randint(0, len(tour) - 1)
    B_city = random.randint(0, len(tour) - 1)

    while B_city == A_city:
        B_city = random.randint(0, len(tour) - 1)

    tour[A_city], tour[B_city] = tour[B_city], tour[A_city]
    return tour

def applyMutations(new_pop, mutation_chance, opt_chance, distances):
    final_new_pop = []
    for child in new_pop:
        if random.randint(1, mutation_chance) == 1:
            new_child = shift_change_mutation(child)
        else:
            new_child = child

        if random.randint(1, opt_chance) == 1:
            new_child = two_opt_mutation(child, distances)

        final_new_pop.append(new_child)

    return final_new_pop

def testPopulation(population, top_fitness, top_tour, map_of_distances):
    for tour in population:
        if top_fitness >= tourFitness(tour, map_of_distances):
            top_fitness = tourFitness(tour, map_of_distances)
            top_tour = tour
    return top_fitness, top_tour

def parent_tournament(prospective_parents, parents_fitness, round_size):
    parent_indexes = [i for i in range(len(prospective_parents))]
    group_A = random.choices(parent_indexes, k=round_size)
    group_B = random.choices(parent_indexes, k=round_size)

    while set(group_A) in set(group_B):
        group_B = random.choices(parent_indexes, k=round_size)

    group_A_max = (0,0)
    group_B_max = (0,0)

    for i in range(len(group_A)):
        if parents_fitness[group_A[i]] >= group_A_max[0]:
            group_A_max = (parents_fitness[group_A[i]], group_A[i] )

        if parents_fitness[group_B[i]] >= group_B_max[0]:
            group_B_max = (parents_fitness[group_B[i]], group_B[i] )

    return prospective_parents[group_A_max[1]], prospective_parents[group_B_max[1]]

def runTraining(time_frame,map_of_distances,  mutation_chance, opt_chance, popsize):
    tau = max_tour(map_of_distances)
    top_fitness = max_tour(map_of_distances)
    top_tour = []
    population = genStartPopulation(popsize, map_of_distances[0])

    greedy_population = genGreedyPopulation(len(map_of_distances[0]), map_of_distances)

    population += greedy_population



    start_time = time.time()
    # your code
    elapsed_time = time.time() - start_time

    while(time.time() - start_time < time_frame):
        #looping over each generation
        #print(f"{time.time() - start_time}/{time_frame}")

        population_fitness = [tourFitness(t, map_of_distances) for t in population]
        total_fitness = sum(population_fitness)
        population_percentage = [(tau - fitness)/total_fitness for fitness in population_fitness]

        new_pop = []

        for j in range(popsize):
            #making as many children as there are parents
            parents = random.choices(population, weights=population_percentage, k=2)

            #parents_set_b = parent_tournament(population, population_fitness, 5)
            #parents = (parents_set_a[0], parents_set_b[0])
            childA, childB = cycleCrossoverOperator(parents[0], parents[1])

            childA_tour_length = tourFitness(childA, map_of_distances)
            childB_tour_length = tourFitness(childB, map_of_distances)

            p_a = tourFitness(parents[0], map_of_distances)
            p_b = tourFitness(parents[1], map_of_distances)

            if childA_tour_length <= childB_tour_length:
                new_pop.append(childA)
            else:
                new_pop.append(childB)

            #if p_b <= p_a:
                #new_pop.append(parents[0])
            #else:
                #new_pop.append(parents[1])

        population = applyMutations(new_pop, mutation_chance, opt_chance, map_of_distances)
        #print(population)

        top_fitness, top_tour = testPopulation(population, top_fitness, top_tour, map_of_distances)
        population.append(top_tour)
        print(top_fitness)

    return top_tour, tourFitness(top_tour, map_of_distances)

def main(map):
    print(runTraining(3600, map, 1, 1, 2*len(map[0])))



if __name__ == '__main__':
    print(runTraining(3600, map, 1, 1, 2*len(map[0])))