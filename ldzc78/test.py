import random
def randomShuffle(list):
    shuffled = []
    for i in range(len(list)):
        index = random.randint(0,len(list)-1)
        while list[index] in shuffled:
            index = random.randint(0,len(list)-1)
        shuffled.append(list[index])
    return shuffled

def vectorByPermutation(target_vec, start_vec):
    # makes vector from start to target
    list_cities = target_vec.copy()
    partner = {}
    cycles = []
    for city_i in range(len(target_vec)):
        partner[target_vec[city_i]] = start_vec[city_i]

    while len(list_cities) != 0:
        cycle = []
        beginning = list_cities.pop()
        current_city = beginning
        while partner[current_city] != beginning:
            cycle.append(current_city)

            current_city = partner[current_city]
            if current_city != beginning:
                del list_cities[list_cities.index(current_city)]
        cycle.append(current_city)

        if len(cycle) != 0:
            cycles.append(cycle)

    sorted_c =[]
    for cycle in cycles:
        old = cycle
        min_index = cycle.index(min(cycle))
        sorted_c.append([cycle[min_index]] + cycle[min_index + 1:] + cycle[:min_index])


    sorted_c.sort(key=lambda a: a[0])

    swaps = []
    for cycle in sorted_c:
        for i in range(len(cycle)-1):
            swaps.append((target_vec.index(cycle[i]), target_vec.index(cycle[i + 1])))

    return swaps

def applyVector(tour, vector):
    try:
        for swap in vector:
                a, b = tour.index(tour[swap[0]]), tour.index(tour[swap[1]])
                tour[b], tour[a] = tour[a], tour[b]
        return tour
    except:
        print('swap failed')

list = [1,2,3,4,5,6,7,8,9,0]

for i in range(100000):
    list_a = randomShuffle(list)
    list_b = randomShuffle(list)

    atob =vectorByPermutation(list_a, list_b)
    #print(list_a)
    #print(list_b)
    #print(applyVector(list_a, atob))
    if applyVector(list_a, atob) != list_b:
        print("!")