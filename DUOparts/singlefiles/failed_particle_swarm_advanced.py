import random
import copy
import math
import time
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

def simple_inercia(start, c, multply_func):
    return start

def constantDegradeInercia(start, c, multply_func):
    return multply_func(start, c)

def tourFitness(tour, weights):
    distance = 0
    for cty_order in range(len(tour)):
        if tour[cty_order] == tour[-1]:
            distance += weights[tour[-1]][tour[0]]
        else:
            distance += weights[tour[cty_order]][tour[cty_order + 1]]
    return distance

class particle:
    def __init__(self):
        self.best_personal_tour = []
        self.worst_personal_tour =[]
        self.current_tour = []

        self.current_vector = []

    def updatePosition(self):
        tour = self.current_tour
        try:
            for swap in self.current_vector:
                    a, b = tour.index(tour[swap[0]]), tour.index(tour[swap[1]])
                    tour[b], tour[a] = tour[a], tour[b]
            return tour
        except:
            return tour

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

    def updatePosition(self, tour, vector):
        try:
            for swap in vector:
                    a, b = tour.index(tour[swap[0]]), tour.index(tour[swap[1]])
                    tour[b], tour[a] = tour[a], tour[b]
            return tour
        except:
            return tour


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
        new_tour = tour
        try:
            for swap in vector:
                    a, b = new_tour.index(tour[swap[0]]), tour.index(new_tour[swap[1]])
                    new_tour[b], new_tour[a] = new_tour[a], new_tour[b]
            return new_tour
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
            if constlist[i] >= threshold and (len(vector) -1 >= i):
                result.append(vector[i])
        return result

    def applyConstVector(self, vector, const):
        for i in range(len(vector)-1):
            vector[i] *= const
        return vector

    def reverse_vec(self, vector):
        return (vector[1], vector[0])



    def procedure(self, particleNUmber, iterations):
        #creating population of particles with random positions and vectors
        for i in range(particleNUmber):
            p = particle()
            p.current_tour, p.best_personal_tour, p.worst_personal_tour,  = randomShuffle(
                [i for i in range(len(self.weights[0]))]), randomShuffle([i for i in range(len(self.weights[0]))]), randomShuffle([i for i in range(len(self.weights[0]))])
            proposed_vec = respectingBubbleSort(p.current_tour, randomShuffle([i for i in range(len(self.weights[0]))]))
            p.current_vector = proposed_vec[:min(300, len(proposed_vec))]
            self.all_particles.append(p)

        global_best_index = [self.tourFitness(p.best_personal_tour, self.weights) for p in self.all_particles].index(min([self.tourFitness(p.best_personal_tour, self.weights) for p in self.all_particles]))
        global_best = self.all_particles[global_best_index].best_personal_tour

        time_counter = 0

        start_time = time.time()
        # your code
        elapsed_time = time.time() - start_time
        c_gen = 0
        #while (time_counter < iterations):
        while (time.time() - start_time) < iterations:
            for current_particle in self.all_particles:
                #print(current_particle.best_personal_tour)

                all_tour_weights = [self.tourFitness(p.best_personal_tour, self.weights) for p in self.neighborhood(current_particle.current_tour)]
                neighbor_best_index = all_tour_weights.index(min(all_tour_weights))
                neighbor_worst_index = all_tour_weights.index(max(all_tour_weights))
                neighbor_best = self.all_particles[neighbor_best_index].best_personal_tour
                neighbor_worst = self.all_particles[neighbor_worst_index].worst_personal_tour

                inercial_velocity = self.intertia_func(current_particle.current_vector, 1, self.multiplyVectorByConst)
                cognative_velocity = self.threshholdVector(self.applyConstVector(self.randomZeroOneVector(len(current_particle.best_personal_tour + current_particle.current_tour)), self.cognative_LF), respectingBubbleSort(current_particle.current_tour, current_particle.best_personal_tour), 0.5)
                social_velocity = self.threshholdVector(self.applyConstVector(self.randomZeroOneVector(len(neighbor_best + current_particle.current_tour)), self.social_LF),respectingBubbleSort(current_particle.current_tour, neighbor_best), 0.5)

                neg_cognative_velocity = self.threshholdVector(self.applyConstVector(self.randomZeroOneVector(len(current_particle.worst_personal_tour + current_particle.current_tour)),self.cognative_LF), respectingBubbleSort(current_particle.current_tour,current_particle.worst_personal_tour), 0.5)
                neg_social_velocity = self.threshholdVector(self.applyConstVector(self.randomZeroOneVector(len(neighbor_worst + current_particle.current_tour)),self.social_LF),respectingBubbleSort(current_particle.current_tour, neighbor_worst), 0.5)

                #print(inercial_velocity , cognative_velocity , social_velocity)

                to_best_vector = inercial_velocity + cognative_velocity + social_velocity
                away_worst_vector = inercial_velocity + list(reversed(list(map(self.reverse_vec, neg_cognative_velocity)))) + list(reversed(list(map(self.reverse_vec, neg_social_velocity))))

                to_best_score = self.tourFitness(self.applyVector(current_particle.current_tour, to_best_vector), self.weights)
                away_worst_score = self.tourFitness(self.applyVector(current_particle.current_tour, away_worst_vector), self.weights)

                if to_best_score < away_worst_score:
                    current_particle.current_vector = to_best_vector
                else:
                    current_particle.current_vector = away_worst_vector

                current_particle.updatePosition()

                #new_tour = self.applyVector(current_particle.current_tour, current_particle.current_vector)

                if self.tourFitness(current_particle.current_tour, self.weights) < self.tourFitness(current_particle.best_personal_tour, self.weights):
                    #print(self.tourFitness(current_particle.current_tour, self.weights) , self.tourFitness(current_particle.best_personal_tour, self.weights))
                    current_particle.best_personal_tour = (current_particle.current_tour).copy()

                elif self.tourFitness(current_particle.current_tour, self.weights) > self.tourFitness(current_particle.worst_personal_tour, self.weights):
                    #print(self.tourFitness(current_particle.current_tour, self.weights) , self.tourFitness(current_particle.best_personal_tour, self.weights))
                    current_particle.worst_personal_tour = (current_particle.current_tour).copy()

                if self.tourFitness(current_particle.best_personal_tour, self.weights) < self.tourFitness(global_best, self.weights):
                    global_best = (current_particle.best_personal_tour).copy()
                    print(time_counter, self.tourFitness(global_best, self.weights))


                #print(".")
            time_counter += 1
            #print(time_counter, self.tourFitness(global_best, self.weights))


        return global_best


class swarmController:
    def __init__(self, distances,  swarm_number, swarm_population, gens_before_merge):
        self.swarms = []
        self.swarm_number = swarm_number
        self.swarm_pop = swarm_population

        self.dist_matrix = distances
        self.time_before_merge = gens_before_merge

    def tourFitness(self, particle):
        tour = particle.best_personal_tour

        distance = 0
        for cty_order in range(len(tour)):
            if tour[cty_order] == tour[-1]:
                distance += self.dist_matrix[tour[-1]][tour[0]]
            else:
                distance += self.dist_matrix[tour[cty_order]][tour[cty_order + 1]]
        return distance

    def inicialiseSwarms(self):
        for i in range(self.swarm_number):
            self.swarms.append(swarm(self.dist_matrix, simple_inercia, 2.8, 1.3, None))

    def mix_swarms(self):
        all_s_particles = []
        for subswarm in self.swarms:
            all_s_particles.extend(subswarm.all_particles)
            subswarm.all_particles = []
        all_s_particles.sort(key = self.tourFitness)

        while len(all_s_particles) != 0:
            for subswarm in self.swarms:
                if len(all_s_particles) != 0:
                    subswarm.all_particles.append(all_s_particles.pop())

        for subswarm in self.swarms:
            subswarm.all_particles.sort(key=self.tourFitness)
            subswarm.swarm_best_tour = subswarm.all_particles[0]

        return 1

    def bestParticle(self, groups):
        all_s_particles = []
        for subswarm in groups:
            all_s_particles.extend(subswarm.all_particles)
            subswarm.all_particles = []
        all_s_particles.sort(key=self.tourFitness)

        return all_s_particles[0]
    def run(self, time_limmit):
        start_time = time.time()
        self.inicialiseSwarms()

        while (time.time() - start_time) < time_limmit:
            for subswarm in self.swarms:
                if time_limmit - (time.time() - start_time) > self.time_before_merge:
                    subswarm.procedure(self.swarm_pop, self.time_before_merge)
                else:
                    break
            self.mix_swarms()


        overall_best_p = self.bestParticle(self.swarms)
        overall_score = self.tourFitness(overall_best_p)
        return overall_score

def main(dist_matrix):
    for i in range(10, 180, 10):
        print(swarmController(dist_matrix, 4, 30, 5).run(5*60))


if __name__ == '__main__':
    top = swarm(input_map, simple_inercia, 2.8, 1.3, None).procedure(30, 1000)
    print(tourFitness(top, input_map))
#magicly correct coefficients: 2.8, 1.3
#Carlisle, A., Dozier, G., 2001. An Off-the-shelf PSO.
#Proceedings of the Workshop on Particle Swarm
#Optimization, p. 1-6.
