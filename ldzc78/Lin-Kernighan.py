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

def validateTour(proposed_edges, weights):
    """
    every city shuold appear in exactly two edges. thould be as amny edges as cities
    :param proposed_edges:
    :param weights:
    :return: T/F dependiing on validity of the tour
    """
    if len(proposed_edges) != len(weights[0]):
        return False
    city_count = [i for i in range(len(weights) -1)]

    for edge in proposed_edges:
        city_count[edge[0]] += 1
        city_count[edge[1]] += 1

    for city in city_count:
        if city != 2:
            return False

    return True




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
        for city_i in len(self.tour):
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
        for edge in self.edgesList(self.tour):
            if edge[0] == city:
                connected_citys.append(edge[1])
            elif edge[1] == city:
                connected_citys.append(edge[0])

        return connected_citys

    def validPotentialNeighbors(self, city):
        """
        returns a whitlelist containg the city and the city currently connected to in the tour
        :param city:
        :return:
        """
        black_list = set(city)
        all_edges = self.edgesList()
        for edge in all_edges:
            if edge[0] == city:
                black_list.append(edge[1])

        return all_edges.difference(black_list)




class Improvement:
    def __init__(self, tour):
        self.total_gain = 0
        self.input_tour = tour

        self.add_edges = set()
        self.remove_edges = set()

        self.found_better = True

    def setWeightLost(self):
        """
        looks at both of the add and remove sets. calculates the weight lost (or gained)
        :return:
        """
        pass

    def swapEdgeSets(self):
        current_edges = self.input_tour.edgesList()
        new_tour_set = self.add_edges.union((current_edges.differance(self.remove_edges)))

        return new_tour_set

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
                self.remove_edges.add((T1, T2))

                for T3 in self.input_tour.validPotentialNeighbors(T2):
                    self.add_edges.add((T2, T3))








def main(weights):
    current_tour = randomShuffle([i for i in range(len(weights) - 1)])
    continue_search = True


    while continue_search:
        #goes though this for every inprovement it finds

        #set up tour and inprovemtn object
        old_tour = Tour(weights, current_tour)
        inproved_tour = Improvement(old_tour)

        #seach for a better tour
        inproved_tour.searchBetter()

        #if a better one found, repeite
        continue_search = inproved_tour.found_better
        current_tour = continue_search.tour






if __name__ == '__main__':
    main(input_map)


