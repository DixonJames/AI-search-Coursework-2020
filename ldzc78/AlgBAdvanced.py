############
############ ALTHOUGH I GIVE YOU THE 'BARE BONES' OF THIS PROGRAM WITH THE NAME
############ 'skeleton.py', YOU CAN RENAME IT TO ANYTHING YOU LIKE. HOWEVER, FOR
############ THE PURPOSES OF THE EXPLANATION IN THESE COMMENTS, I ASSUME THAT
############ THIS PROGRAM IS STILL CALLED 'skeleton.py'.
############
############ IF YOU WISH TO IMPORT STANDARD MODULES, YOU CAN ADD THEM AFTER THOSE BELOW.
############ NOTE THAT YOU ARE NOT ALLOWED TO IMPORT ANY NON-STANDARD MODULES!
############

import os
import sys
import time
import random


############
############ NOW PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS.
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############

def read_file_into_string(input_file, ord_range):
    the_file = open(input_file, 'r')
    current_char = the_file.read(1)
    file_string = ""
    length = len(ord_range)
    while current_char != "":
        i = 0
        while i < length:
            if ord(current_char) >= ord_range[i][0] and ord(current_char) <= ord_range[i][1]:
                file_string = file_string + current_char
                i = length
            else:
                i = i + 1
        current_char = the_file.read(1)
    the_file.close()
    return file_string


def remove_all_spaces(the_string):
    length = len(the_string)
    new_string = ""
    for i in range(length):
        if the_string[i] != " ":
            new_string = new_string + the_string[i]
    return new_string


def integerize(the_string):
    length = len(the_string)
    stripped_string = "0"
    for i in range(0, length):
        if ord(the_string[i]) >= 48 and ord(the_string[i]) <= 57:
            stripped_string = stripped_string + the_string[i]
    resulting_int = int(stripped_string)
    return resulting_int


def convert_to_list_of_int(the_string):
    list_of_integers = []
    location = 0
    finished = False
    while finished == False:
        found_comma = the_string.find(',', location)
        if found_comma == -1:
            finished = True
        else:
            list_of_integers.append(integerize(the_string[location:found_comma]))
            location = found_comma + 1
            if the_string[location:location + 5] == "NOTE=":
                finished = True
    return list_of_integers


def build_distance_matrix(num_cities, distances, city_format):
    dist_matrix = []
    i = 0
    if city_format == "full":
        for j in range(num_cities):
            row = []
            for k in range(0, num_cities):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    elif city_format == "upper_tri":
        for j in range(0, num_cities):
            row = []
            for k in range(j):
                row.append(0)
            for k in range(num_cities - j):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    else:
        for j in range(0, num_cities):
            row = []
            for k in range(j + 1):
                row.append(0)
            for k in range(0, num_cities - (j + 1)):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    if city_format == "upper_tri" or city_format == "strict_upper_tri":
        for i in range(0, num_cities):
            for j in range(0, num_cities):
                if i > j:
                    dist_matrix[i][j] = dist_matrix[j][i]
    return dist_matrix


def read_in_algorithm_codes_and_tariffs(alg_codes_file):
    flag = "good"
    code_dictionary = {}
    tariff_dictionary = {}
    if not os.path.exists(alg_codes_file):
        flag = "not_exist"
        return code_dictionary, tariff_dictionary, flag
    ord_range = [[32, 126]]
    file_string = read_file_into_string(alg_codes_file, ord_range)
    location = 0
    EOF = False
    list_of_items = []
    while EOF == False:
        found_comma = file_string.find(",", location)
        if found_comma == -1:
            EOF = True
            sandwich = file_string[location:]
        else:
            sandwich = file_string[location:found_comma]
            location = found_comma + 1
        list_of_items.append(sandwich)
    third_length = int(len(list_of_items) / 3)
    for i in range(third_length):
        code_dictionary[list_of_items[3 * i]] = list_of_items[3 * i + 1]
        tariff_dictionary[list_of_items[3 * i]] = int(list_of_items[3 * i + 2])
    return code_dictionary, tariff_dictionary, flag


############
############ THE RESERVED VARIABLE 'input_file' IS THE CITY FILE UNDER CONSIDERATION.
############
############ IT CAN BE SUPPLIED BY SETTING THE VARIABLE BELOW OR VIA A COMMAND-LINE
############ EXECUTION OF THE FORM 'python skeleton.py city_file.txt'. WHEN SUPPLYING
############ THE CITY FILE VIA A COMMAND-LINE EXECUTION, ANY ASSIGNMENT OF THE VARIABLE
############ 'input_file' IN THE LINE BELOW iS SUPPRESSED.
############
############ IT IS ASSUMED THAT THIS PROGRAM 'skeleton.py' SITS IN A FOLDER THE NAME OF
############ WHICH IS YOUR USER-NAME, E.G., 'abcd12', WHICH IN TURN SITS IN ANOTHER
############ FOLDER. IN THIS OTHER FOLDER IS THE FOLDER 'city-files' AND NO MATTER HOW
############ THE NAME OF THE CITY FILE IS SUPPLIED TO THIS PROGRAM, IT IS ASSUMED THAT
############ THE CITY FILE IS IN THE FOLDER 'city-files'.
############

input_file = "AISearchfile180.txt"

############
############ PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS.
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############

if len(sys.argv) > 1:
    input_file = sys.argv[1]

the_particular_city_file_folder = "city-files"

if os.path.isfile("../" + the_particular_city_file_folder + "/" + input_file):
    ord_range = [[32, 126]]
    file_string = read_file_into_string("../" + the_particular_city_file_folder + "/" + input_file, ord_range)
    file_string = remove_all_spaces(file_string)
    print("I have found and read the input file " + input_file + ":")
else:
    print(
        "*** error: The city file " + input_file + " does not exist in the folder '" + the_particular_city_file_folder + "'.")
    sys.exit()

location = file_string.find("SIZE=")
if location == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()

comma = file_string.find(",", location)
if comma == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()

num_cities_as_string = file_string[location + 5:comma]
num_cities = integerize(num_cities_as_string)
print("   the number of cities is stored in 'num_cities' and is " + str(num_cities))

comma = comma + 1
stripped_file_string = file_string[comma:]
distances = convert_to_list_of_int(stripped_file_string)

counted_distances = len(distances)
if counted_distances == num_cities * num_cities:
    city_format = "full"
elif counted_distances == (num_cities * (num_cities + 1)) / 2:
    city_format = "upper_tri"
elif counted_distances == (num_cities * (num_cities - 1)) / 2:
    city_format = "strict_upper_tri"
else:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()

dist_matrix = build_distance_matrix(num_cities, distances, city_format)
print("   the distance matrix 'dist_matrix' has been built.")

############
############ YOU NOW HAVE THE NUMBER OF CITIES STORED IN THE INTEGER VARIABLE 'num_cities'
############ AND THE TWO_DIMENSIONAL MATRIX 'dist_matrix' HOLDS THE INTEGER CITY-TO-CITY
############ DISTANCES SO THAT 'dist_matrix[i][j]' IS THE DISTANCE FROM CITY 'i' TO CITY 'j'.
############ BOTH 'num_cities' AND 'dist_matrix' ARE RESERVED VARIABLES AND SHOULD FEED
############ INTO YOUR IMPLEMENTATIONS.
############

############
############ THERE NOW FOLLOWS CODE THAT READS THE ALGORITHM CODES AND TARIFFS FROM
############ THE TEXT-FILE 'alg_codes_and_tariffs.txt' INTO THE RESERVED DICTIONARIES
############ 'code_dictionary' AND 'tariff_dictionary'. DO NOT AMEND THIS CODE!
############ THE TEXT FILE 'alg_codes_and_tariffs.txt' SHOULD BE IN THE SAME FOLDER AS
############ THE FOLDER 'city-files' AND THE FOLDER WHOSE NAME IS YOUR USER-NAME, E.G., 'abcd12'.
############

code_dictionary, tariff_dictionary, flag = read_in_algorithm_codes_and_tariffs("../alg_codes_and_tariffs.txt")

if flag != "good":
    print("*** error: The text file 'alg_codes_and_tariffs.txt' does not exist.")
    sys.exit()

print("The codes and tariffs have been read from 'alg_codes_and_tariffs.txt':")

############
############ YOU NOW NEED TO SUPPLY SOME PARAMETERS.
############
############ THE RESERVED STRING VARIABLE 'my_user_name' SHOULD BE SET AT YOUR USER-NAME, E.G., "abcd12"
############

my_user_name = "ldzc78"

############
############ YOU CAN SUPPLY, IF YOU WANT, YOUR FULL NAME. THIS IS NOT USED AT ALL BUT SERVES AS
############ AN EXTRA CHECK THAT THIS FILE BELONGS TO YOU. IF YOU DO NOT WANT TO SUPPLY YOUR
############ NAME THEN EITHER SET THE STRING VARIABLES 'my_first_name' AND 'my_last_name' AT
############ SOMETHING LIKE "Mickey" AND "Mouse" OR AS THE EMPTY STRING (AS THEY ARE NOW;
############ BUT PLEASE ENSURE THAT THE RESERVED VARIABLES 'my_first_name' AND 'my_last_name'
############ ARE SET AT SOMETHING).
############

my_first_name = "James"
my_last_name = "Dixon"

############
############ YOU NEED TO SUPPLY THE ALGORITHM CODE IN THE RESERVED STRING VARIABLE 'algorithm_code'
############ FOR THE ALGORITHM YOU ARE IMPLEMENTING. IT NEEDS TO BE A LEGAL CODE FROM THE TEXT-FILE
############ 'alg_codes_and_tariffs.txt' (READ THIS FILE TO SEE THE CODES).
############

algorithm_code = "GA"

############
############ DO NOT TOUCH OR ALTER THE CODE BELOW! YOU HAVE BEEN WARNED!
############

if not algorithm_code in code_dictionary:
    print("*** error: the agorithm code " + algorithm_code + " is illegal")
    sys.exit()
print("   your algorithm code is legal and is " + algorithm_code + " -" + code_dictionary[algorithm_code] + ".")

############
############ YOU CAN ADD A NOTE THAT WILL BE ADDED AT THE END OF THE RESULTING TOUR FILE IF YOU LIKE,
############ E.G., "in my basic greedy search, I broke ties by always visiting the first
############ city found" BY USING THE RESERVED STRING VARIABLE 'added_note' OR LEAVE IT EMPTY
############ IF YOU WISH. THIS HAS NO EFFECT ON MARKS BUT HELPS YOU TO REMEMBER THINGS ABOUT
############ YOUR TOUR THAT YOU MIGHT BE INTERESTED IN LATER.
############

added_note = ""

############
############ NOW YOUR CODE SHOULD BEGIN.
############

normal_mutation_const = 2
crossover_mutation_const = 5
population_size = 50

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


    if True:
        mid_section = (tour[A_city_i + 2: B_city_i ])[::-1]
        front_section = tour[:A_city_i + 1]
        tail_section = tour[B_city_i + 1:]


        new = front_section + [B_city] + mid_section + [A_n_city] + tail_section


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
    start_time = time.time()
    tau = max_tour(map_of_distances)
    top_fitness = max_tour(map_of_distances)
    top_tour = []




    population = genStartPopulation(popsize, map_of_distances[0])

    greedy_population = genGreedyPopulation(popsize, map_of_distances)

    #population += greedy_population

    if popsize < len(greedy_population):
        population = population[:(popsize//2)] + greedy_population[:(popsize//2)]



    # your code
    elapsed_time = time.time() - start_time

    tour_time_taken = time.time() - time.time()

    while(time.time() - start_time +  tour_time_taken < time_frame):
        start_gen_time = time.time()
        #looping over each generation


        population_fitness = [tourFitness(t, map_of_distances) for t in population]
        total_fitness = sum(population_fitness)
        population_percentage = [(tau - fitness)/total_fitness for fitness in population_fitness]

        new_pop = []

        for j in range(popsize):
            #making as many children as there are parents
            parents_set_a = random.choices(population, weights=population_percentage, k=2)

            parents_set_b = parent_tournament(population, population_fitness, 5)
            parents = (parents_set_a[0], parents_set_b[0])
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


        top_fitness, top_tour = testPopulation(population, top_fitness, top_tour, map_of_distances)
        population.append(top_tour)


        tour_time_taken = time.time() - start_gen_time

    #print(tour_time_taken, time.time() - start_time +  tour_time_taken)
    return top_tour, tourFitness(top_tour, map_of_distances)

def main(map):
    return runTraining(58, map, normal_mutation_const, crossover_mutation_const, population_size)

tour, tour_length = main(dist_matrix)

############
############ YOUR CODE SHOULD NOW BE COMPLETE AND WHEN EXECUTION OF THIS PROGRAM 'skeleton.py'
############ REACHES THIS POINT, YOU SHOULD HAVE COMPUTED A TOUR IN THE RESERVED LIST VARIABLE 'tour',
############ WHICH HOLDS A LIST OF THE INTEGERS FROM {0, 1, ..., 'num_cities' - 1}, AND YOU SHOULD ALSO
############ HOLD THE LENGTH OF THIS TOUR IN THE RESERVED INTEGER VARIABLE 'tour_length'.
############

############
############ YOUR TOUR WILL BE PACKAGED IN A TOUR FILE OF THE APPROPRIATE FORMAT AND THIS TOUR FILE,
############ WHOSE NAME WILL BE A MIX OF THE NAME OF THE CITY FILE, THE NAME OF THIS PROGRAM AND THE
############ CURRENT DATA AND TIME. SO, EVERY SUCCESSFUL EXECUTION GIVES A TOUR FILE WITH A UNIQUE
############ NAME AND YOU CAN RENAME THE ONES YOU WANT TO KEEP LATER.
############

############
############ DO NOT TOUCH OR ALTER THE CODE BELOW THIS POINT! YOU HAVE BEEN WARNED!
############

flag = "good"
length = len(tour)
for i in range(0, length):
    if isinstance(tour[i], int) == False:
        flag = "bad"
    else:
        tour[i] = int(tour[i])
if flag == "bad":
    print("*** error: Your tour contains non-integer values.")
    sys.exit()
if isinstance(tour_length, int) == False:
    print("*** error: The tour-length is a non-integer value.")
    sys.exit()
tour_length = int(tour_length)
if len(tour) != num_cities:
    print("*** error: The tour does not consist of " + str(num_cities) + " cities as there are, in fact, " + str(
        len(tour)) + ".")
    sys.exit()
flag = "good"
for i in range(0, num_cities):
    if not i in tour:
        flag = "bad"
if flag == "bad":
    print("*** error: Your tour has illegal or repeated city names.")
    sys.exit()
check_tour_length = 0
for i in range(0, num_cities - 1):
    check_tour_length = check_tour_length + dist_matrix[tour[i]][tour[i + 1]]
check_tour_length = check_tour_length + dist_matrix[tour[num_cities - 1]][tour[0]]
if tour_length != check_tour_length:
    flag = print("*** error: The length of your tour is not " + str(tour_length) + "; it is actually " + str(
        check_tour_length) + ".")
    sys.exit()
print("You, user " + my_user_name + ", have successfully built a tour of length " + str(tour_length) + "!")

local_time = time.asctime(time.localtime(time.time()))
output_file_time = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
output_file_time = output_file_time.replace(" ", "0")
script_name = os.path.basename(sys.argv[0])
if len(sys.argv) > 2:
    output_file_time = sys.argv[2]
output_file_name = script_name[0:len(script_name) - 3] + "_" + input_file[
                                                               0:len(input_file) - 4] + "_" + output_file_time + ".txt"

f = open(output_file_name, 'w')
f.write("USER = " + my_user_name + " (" + my_first_name + " " + my_last_name + "),\n")
f.write("ALGORITHM CODE = " + algorithm_code + ", NAME OF CITY-FILE = " + input_file + ",\n")
f.write("SIZE = " + str(num_cities) + ", TOUR LENGTH = " + str(tour_length) + ",\n")
f.write(str(tour[0]))
for i in range(1, num_cities):
    f.write("," + str(tour[i]))
f.write(",\nNOTE = " + added_note)
f.close()
print("I have successfully written your tour to the tour file:\n   " + output_file_name + ".")
















