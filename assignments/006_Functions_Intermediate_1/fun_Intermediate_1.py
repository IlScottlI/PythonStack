import random


def randInt(min=0, max=100):
    if min > 0:
        max = max - min
    num = random.random() * max + min
    return round(num)
