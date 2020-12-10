import random



def randomShuffle(list):
    shuffled = []
    for i in range(len(list)):
        index = random.randint(0,len(list)-1)
        while list[index] in shuffled:
            index = random.randint(0,len(list)-1)
        shuffled.append(list[index])
    return shuffled

mylist = [1,2,3,4,5,6,7,8,9]


print(randomShuffle(mylist))