input_map = [[0, 31, 32, 5, 30, 9, 15, 40, 14, 21, 7, 13], [31, 0, 5, 30, 40, 15, 8, 2, 4, 17, 50, 27], [32, 5, 0, 32, 25, 16, 3, 3, 10, 8, 40, 21], [5, 30, 32, 0, 50, 6, 30, 53, 10, 35, 12, 20], [30, 40, 25, 50, 0, 32, 10, 20, 34, 7, 20, 6], [9, 15, 16, 6, 32, 0, 15, 15, 4, 14, 21, 25], [15, 8, 3, 30, 10, 15, 0, 6, 9, 4, 9, 9], [40, 2, 3, 53, 20, 15, 6, 0, 7, 8, 30, 29], [14, 4, 10, 10, 34, 4, 9, 7, 0, 13, 31, 35], [21, 17, 8, 35, 7, 14, 4, 8, 13, 0, 12, 11], [7, 50, 40, 12, 20, 21, 9, 30, 31, 12, 0, 5], [13, 27, 21, 20, 6, 25, 9, 29, 35, 11, 5, 0]]


def tourWeight(order):
    total = 0

    for city_i in range(len(order)-1):
        total += input_map[order[city_i]][order[city_i+1]]
    return total

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


print(nearestNeighborAlg(input_map))
print(tourWeight([0, 3, 5, 8, 1, 7, 2, 6, 9, 4, 11, 10, 0]))
