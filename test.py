import random
map = [[0, 31, 32, 5, 30, 9, 15, 40, 14, 21, 7, 13], [31, 0, 5, 30, 40, 15, 8, 2, 4, 17, 50, 27], [32, 5, 0, 32, 25, 16, 3, 3, 10, 8, 40, 21], [5, 30, 32, 0, 50, 6, 30, 53, 10, 35, 12, 20], [30, 40, 25, 50, 0, 32, 10, 20, 34, 7, 20, 6], [9, 15, 16, 6, 32, 0, 15, 15, 4, 14, 21, 25], [15, 8, 3, 30, 10, 15, 0, 6, 9, 4, 9, 9], [40, 2, 3, 53, 20, 15, 6, 0, 7, 8, 30, 29], [14, 4, 10, 10, 34, 4, 9, 7, 0, 13, 31, 35], [21, 17, 8, 35, 7, 14, 4, 8, 13, 0, 12, 11], [7, 50, 40, 12, 20, 21, 9, 30, 31, 12, 0, 5], [13, 27, 21, 20, 6, 25, 9, 29, 35, 11, 5, 0]]


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

mylist = [1,2,3,4,5,6,7,8,9]

p1 = [1,2,3,4,5,6,7,8]
p2 = [8,5,2,1,3,6,4,7]

p3 = [3,4,8,2,7,1,6,5]
p4 = [4,2,5,1,6,8,3,7]
print(cycleCrossoverOperator(p3, p4))