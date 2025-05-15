import random

def createRandom(numNo):
    numList = []
    for i in range(0, numNo):
        num = random.randint(10, 99)
        numList.append(num)
    return numList

# if __name__ == "__main__":
#     a=createRandom(2)
#     print(a)