import time
import random


def getRandomInt():
    # seed random number generator
    random.seed(time.perf_counter())
    for var in list(range(5)):
        min = random.randint(10, 20)
        max = random.randint(30, 40)
        wait = random.randint(min, max)
        print(wait)


refresh = 3


def test():
    global refresh
    if(refresh > 0):
        print(refresh)
        refresh = refresh - 1
        test()
    else:
        print('Done')
        refresh = 3


print('start')
# getRandomInt()
test()
