import random

input_map = [[0, 31, 32, 5, 30, 9, 15, 40, 14, 21, 7, 13], [31, 0, 5, 30, 40, 15, 8, 2, 4, 17, 50, 27], [32, 5, 0, 32, 25, 16, 3, 3, 10, 8, 40, 21], [5, 30, 32, 0, 50, 6, 30, 53, 10, 35, 12, 20], [30, 40, 25, 50, 0, 32, 10, 20, 34, 7, 20, 6], [9, 15, 16, 6, 32, 0, 15, 15, 4, 14, 21, 25], [15, 8, 3, 30, 10, 15, 0, 6, 9, 4, 9, 9], [40, 2, 3, 53, 20, 15, 6, 0, 7, 8, 30, 29], [14, 4, 10, 10, 34, 4, 9, 7, 0, 13, 31, 35], [21, 17, 8, 35, 7, 14, 4, 8, 13, 0, 12, 11], [7, 50, 40, 12, 20, 21, 9, 30, 31, 12, 0, 5], [13, 27, 21, 20, 6, 25, 9, 29, 35, 11, 5, 0]]

def nearestNeighborAlg(map):
    visited = [0]
    current = 0
    while len(visited) != len(map[0]):
        valid = []
        for i in range(len(map[current])):
            if i not in visited:
                valid.append(map[current][i])
        nearest = min(valid)
        current = map[current].index(nearest)
        visited.append(current)

    visited.append(visited[0])

    return visited



class ant:
    def __init__(self, start_node = None):

        if start_node == None:
            self.location = -1
            self.current_tour = []
        else:
            self.location = start_node
            self.current_tour = [start_node]

        self.complete_tour = False
        self.tot_tour_weight = -1


class ACOvanilla:
    def __init__(self, map, evap_const, alpha_const, beta_comst):
        self.weights = map
        self.pheromone_map = [[0.1 for i in self.weights] for i in self.weights]

        self.ant_list = []
        self.pheromone_evap_rate = evap_const

        self.alpha = alpha_const
        self.beta = beta_comst

        self.top_tour = nearestNeighborAlg(self.weights)
        self.top_tour_score = self.tourWeight(self.top_tour)

        #for testing only! deleite when submitting V
        self.top_tour_score = 300

    def createWorkers(self, number, wipe_clean = None):
        """
        creates number instances of the ant class,
        assigns a random starting location,
        adds to list of workers
        :param number: number of ants to add
        """
        if wipe_clean:
            self.ant_list = []
        for i in range(number):
            self.ant_list.append(ant(random.randint(0, len(self.weights)-1)))

    def workerTourWeight(self, worker):
        total = 0
        for i in range(len(worker.current_tour)-1):
            total += self.weights[worker.current_tour[i]][worker.current_tour[i]]
        total += self.weights[worker.current_tour[0]][worker.current_tour[-1]]
        return total

    def tourWeight(self, order):
        total = 0
        for i in range(len(order)-1):
            total += self.weights[order[i]][order[i+1]]
        total += self.weights[order[0]][order[-1]]
        return total

    def nextVertex(self, boid):
        """
        calculates the probability of going down each valid vertex
        moves boid there accordingly and changes its stats
        :param boid: an instance of ant class
        :return: None
        """
        valid_neighbors = [i for i in range(len(self.weights[0])) if not(i == boid.location or i in boid.current_tour)]

        if len(valid_neighbors) == 1:
            next_node = valid_neighbors[0]

        elif len(valid_neighbors) != 0:
            valid_neighbors_pheromone_Lvl = [((self.pheromone_map[boid.location][i])**self.alpha) * ((self.weights[boid.location][i])**self.beta) for i in range(len(valid_neighbors))]
            total_pheromone_Lvl = sum(valid_neighbors_pheromone_Lvl)
            try:
                valid_neighbors_prob = [valid_neighbors_pheromone_Lvl[i]/total_pheromone_Lvl for i in range(len(valid_neighbors)) ]
                next_node = random.choices(valid_neighbors, weights=valid_neighbors_prob, k=1)[0]
            except:
                print("oops")



        else:
            next_node = boid.current_tour[0]
            boid.complete_tour = True

        boid.current_tour.append(next_node)
        boid.tot_tour_weight += self.weights[boid.location][next_node]
        boid.location = next_node


    def initialiseGPL(self):
        #when this is run, the top tour is equal to a bad  neighrest neighbor tour
        nn_tour_weight = self.top_tour_score
        base_P_lvl = nn_tour_weight / len(self.ant_list)

        self.pheromone_map = [[base_P_lvl for i in range(len(self.pheromone_map[0]))]for j in range(len(self.pheromone_map))]


    def updateGlobalPheromones(self):

        #evaporation of pheromone. controlled by constant alpha
        self.pheromone_map = [[((1-self.pheromone_evap_rate) * self.pheromone_map[vertex][edge]) for edge in range(len(self.pheromone_map[0]))] for vertex in range(len(self.pheromone_map))]

        #adding pheromone on path depending on length of tour it is used in
        for worker in self.ant_list:
            for s in range(len(worker.current_tour)-1):
                start_point = worker.current_tour[s]
                end_point = worker.current_tour[s+1]
                self.pheromone_map[start_point][end_point] += 1/worker.tot_tour_weight

        #print(self.pheromone_map)


    def iterateACO(self):
        for worker in self.ant_list:

            while worker.complete_tour == False:
                self.nextVertex(worker)
            worker.complete_tour = False

            if self.tourWeight(worker.current_tour) <  self.top_tour_score:
                self.top_tour = worker.current_tour
                self.top_tour_score = self.tourWeight(worker.current_tour)

    def updateLocalPheromone(self):
        """
        POSSIBLY FOR ENHANCED VERSION:
        updates one edge for the duration of the solution generation
        will perswade more ants to explore new paths other than ones already traveld for this iteration
        :return:
        """
        pass


def runIterations(graph, iterations, number_workers):
    AOP_work_instance = ACOvanilla(graph, 0.3, 0.5, 0.1)
    AOP_work_instance.createWorkers(number_workers)
    AOP_work_instance.initialiseGPL()



    for i in range(iterations):
        AOP_work_instance.createWorkers(number_workers, True)
        AOP_work_instance.iterateACO()
        AOP_work_instance.updateGlobalPheromones()

    return AOP_work_instance.top_tour, AOP_work_instance.top_tour_score



if __name__ == '__main__':
    print(runIterations(input_map, 100, 100))

