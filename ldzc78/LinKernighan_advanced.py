import time
import random

input_map = [[0, 31, 32, 5, 30, 9, 15, 40, 14, 21, 7, 13], [31, 0, 5, 30, 40, 15, 8, 2, 4, 17, 50, 27], [32, 5, 0, 32, 25, 16, 3, 3, 10, 8, 40, 21], [5, 30, 32, 0, 50, 6, 30, 53, 10, 35, 12, 20], [30, 40, 25, 50, 0, 32, 10, 20, 34, 7, 20, 6], [9, 15, 16, 6, 32, 0, 15, 15, 4, 14, 21, 25], [15, 8, 3, 30, 10, 15, 0, 6, 9, 4, 9, 9], [40, 2, 3, 53, 20, 15, 6, 0, 7, 8, 30, 29], [14, 4, 10, 10, 34, 4, 9, 7, 0, 13, 31, 35], [21, 17, 8, 35, 7, 14, 4, 8, 13, 0, 12, 11], [7, 50, 40, 12, 20, 21, 9, 30, 31, 12, 0, 5], [13, 27, 21, 20, 6, 25, 9, 29, 35, 11, 5, 0]]


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
                for each of T2's POSISBLE neighbors check if replacing T1->T2 edge with T2->T3 has a better weighting
                    if so:
                        find another edge to remove
        updates tour with new more efficint tour if such a tour is found
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
                            self.added.update(self.add_edges)
                            self.removed.update(self.remove_edges)
                            return True
        return False









def main(weights):
    time_frame = 58
    current_tour = randomShuffle([i for i in range(len(weights))])
    continue_search = True

    start_time = time.time()

    elapsed_time = time.time() - start_time

    added = set()
    removed = set()

    last_res = 0

    while continue_search:
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
        if(time.time() - start_time > time_frame):
            continue_search = False



        current_tour = old_tour.tour
        #inprovement that if get same result twice, end it
        if tourFitness(current_tour, weights) == last_res:
            continue_search  = False



        print((inproved_tour.k_opt), tourFitness(current_tour, weights))
        last_res = tourFitness(current_tour, weights)

    print(time.time() - start_time )
    return old_tour.tour, tourFitness(old_tour.tour, weights)






if __name__ == '__main__':
    main(input_map)


