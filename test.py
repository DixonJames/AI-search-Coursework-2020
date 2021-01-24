import random
map = [[0, 31, 32, 5, 30, 9, 15, 40, 14, 21, 7, 13], [31, 0, 5, 30, 40, 15, 8, 2, 4, 17, 50, 27], [32, 5, 0, 32, 25, 16, 3, 3, 10, 8, 40, 21], [5, 30, 32, 0, 50, 6, 30, 53, 10, 35, 12, 20], [30, 40, 25, 50, 0, 32, 10, 20, 34, 7, 20, 6], [9, 15, 16, 6, 32, 0, 15, 15, 4, 14, 21, 25], [15, 8, 3, 30, 10, 15, 0, 6, 9, 4, 9, 9], [40, 2, 3, 53, 20, 15, 6, 0, 7, 8, 30, 29], [14, 4, 10, 10, 34, 4, 9, 7, 0, 13, 31, 35], [21, 17, 8, 35, 7, 14, 4, 8, 13, 0, 12, 11], [7, 50, 40, 12, 20, 21, 9, 30, 31, 12, 0, 5], [13, 27, 21, 20, 6, 25, 9, 29, 35, 11, 5, 0]]


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

    original_p_weight = distances[B_n_city][B_city] + distances[A_n_city][A_city]
    new_p_weight = distances[A_city][B_city] + distances[A_city_i][B_city_i]

    if original_p_weight > new_p_weight:
        mid_section = (tour[A_city_i + 2: B_city_i ])[::-1]
        front_section = tour[:A_city_i + 1]
        tail_section = tour[B_city_i + 1:]


        new = front_section + [B_city] + mid_section + [A_n_city] + tail_section
        if len(set(new)) != len(tour):
            print("s")

        tour = front_section + [B_city] + mid_section + [A_n_city] + tail_section

    return tour

mylist = [1,2,3,4,5,6,7,8,9]

p1 = [1,2,3,4,5,6,7,8]
p2 = [8,5,2,1,3,6,4,7]

p3 = [3,4,8,2,7,1,6,5]
p4 = [4,2,5,1,6,8,3,7]

for i in range(100):
    p1 = two_opt_mutation(p1, map)
    print(p1)