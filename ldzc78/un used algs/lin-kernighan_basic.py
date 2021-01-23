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


class LKA:
    def __init__(self):
        self.edges = input_map
        self.current_tour = nearestNeighborAlg(self.edges)

        #though an iteration will change to show proposed new edges and currently used edges
        self.current_edge_use = self.resetEdgeUse()

        # a series of tuples
        self.remove_list = []
        self.add_list = []

        #index of what vertex was first to be randomly chosen and end being the vertex that currently needs to be expanded from
        self.start_vertex = 0
        self.end_vertex = 0

    def resetEdgeUse(self):
        self.current_edge_use = [[0 for i in range(len(input_map[0] - 1))] for j in range(len(input_map))]

        for edge in self.current_tour:
            self.current_edge_use[edge[0]][edge[1]] = 1
            self.current_edge_use[edge[1]][edge[0]] = 1

    def randStartEdge(self):
        vertex = random.choice(self.current_tour)

    def randLeadingVertex(self, start_vertex_index):
        """
        returns a random vertex that is currently not being used in the given tour
        :param start_vertex_index:
        :return:
        """
        #create set of all i's of map[start_vertex][i] that are valid
        valid_indexs = []
        for trial_i in range(len(self.edges[start_vertex_index])-1):
            if trial_i != start_vertex_index and self.current_edge_use[start_vertex_index][trial_i] == 0:
                valid_indexs.append(trial_i)

        return random.choice(valid_indexs)

    def compareTotalEdgeWeightes(self):
        prior_sum = 0
        post_sum = 0

        for item in self.remove_list:
            prior_sum += self.edges[item[0]][item[1]]
        for item in self.add_list:
            post_sum += self.edges[item[0]][item[1]]

        if prior_sum - post_sum >= 0:
            return True
        return False


    def LK_iteration(self):
        """
        http://akira.ruc.dk/~keld/research/LKH/LKH-2.0/DOC/LKH_REPORT.pdf
         6. Choose xi
 = (t2i-1,t2i) Î T such that
 (a) if t2i is joined to t1
, the resulting configuration is a
 tour, T’, and
 (b) xi ¹ ys
 for all s < i.
 If T’ is a better tour than T, let T = T’ and go to Step 2.
 7. Choose yi
 = (t2i,t2i+1) Ï T such that
 (a) Gi
 > 0,
 (b) yi ¹ xs
 for all s £ i, and
 (c) xi+1 exists.
 If such yi
 exists, go to Step 5.
 8. If there is an untried alternative for y2
, let i = 2 and go to Step 7.
 9. If there is an untried alternative for x2
, let i = 2 and go to Step 6.
10. If there is an untried alternative for y1
, let i = 1 and go to Step 4.
11. If there is an untried alternative for x1
, let i = 1 and go to Step 3.
12. If there is an untried alternative for t1
, then go to Step 2.
13. Stop (or go to Step 1).
        :return:
        """

        pass



