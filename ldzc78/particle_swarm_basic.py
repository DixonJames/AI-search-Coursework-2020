import random
import copy
import math
"""
basic bubble discretization of particle swarm in the main lecture #10
"""
input_map = [[0, 31, 32, 5, 30, 9, 15, 40, 14, 21, 7, 13], [31, 0, 5, 30, 40, 15, 8, 2, 4, 17, 50, 27], [32, 5, 0, 32, 25, 16, 3, 3, 10, 8, 40, 21], [5, 30, 32, 0, 50, 6, 30, 53, 10, 35, 12, 20], [30, 40, 25, 50, 0, 32, 10, 20, 34, 7, 20, 6], [9, 15, 16, 6, 32, 0, 15, 15, 4, 14, 21, 25], [15, 8, 3, 30, 10, 15, 0, 6, 9, 4, 9, 9], [40, 2, 3, 53, 20, 15, 6, 0, 7, 8, 30, 29], [14, 4, 10, 10, 34, 4, 9, 7, 0, 13, 31, 35], [21, 17, 8, 35, 7, 14, 4, 8, 13, 0, 12, 11], [7, 50, 40, 12, 20, 21, 9, 30, 31, 12, 0, 5], [13, 27, 21, 20, 6, 25, 9, 29, 35, 11, 5, 0]]

test_a = [1,6,3,2,4,7,9,8,5,0]
test_b = [0,1,2,3,4,5,6,7,8,9]

def respectingBubbleSort(list, order):
    swaps = []
    swapped = False
    repeat = True

    while repeat:
        swapped = False
        for i in range(len(list)-1):
            below, above = list[i], list[i+1]
            if order.index(below) > order.index(above):
                swaps.append((i, i+1))
                temp = copy.copy(list[i+1])
                list[i+1] = below
                list[i] = temp
                swapped = True
        if not swapped:
            repeat = False
    return swaps

def randomShuffle(list):
    shuffled = []
    for i in range(len(list)):
        index = random.randint(0,len(list)-1)
        while list[index] in shuffled:
            index = random.randint(0,len(list)-1)
        shuffled.append(list[index])
    return shuffled


class particle:
    def __init__(self):
        self.best_personal_tour = []
        self.current_tour = []

        self.current_vector = []

class swarm:
    def __init__(self, weights, intertia_func, cognative_LF, social_LF, neighborhoodRadius = None):
        self.weights = weights
        self.intertia_func = intertia_func
        self.all_particles = []
        self.swarm_best_tour = []

        self.time = 0
        self.cognative_LF = cognative_LF
        self.social_LF = social_LF
        self.neighborhood_radius = neighborhoodRadius

    def tourFitness(self, tour, weights):
        distance = 0
        for cty_order in range(len(tour)):
            if tour[cty_order] == tour[-1]:
                distance += weights[tour[-1]][tour[0]]
            else:
                distance += weights[tour[cty_order]][tour[cty_order + 1]]
        return distance

    def neighborhood(self, position):
        if self.neighborhood_radius == None:
            return self.all_particles
        return [p for p in self.all_particles if self.distance(position, p.current_tour) < self.neighborhood_radius]


    def multiplyVectorByConst(self, vector, constant):
        if constant < 0:
            print("invalid con constant")
            return False
        if constant >= 0 and constant <= 1:
            final  = math.floor(constant * len(vector))
            return vector[:final-1]
        else:
            return math.floor(constant) * vector + self.multiplyVector(constant - math.floor(constant), vector)

    def multiplyVecotrs(self, constVec, swapsVec):
        result = []
        for const in constVec:
            result += self.multiplyVectorByConst(swapsVec, const)
        return result


    def distance(self, vectorA, vectorB):
        return abs(len(respectingBubbleSort(vectorA, vectorB)))

    def randTour(self):
        return random.shuffle([i for i in range(len(self.weights[0])-1)])

    def applyVector(self, tour, vector):
        try:
            for swap in vector:
                    a, b = tour.index(tour[swap[0]]), tour.index(tour[swap[1]])
                    tour[b], tour[a] = tour[a], tour[b]
            return tour
        except:
            print('swap failed')




    def randomZeroOneVector(self, length):
        vec = []
        for i in range(length):
            vec.append(random.randrange(1, 9, 1)/10)
        return vec

    def threshholdVector(self, constlist, vector, threshold):
        result = []
        for i in range(len(constlist)-1):
            if constlist[i] >= threshold:
                result.append(vector[i])
        return result

    def applyConstVector(self, vector, const):
        for i in range(len(vector)-1):
            vector[i] *= const
        return vector



    def procedure(self, particleNUmber, iterations):
        for i in range(particleNUmber):
            p = particle()
            random_tour = randomShuffle([i for i in range(len(self.weights[0]))])
            p.current_tour, p.best_personal_tour = random_tour, random_tour
            p.current_vector = respectingBubbleSort(p.current_tour, randomShuffle([i for i in range(len(self.weights[0]))]))
            self.all_particles.append(p)
        global_best_index = [self.tourFitness(p.best_personal_tour, self.weights) for p in self.all_particles].index(min([self.tourFitness(p.best_personal_tour, self.weights) for p in self.all_particles]))
        global_best = self.all_particles[global_best_index].best_personal_tour

        time_counter = 0
        while time_counter < iterations:
            for current_particle in self.all_particles:
                print(current_particle)

                neighbor_best_index = [self.tourFitness(p.best_personal_tour, self.weights) for p in self.neighborhood(current_particle.current_tour)].index(
                    min([self.tourFitness(p.best_personal_tour, self.weights) for p in self.neighborhood(current_particle.current_tour)]))
                neighbor_best = self.all_particles[neighbor_best_index].best_personal_tour

                current_particle.current_tour = self.applyVector(current_particle.current_tour, current_particle.current_vector)

                inercial_velocity = self.intertia_func(current_particle.current_vector)
                cognative_velocity = self.threshholdVector(self.applyConstVector(self.randomZeroOneVector(len(current_particle.best_personal_tour + current_particle.current_tour)), self.cognative_LF), respectingBubbleSort(current_particle.current_tour, current_particle.best_personal_tour), 0.5)

                social_velocity = self.threshholdVector(self.applyConstVector(self.randomZeroOneVector(len(neighbor_best + current_particle.current_tour)), self.social_LF),respectingBubbleSort(current_particle.current_tour, neighbor_best), 0.5)

                current_particle.current_vector = inercial_velocity + cognative_velocity + social_velocity




                if self.tourFitness(current_particle.current_tour, self.weights) > self.tourFitness(current_particle.best_personal_tour, self.weights):
                    current_particle.best_personal_tour = current_particle.current_tour

            global_best_index = [self.tourFitness(p.best_personal_tour, self.weights) for p in self.all_particles].index(
                min([self.tourFitness(p.best_personal_tour, self.weights) for p in self.all_particles]))
            global_best = self.all_particles[global_best_index].best_personal_tour
            time_counter += 1
        return global_best, self.tourFitness(global_best, self.weights)

def simple_inercia(start):
    return start

if __name__ == '__main__':
    top = swarm(input_map, simple_inercia, 0.5, 0.5).procedure(100, 100)
    print(top)

