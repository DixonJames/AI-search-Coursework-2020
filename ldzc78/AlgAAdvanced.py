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

algorithm_code = "LK"

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



def tourFitness(candidate_tour, weights):
    distance = 0
    for cty_order in range(len(candidate_tour)):
        if candidate_tour[cty_order] == candidate_tour[-1]:
            distance += weights[candidate_tour[-1]][candidate_tour[0]]
        else:
            distance += weights[candidate_tour[cty_order]][candidate_tour[cty_order + 1]]
    return distance


def randomShuffle(candidate_tour):
    shuffled = []
    for i in range(len(candidate_tour)):
        index = random.randint(0, len(candidate_tour) - 1)
        while candidate_tour[index] in shuffled:
            index = random.randint(0, len(candidate_tour) - 1)
        shuffled.append(candidate_tour[index])
    return shuffled

def partner(index, relationchip):
    if index == relationchip[0]:
        return relationchip[1]
    return relationchip[0]

def validateTour(proposed_edges, weights):
    """
    every city shuold appear in exactly two edges. thould be as amny edges as cities
    :param proposed_edges:
    :param weights:
    :return: T/F dependiing on validity of the tour
    """
    if len(proposed_edges) != len(weights[0]):
        return False
    city_count = [0 for i in range(len(weights))]

    for edge in proposed_edges:
        city_count[edge[0]] += 1
        city_count[edge[1]] += 1

    for city in city_count:
        if city != 2:
            return False

    if createCycle(proposed_edges) == False:
        return False



    return True

def createCycle(edge_set):
    parts = []
    edge_list = list(edge_set)

    for edge in edge_list:
        parts.append([edge[0], edge[1]])

    tour = []


    tour = [parts[0][0], parts[0][1]]
    parts.remove(parts[0])

    while len(tour) != len(edge_list):
        for part in parts:

            if tour[0] == part[0]:
                tour = (list(reversed(tour)) + part[1:])
                parts.remove(part)
            elif tour[-1] == part[0]:
                tour = (tour + part[1:])
                parts.remove(part)
            elif tour[0] == part[-1]:
                tour = (part + tour[1:])
                parts.remove(part)
            elif tour[-1] == part[-1]:
                tour = (part + list(reversed(tour))[1:])
                parts.remove(part)
        if tour[0] == tour[-1] and len(tour) != 1:
            return False

    return tour











class Tour:
    def __init__(self, weights, tour):
        self.weights = weights
        self.tour = tour
        self.score = tourFitness(self.tour, self.weights)

    def edgesSet(self):
        """
        :return: a list of edge tuples
        """
        all_edges = set()
        for city_i in range(len(self.tour)):
            if self.tour.index(self.tour[city_i]) != len(self.tour) - 1:
                all_edges.add((self.tour[city_i], self.tour[city_i + 1]))
            else:
                all_edges.add((self.tour[city_i], self.tour[0]))

        return all_edges

    def currentConnections(self, city):
        """
        :param city: the city's current tour connections we are looking for
        :return: list of citys that are connected to the city in the tour (should be 2)
        """
        connected_citys = []
        for edge in self.edgesSet():
            if edge[0] == city:
                connected_citys.append(edge[1])
            elif edge[1] == city:
                connected_citys.append(edge[0])

        return connected_citys

    def validPotentialNeighbors(self, city, nearest = None):
        """
        returns a whitlelist containg the city and the city currently connected to in the tour
        :param city:
        :return:
        """
        black_list = set()
        black_list.add(city)
        all_edges = self.edgesSet()

        for edge in all_edges:
            if edge[0] == city:
                black_list.add(edge[1])

        valid =  list(set(i for i in range(len(self.weights[0])) if i != city).difference(black_list).difference(black_list))
        if nearest != None:
            best_neighbors = sorted(valid, key= (lambda c : self.weights[city][c]))[:nearest]
            return best_neighbors
        return valid




class Improvement:
    def __init__(self, tour):
        self.total_gain = 0
        self.input_tour = tour

        self.add_edges = set()
        self.remove_edges = set()

        self.found_better = True

        self.k_opt = 2

        self.added = set()
        self.removed = set()

    def setWeightLost(self, custom_add=None, custom_rem=None):
        """
        looks at both of the add and remove sets. calculates the weight lost (or gained)
        :return:
        """
        add_tot = 0
        remove_tot = 0

        add_set = set()
        rem_set = set()

        if (custom_add is not None) and (custom_rem is not None):
            add_set = custom_add
            rem_set = custom_rem
        else:
            add_set = self.add_edges
            rem_set = self.remove_edges

        for edge in add_set:
            add_tot += self.input_tour.weights[edge[0]][edge[1]]
        for edge in rem_set:
            remove_tot += self.input_tour.weights[edge[0]][edge[1]]
        weight_loss = remove_tot - add_tot
        return weight_loss


    def swapEdgeSets(self, custom_add=None, custom_rem=None):
        current_edges = self.input_tour.edgesSet()
        if not((custom_add is not None) and (custom_rem is not None)):
            custom_add = self.add_edges
            custom_rem = self.remove_edges

        for edge in custom_rem:
            reversed_edge = (edge[1], edge[0])
            if edge in current_edges:
                current_edges.remove(edge)
            if reversed_edge in current_edges:
                current_edges.remove(reversed_edge)

        for edge in custom_add:
            current_edges.add(edge)


        return current_edges

    def removeEdge(self, original_city, T2, tail_removal_city):
        # test if new tour is valid
        # test if the gain is posative
        # if so we have sucseeded, set tour to this one and re-start
        # otherwose we look for a new line to add

        for head_removal_city in self.input_tour.currentConnections(tail_removal_city):
            test_rem = (tail_removal_city, head_removal_city)
            test_add = (head_removal_city, original_city)


            if head_removal_city != original_city and not(test_rem in self.added) and not((test_rem[1], test_rem[0]) in self.added):

                temp_removal_edges = self.remove_edges.copy()
                temp_removal_edges.update({test_rem})

                temp_add_edges = self.add_edges.copy()
                temp_add_edges.update({test_add})

                trial_tour = self.swapEdgeSets(temp_add_edges, temp_removal_edges)

                if validateTour(trial_tour, self.input_tour.weights):
                    if self.setWeightLost(temp_add_edges, temp_removal_edges) > 0:
                        self.input_tour.tour = createCycle(trial_tour)
                        return True
                    else:
                        self.remove_edges.add(test_rem)
                        return self.addEdge(original_city, tail_removal_city, head_removal_city)
        return False


    def addEdge(self, original_city, tail, head):
        for trial_add_city in self.input_tour.validPotentialNeighbors(head, 5):
            #inproved: only looks at 5 best neighbors

            trial_edge_b = (trial_add_city, head)
            trial_edge_f = (head, trial_add_city)
            if trial_add_city != tail and not(trial_edge_f  in self.input_tour.edgesSet()) and not(trial_edge_b  in self.input_tour.edgesSet()) and not(trial_edge_f  in self.removed) and not(trial_edge_b  in self.removed):

                temp_removal_edges = self.remove_edges.copy()

                temp_add_edges = self.add_edges.copy()
                temp_add_edges.update({trial_edge_f})

                if self.setWeightLost() - self.input_tour.weights[head][trial_add_city] > 0:
                    self.k_opt += 1
                    self.add_edges.add(trial_edge_f)

                    return self.removeEdge(original_city, head, trial_add_city)
        return False




    def LKinprovemnt(self):
        """
        the main part of LK
        goes though all possible staring cities (T1)
            for each stating city, pick one of its tour adjacent cities (T2)(will trial both)
                for each of T2's POSSIBLE neighbors check if replacing T1->T2 edge with T2->T3 has a better weighting
                    if so:
                        find another edge to remove
        updates tour with new more efficient tour if such a tour is found
        :return: True if improvement found, otherwise False.
        """
        self.add_edges = set()
        self.remove_edges = set()

        for T1 in self.input_tour.tour:
            for T2 in self.input_tour.currentConnections(T1):
                self.remove_edges = set()
                self.remove_edges.add((T1, T2))
                remove_edge_found = True

                for T3 in self.input_tour.validPotentialNeighbors(T2):
                    self.add_edges = set()
                    self.add_edges.add((T2, T3))

                    if self.setWeightLost() > 0:
                        remove_edge_found = self.removeEdge(T1, T2, T3)

                        if remove_edge_found:
                            #self.added.update(self.add_edges)
                            #self.removed.update(self.remove_edges)
                            return True
        return False









def main(weights):
    start_time = time.time()
    time_frame = 58
    current_tour = randomShuffle([i for i in range(len(weights))])
    continue_search = True



    elapsed_time = time.time() - start_time

    added = set()
    removed = set()

    last_res = 0

    largest_inp_time = time.time() - time.time()

    while continue_search:
        starting_imp_time = time.time()
        #goes though this for every inprovement it finds

        #set up tour and inprovemtn object
        old_tour = Tour(weights, current_tour)
        inproved_tour = Improvement(old_tour)
        inproved_tour.added = added
        inproved_tour.removed = removed

        #seach for a better tour


        #if a better one found, repeite
        continue_search = inproved_tour.LKinprovemnt()
        added.update(inproved_tour.added)
        removed.update(inproved_tour.removed)

        if continue_search == False:
            added = set()
            removed = set()

            #if we run out of edges, have what we got as the starting tour and begin again
            continue_search = True
        if(time.time() - start_time +largest_inp_time > time_frame):
            continue_search = False



        current_tour = old_tour.tour
        #inprovement that if get same result twice, end it
        if tourFitness(current_tour, weights) == last_res:
            continue_search  = False




        last_res = tourFitness(current_tour, weights)

        if(time.time() - starting_imp_time > largest_inp_time):
            largest_inp_time = time.time() - starting_imp_time

    #print(largest_inp_time)
    #print(time.time() - start_time)
    return old_tour.tour, tourFitness(old_tour.tour, weights)



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
















